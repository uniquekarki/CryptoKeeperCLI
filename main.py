import time
import sqlite3
import os
import getpass
from modules.root import create_root_user, encrypt_password
from modules.db import create_root_user_table
from modules.session import store_session_token, remove_session_info

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(create_root_user_table())

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
                key = encrypt_password(root_password,root_user[3])
                if not key == root_user[2]:
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
        print("  add       : Add a new password")
        print("  update    : Update an existing password")
        print("  retrieve  : Retrieve a password")
        print("  change    : Change the root password")
        print("  delete    : Delete the stored password")
        print("  list      : List all stored passwords")
        print("  logout    : Logout")
        print("===================================================")
        user_option = input("\nEnter your option: ").strip().lower()
        print(f"option selected: {user_option}")
        if user_option == "logout":
            remove_session_info()
            break
        elif user_option == "add":
            pass
        elif user_option == "update":
            pass
        elif user_option == "retrieve":
            pass
        elif user_option == "change":
            pass
        elif user_option == "delete":
            pass
        elif user_option == "list":
            pass

if __name__ == '__main__':
    create_tables()
    get_login()