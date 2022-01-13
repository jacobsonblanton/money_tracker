from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Account, Paycheck
import itertools

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("base.html")

@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        pass
    return render_template("home.html", user=current_user)

@views.route('/add-account', methods=['POST', 'GET'])
@login_required
# this method allows user to add bank, bank accounts, and the type of bank accounts, then stores this data in the Account database
def add_account():
    if request.method == 'POST':
        bank = request.form.get('bank-content')
        acct_type = request.form.get('bank-account-type-content')
        acct_number = request.form.get('bank-account-number-content')
        acct_balance = request.form.get('account-balance-content')
        # getting the data from 'add_account.html', then checking if the info is entered correctly
        account = Account.query.filter_by(acct_number=acct_number).first()
        if account:
            flash('This bank account already exists.', category='error')
            return redirect(url_for('views.add_account'))
        elif len(acct_number) != 8 or len(acct_number) != 9:
            flash('Your account number must be 8 or 9 digits, max!', category='error')
            return redirect(url_for('views.add_account'))
        elif len(acct_number) == 0:
            flash('Account number cannot be left blank', category='error')
            return redirect(url_for('views.add_account'))
        elif len(acct_type) == 0:
            flash('Account type cannot be left blank', category='error')
            return redirect(url_for('views.add_account'))
        elif len(bank) == 0:
            flash('Bank cannot be left blank', category='error')
            return redirect(url_for('views.add_account'))
        else:
            new_account = Account(bank=bank, acct_type=acct_type, acct_number=acct_number, acct_balance=acct_balance)
            db.session.add(new_account)
            db.session.commit()
            flash('Your bank account has been added!', category='success')

            return redirect(url_for('views.home'))

    return render_template('add_account.html', user=current_user)

@views.route('/financial-calculator', methods=['POST', 'GET'])
@login_required
# this method allows the user to add finanical calculator to their bank accounts, which implements a paycheck and the 50-30-30 rule
def financial_calculator():
    if request.method == 'POST':
        payday = request.form.get('payday-content')
        amount = request.form.get('paycheck-content')
        # querying the Paycheck database by the amount 
        paycheck = Paycheck.query.all()
        if len(paycheck) == 0:
            flash('Paycheck cannot be empty.', category='error')

    else:
        return render_template('financial_calc.html', user=current_user)

@views.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    if request.method == 'POST':
        pass
    else:
        # displaying the accounts from the database table
        account = Account.query.all()
        # querying the Account database table for only the account balances in the acct_balance columns
        # this will show each column as a list of tuples
        total_acct_balances = Account.query.with_entities(Account.acct_balance).all()
        # converting the list of tuples to a list of integers and adding the components of the list
        tab = sum(list(itertools.chain(*total_acct_balances)))
        # checking the both variables
        print(total_acct_balances)
        print(tab)
        return render_template("account.html", user=current_user, account=account, tab=tab)


@views.route('/expenses', methods=['POST', 'GET'])
@login_required
def expenses():
    if request.method == 'POST':
        pass
    return render_template("expenses.html", user=current_user)


@views.route('/investing', methods=['POST', 'GET'])
@login_required
def investing():
    if request.method == 'POST':
        pass
    return render_template("investing.html", user=current_user)


@views.route('/notifications', methods=['POST', 'GET'])
@login_required
def notifications():
    if request.method == 'POST':
        pass
    return render_template("notifications.html", user=current_user)


@views.route('/help', methods=['POST', 'GET'])
@login_required
def help():
    if request.method == 'POST':
        pass
    return render_template("help.html", user=current_user)