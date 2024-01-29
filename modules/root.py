import time
import sqlite3
import os
import getpass
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def encrypt_password(password, salt):
    # Derive a key from the raw password using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend = default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode())).decode('utf-8')
    return key

def create_key_salt(root_password):

    # Generate a random salt for the root user
    salt = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')

    key = encrypt_password(root_password,salt)
    return {'key': str(key), 'salt': str(salt)}

def create_root_user():
    conn = sqlite3.connect('database.db')
    os.system('clear')
    while True:
        print("CREATE NEW ROOT USER:")
        print("===================================================\n")
        root_username = input("Enter unique username: ")
        root_password = getpass.getpass("Create a strong password: ")

        curr = conn.cursor()
        
        if_exists =  curr.execute(f'''
            SELECT * FROM root_user WHERE username = '{root_username}'
        ''').fetchone()

        if not if_exists:
            encrypted_dict = create_key_salt(root_password=root_password)
            encrypted_password = encrypted_dict['key']
            salt = encrypted_dict['salt']
            query = f"INSERT INTO root_user (username, encrypted_password, salt) VALUES (?,?,?);"                
            curr.execute(query, (root_username, encrypted_password, salt))
            conn.commit()
            print(f"\nRoot user {root_username} created successfully!")
        else:
            print(f"\nRoot user {root_username} exists!")
        time.sleep(2)
        conn.close()
        break