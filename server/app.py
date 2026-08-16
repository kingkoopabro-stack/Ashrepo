import os
import json
import requests
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
import stripe
from db import init_db, save_order

load_dotenv()

app = Flask(__name__)
init_db()

# Stripe setup
STRIPE_SECRET = os.getenv('STRIPE_SECRET_KEY')
if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET

# Helpers
def parse_price(price):
    try:
        return int(float(price) * 100)
    except Exception:
        return 0

@app.route('/')
def index():
    return jsonify({'status':'ok','service':'rare-candy-payments'})

# Stripe Checkout session
@app.route('/create_stripe_session', methods=['POST'])
def create_stripe_session():
    if not STRIPE_SECRET:
        return jsonify({'error':'Stripe not configured'}), 400
    data = request.json or {}
    try:
        line_items = [{
            'price_data':{
                'currency':'USD',
                'product_data':{'name': data.get('name','Item')},
                'unit_amount': parse_price(data.get('price', '0'))
            },
            'quantity': int(data.get('quantity',1))
        }]
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=data.get('success_url') or os.getenv('SUCCESS_URL'),
            cancel_url=data.get('cancel_url') or os.getenv('CANCEL_URL')
        )
        return jsonify({'id': session.id, 'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PayPal create order
@app.route('/create_paypal_order', methods=['POST'])
def create_paypal_order():
    client_id = os.getenv('PAYPAL_CLIENT_ID')
    secret = os.getenv('PAYPAL_SECRET')
    env = os.getenv('PAYPAL_ENV','sandbox')
    if not client_id or not secret:
        return jsonify({'error':'PayPal not configured'}), 400
    base = 'https://api-m.sandbox.paypal.com' if env == 'sandbox' else 'https://api-m.paypal.com'
    # get token
    auth = requests.post(f'{base}/v1/oauth2/token', auth=(client_id, secret), data={'grant_type':'client_credentials'})
    if auth.status_code != 200:
        return jsonify({'error':'failed to authenticate with PayPal','detail':auth.text}), 500
    token = auth.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}', 'Content-Type':'application/json'}
    data = request.json or {}
    price = str(data.get('price','0.00'))
    order_body = {
        'intent':'CAPTURE',
        'purchase_units': [{
            'amount':{
                'currency_code':'USD',
                'value': price
            },
            'items': [{
                'name': data.get('name','Item'),
                'unit_amount': {'currency_code':'USD','value':price},
                'quantity': '1'
            }]
        }],
        'application_context':{
            'return_url': data.get('success_url') or os.getenv('SUCCESS_URL'),
            'cancel_url': data.get('cancel_url') or os.getenv('CANCEL_URL')
        }
    }
    resp = requests.post(f'{base}/v2/checkout/orders', headers=headers, json=order_body)
    if resp.status_code >= 400:
        return jsonify({'error':resp.text}), 500
    return jsonify(resp.json())

# Square create payment link
@app.route('/create_square_link', methods=['POST'])
def create_square_link():
    token = os.getenv('SQUARE_ACCESS_TOKEN')
    location = os.getenv('SQUARE_LOCATION_ID')
    if not token or not location:
        return jsonify({'error':'Square not configured'}), 400
    data = request.json or {}
    amount = parse_price(data.get('price','0'))
    body = {
        'idempotency_key': os.urandom(16).hex(),
        'quick_pay': {
            'name': data.get('name','Item'),
            'price_money': {'amount': amount, 'currency': 'USD'},
            'location_id': location
        }
    }
    headers = {'Authorization': f'Bearer {token}', 'Content-Type':'application/json'}
    resp = requests.post('https://connect.squareup.com/v2/online-checkout/payment-links', headers=headers, json=body)
    if resp.status_code >= 400:
        return jsonify({'error':resp.text}), 500
    return jsonify(resp.json())

# Webhooks
@app.route('/webhook/stripe', methods=['POST'])
def webhook_stripe():
    payload = request.data
    sig = request.headers.get('Stripe-Signature')
    # optional signature verification omitted for simplicity; recommend verifying in production
    try:
        event = json.loads(payload)
    except Exception:
        event = {'raw': payload.decode('utf-8', errors='ignore')}
    save_order('stripe', event.get('id', event.get('type','unknown')), json.dumps(event))
    return '', 200

@app.route('/webhook/paypal', methods=['POST'])
def webhook_paypal():
    event = request.json or {}
    save_order('paypal', event.get('id', event.get('event_type','unknown')), json.dumps(event))
    return '', 200

@app.route('/webhook/square', methods=['POST'])
def webhook_square():
    event = request.json or {}
    save_order('square', event.get('event_id', event.get('type','unknown')), json.dumps(event))
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)), debug=(os.getenv('FLASK_ENV')=='development'))
