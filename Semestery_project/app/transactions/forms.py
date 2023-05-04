from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from app.cnb_requests import get_currency_list


class DepositForm(FlaskForm):
    amount = IntegerField("amount", validators=[DataRequired()], default=0)
    # currency as a dropdown menu
    currency = SelectField(
        "currency", choices=get_currency_list(), validators=[DataRequired()]
    )
    # submit = SubmitField('Deposit')
    # amount_in_czk = amount * exchange_rate

    submit = SubmitField("Deposit")


class WithdrawalForm(FlaskForm):
    amount = IntegerField("amount", validators=[DataRequired()], default=0)
    # currency as a dropdown menu
    currency = SelectField(
        "currency", choices=get_currency_list(), validators=[DataRequired()]
    )
    # submit = SubmitField('Withdraw')
    # amount_in_czk = amount * exchange_rate

    submit = SubmitField("Withdraw")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def validate_amount(self, amount):
        if self.user.account.balance < amount.data:
            raise ValidationError("You Can Not Withdraw More Than Your Balance.")
