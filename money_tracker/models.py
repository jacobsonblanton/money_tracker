from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from sqlalchemy.sql import func

# creating the classes and objects for the app. 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    paychecks = db.relationship('Paycheck', backref='user')
    accounts = db.relationship('Account', backref='user')
    expsenses = db.relationship('Expenses', backref='user')
    net_balance = db.relationship('Net_Balance', backref='user')

# create a class for account, paycheck, expenses, total balance
class Paycheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    user_paycheck = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(200), nullable=False)
    acct_type = db.Column(db.String(200), nullable=False)
    acct_number = db.Column(db.String(200), nullable=False)
    acct_balance = db.Column(db.Integer, nullable=True)
    user_acct = db.Column(db.Integer, db.ForeignKey('user.id'))

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_type = db.Column(db.String(200), nullable=False)
    user_expense = db.Column(db.Integer, db.ForeignKey('user.id'))

class Net_Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)
    user_balance = db.Column(db.Integer, db.ForeignKey('user.id'))