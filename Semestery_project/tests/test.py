import pytest
from flask import Response

"""
Code Analysis

Objective:
The objective of the verify_password function is to authenticate a user's credentials by checking if the provided username and password match with the ones stored in the database.

Inputs:
- username: a string representing the username of the user trying to authenticate
- password: a string representing the password of the user trying to authenticate

Flow:
1. The function queries the User table in the database to find a user with the provided username.
2. If no user is found, the function returns False.
3. If a user is found, the function sets the current user in the Flask application context (g.current_user).
4. The function then calls the check_password method of the User object to verify if the provided password matches the hashed password stored in the database.
5. If the password is correct, the function returns True, indicating that the user is authenticated. Otherwise, it returns False.

Outputs:
- True: if the provided username and password match with the ones stored in the database and the user is authenticated.
- False: if the provided username does not exist in the database or the provided password does not match with the hashed password stored in the database.

Additional aspects:
- The function uses the HTTPBasicAuth decorator from the Flask-HTTPAuth library to enable basic authentication for the Flask application.
- The function sets the current user in the Flask application context (g.current_user) to be used by other parts of the application.
- The function calls the check_password method of the User object to verify the password, which uses the check_password_hash function from the Werkzeug security library to compare the hashed password stored in the database with the provided password.
"""


class TestVerifyPassword:
    # Tests that verify_password returns True when given a valid username and password.
    def test_verify_password_success(self):
        # Happy path test
        user = User(username="testuser", email="testuser@test.com", pin="password")
        assert user.check_password("password") == True
        assert verify_password("testuser", "password") == True

    # Tests that verify_password returns False when given an invalid username or password.
    def test_verify_password_failure(self):
        # Happy path test
        user = User(username="testuser", email="testuser@test.com", pin="password")
        assert user.check_password("wrongpassword") == False
        assert verify_password("testuser", "wrongpassword") == False

    # Tests that verify_password returns False when given an empty username.
    def test_verify_password_empty_username(self):
        # Edge case test
        assert verify_password("", "password") == False

    # Tests that verify_password returns False when given an empty password.
    def test_verify_password_empty_password(self):
        # Edge case test
        assert verify_password("testuser", "") == False

    # Tests that verify_password still works if the password hashing algorithm changes in the future.
    def test_verify_password_password_hashing(self):
        # General behavior test
        user = User(username="testuser", email="testuser@test.com", pin="password")
        user.pin = "newpassword"
        assert user.check_password("newpassword") == True
        assert verify_password("testuser", "newpassword") == True

    # Tests that verify_password returns False when given a username that does not exist in the database.
    def test_verify_password_nonexistent_user(self):
        # Edge case test
        assert verify_password("nonexistentuser", "password") == False

    # Tests that the basic_auth_error function returns an error response with the correct payload.
    def test_basic_auth_error_returns_error_response_with_correct_payload(self):
        response = basic_auth_error()
        assert response.status_code == 401
        assert response.json == {"error": "Unauthorized"}

    # Tests that the basic_auth_error function returns an error response with a message when provided.
    def test_basic_auth_error_returns_error_response_with_message(self):
        response = basic_auth_error(message="Invalid credentials")
        assert response.status_code == 401
        assert response.json == {
            "error": "Unauthorized",
            "message": "Invalid credentials",
        }

    # Tests that the basic_auth_error function returns a 401 status code.
    def test_basic_auth_error_returns_correct_status_code(self):
        response = basic_auth_error()
        assert response.status_code == 401

    # Tests that the basic_auth_error function returns an error response with a default message when not provided.
    def test_basic_auth_error_returns_error_response_with_default_message(self):
        response = basic_auth_error()
        assert response.status_code == 401
        assert response.json == {"error": "Unauthorized"}

    # Tests that the basic_auth_error function returns an error response.
    def test_basic_auth_error_returns_error_response(self):
        response = basic_auth_error()
        assert isinstance(response, Response)

    # Tests that the basic_auth_error function returns a JSON response.
    def test_basic_auth_error_returns_json_response(self):
        response = basic_auth_error()
        assert response.content_type == "application/json"
