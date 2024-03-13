import os
import base64
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
    return encrypted_str, key

def decrypt_func(encrypted_str, key):
    # Initialize the Fernet cipher with the given key
    cipher = Fernet(key)

    # Decrypt the encrypted string
    decrypted_str = cipher.decrypt(encrypted_str)

    # Return the decrypted string
    return decrypted_str.decode('utf-8')

# Test the functions
original_str = 'hello world'
print("Original string:", original_str)

encrypted_str, key = encrypt_func(original_str)
print("Encrypted string:", encrypted_str)
print("Key:", key)

decrypted_str = decrypt_func(encrypted_str, key)
print("Decrypted string:", decrypted_str)

# Check if decrypted string matches original string
assert decrypted_str == original_str, "Decrypted string doesn't match original string"
print("Decrypted string matches original string")
