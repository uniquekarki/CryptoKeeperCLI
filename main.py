import time
import sqlite3
import os
import getpass
from modules.root import create_root_user
from modules.password import decrypt_func
from modules.db import create_root_user_table, create_password_store_table
from modules.session import store_session_token, remove_session_info
from modules.crud import add_password, view_one_password, view_all_password, update_password

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(create_root_user_table())
    cursor.execute(create_password_store_table())

    conn.commit()
    conn.close()

def get_login():
    time.sleep(2)
    while True:
        os.system('clear')
        command = input("Press 'L' to login, 'C' to create a new user, 'X' to exit: ").lower()
        if command == 'l':
            print("LOGIN:\n")
            root_username = input("Username: ")
            root_password = getpass.getpass("Password: ")
            
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            root_user =  cursor.execute(f'''
                SELECT * FROM root_user WHERE username = '{root_username}'
            ''').fetchone()

            if not root_user:
                print("INVALID USERNAME!\n")
                time.sleep(2)
            else:
                decrypted_password = decrypt_func(root_user[2],root_user[3])
                if not root_password == decrypted_password:
                    print("INVALID PASSWORD!\n")
                    time.sleep(2)
                else:
                    print("LOGIN SUCCESSFUL!\n")
                    store_session_token(root_user[0])
                    time.sleep(2)
                    main()
        elif command == 'c':
            time.sleep(2)
            create_root_user()
        elif command == 'x':
            print('Thank you for using this service!')
            flag = False
            time.sleep(2)
            break
            
           
def main():

    while True:
        time.sleep(2)
        os.system('clear')
        print("WELCOME TO CRYPTO KEEPER: A Secure Password Manager")
        print("===================================================\n")
        print("Options:")
        print("  a    : Add a new password")
        print("  u    : Update an existing password")
        print("  r    : Retrieve a password")
        print("  c    : Change the root password")
        print("  d    : Delete the stored password")
        print("  l    : List all stored passwords")
        print("  e    : Logout")
        print("===================================================")
        user_option = input("\nEnter your option: ").strip().lower()
        print(f"option selected: {user_option}")
        if user_option == "e":
            remove_session_info()
            break
        elif user_option == "a":
            add_password()
        elif user_option == "u":
            update_password()
        elif user_option == "r":
            view_one_password()
        elif user_option == "c":
            pass
        elif user_option == "d":
            pass
        elif user_option == "l":
            view_all_password()

if __name__ == '__main__':
    create_tables()
    remove_session_info()
    get_login()