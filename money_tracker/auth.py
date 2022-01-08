import re
from flask import Flask, render_template, redirect, url_for, request, flash, Blueprint
import flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_manager, login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Account

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email-content')
        first_name = request.form.get('first-name-content')
        last_name = request.form.get('last-name-content')
        password = request.form.get('password-content')
        # filtering the database by email and checking if the email entered matches another in the database.
        # Then adding the user's info, if the user email doesnt exists in database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(email) < 4:
            flash('Email must have at least 4 characters.', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(first_name) < 2:
            flash('First name must have at least 2 characters.', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(last_name) < 2:
            flash('Last name must have at least 2 characters.', category='error')
            return redirect(url_for('auth.sign_up')) 
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            

            return redirect(url_for('views.home')) 


    return render_template("sign_up.html")



@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email-content')
        password = request.form.get('password-content')

        user = User.query.filter_by(email=email).first()
        # logging in user if email and password match (redirecting user to home.html), flashing error message if password is incorrect 
        # and redirecting user to back to login page, prompting re-entry 
        if user:
            if check_password_hash(user.password, password):
                flash('You have successfully logged in!', category='success')
                flash('Welcome to Money Tracker App! You are taking the right step towards a greater future!', category='light')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('The password entered is incorrect.', category='error')
                return redirect(url_for('auth.login'))
        # flashing message if the email is not in the database and redirecting user back to login page, prompting re-entry     
        else:
            flash('Could not find that email. Make sure you tying it correctly.', category='error')
            return redirect(url_for('auth.login'))
    # rendering the login page if the request is not a 'POST' with the current user that is logged in
    return render_template("login.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("views.index"))

