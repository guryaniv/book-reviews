from . import app
from .forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from .models import User, add_user
from .config import basedir
import os

@app.route('/')
@app.route('/index')
def index():
    user = current_user
    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=user)
    else:
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:   # user already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():       # form was submitted and form validators are ok
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Incorrect username or password.')
            flash('Incorrect username or password.')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    else:   # form not valid on submit
        return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/notlogged')
def notlogged():
    return render_template('notlogged.html', title='Hello Stranger!')



@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():   # form was submitted and form validators are ok (incl. checks for existing users)
        username = form.username.data
        password = form.password.data
        email = form.email.data
        add_user(username, password, email)     # add user to the database
        return redirect(url_for('index'))
    else:
        print("signup not valid on submit")
        print(form.errors)
        return render_template('signup.html', title='Sign Up', form=form)



@app.route('/testdb')
def testdb():
    users = User.query.all()
    print(users)
    return render_template("test.html", list=users, title="test")