from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

# Create one PasswordHasher instance for the entire module.
# This avoids recreating it every time a function is called.
ph = PasswordHasher()

# The hash function will automatically generate a random salt and include it in the returned hash string.
def hash_password(password: str) -> str:
    """
    Hash a user's password using Argon2.

    This function should be used when creating new user accounts.
    The returned hash should be stored in the users.txt file.
    """
    # The hash function will automatically generate a random salt and include it in the returned hash string.
    return ph.hash(str(password))

# The verify function will check the password against the stored hash, including the salt and all parameters.
def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verify that a password matches the stored Argon2 hash.

    Returns True if the password is correct.
    Returns False if the password is incorrect or the hash is invalid.
    """
    # The verify function will raise an exception if the password does not match the hash,
    try:
        # or if the stored hash is not a valid Argon2 hash.
        return ph.verify(stored_hash, str(password))
    # In either case, we return False to indicate that the password is not valid.
    except (VerifyMismatchError, InvalidHash):
        # In a real application, we might want to log these exceptions for security monitoring purposes.
        return False