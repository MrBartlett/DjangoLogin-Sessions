import os
from ..Classes.user import User


def get_users_file_path():
    """
    Return the full path to users.txt.

    The users.txt file acts as our "fake database".
    It is stored in the same folder as this DAL module.

    We build the path dynamically so the program works
    regardless of where the project folder is located.
    """

    # __file__ is the location of this Python file.
    current_folder = os.path.dirname(__file__)

    # Join the folder path with the filename.
    return os.path.join(current_folder, "users.txt")


def get_user_by_username(username: str):
    """
    Search users.txt for a user with the given username.

    Returns:
        User object if the username is found
        None if the username does not exist

    This function is mainly used during login.

    Important:
    The DAL does NOT decrypt the real name and does NOT verify
    the password hash. It only reads raw data from the file.
    """

    file_path = get_users_file_path()

    # If the users file does not exist yet,
    # then there cannot be any users stored.
    if not os.path.exists(file_path):
        return None

    # Open the file for reading.
    with open(file_path, "r", encoding="utf-8") as file:

        # Read the file line by line.
        for line in file:

            # Remove spaces and newline characters.
            line = line.strip()

            # Skip blank lines.
            if not line:
                continue

            # Each line should now be formatted as:
            # username|encrypted_real_name|password_hash
            parts = line.split("|")

            # If the line is not correctly formatted,
            # skip it instead of crashing the program.
            if len(parts) != 3:
                continue

            # Read each part of the stored record.
            stored_username = parts[0]
            encrypted_real_name = parts[1]
            password_hash = parts[2]

            # Check if this record matches the username we are searching for.
            if stored_username == username:

                # Create and return a User object using the raw stored values.
                # The real name stays encrypted here because decryption
                # should happen in the Business Logic layer (BL), not in the DAL.
                return User(stored_username, encrypted_real_name, password_hash)

    # If we reach here, the username was not found.
    return None


def username_exists(username: str) -> bool:
    """
    Check whether a username already exists in the database.

    This is mainly used during signup so we do not allow
    duplicate usernames.

    Returns:
        True  -> username already exists
        False -> username is available
    """

    # Reuse the search function we already wrote.
    user = get_user_by_username(username)

    return user is not None


def add_user(user: User):
    """
    Add a new user record to users.txt.

    The User object should already contain:
        - the username
        - the encrypted real name
        - the hashed password

    Important:
    Encryption and password hashing are NOT done here.
    That happens in the Business Logic layer (BL).

    The DAL's job is only to store the final values.
    """

    file_path = get_users_file_path()

    # Open the file in append mode ("a").
    # This means new data will be added to the end of the file
    # without deleting the existing records.
    with open(file_path, "a", encoding="utf-8") as file:

        # Write the new record in the format:
        # username|encrypted_real_name|password_hash
        file.write(f"{user.username}|{user.encrypted_real_name}|{user.password_hash}\n")