from book_reviews import app
from app.forms import LoginForm, SignupForm, SearchForm, ReviewForm
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import current_user, logout_user, login_user, login_required
from app.models import User, add_user, Book
from sqlalchemy import func

@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def index():
    user = current_user
    if current_user.is_authenticated:
        # if a user is logged in, he gets the search page
        # where he can search for a book by ISBN, author or title
        form = SearchForm()
        if form.validate_on_submit():   # form was submitted and form validators are ok
            return search_results(form) # get results
        else:
            return render_template('search.html', title='Home', user=user, form=form)
    else:
        # user is not logged in, we require a login (or signup)
        return redirect(url_for('login'))

@login_required
@app.route('/search_results', methods=['GET'])
def search_results(form):
    """get search results according to the submitted search form"""
    search_string = form.data['search']
    search_string = search_string.lower()
    if search_string == '': #empty search
        return redirect(url_for('search'))
    else:
        results=[]
        # if the search_string is ISBN (or partial ISBN)
        results.extend(Book.query.filter(func.lower(Book.isbn).contains(func.lower(search_string))).all())
        # if the search_string is title (or partial title)
        results.extend(Book.query.filter(func.lower(Book.title).contains(func.lower(search_string))).all())
        # if the search_string is author (or partial author)
        results.extend(Book.query.filter(func.lower(Book.author).contains(func.lower(search_string))).all())
        if len(results) == 0:
            flash("No results were found. Try again.")
            return redirect(url_for('index'))
        else:
            if len(results) == 1:
                line = "Is this the book you searched for?"
            else:
                line = "Is one of these the book you searched for?"
            return render_template('results.html', results=results, line=line, title="Search Results")


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
        return render_template('login.html', title='Hello Stranger!', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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


@login_required
@app.route("/books/<string:isbn>", methods=['GET','POST'])
def book_page(isbn):
    """page with the book's details and reviews, with an option to leave a new review"""
    # Make sure book exists
    book = Book.query.get(isbn)
    if book is None:
        flash("No such book. Search again.")
        return redirect(url_for('index'))
    form = ReviewForm()
    success = None
    if form.validate_on_submit():
        score = int(form.score.data)
        text = form.text.data
        user_name = current_user.username
        success = book.add_review(user=user_name, score=score, text=text)
        if not success:
            flash("You can only rate a book once.")
        else:
            flash("Your review was added.")
    # Get all book reviews
    reviews = book.reviews
    return render_template("book.html", book=book, reviews=reviews, form=form, title="Book Page", success=success)


@app.route("/api/<string:isbn>")
def api_access(isbn):
    """If users makes a GET request to my website’s /api/<isbn> route, where <isbn> is an ISBN number,
     we return a JSON response with the book's details and rating"""
    book = Book.query.get(isbn)
    if book is None:
        return jsonify({"error": "ISBN not found"}), 404
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": book.review_count,
        "average_score": book.average_score
    })


@app.route('/about')
def about():
    return render_template('about.html', title='About')

