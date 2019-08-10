from app import db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(): #UserMixin, db.model
    def __init__(self, form_username=None, form_password=None, form_email=None):
        id = None                # get when inserted to db
        username = form_username #check unique?
        password_hash = None     # need to use set_password with form_password
        email = form_email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(user_id):
    # reload the user object from the user ID stored in the session.
    # It should take the unicode ID of a user, and return the corresponding user object
    # It should return None if the ID is not valid.
    # (In that case, the ID will manually be removed from the session and processing will continue.
    return User.query.get(int(user_id))