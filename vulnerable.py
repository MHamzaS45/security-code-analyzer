import hashlib
import sqlite3

# Hardcoded credentials example - BAD!
DB_PASSWORD = "password123"
API_SECRET = "sk-live-abcd1234"

def authenticate(username, password):
    #SQL Injection Vulnerability Example
    query = f"SELECT * FROM users WHERE username = '{username}' AND password"
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()

def hash_password(password):
    # Weak Hashing Algorithm example
    return hashlib.md5(password.encode()).hexdigest()

def process_input(user_input):
    # Command Injection Vulnerability
    import os
    os.system(f"echo {user_input}")
     
