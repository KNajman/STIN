import base64
import os
from app import db
from datetime import datetime, timedelta
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.mail_sending import send_validation_email


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    pin_hash = db.Column(db.String(32))
    two_factor_hash = db.Column(db.String(32))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    account_id = db.Column(db.Integer, db.ForeignKey("userbankaccounts.id"))
    deposits = db.relationship(
        "Deposit", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    withdrawals = db.relationship(
        "Withdrawal", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    interests = db.relationship(
        "Interest", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"{self.username}"

    @property
    def pin(self):
        raise AttributeError("Password field is not readable")

    @pin.setter
    def pin(self, password_hash: str):
        self.pin_hash = generate_password_hash(password_hash)

    def check_password(self, password_hash: str):
        return check_password_hash(self.pin_hash, password_hash)

    @property
    def full_name(self):
        if hasattr(self, "account"):
            return f"{self.account.first_name.title()} {self.account.last_name.title()}"

    @property
    def balance(self):
        if hasattr(self, "account"):
            return self.account.balance

    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
            "account_no": self.account.account_no,
            "first_name": self.account.first_name,
            "last_name": self.account.last_name,
            "balance": str(self.balance),
            "acct_created_at": self.account.created_at.isoformat() + "Z",
        }
        return data

    def from_dict(self, data: dict, new_user: bool = False):
        for field in ["username", "email"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "pin" in data:
            self.pin = data["pin"]
        if "two_factor" in data:
            self.set_two_factor_hash(data["two_factor"])

    def get_token(self, expires_in: int = 3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def set_two_factor_hash(self, two_factor: str):
        self.two_factor_hash = two_factor

    def get_email(self):
        return self.email

    def check_two_factor(self, two_factor: str):
        print(self.two_factor_hash)
        if self.two_factor_hash is None:
            return True
        else:
            return check_password_hash(self.two_factor_hash, two_factor)

    def send_two_factor_email(self):
        hash = send_validation_email(self.email)
        self.set_two_factor_hash(hash)

    @staticmethod
    def check_token(token: str):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login_manager.user_loader
def load_user(id: int):
    return User.query.get(int(id))


class UserBankAccount(db.Model):
    __tablename__ = "userbankaccounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_no = db.Column(db.String(10), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    initial_deposit_date = db.Column(db.DateTime)
    user = db.relationship("User", backref="account", lazy=True, uselist=False)

    def __repr__(self) -> str:
        return f"{self.account_no}"


class Deposit(db.Model):
    __tablename__ = "deposits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    currency = db.Column(db.String(3), default="CZK")

    def __repr__(self):
        return f"{self.user.username}"
    
    def get_currency(self):
        return self.currency
    
    def set_currency(self, currency):
        self.currency = currency


class Withdrawal(db.Model):
    __tablename__ = "withdrawals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    currency = db.Column(db.String(3), default="CZK")

    def __repr__(self):
        return f"{self.user.username}"
    
    def get_currency(self):
        return self.currency
    
    def set_currency(self, currency):
        self.currency = currency


class Interest(db.Model):
    __tablename__ = "interests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"{self.user.username}"
