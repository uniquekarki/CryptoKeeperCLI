from datetime import date
from dateutil.relativedelta import relativedelta
import sqlite3
import os
import time
import getpass
from modules.password import encrypt_func
from prettytable import PrettyTable
import json
from modules.password import decrypt_func

def create_table(fields, values):
    table = PrettyTable()
    
    table.field_names = fields

    for value in values:
        table.add_row(value)
    
    table.align = "l"
    table.padding_width = 1
    table.border = True

    return table

def add_password():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    os.system('clear')

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
    else:
        f = open('session_config.json')
        data = json.load(f)
        user_id = data.get('user_id')

        username_dict = encrypt_func(username)
        password_dict = encrypt_func(password)

        username_encrypted, username_key = username_dict.get('encrypted_str'), username_dict.get('key')
        password_encrypted, password_key = password_dict.get('encrypted_str'), password_dict.get('key')
        
        if expiration_months:
            expiration_date = date.today() + relativedelta(months=+expiration_months)
            optional_fields['expiration_date'] = expiration_date
        
        if pin:
            pin_dict = encrypt_func(pin)
            pin_encrypted, pin_key = pin_dict.get('encrypted_str'), pin_dict.get('key')
            optional_fields['pin'] = pin_encrypted
            optional_fields['pin_key'] = pin_key

        # Dynamically construct the SQL query and parameters based on the optional fields
        query = f"""
                INSERT INTO passwords 
                (account_name, username, password, username_key, password_key, user_id {''.join([f',{field}' for field in optional_fields])}) 
                VALUES (?, ?, ?, ?, ?, ? {''.join([', ?' for _ in optional_fields])})
                """
        params = (account_name, username_encrypted, password_encrypted, username_key, password_key, user_id)
        params += tuple(optional_fields[field] for field in optional_fields)
        curr.execute(query, params)
        conn.commit()
        print("Password Added Successfully!")

def view_one_password():

    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    os.system('clear')

    print("VIEW PASSWORD")
    print("===================================================\n")
    f = open('session_config.json')
    data = json.load(f)
    user_id = data.get('user_id')
    while True:
        account_name = input("Enter the name of the website/account:")
        query = f'''
                SELECT id, account_name, username, password, pin, username_key, password_key, pin_key FROM passwords WHERE user_id = ? AND account_name = ?
                '''
        curr.execute(query, (user_id, account_name))
        values = curr.fetchone()
        if values:
            fields = [description[0] for description in curr.description][:5]
            encrypted_values = values[2:5]
            keys = values[5:]
            relevant_value = [decrypt_func(value,key) for value,key in zip(encrypted_values, keys)]
            table = create_table(fields, [list(values[:2]) + list(relevant_value)])
            print(table)
        else:
            print("No such account in database")
            time.sleep(2)
            break

def view_all_password():

    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    os.system('clear')

    print("VIEW ALL PASSWORDS")
    print("===================================================\n")

    f = open('session_config.json')
    data = json.load(f)
    user_id = data.get('user_id')
    query = f'''
            SELECT id, account_name, username, password, pin, username_key, password_key, pin_key FROM passwords WHERE user_id = ?
            '''
    curr.execute(query, (user_id,))
    values = curr.fetchall()
    if values:
        fields = [description[0] for description in curr.description][:5]
        table_rows = []
        for row in values:
            encrypted_values = row[2:5]
            keys = row[5:]
            relevant_value = [decrypt_func(value,key) for value,key in zip(encrypted_values, keys)]
            table_rows.append(list(row[:2]) + list(relevant_value))
        table = create_table(fields, table_rows)
        print(table)
        print('\nPress any key to exit...')
        input()
    else:
        print("No passwords to list")
        time.sleep(2)

def update_password():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    os.system('clear')

    print("UPDATE PASSWORD")
    print("===================================================\n")

    f = open('session_config.json')
    data = json.load(f)
    user_id = data.get('user_id')
    optional_fields = {}
    account_name = input("Name of the website/account you want to update: ")
    record = curr.execute('SELECT id FROM passwords WHERE user_id = ? AND account_name = ?', (user_id, account_name))
    
    if not record.fetchone():
        print("No Such Record Found!")
        return None
    else:            
        username = input("Enter new username (press Enter to skip): ")
        if username:
            verify_username = getpass.getpass("Enter username again: ")
            if username != verify_username:
                print("Username did not match")
                time.sleep(2)
                return None
            else:
                username_dict = encrypt_func(username)
                username_encrypted, username_key = username_dict.get('encrypted_str'), username_dict.get('key')
                optional_fields['username'] = username_encrypted
                optional_fields['username_key'] = username_key

        password = getpass.getpass("Enter new password (press Enter to skip): ")
        if password:
            verify_password = getpass.getpass("Enter password again: ")
            if password != verify_password:
                print("Password did not match")
                time.sleep(2)
                return None
            else:
                password_dict = encrypt_func(password)
                password_encrypted, password_key = password_dict.get('encrypted_str'), password_dict.get('key')
                optional_fields['password'] = password_encrypted
                optional_fields['password_key'] = password_key
        
        pin = getpass.getpass("Enter new PIN (press Enter to skip): ")
        if pin:
            verify_pin = getpass.getpass("Enter password again: ")
            if pin != verify_pin:
                print("PIN did not match")
                time.sleep(2)
                return None
            else:
                pin_dict = encrypt_func(pin)
                pin_encrypted, pin_key = pin_dict.get('encrypted_str'), pin_dict.get('key')
                optional_fields['pin'] = pin_encrypted
                optional_fields['pin_key'] = pin_key

        expiration_months = input("Enter the number of months for password expiration (press Enter to skip): ")
        if expiration_months:
            expiration_date = date.today() + relativedelta(months=+expiration_months)
            optional_fields['expiration_date'] = expiration_date

        if not optional_fields:
            print("\n\nNo New Update!")
            return None
        else:
            q_str = ''
            for key,val in optional_fields.items():
                q_str += str()

            query = f'''
                    UPDATE
                        passwords
                    SET
                        {' = ?, '.join(key for key in optional_fields.keys())} = ?
                    WHERE
                        user_id = ?
                    AND
                        account_name = ?
                    '''
            params = list(optional_fields.values()) + [user_id, account_name]
            curr.execute(query, params)
            conn.commit()
            print("\n\nSucessfully Updated record!")