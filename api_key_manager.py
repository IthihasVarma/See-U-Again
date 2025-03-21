import os
import secrets
import sqlite3
import bcrypt
from flask import Flask, request, jsonify
import logging
import time

app = Flask(__name__)
# Removed the Limiter initialization from here

# Database setup
DATABASE = 'api_keys.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY,
                key TEXT NOT NULL UNIQUE,
                revoked INTEGER DEFAULT 0,
                expiration INTEGER
            )
        ''')
        conn.commit()

# API Key Generation
def generate_api_key():
    return secrets.token_urlsafe(32)

# Store API Key
def store_api_key(api_key, expiration=None):
    hashed_key = bcrypt.hashpw(api_key.encode('utf-8'), bcrypt.gensalt())
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO api_keys (key, expiration) VALUES (?, ?)', (hashed_key, expiration))
        conn.commit()

# Validate API Key
def validate_api_key(api_key):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT key, expiration FROM api_keys WHERE revoked = 0')
        keys = cursor.fetchall()
        for (hashed_key, expiration) in keys:
            if bcrypt.checkpw(api_key.encode('utf-8'), hashed_key):
                if expiration is None or expiration > int(time.time()):
                    return True
    return False

@app.route('/validate_key', methods=['POST'])
def validate_key():
    data = request.json
    api_key = data.get('api_key')
    if validate_api_key(api_key):
        return jsonify({"valid": True}), 200
    return jsonify({"valid": False}), 403

# Key Revocation
def revoke_api_key(api_key):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE api_keys SET revoked = 1 WHERE key = ?', (api_key,))
        conn.commit()

@app.route('/revoke_key', methods=['POST'])
def revoke_key():
    data = request.json
    api_key = data.get('api_key')
    revoke_api_key(api_key)
    return jsonify({"message": "API key revoked successfully."}), 200

# Key Rotation
def rotate_api_key(old_key):
    revoke_api_key(old_key)
    new_key = generate_api_key()
    store_api_key(new_key)
    return new_key

@app.route('/rotate_key', methods=['POST'])
def rotate_key():
    data = request.json
    old_key = data.get('old_key')
    new_key = rotate_api_key(old_key)
    return jsonify({"new_key": new_key}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5006)  # Run on a different port
