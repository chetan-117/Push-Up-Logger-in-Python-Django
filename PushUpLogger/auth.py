from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    # return 'This is the signup page'
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # print(email, name, password)

    # first need to check if the user is already logged in or not
    user = User.query.filter_by(email=email).first()

    if user:
        print('User already Exists!')
    # otherwise just add the user by first creating a User instance of it
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # adding this to the database session
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    # return 'This is the login page'
    return render_template('login.html')


# method to get the data from the form with the POST method
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # first verify if that email ID is present in the database
    # also check if the hash of that password matches with the given hash
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('auth.login'))

    # officially login the user using flask method
    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
