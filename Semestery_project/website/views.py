from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Account, User
from . import db
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for

import functions as my_functions

views = Blueprint("views", __name__)

supported_currencies = [
    "USD",
    "EUR",
    "GBP",
    "CHF",
    "JPY",
    "CAD",
    "AUD",
    "NZD",
    "RUB",
    "CNY",
]


# Home page
@views.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", user=current_user)


# Deposit page + possibility to deposit money in different currencies
@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        amount = request.form.get("amount")
        currency = request.form.get("currency")
        if amount == "":
            flash("Please enter a valid amount", category="error")
        else:
            amount = float(amount)
            if amount <= 0:
                flash("Please enter a valid amount", category="error")
            else:
                # Check if the currency is supported by the bank

                if currency not in supported_currencies:
                    flash("The selected currency is not supported", category="error")
                else:
                    # Check if the bank account is associated with the user
                    if current_user.account is None:
                        flash("You don't have a bank account", category="error")
                    else:
                        # Deposit the money
                        current_user.deposit(amount, currency)
                        flash("Deposit successful", category="success")
    return render_template("deposit.html", user=current_user)


# Payment page + possibility to pay in different currencies
@views.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    if request.method == "POST":
        amount = request.form.get("amount")
        currency = request.form.get("currency")
        if not amount:
            flash("Please enter a valid amount", category="error")
        else:
            try:
                amount = float(amount)
            except ValueError:
                flash("Please enter a valid amount", category="error")
            else:
                if amount <= 0:
                    flash("Please enter a valid amount", category="error")
                else:
                    # Check if the currency is supported by the bank
                    if currency not in supported_currencies:
                        flash(
                            "The selected currency is not supported", category="error"
                        )
                    else:
                        # Check if the bank account is associated with the user
                        if current_user.account is None:
                            flash("You don't have a bank account", category="error")
                        else:
                            # Pay the bill
                            success = current_user.pay_bills(amount, currency)
                    if success:
                        flash("Payment successful", category="success")
                    else:
                        flash(
                            "Payment failed. Please check your account balance and try again.",
                            category="error",
                        )
    return render_template(
        "payment.html", user=current_user, supported_currencies=supported_currencies
    )
