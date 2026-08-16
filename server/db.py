import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv('ORDERS_DB', os.path.join(os.path.dirname(__file__), 'orders.db'))

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT,
        event_id TEXT,
        payload TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

def save_order(provider, event_id, payload):
    conn = get_conn()
    c = conn.cursor()
    c.execute('INSERT INTO orders (provider, event_id, payload, created_at) VALUES (?, ?, ?, ?)', (provider, event_id, payload, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('DB initialized at', DB_PATH)
