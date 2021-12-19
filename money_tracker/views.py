from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

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

@views.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    if request.method == 'POST':
        pass
    return render_template("account.html", user=current_user)

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