from . import app
from .forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from .models import User, add_user

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
    if current_user.is_authenticated:   # user already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():       # form was submitted and form validators are ok
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

def validate_signup(form_username=None, form_password=None, form_email=None):
    # Check if username already exists in database
    user_exists = User.query.filter_by(username=form_username).first()
    if user_exists:    # not None
        flash('Username already exists. Select a different one.')
        return False
    else:
        if form_email:
            mail_exists = User.query.filter_by(email=form_email).first()
            if mail_exists:  # not None
                flash('There is Already a user with that email address.')
                return False
        # add more checks ?
        return True

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():   # form was submitted and form validators are ok
        username = form.username.data
        password = form.password.data
        email = form.email.data
        valid = validate_signup(username, password, email)
        if valid:
            # create user, add to db
            add_user(username, password, email)
            return redirect(url_for('index'))
        else:
            # wrong something - handled in validate_signup
            return redirect(url_for('signup'))
    return render_template('signup.html', title='Sign In', form=form)

# @app.route('/post_signup', methods = ['POST'])
# def post_signup():
#     nam_s = request.form['nama_signup']
#     pwd_s = request.form['pass_signup']
#     data.append({'nama': nam_s, 'pass': pwd_s})
#     y = json.dumps(data)
#
#     json_data = open('bikin_database.json', 'w')
#     json_data.write(y)
#     return '<h1>Selamat ' + nam_s + ', Anda berhasil Register</h1>'

@app.route('/testdb')
def testdb():
    users = User.query.all()
    print(users)
    return render_template("test.html", list=users, title="test")