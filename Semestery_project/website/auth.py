from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import functions as my_functions

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        pin = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.pin, pin):
                flash("Uspěšné přihlášení!", category="success")
                login_user(user, remember=True)
                hash = my_functions.send_validation_email(user.email)
                return redirect(url_for("auth.verification", hash=hash))
            else:
                flash("Špatně zadaný PIN.", category="error")
        else:
            flash("Email není registrován.", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Odhlášení proběhlo úspěšně.", category="success")
    return redirect(url_for("auth.login"))


@auth.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("firstName")
        pin = request.form.get("pin")
        pin_again = request.form.get("pin-again")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email je již registrována.", category="error")
        elif my_functions.is_valid_email(email) == False:
            flash("Email není platný.", category="error")
        elif my_functions.is_valid_name(name) == False:
            flash("Jméno musí být delší než 1 znak.", category="error")
        elif my_functions.is_valid_pin(pin) == False:
            flash("PIN musí být dlouhý 4 znaky", category="error")
        elif my_functions.hash_code_generator(pin) != my_functions.hash_code_generator(
            pin_again
        ):
            flash("PIN se neshoduje.", category="error")

            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(pin, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Účet vytvořen!", category="success")
            return redirect(url_for("views.home"))

    return render_template("registration.html", user=current_user)


@auth.route("/verification", methods=["GET", "POST"])
def verification():

    hash = request.args.get("hash")

    if request.method == "POST":
        code = request.form.get("code")

        if check_password_hash(hash, code):
            flash("Úspěšně ověřeno!", category="success")
            return redirect(url_for("views.home"))
        else:
            flash("Špatný kód!", category="error")

    return render_template("verification.html", user=current_user)
