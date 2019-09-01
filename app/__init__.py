from flask import Flask
from app.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import lazy_gettext as _l

goodreads_API_key = "IHK16b7ODRjS2TBA6dH2w"


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login'  # the name we would use in a url_for() call to log in
login.login_message = _l('Please log in to access this page.')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)    # load configurations from the config.py file

    db.init_app(app)
    login.init_app(app)

    return app


from app import routes, models