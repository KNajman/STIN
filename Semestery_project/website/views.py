from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Account, User
from . import db
import json
import functions

views = Blueprint('views', __name__)


# Home page
@views.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", user=current_user)

# User account page
@views.route("/account", methods=["GET"])
@login_required
def account():
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template("account.html", user=current_user, accounts=user_accounts)

# Add new account page
@views.route("/add_account", methods=["GET", "POST"])
@login_required
def add_account():
    if request.method == "POST":
        account_type = request.form.get("account_type")
        balance = request.form.get("balance")
        if account_type and balance:
            new_account = Account(account_type=account_type, balance=balance, user_id=current_user.id)
            db.session.add(new_account)
            db.session.commit()
            flash("Nový účet byl vytvořen!", category="success")
            return redirect(url_for("views.account"))
        else:
            flash("Něco je špatně, zkontrolujte, zda jste vyplnili všechna pole.", category="error")
    return render_template("add_account.html", user=current_user)

# Transfer money page
@views.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        from_account = request.form.get("from_account")
        to_account = request.form.get("to_account")
        amount = request.form.get("amount")
        if from_account and to_account and amount:
            from_account = Account.query.filter_by(id=from_account).first()
            to_account = Account.query.filter_by(id=to_account).first()
            if from_account and to_account and from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                new_transaction = Transaction(amount=amount, from_account=from_account.id, to_account=to_account.id)
                db.session.add(new_transaction)
                db.session.commit()
                flash("Převod byl úspěšně proveden!", category="success")
                return redirect(url_for("views.account"))
            else:
                flash("Něco je špatně, zkontrolujte, zda jste vyplnili všechna pole a zda máte dostatek prostředků na účtu.", category="error")
        else:
            flash("Něco je špatně, zkontrolujte, zda jste vyplnili všechna pole.", category="error")
    return render_template("transfer.html", user=current_user, accounts=user_accounts)
