def create_root_user_table():
    return('''
        CREATE TABLE IF NOT EXISTS root_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            encrypted_password TEXT,
            key BLOB
        )
    ''')

def create_password_store_table():
    return('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            account_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            pin TEXT,
            username_key BLOB NOT NULL,
            password_key BLOB NOT NULL,
            pin_key BLOB,
            expiration_date DATE NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES root_user (id)
        )
    ''')