import sqlite3
import os
import time
import getpass

def add_password():
    print()
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    os.system('clear')

    while True:
        print("ADD PASSWORD")
        print("===================================================\n")
        account_name = input("Name of the website/account: ")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        pin = getpass.getpass("Enter PIN if relevant: ")
        verify_password = getpass.getpass("Enter password again: ")
        if not password == verify_password:
            print("Password did not match")
            time.sleep(2)
            continue
        else:
            query = f"INSERT INTO passwords (account_name, username, password, pin, salt) VALUES (?,?,?);"                
            curr.execute(query, (account_name, username, password, pin, salt))
            conn.commit()