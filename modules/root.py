import time
import sqlite3
import os
import getpass
from modules.password import create_key_salt

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