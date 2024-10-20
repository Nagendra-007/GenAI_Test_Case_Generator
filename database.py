import sqlite3

DB_FILE = 'users.db'

def initialize_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT UNIQUE,
                phone TEXT
            )
        ''')
        conn.commit()

def add_user(username, password, email, phone):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, email, phone)
                VALUES (?, ?, ?, ?)
            ''', (username, password, email, phone))
            conn.commit()
    except sqlite3.IntegrityError:
        return False
    return True

def authenticate_user(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    
    # Query to check if the username and password match in the database
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    connection.close()
    
    if user:
        return True
    return False