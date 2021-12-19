from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'udhfshdoho ijsdfoi'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # import auth and views from their files, then registering their routes with '/' as their prefix
    # this allows the web app to use mutliple routes to access different pages. Helps protect the pages that need it 
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # importing all classes and their objects from the models file so they can be access by the web app 
    from .models import User, Account, Paycheck, Expenses
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('money_tracker/' + DB_NAME):
        db.create_all(app=app)
        print('Database created!')

