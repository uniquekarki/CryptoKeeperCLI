import time
import sqlite3
import os
import getpass
import json
from modules.password import encrypt_func, decrypt_func

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

def change_root_password():
    os.system('clear')
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()

    print("CHANGE ROOT PASSWORD")
    print("===================================================\n")


    f = open('session_config.json')
    data = json.load(f)
    user_id = data.get('user_id')

    root_user =  curr.execute(f'''
        SELECT * FROM root_user WHERE id = '{user_id}'
    ''').fetchone()

    current_password = getpass.getpass("Enter Current Password: ")
    decrypted_password = decrypt_func(root_user[2],root_user[3])
    if not current_password == decrypted_password:
        print("Invalid Password!")
        return None
    else:
        new_password = getpass.getpass("Enter New Password: ")
        re_new_password = getpass.getpass("Enter New Password Again: ")
        if new_password == re_new_password:
            encrypted_dict = encrypt_func(new_password)
            encrypted_password = encrypted_dict.get('encrypted_str')
            key = encrypted_dict.get('key')
            query = '''
                    UPDATE root_user
                    SET encrypted_password = ?, key = ?
                    WHERE id = ?
                    '''
            curr.execute(query, (encrypted_password, key, user_id))
            conn.commit()
            conn.close()
            print("\nRoot Password Successfully Updated!")
            time.sleep(2)
        else:
            print("\nPasswords did not match!")
            time.sleep(2)
