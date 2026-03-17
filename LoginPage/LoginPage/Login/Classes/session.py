from datetime import datetime


class Session:
    def __init__(self, session_token: str, username: str, expiry: datetime):
        # Unique random token used to identify this session
        self.session_token = session_token

        # Username of the logged-in user this session belongs to
        self.username = username

        # Time when this session expires
        self.expiry = expiry