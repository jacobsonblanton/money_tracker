from os import error
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Account, Paycheck
import itertools
from tabulate import tabulate

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("base.html")

@views.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        pass
    else:
        # querying the Paycheck database 
        paycheck = Paycheck.query.all() 
        # querying the Paycheck database for just the payday and storing that info in a varibale 
        # changing the list of tuples of a string to a list of a string and then converting that to a string
        payday_list = list(itertools.chain(*(Paycheck.query.with_entities(Paycheck.payday).all())))
        payday = payday_list[0]
        print(payday)
        # getting the date for today and defining a table to append the list of paydays to 
        today = date.today() # current day 
        table = []
        
        paycheck_amount_after_tax = round((sum(list(itertools.chain(*(Paycheck.query.with_entities(Paycheck.amount).all()))))*52)/1.12, 2)
        print(paycheck_amount_after_tax)
        for d in every_payday(2022):
            table.append(d.strftime("%Y-%m-%d"))
        
        return render_template("home.html", user=current_user, paycheck=paycheck, table=table, payday=payday, paycheck_amount_after_tax=paycheck_amount_after_tax)

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
        elif len(acct_number) == 0:
            flash('Account number cannot be left blank', category='error')
            return redirect(url_for('views.add_account'))
        elif len(acct_number) != 8 :
            flash('Account number must be 8 digits.', category='error')
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

def every_payday(year):
    # this method will get every "weekly" payday for the given year 
    d = date(year, 1, 7) # getting the first friday
    d += timedelta(days = 4 - d.weekday()) # adding every friday to d
    while d.year == year: # looping through the entire year while the d.year is equal to the specified year. 
        yield d
        d += timedelta(days = 7) # since payday is weekly or every 7 days
    



@views.route('/financial-calculator', methods=['POST', 'GET'])
@login_required
# this method allows the user to add finanical calculator to their bank accounts, which implements a paycheck and the 50-30-20 rule
def financial_calculator():
    if request.method == 'POST':
        payday = request.form.get('payday-content')
        amount = request.form.get('paycheck-content') 
        
        if len(amount) == 0:
            flash('Paycheck cannot be empty.', category='error')
            return redirect(url_for('views.financial_calculator'))
        elif len(payday) == 0:
            flash('Payday cannot be empty.', category='error')
            return redirect(url_for('views.financial_calculator'))
        elif payday != 'weekly':
            flash('Payday must be weekly for this financial calculator.', category='error')
            return redirect(url_for('views.financial_calculator'))
        else:
            new_paycheck = Paycheck(amount=amount, payday=payday)
            db.session.add(new_paycheck)
            db.session.commit()
            flash('Your paycheck info has been added', category='success')

            return redirect(url_for('views.home'))

    else:
        # querying the Paycheck database 
        paycheck = Paycheck.query.all() 

        # getting the date for today and defining a table to append the list of paydays to 
        today = date.today() # current day 
        table = []

        for d in every_payday(2022):
            table.append(d.strftime("%Y-%m-%d"))
        
        print(tabulate(table, tablefmt='fancy_grid', showindex=True))


        return render_template('financial_calc.html', user=current_user, paycheck=paycheck, table=table)

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