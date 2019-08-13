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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.Integer)    # could be null if book only exists in our app and not in goodreads
    year = db.Column(db.Integer)
    review_count = db.Column(db.Integer)
    average_score = db.Column(db.Integer)
    gr_review_count = db.Column(db.Integer)
    gr_average_score = db.Column(db.Integer)

    def __init__(self, title, author, isbn=None, year=None):
        # self.id   # get when inserted to db
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.review_count = 0   # no reviews on our site initially
        self.average_score = 0  # no reviews on our site initially
        self.gr_review_count, self.gr_average_score = get_gr_reviews_data(isbn)


def  get_gr_reviews_data(isbn):
    """access goodreads api, get work_ratings_count , average_rating for the given isbn, return None if unavailable"""
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": goodreads_API_key, "isbns": isbn})
    if res.status_code == 404:
        return None, None
    json = res.json()
    work_ratings_count = json["books"]["work_ratings_count"]
    average_rating = json["books"]["average_rating"]
    return work_ratings_count, average_rating