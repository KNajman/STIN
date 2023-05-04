from flask import (
    render_template,
    redirect,
    session,
    url_for,
    flash,
    request,
    current_app,
)
from . import auth
from werkzeug.urls import url_parse
from app import db
from flask_login import current_user, login_user, logout_user
from app.auth.forms import RegisterForm, LoginForm, TwoStepVerification
from random import randint
from app.models import *
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.mail_sending import send_validation_email


def generate_account_no():
    num = "".join([f"{randint(0, 9)}" for _ in range(0, 10)])
    return int(num)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("transaction.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                pin=form.pin.data,
            )

            accout_details = UserBankAccount(
                account_no=generate_account_no(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )

            db.session.commit()

            new_user.account = accout_details

            if new_user.email in current_app.config["ADMINS"]:
                new_user.is_admin = True

            db.session.add(new_user)
            db.session.commit()

            flash(
                """Thank You For Creating A Bank Account {}.
                    Your Account Number is {}, Please use this number to login
                    s""".format(
                    new_user.full_name, new_user.account.account_no
                ),
                "success",
            )
            return redirect(url_for("auth.login"))
        except Exception as e:
            print(e)
            flash("Registration failed, please try again later", "danger")
            return redirect(url_for("auth.register"))

    context = {
        "title": "Create a Bank Account",
        "form": form,
    }

    return render_template("auth/register.html", **context)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("transaction.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.pin.data):
            flash("Invalid username or password", "warning")
            return redirect(url_for("auth.login"))
        else:
            session["user_id"] = user.id
            return redirect(url_for("auth.verification"))

    context = {"form": form, "title": "Load Account Details"}
    return render_template("auth/login.html", **context)


@auth.route("/verification", methods=["GET", "POST"], endpoint="verification")
def verification():
    # get the user from the database
    user = User.query.filter_by(id=session.get("user_id")).first()
    if user is None:
        return redirect(url_for("auth.login"))
    else:
        if current_user.is_authenticated:
            return redirect(url_for("transaction.index"))

    user.send_two_factor_email()
    user.set_two_factor(hash)

    form = TwoStepVerification()
    if form.validate_on_submit():
        code = form.code.data
        if user.check_two_factor(generate_password_hash(code)):
            # mark the user as authenticated
            session["user_id"] = user.id
            login_user(user, remember=form.remember_me.data)
            flash("You have been logged in.")
            return redirect(url_for("transaction.index"))
        else:
            flash("Invalid two-factor authentication code.")
    return render_template("auth/verification.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))
