import os
from django.conf import settings
from cryptography.fernet import Fernet

# ------------------------------------------------------------
# Load encryption key
#
# In this project the key is stored in a separate file so that
# it is not stored inside the database files.
#
# In a real production system, encryption keys should NOT be
# shared with the database or committed to version control.
# They would normally be stored in a secure secrets manager
# or environment configuration on the server.
#
# For this assignment the key file is included so that the
# project can be easily shared and marked.
# ------------------------------------------------------------

# Build the file path to the secret key file.
def get_key_path():
    """
    Build the full file path to the secret key file.

    settings.BASE_DIR points to the Django project folder.
    From there we go into the app (in this example "login"), then the Secrets folder.
    """
    return os.path.join(settings.BASE_DIR, "login", "Secrets", "secret.key")


# Generate a new encryption key and save it to a file.
# This only needs to be done once.
#
# If you lose this key, any data encrypted with it cannot
# be decrypted later.
#
# In a real system this key would be stored more securely.
def generate_key():
    key = Fernet.generate_key()
    key_path = get_key_path()

    # Make sure the Secrets folder exists before writing the file.
    os.makedirs(os.path.dirname(key_path), exist_ok=True)

    with open(key_path, "wb") as f:
        f.write(key)

# Load the encryption key from the file and return it.
def load_key():
    """
    Read the encryption key from the key file and return it.
    """
    key_path = get_key_path()

    with open(key_path, "rb") as f:
        key = f.read()

    return key

# Create and return a Fernet cipher object using the saved key.
def load_cipher():
    """
    Create and return a Fernet cipher object using the saved key.
    """
    key = load_key()
    return Fernet(key)

# Encrypt data and return the encrypted version.
def encrypt_data(data):
    

    cipher = load_cipher()

    # .encode only works on strings so we need to convert the input data into a string before encoding it.
    # Fernet can only encrypt bytes, so we need to convert the input data into bytes before encrypting it.
    data_bytes = str(data).encode()

    # Encrypt the bytes.
    encrypted_bytes = cipher.encrypt(data_bytes)

    # Convert the encrypted bytes back into a normal string
    # so it can be stored in a text file.
    encrypted_text = encrypted_bytes.decode()

    return encrypted_text

# Decrypt an encrypted string and return the original plain text.
# The input should be the encrypted string that was returned by the encrypt_data function.
# The output will be the original plain text that was passed to the encrypt_data function.
def decrypt_data(encrypted_data):
    cipher = load_cipher()

    # Convert the encrypted string back into bytes.
    encrypted_bytes = encrypted_data.encode()

    # Decrypt the bytes.
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    # Convert bytes back into a normal string.
    decrypted_text = decrypted_bytes.decode()

    return decrypted_text