import secrets
from datetime import datetime, timedelta
from ..Classes.session import Session
from ..DAL.dalSessions import add_session, get_session, delete_session


# ------------------------------------------------------------
# CREATE SESSION
# ------------------------------------------------------------
def create_session(username: str) -> Session:
    """
    Creates a new Session object for a successfully authenticated user.

    This function:
    1. Generates a secure random token
    2. Calculates when the session should expire
    3. Creates a Session object
    4. Stores the session using the DAL
    5. Returns the Session so the view can access its token

    The BL defines the rules for how sessions work,
    while the DAL only handles storing the data.
    """

    # Generate a secure random session token.
    # This must be unpredictable so attackers cannot guess it.
    session_token = secrets.token_hex(32)

    # Work out when the session should expire.
    # Here, the session is valid for 30 minutes.
    expiry = datetime.utcnow() + timedelta(minutes=30)

    # Create a Session object to group all session data together
    session = Session(session_token, username, expiry)

    # Store the session using the DAL
    add_session(session)

    # Return the full Session object (not just the token)
    return session


# ------------------------------------------------------------
# VALIDATE SESSION
# ------------------------------------------------------------
def validate_session(session_token: str):
    """
    Checks whether a session token is valid.

    Returns:
    - the username if the session is valid
    - None if the session is invalid or expired

    This function:
    - retrieves the Session object
    - checks if it exists
    - checks if it has expired
    """

    # Ask the DAL for the Session object linked to this token
    session = get_session(session_token)

    # If no session exists, the token is invalid
    if session is None:
        return None

    # Decision:
    # Check whether the session has expired
    if datetime.utcnow() > session.expiry:

        # If expired, remove it from storage
        delete_session(session_token)

        # Return None to indicate invalid session
        return None

    # If we reach this point, the session is valid
    return session.username


# ------------------------------------------------------------
# LOGOUT SESSION
# ------------------------------------------------------------
def logout_session(session_token: str):
    """
    Logs out a user by deleting their session token.

    This removes the session from storage so it can no longer be used.
    """

    # Remove the session from storage
    delete_session(session_token)