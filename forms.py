from . import app
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import *

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class LoginForm(FlaskForm):
    """user login form generated using wtforms"""
    username = StringField('Username', validators=[DataRequired()])     # DataRequired() validates it's not empty
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    """user signup form generated using wtforms"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    len = 'Password length must be between %d and %d characters long.' % (4, 16)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=16, message=len)])
    match = 'Passwords must match.'
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message=match)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """check if username already exists in the database"""
        user_exists = User.query.filter_by(username=username.data).first()
        if user_exists is not None:
            raise ValidationError('Username already exists. Please use a different Username.')

    def validate_email(self, email):
        """check if email address already exists in the database"""
        mail_exists = User.query.filter_by(email=email.data).first()
        if mail_exists is not None:
            raise ValidationError('Please use a different Email address.')


class SearchForm(FlaskForm):
    """form for the search page, where the user can search for a book by ISBN, title, or author"""
    search = StringField('Search for a book...', validators=[DataRequired()])
    submit = SubmitField('Search')