from datetime import date
from dateutil.relativedelta import relativedelta
import sqlite3
import os
import time
import getpass
from modules.password import create_key_salt

def add_password():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    os.system('clear')

    while True:
        print("ADD PASSWORD")
        print("===================================================\n")

        account_name = input("Name of the website/account: ")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        verify_password = getpass.getpass("Enter password again: ")
        pin = getpass.getpass("Enter PIN if relevant: ")
        expiration_months = input("Enter the number of months for password expiration (press Enter to skip): ")

        optional_fields = {}

        if not password == verify_password:
            print("Password did not match")
            time.sleep(2)
            break
        else:
            username_dict = create_key_salt(username)
            password_dict = create_key_salt(password)
            if pin:
                pin_dict = create_key_salt(pin)

            username_key, username_salt = username_dict.get('key'), username_dict.get('salt')
            password_key, password_salt = password_dict.get('key'), password_dict.get('salt')
            
            if expiration_months:
                expiration_date = date.today() + relativedelta(months=+expiration_months)
                optional_fields['expiration_date'] = expiration_date
            
            if pin:
                pin_key, pin_salt = pin_dict.get('key'), pin_dict.get('salt')
                optional_fields['pin_key'] = pin_key
                optional_fields['pin_salt'] = pin_salt

            # Dynamically construct the SQL query and parameters based on the optional fields
            query = f"""
                    INSERT INTO passwords 
                    (account_name, username, password, username_salt, password_salt {''.join([f',{field}' for field in optional_fields])}) 
                    VALUES (?, ?, ?, ?, ? {''.join([', ?' for _ in optional_fields])})
                    """
            params = (account_name, username_key, password_key, username_salt, password_salt)
            params += tuple(optional_fields[field] for field in optional_fields)
            curr.execute(query, params)
            conn.commit()
            print("Password Added Successfully!")
            break