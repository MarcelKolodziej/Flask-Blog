from flask import Blueprint, render_template, redirect, url_for,request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required
auth = Blueprint("auth", __name__)

@auth.route("/login",  methods=['GET', 'POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    return render_template("login.html")

@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exist = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exist:
            """Flash a msg on the screen"""
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use', category='error')
        elif password1 != password2:
            flash('Password don\t match', category='error')
        elif len(username) < 3:
            flash('Username too short!', category='error')
        elif len(password1) < 6:
            flash('Password too short!')
        elif len(email) < 5:
            flash('Email too short!', category='error')
        else:
            new_user = User(email='email', username='username', password = 'password1')
            db.session.add(new_user)
            db.session.commit()
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html")

@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))
