import sqlite3

conn = sqlite3.connect('password_manager.sql')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS root (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        
    )
''')