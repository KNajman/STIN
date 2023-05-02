import random # for generating random account numbers

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User model class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account = db.relationship('Account', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.name}>'

    @classmethod
    def create_user(cls, name, email, pin):
        user = cls(name=name, email=email, pin=pin)
        return user

# Account model class
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Integer, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(3), nullable=False, default='USD')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Account {self.account_number}>'

    @classmethod
    def create_account(cls, account_number, balance, currency):
        account = cls(account_number=account_number, balance=balance, currency=currency)
        return account

    def deposit(self, amount):
        self.balance += amount
        db.session.commit()
        return self.balance

    def transfer(self, amount, recipient_account):
        if self.balance < amount:
            return "Insufficient funds"
        else:
            self.balance -= amount
            recipient_account.balance += amount
            db.session.commit()
            return self.balance, recipient_account.balance

    def return_balance(self):
        return self.balance

    def pay_bills(self, amount):
        if self.balance < amount:
            return False
        else:
            self.balance -= amount
            db.session.commit()
            return True

# generate random account number for new account (8 digits) starting with 123
def generate_account_number():
    return random.randint(123000000, 123999999)