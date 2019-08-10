from app import app, db_session
from app.forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    user = current_user
    if current_user.is_authenticated:
        return render_template('index.html', title='Home', user=user)
    else:
        return redirect(url_for('notlogged'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/notlogged')
def notlogged():
    return render_template('notlogged.html', title='Hello Stranger!')

@app.route('/signup')
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/testdb')
def testdb():
    users = db_session.execute("SELECT * FROM users").fetchall()
    print(users)
    return render_template("test.html", list=users, title="test")