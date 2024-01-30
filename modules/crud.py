import sqlite3
import os
import time
import getpass

def add_password():
    print()
    conn = sqlite3.connect('database.db')
    os.system('clear')
    while True:
        print("ADD PASSWORD")
        print("===================================================\n")
        account_name = input("Name of the website/account: ")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        verify_password = getpass.getpass("Enter password again: ")
        if not password == verify_password:
            print("Password did not match")
            time.sleep(2)
            continue
        else:
            