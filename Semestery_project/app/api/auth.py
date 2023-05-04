from flask import g, Response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_login import current_user
from app.models import User
from app.api.errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username: str, password: str):
    """
    Verify the password of a user.

    Args:
        username (str): The username of the user.
        password (str): The password to verify.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error() -> Response:
    return error_response(401)


@token_auth.verify_token
def verify_token(token: str):
    """Verify if the given token is valid and set the current user."""
    return True if g.current_user is not None else False


@token_auth.error_handler
def token_auth_error():
    return error_response(401)
