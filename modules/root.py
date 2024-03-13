import time
import sqlite3
import os
import getpass
from modules.password import encrypt_func

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
            encrypted_dict = encrypt_func(root_password)
            encrypted_password = encrypted_dict.get('encrypted_str')
            key = encrypted_dict.get('key')
            query = f"INSERT INTO root_user (username, encrypted_password, key) VALUES (?,?,?);"                
            curr.execute(query, (root_username, encrypted_password, key))
            conn.commit()
            print(f"\nRoot user {root_username} created successfully!")
        else:
            print(f"\nRoot user {root_username} exists!")
        time.sleep(2)
        conn.close()
        break