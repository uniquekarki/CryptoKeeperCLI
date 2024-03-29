from cryptography.fernet import Fernet

def generate_key():
    # Generate a random 32-byte key
    key = Fernet.generate_key()
    return key

def encrypt_func(original_str):
    # Generate a random key
    key = generate_key()

    # Encrypt the original string using Fernet
    cipher = Fernet(key)
    encrypted_str = cipher.encrypt(original_str.encode())

    # Return the encrypted string and the key
    return {'encrypted_str':encrypted_str, 'key': key}

def decrypt_func(encrypted_str, key):
    # Initialize the Fernet cipher with the given key
    cipher = Fernet(key)

    # Decrypt the encrypted string
    decrypted_str = cipher.decrypt(encrypted_str)

    # Return the decrypted string
    return decrypted_str.decode('utf-8')