def create_root_user_table():
    return('''
        CREATE TABLE IF NOT EXISTS root_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            encrypted_password TEXT,
            salt TEXT
        )
    ''')