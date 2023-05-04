from flask import jsonify, request, url_for, g
from app import db
from datetime import datetime
from app.api import api
from app.models import User, Deposit, Withdrawal, UserBankAccount
from app.auth.views import generate_account_no
from app.api.auth import token_auth
from .errors import bad_request
from dateutil.parser import parse

@api.get('/user_account_details/')
@token_auth.login_required
def get_user_acct():
    if g.current_user.account is not None:
        return jsonify(User.query.get_or_404(g.current_user.id).to_dict())
    else:
        return {}


@api.post('/deposit/')
@token_auth.login_required
def deposit_amt():
    user = User.query.get_or_404(g.current_user.id)
    data = request.get_json()['amt'] or {}

    deposit = Deposit(amount=int(data))
    user.deposits.append(deposit)
    if not user.account.initial_deposit_date:
        user.account.initial_deposit_date = datetime.utcnow() 
    db.session.add(deposit)
    db.session.commit()

    user.account.balance += deposit.amount
    db.session.commit()
    return jsonify({'message': 'success'}), 201


@api.post('/withdraw/')
@token_auth.login_required
def withdraw_amt():
    user = User.query.get_or_404(g.current_user.id)
    data = request.get_json()['amt'] or {}

    if data > user.account.balance:
        return jsonify({'message': 'insufficient funds'})

    withdrawal = Withdrawal(amount=int(data))
    user.withdrawals.append(withdrawal)
    db.session.add(withdrawal)
    db.session.commit()

    user.account.balance -= withdrawal.amount
    db.session.commit()
    return jsonify({'message': 'success'}), 201



@api.post('/create_user')
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'pin' not in data:
        return bad_request('must include username, email and pin fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username.')
    if User.query.filter_by(username=data['email']).first():
        return bad_request('please use a different email address.')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()

    accout_details = UserBankAccount(
        account_no=generate_account_no(),
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=parse(data['date_of_birth'])
    )
           
    db.session.add_all([accout_details])
    
    user.account = accout_details
    db.session.add(user)
    db.session.commit()
    
    g.current_user = user

    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user_acct')
    return response