import os

from flask import Flask
from .models import *

os.environ[
        "DATABASE_URL"] = "postgres://buuzvdtusoaaqi:339ae0c9ab3a80f649353d13207687b6cbc5be855ccdb3ef55f3d66a74e8" \
                          "99d6@ec2-174-129-231-100.compute-1.amazonaws.com:5432/d9fmk2vkh5brl6"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def import_books(csv_path):
    """import books from a csv file to the database
    The file should contain isbn,title,author,year"""
    # TODO

def main():
    """create all database tables according to models"""
    db.create_all()
    # import_books("books.csv") TODO

if __name__ == "__main__":
    with app.app_context():
        main()