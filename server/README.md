Rare Candy Payments backend (Flask)

This small Flask app provides endpoints to create payment sessions/links and receive webhooks for Stripe, PayPal, and Square.

Setup (local or Pi):
1. Copy server/.env.example -> server/.env and fill keys.
2. Create a virtualenv and install deps:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. Initialize DB: python -c "from db import init_db; init_db()"
4. Run locally for testing: FLASK_ENV=development flask run --host=0.0.0.0 --port=5000

Endpoints:
- POST /create_stripe_session  {name, price, quantity, success_url, cancel_url}
- POST /create_paypal_order   {name, price, success_url, cancel_url}
- POST /create_square_link    {name, price}
- POST /webhook/stripe
- POST /webhook/paypal
- POST /webhook/square

Testing webhooks: use ngrok or localtunnel to expose localhost and configure provider webhook URLs in test mode.

Security: keep API keys out of repo and use environment variables. Verify Stripe webhook signatures in production.
