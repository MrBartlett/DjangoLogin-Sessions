from .BL.bl import signup_user, authenticate_user, get_real_name_by_username
from django.shortcuts import render, redirect


def index(request):
    """
    Main page for login and signup.

    This view receives form data and sends it to the
    Business Logic layer for processing.
    """

    message = ""
    success = None
    # We check if the request method is POST, which means that the user has submitted a form.
    if request.method == "POST":
        # We use the form_type field to determine whether the user is trying to log in or sign up.
        form_type = request.POST.get("form_type")
        # We get the common fields (username and password) from the form data.
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # ------------------------------------------------------------
        # LOGIN
        # ------------------------------------------------------------
        if form_type == "login":
            # Validate the form data before sending it to BL.
            if authenticate_user(username, password):

                # Get the decrypted real name from BL
                real_name = get_real_name_by_username(username)

                message = f"You have logged in {real_name}"
                success = True
                # In a real application, we would also create a session token here and send it to the browser as a cookie.
            else:
                message = "Invalid username or password."
                success = False

        # ------------------------------------------------------------
        # SIGNUP
        # ------------------------------------------------------------
        elif form_type == "signup":
            # For signup, we need to get the real name and confirm password fields as well.
            real_name = request.POST.get("real_name", "").strip()
            confirm_password = request.POST.get("confirm_password", "").strip()

            # Validate the form data before sending it to BL.
            if username == "" or real_name == "" or password == "" or confirm_password == "":
                message = "All fields must be completed."
                success = False

            # In a real application, we would also validate the password strength here.
            elif password != confirm_password:
                message = "Passwords do not match."
                success = False

            # If the form data is valid, we send it to the BL to create the account.
            else:
                # The BL will return False if the username already exists, and True if the account was created successfully.
                if signup_user(username, real_name, password):
                    # If the account was created successfully, we can log the user in immediately.
                    message = "Account created successfully."
                    success = True
                else:
                    # The most likely reason for failure is that the username already exists.
                    message = "Username already exists."
                    success = False

    # Finally, we render the page with the message and success status to inform the user of the result of their action.
    return render(request, "Login/index.html", {
        "message": message,
        "success": success
    })

# -----------------------------------------------------------
def logged_in_only(request):
    """
    Example protected page.

    This page should only be accessible if the user is logged in.

    In the future, this will work by checking a session token that
    is stored in the user's browser cookie.

    For now, we simply check whether the cookie exists.
    In the next lesson we will add proper validation of the token.
    """

    # Read the session token from the browser cookie.
    # If the user has logged in successfully, the server
    # will later send this cookie to the browser.
    session_token = request.COOKIES.get("session_token")

    # If there is no session token at all, the user is not logged in.
    # Redirect them back to the login page.
    if not session_token:
        # Redirect is the correct way to send a user to a new page
        return redirect("index")

    # ------------------------------------------------------------
    # Future step (next lesson)
    # ------------------------------------------------------------
    # Here we will validate the session token by:
    #
    # 1. Searching for the token in sessions.txt
    # 2. Checking that the session has not expired
    # 3. Retrieving the username linked to the session
    #
    # If the token is invalid or expired,
    # the user will be redirected to login.

    # For now we assume the token is valid if it exists.
    return render(request, "Login/LoggedInOnly.html")