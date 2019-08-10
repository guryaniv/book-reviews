from flask import Flask
from .config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session

from flask_login import LoginManager
import os

goodreads_API_key = "IHK16b7ODRjS2TBA6dH2w"

app = Flask(__name__)
app.config.from_object(Config)  # load configurations from the config.py file
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'      # the name we would use in a url_for() call to log in

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))       # an Engine, which the Session will use for connection
db_session = scoped_session(sessionmaker(bind=engine))  # create a session using a configured "Session" class

from app import routes, models