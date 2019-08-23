from flask import Flask
from .config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

from flask_login import LoginManager

goodreads_API_key = "IHK16b7ODRjS2TBA6dH2w"

# app = Flask(__name__)
# app.config.from_object(Config)  # load configurations from the config.py file

db = SQLAlchemy()
# db.init_app(app)

login = LoginManager()
# login.init_app(app)
login.login_view = 'auth.login'
# login.login_message = _l('Please log in to access this page.')
# login.login_view = 'login'      # the name we would use in a url_for() call to log in

# session = Session(app)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)    # load configurations from the config.py file

    db.init_app(app)
    # migrate.init_app(app, db)
    login.init_app(app)


    # if not app.debug and not app.testing:
    #
    #     # ... no changes to logging setup

    return app


from . import routes, models