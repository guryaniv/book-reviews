from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login, db
from flask_login import login_user


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

# class
