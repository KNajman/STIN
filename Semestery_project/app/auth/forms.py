from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from app.models import User, UserBankAccount

from app.mail_sending import send_validation_email


class RegisterForm(FlaskForm):
    """
    Form for user registration.
    """

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=5, max=20)],
        render_kw={"placeholder": "login name"},
    )
    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"placeholder": "first name"},
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"placeholder": "last name"},
    )
    email = StringField("Email", validators=[DataRequired(), Email()])

    pin = PasswordField(
        "PIN",
        validators=[DataRequired(), Length(min=4, max=4)],
        render_kw={"placeholder": "4 digit pin"},
    )
    pin2 = PasswordField(
        "Confirm PIN",
        validators=[DataRequired(), EqualTo("pin"), Length(min=4, max=4)],
        render_kw={"placeholder": "confirm 4 digit pin"},
    )
    submit = SubmitField("Register")


def validate_email(self, email: str):
    """
    Check if email is already registered.

    :param email: The email to check.
    :raises ValidationError: If the email is already registered.
    """

    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError("Email already exists, please pick another email.")


def validate_username(user: User, username: str):
    """
    Check if username is already taken.
    """
    if not username:
        raise ValidationError("Username cannot be empty.")
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError("Username already exists, please pick another username.")


class LoginForm(FlaskForm):
    """
    Form for user login.
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=50)]
    )
    pin = PasswordField("PIN", validators=[DataRequired(), Length(min=4, max=4)])
    submit = SubmitField("Log In")


class TwoStepVerification(FlaskForm):
    """
    Form for two step verification
    """

    code = StringField(
        "Code",
        validators=[DataRequired(), Length(min=6, max=6)],
        render_kw={"placeholder": "6 digit code"},
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Submit")
