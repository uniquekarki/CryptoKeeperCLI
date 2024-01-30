def create_root_user_table():
    return('''
        CREATE TABLE IF NOT EXISTS root_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            encrypted_password TEXT,
            salt TEXT
        )
    ''')

def create_password_store_table():
    return('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT,
            username TEXT,
            password TEXT,
            salt TEXT,
            FOREIGN KEY (user_id) REFERENCES root_user (id)
        )
    ''')