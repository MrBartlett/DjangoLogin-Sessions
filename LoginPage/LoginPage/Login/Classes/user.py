class User:
    """
    Represents one user record from users.txt.

    Attributes:
        username (str): The username stored in the file
        password_hash (str): The Argon2 password hash stored in the file
    """

    def __init__(self, username: str, encrypted_real_name: str, password_hash: str):
        self.username = username
        self.encrypted_real_name = encrypted_real_name
        self.password_hash = password_hash
