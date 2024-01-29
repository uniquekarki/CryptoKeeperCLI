import json
import os
import uuid
import time

SESSION_FILE = "session_config.json"

def generate_session_token():
    return str(uuid.uuid4())

def store_session_token(user_id):
    session_token = generate_session_token()
    config = {"user_id": user_id,"session_token": session_token}
    with open(SESSION_FILE, "w") as config_file:
        json.dump(config, config_file)

def get_session_info():
    try:
        with open(SESSION_FILE, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return None

def check_session_validity():
    session_info = get_session_info()
    return session_info is not None and "session_token" in session_info

def remove_session_info():
    try:
        os.remove(SESSION_FILE)
        print("Logout Successful.")
        time.sleep(2)
    except FileNotFoundError:
        print("No active session to logout from.")
        time.sleep(2)