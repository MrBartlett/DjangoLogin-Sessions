from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

# Create one PasswordHasher instance for the entire module.
# This avoids recreating it every time a function is called.
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a user's password using Argon2.

    This function should be used when creating new user accounts.
    The returned hash should be stored in the users.txt file.
    """
    return ph.hash(str(password))


def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verify that a password matches the stored Argon2 hash.

    Returns True if the password is correct.
    Returns False if the password is incorrect or the hash is invalid.
    """

    try:
        return ph.verify(stored_hash, str(password))
    except (VerifyMismatchError, InvalidHash):
        return False