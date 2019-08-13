from . import app
from .forms import LoginForm, SignupForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from .models import *
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

@app.route('/search')
def search_page():
    """search for a book. Users should be able to type in the ISBN number of a book, the title of a book,
    or the author of a book. After performing the search, your website should display a list of possible
     matching results, or some sort of message if there were no matches. If the user typed in only part of a title,
      ISBN, or author name, your search page should find matches for those as well!"""
    # TODO

@app.route("/books/<int:book_id>")
def book_page():
    """When users click on a book from the results of the search page, they should be taken to a book page,
     with details about the book: its title, author, publication year, ISBN number, and any reviews that users
      have left for the book on your website."""
    # TODO
    """Review Submission: On the book page, users should be able to submit a review: consisting of a rating on
     a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book.
      Users should not be able to submit multiple reviews for the same book."""

@app.route("/api/<int:isbn>")
def api_access():
    """If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should
     return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average
      score. The resulting JSON should follow the format:"""
    # TODO
    {
        "title": "Memory",
        "author": "Doug Lloyd",
        "year": 2015,
        "isbn": "1632168146",
        "review_count": 28,
        "average_score": 5.0
    }

@app.route('/testu')
def testusers():
    users = User.query.all()
    print(users)
    return render_template("test.html", list=users, title="test")

@app.route('/testb')
def testbooks():
    books = Book.query.all()
    print(books)
    return render_template("test.html", list=books, title="test")

@app.route('/testapi')
def testapi():
    json = get_gr_reviews_data("0380795272")
    book = json["books"]
    return render_template("test.html", list=book, title="test")

