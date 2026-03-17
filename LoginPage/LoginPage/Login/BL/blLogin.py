# Import the necessary functions and classes from the DAL, hasher, and encryption modules.
from ..DAL.dalLogin import get_user_by_username, username_exists, add_user
from ..Classes.user import User
from .hasher import hash_password, verify_password
from .Encryption import encrypt_data, decrypt_data


def signup_user(username: str, real_name: str, password: str) -> bool:
    """
    Create a new user account.

    Steps performed here:
    1. Check if the username already exists.
    2. Encrypt the real name because it is sensitive information.
    3. Hash the password using Argon2.
    4. Create a User object.
    5. Store the user using the DAL.

    Returns:
        True  -> signup successful
        False -> username already exists
    """

    # Do not allow duplicate usernames.
    if username_exists(username):
        return False

    # Encrypt the real name before storing it.
    # Real names are sensitive personal information,
    # so we do not want to store them as plain text.
    encrypted_real_name = encrypt_data(real_name)

    # Hash the password before storing it.
    # We NEVER store plain text passwords.
    password_hash = hash_password(password)

    # Create a User object containing all stored fields.
    new_user = User(username, encrypted_real_name, password_hash)

    # Save the user record using the DAL.
    add_user(new_user)

    return True


def authenticate_user(username: str, password: str) -> bool:
    """
    Check whether a username and password are correct.

    Steps performed here:
    1. Look up the user using the DAL.
    2. If the user does not exist, login fails.
    3. If the user exists, verify the password hash.

    Returns:
        True  -> login successful
        False -> login failed
    """

    # Ask the DAL to retrieve the user record.
    user = get_user_by_username(username)

    # If the username does not exist in the database,
    # authentication must fail.
    if user is None:
        return False

    # Verify the entered password against the stored Argon2 hash.
    return verify_password(user.password_hash, password)


def get_real_name_by_username(username: str):
    """
    Get the user's real name and decrypt it.

    This is useful after a successful login when we want to display
    a message such as:
        You have logged in Jimmy Smith

    Returns:
        decrypted real name if the user exists
        None if the user does not exist
    """

    # Ask the DAL to retrieve the user record.
    user = get_user_by_username(username)

    # If no user was found, return None.
    if user is None:
        return None

    # The DAL stores the real name in encrypted form.
    # The BL decrypts it when needed.
    real_name = decrypt_data(user.encrypted_real_name)

    return real_name