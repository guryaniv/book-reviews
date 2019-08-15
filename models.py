from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login, db
from flask_login import login_user
import requests
from . import goodreads_API_key


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)

    def __init__(self, form_username, form_password, form_email=None):
        # self.id   # get when inserted to db
        self.username = form_username
        self.password_hash = generate_password_hash(form_password)
        self.email = form_email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User #{self.id} - {self.username}>'


def add_user(username, password, email=None):
    """Creates a new User object and adds it to the database"""
    new_user = User(username, password, email)
    db.session.add(new_user)
    db.session.commit() # insert the new user object to the database
    login_user(new_user)


@login.user_loader
def load_user(user_id):
    # reload the user object from the user ID stored in the session.
    # It should take the unicode ID of a user, and return the corresponding user object
    # It should return None if the ID is not valid.
    # (In that case, the ID will manually be removed from the session and processing will continue.
    return User.query.get(int(user_id))

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)   # ISBN can contain X, not only numbers
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    review_count = db.Column(db.Integer)
    average_score = db.Column(db.Float)
    gr_review_count = db.Column(db.Integer)
    gr_average_score = db.Column(db.Float)
    reviews = db.relationship("Review", backref="book", lazy=True)

    def __init__(self, isbn, title, author, year=None):
        # self.id   # get when inserted to db
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.review_count = 0   # no reviews on our site initially
        self.sum_of_scores = 0
        self.average_score = 0
        self.gr_review_count, self.gr_average_score = get_gr_reviews_data(isbn)

    def add_review(self, user_id, score, text):
        """Add a review for this book object"""
        new_review = Review(book_id=self.id, user_id=user_id, score=score, text=text)
        db.session.add(new_review)
        db.session.commit()
        self.gr_review_count += 1  # add review to count
        self.sum_of_scores += score
        self.average_score = (self.sum_of_scores / self.review_count)  # calculate new average


def add_book(isbn, title, author, year=None):
    """Creates a new Book object and adds it to the database"""
    new_book = Book(isbn=isbn, title=title, author=author, year=year)
    db.session.add(new_book)
    db.session.commit() # insert the new book object to the database


class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)         # isbn of the reviewed book
    user_id = db.Column(db.Integer, nullable=False)         # id of the user (reviewer)
    score = db.Column(db.Integer, nullable=False)           # the user rates the book, rating on a scale of 1 to 5
    text = db.Column(db.String)                             # the text review (optional)

    def __init__(self, book_isbn, user_id, score, text):
        # self.review_id   # get when inserted to db
        self.book_isbn = book_isbn
        self.user_id = user_id
        self.score = score
        self.text = text


def  get_gr_reviews_data(isbn):
    """access goodreads api, get work_ratings_count , average_rating for the given isbn, return None if unavailable"""
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": goodreads_API_key, "isbns": isbn})
    if res.status_code == 404:
        return None, None
    json = res.json()
    print("JSON FILE:" + str(json))
    print("COUNT:" + str(json["books"][0]["work_ratings_count"]))
    print("SCORE:" + str(json["books"][0]["average_rating"]))
    work_ratings_count = int(json["books"][0]["work_ratings_count"])
    average_rating = float(json["books"][0]["average_rating"])
    return work_ratings_count, average_rating