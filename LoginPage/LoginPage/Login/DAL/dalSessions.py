# -------------------------------------------------------------
# Session management
# -------------------------------------------------------------

import os
from datetime import datetime
from ..Classes.session import Session


# ------------------------------------------------------------
# GET FILE PATH
# ------------------------------------------------------------
def get_sessions_file_path():
    """
    Returns the full path to the sessions.txt file.

    This function builds the file path step-by-step.
    First it finds the folder this DAL file is stored in,
    then it attaches the filename sessions.txt to that folder.
    """

    # Find the folder this Python file is located in
    current_dir = os.path.dirname(__file__)
    
    # Build and return the full path to sessions.txt
    return os.path.join(current_dir, "sessions.txt")


# ------------------------------------------------------------
# ADD SESSION
# ------------------------------------------------------------
def add_session(session: Session):
    """
    Stores a Session object in sessions.txt.

    The BL creates the Session object, and the DAL is responsible
    for saving its data into permanent storage.

    Each session is stored as one line in the file using this format:
    session_token|username|expiry
    """

    # Find where the sessions file is located
    path = get_sessions_file_path()

    # Open the file in append mode so we add the new session
    # without deleting any existing ones
    with open(path, "a") as file:

        # Write the Session object's values as one line of text
        # expiry is converted to ISO format so it can be turned
        # back into a datetime object later
        file.write(f"{session.session_token}|{session.username}|{session.expiry.isoformat()}\n")


# ------------------------------------------------------------
# GET SESSION
# ------------------------------------------------------------
def get_session(session_token: str):
    """
    Retrieves a Session object by its session token.

    This function checks whether the file exists first.
    If it does, it loops through each stored session one at a time
    until it finds a matching token.

    Returns:
    - a Session object if found
    - None if no matching session exists
    """

    # Find the file location
    path = get_sessions_file_path()

    # Before reading the file, check that it actually exists.
    # If it does not exist yet, then there are no stored sessions.
    if not os.path.exists(path):
        return None

    # Open the file and check each line one by one
    with open(path, "r") as file:
        for line in file:

            # Split the line into its three stored values
            parts = line.strip().split("|")

            # If the line is damaged or not in the correct format,
            # skip it so the program does not crash
            if len(parts) != 3:
                continue

            stored_token, username, expiry_str = parts

            # Check whether this is the session we are looking for
            if stored_token == session_token:

                # Convert the stored expiry string back into a datetime object
                expiry = datetime.fromisoformat(expiry_str)

                # Return a Session object containing the stored data
                return Session(stored_token, username, expiry)

    # If the loop finishes and no token matched, return None
    return None


# ------------------------------------------------------------
# DELETE SESSION
# ------------------------------------------------------------
def delete_session(session_token: str):
    """
    Removes a session from storage.

    This function reads all stored sessions, then rewrites the file
    while leaving out the session that matches the token provided.

    This is used when a user logs out or when a session expires.
    """

    # Find the file location
    path = get_sessions_file_path()

    # If the file does not exist, there is nothing to delete
    if not os.path.exists(path):
        return

    # Read all session records into memory
    with open(path, "r") as file:
        lines = file.readlines()

    # Rewrite the file, keeping only the sessions
    # that do not match the token being deleted
    with open(path, "w") as file:
        for line in lines:

            # If this line does NOT belong to the session being deleted,
            # write it back into the file
            if not line.startswith(session_token + "|"):
                file.write(line)

            # If it DOES match, we skip writing it back
            # which removes it from storage