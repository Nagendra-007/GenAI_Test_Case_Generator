import sqlite3

DB_FILE = 'users.db'
connection = sqlite3.connect('users.db')
cursor = connection.cursor()

# Query to check if the username and password match in the database
cursor.execute('SELECT * FROM users')
user = cursor.fetchone()
print(user)