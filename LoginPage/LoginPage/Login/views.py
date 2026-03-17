from .BL.blLogin import signup_user, authenticate_user, get_real_name_by_username
from django.shortcuts import render, redirect
from .BL.blSessions import create_session, validate_session, logout_session


def index(request):
    """
    Main page for login and signup.

    This view receives form data from the browser and sends it to the
    Business Logic layer for processing.

    The view is responsible for:
    - receiving HTTP form data
    - deciding which form was submitted
    - returning feedback to the template
    - setting the session cookie after successful login

    The view is NOT responsible for:
    - checking password hashes
    - encrypting data
    - generating secure session tokens
    """

    message = ""
    success = None

    if request.method == "POST":

        # Identify which form was submitted.
        # This allows one view to safely handle both login and signup
        # without confusing the two workflows.
        form_type = request.POST.get("form_type")

        # Retrieve shared form fields from the POST request.
        # .strip() removes accidental spaces from the beginning or end.
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # ------------------------------------------------------------
        # LOGIN
        # ------------------------------------------------------------
        if form_type == "login":

            # Ask the Business Logic layer to authenticate the user.
            # The view does not compare passwords itself.
            # Instead, BL handles:
            # - retrieving the stored user
            # - verifying the Argon2 password hash
            # - deciding whether login succeeds
            if authenticate_user(username, password):

                # Retrieve extra user information from BL.
                # If the real name is encrypted in storage,
                # the BL handles decrypting it before returning it.
                real_name = get_real_name_by_username(username)

                # Create a new session for this authenticated user.
                # The BL generates the secure token, sets the expiry,
                # creates the Session object, and stores it through the DAL.
                session = create_session(username)

                # Build the HTTP response that will be sent back to the browser.
                # We create the response first because the session cookie
                # must be attached to the response before it is returned.
                response = render(request, "Login/index.html", {
                    "message": f"You have logged in {real_name}",
                    "success": True
                })

                # Store the session token inside a secure browser cookie.
                # This cookie will be sent automatically with future requests.

                response.set_cookie(
                    key="session_token", # The name of the cookie
                    value=session.session_token,  # The actual session token value
                    httponly=True, # Prevents JavaScript from accessing the cookie (protects against XSS)
                    #secure=True, # Cookie is only sent over HTTPS (protects against interception) - commented out for local testing without HTTPS
                    samesite="Strict" # Prevents the cookie being sent with cross-site requests (protects against CSRF)
                )

                # Return immediately because the response is now complete.
                return response

            else:
                # If authentication fails, give a generic error message.
                # We do not reveal whether the username or password was wrong,
                # because that would help attackers test valid usernames.
                message = "Invalid username or password."
                success = False

        # ------------------------------------------------------------
        # SIGNUP
        # ------------------------------------------------------------
        elif form_type == "signup":

            # Retrieve the additional fields only needed for signup.
            real_name = request.POST.get("real_name", "").strip()
            confirm_password = request.POST.get("confirm_password", "").strip()

            # ------------------------------------------------------------
            # BASIC VALIDATION (Presentation Layer)
            # ------------------------------------------------------------

            # Check that all required fields have been completed.
            # This is simple validation the view can do before sending data
            # into deeper layers of the program.
            if username == "" or real_name == "" or password == "" or confirm_password == "":
                message = "All fields must be completed."
                success = False

            # Check that the user typed the same password twice.
            # This prevents accidental typing mistakes during signup.
            elif password != confirm_password:
                message = "Passwords do not match."
                success = False

            else:
                # Send the cleaned signup data to the Business Logic layer.
                # BL should handle the real security rules, such as:
                # - checking username uniqueness
                # - hashing the password
                # - encrypting sensitive data like the real name
                # - applying stronger validation rules if needed
                if signup_user(username, real_name, password):
                    message = "Account created successfully."
                    success = True
                else:
                    # If signup fails, the most likely reason is that
                    # the username already exists.
                    message = "Username already exists."
                    success = False

    # If the request was GET, or if login/signup failed,
    # render the page normally with the message and success flag.
    return render(request, "Login/index.html", {
        "message": message,
        "success": success
    })

# -----------------------------------------------------------
def logged_in_only(request):
    """
    Example protected page.

    This page should only be accessible if the user has a valid session.

    The view does not decide whether a session token is trustworthy.
    Instead, it sends the token to the Business Logic layer, which checks:

    - whether the session exists
    - whether the session has expired
    - which user the session belongs to

    If the session is invalid, the user is redirected back to login.
    """

    # Read the session token from the browser cookie.
    # If the user has logged in successfully, their browser should send
    # this token back to the server with future requests.
    session_token = request.COOKIES.get("session_token")

    # First, check whether the cookie exists at all.
    # If there is no token, there is no evidence that the user is logged in.
    if not session_token:
        return redirect("index")

    # Send the token to the Business Logic layer for proper validation.
    # The BL will:
    # 1. search for the token in storage
    # 2. check whether it has expired
    # 3. return the username if the session is valid
    username = validate_session(session_token)

    # If BL returns None, the session is not valid.
    # This could happen because:
    # - the token does not exist
    # - the token has expired
    # - the token was deleted during logout
    if username is None:
        return redirect("index")

    # If the program reaches this point, the session is valid
    # and the user is allowed to access the protected page.
    return render(request, "Login/LoggedInOnly.html", {
        "username": username
    })



def logout_view(request):
    """
    Log the user out.

    Logging out is not just about deleting the cookie in the browser.
    The session should also be removed from server-side storage so the
    token cannot be reused later.
    """

    # Read the session token stored in the browser cookie.
    session_token = request.COOKIES.get("session_token")

    # If the browser sent a token, ask the Business Logic layer
    # to remove that session from storage.
    if session_token:
        logout_session(session_token)

    # Create a redirect response back to the login page.
    response = redirect("index")

    # Tell the browser to delete the session cookie.
    response.delete_cookie("session_token")

    return response