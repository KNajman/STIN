
import pytest

"""
Code Analysis

Main functionalities:
The WithdrawalForm class is a FlaskForm used to handle withdrawal requests from a user's account. It allows the user to input the amount they wish to withdraw and select the currency they want to withdraw in. The form also includes a validation method to ensure that the user cannot withdraw more than their account balance.

Methods:
- __init__(self, user, *args, **kwargs): initializes the WithdrawalForm object with the user's account information and any additional arguments or keyword arguments.
- validate_amount(self, amount): validates the amount entered by the user to ensure that it is not greater than their account balance.

Fields:
- amount: an IntegerField that allows the user to input the amount they wish to withdraw.
- currency: a SelectField that allows the user to select the currency they want to withdraw in.
- submit: a SubmitField that allows the user to submit their withdrawal request.
"""

class TestWithdrawalForm:
    # Tests that the form allows a valid withdrawal amount and currency selection. 
    def test_valid_withdrawal(self):
        user = User(account=Account(balance=1000))
        form = WithdrawalForm(user=user, amount=500, currency="USD")
        assert form.validate() is True

    # Tests that the form allows the maximum withdrawal amount and a valid currency selection. 
    def test_maximum_withdrawal(self):
        user = User(account=Account(balance=1000))
        form = WithdrawalForm(user=user, amount=1000, currency="USD")
        assert form.validate() is True

    # Tests that the form raises a validation error when the withdrawal amount exceeds the user's balance. 
    def test_invalid_withdrawal(self):
        user = User(account=Account(balance=1000))
        form = WithdrawalForm(user=user, amount=1500, currency="USD")
        assert form.validate() is False
        assert "You Can Not Withdraw More Than Your Balance." in form.amount.errors

    # Tests that the form raises a validation error when an invalid currency is selected. 
    def test_invalid_currency(self):
        user = User(account=Account(balance=1000))
        form = WithdrawalForm(user=user, amount=500, currency="INVALID")
        assert form.validate() is False
        assert "Not a valid choice" in form.currency.errors

    # Tests that the form is properly initialized with the user object. 
    def test_form_initialization(self):
        user = User(account=Account(balance=1000))
        form = WithdrawalForm(user=user)
        assert form.user == user

    # Tests that the form allows the minimum withdrawal amount and a valid currency selection. 
    def test_minimum_withdrawal(self):
        user = User(account=Account(balance=1000))
        form = WithdrawalForm(user=user, amount=1, currency="USD")
        assert form.validate() is True

    
    # Tests that a valid amount and currency can be submitted. 
    def test_valid_deposit(self, client):
        form_data = {
            "amount": 100,
            "currency": "USD"
        }
        response = client.post("/deposit", data=form_data)
        assert response.status_code == 200
        assert b"Deposit successful!" in response.data

    # Tests that submitting a negative amount raises a validation error. 
    def test_negative_amount(self, client):
        form_data = {
            "amount": -100,
            "currency": "USD"
        }
        response = client.post("/deposit", data=form_data)
        assert b"This field is required." not in response.data
        assert b"Invalid amount." in response.data

    # Tests that submitting a non-integer amount raises a validation error. 
    def test_non_integer_amount(self, client):
        form_data = {
            "amount": "abc",
            "currency": "USD"
        }
        response = client.post("/deposit", data=form_data)
        assert b"This field is required." not in response.data
        assert b"Invalid amount." in response.data

    # Tests that the default value of the amount field is 0. 
    def test_default_amount(self):
        form = DepositForm()
        assert form.amount.data == 0

    # Tests that submitting an invalid currency raises a validation error. 
    def test_invalid_currency(self, client):
        form_data = {
            "amount": 100,
            "currency": "XYZ"
        }
        response = client.post("/deposit", data=form_data)
        assert b"This field is required." not in response.data
        assert b"Invalid currency." in response.data

    # Tests that the amount_in_czk field is correctly calculated based on the exchange rate. 
    def test_amount_in_czk(self):
        form = DepositForm()
        form.amount.data = 100
        form.currency.data = "USD"
        assert form.amount_in_czk.data == 2300.0