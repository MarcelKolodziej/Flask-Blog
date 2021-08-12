from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    """Before we created db we need to import all data from models"""
    createdatabase(app)

    login_menager = LoginManager()
    login_menager.login_view = "auth.login"
    login_menager.init_app(app)

    @login_menager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def createdatabase(app):
    """Checking if DB exist, if not create one, not to do in production"""
    if not path.exists("website/"+ DB_NAME):
        db.create_all(app=app)
        print("DB created!")