import os
import csv

from flask import Flask
from app.models import Book
from app import db

#### RUN THIS FILE TO CREATE THE DATABASE TABLES AND IMPORT BOOKS FROM CSV ####

os.environ[
        "DATABASE_URL"] = "postgres://buuzvdtusoaaqi:339ae0c9ab3a80f649353d13207687b6cbc5be855ccdb3ef55f3d66a74e8" \
                          "99d6@ec2-174-129-231-100.compute-1.amazonaws.com:5432/d9fmk2vkh5brl6"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy()
db.init_app(app)

def import_books(csv_path):
    """import books from a csv file to the database.
    The file should contain isbn,title,author,year"""
    f = open(csv_path)
    reader = csv.reader(f)
    header_line = True
    for isbn,title,author,year in reader:
        if header_line:
            header_line = False
            continue
        print(f"Adding a book titled \"{title}\" by {author}.")
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()

def main():
    """create all database tables according to models"""
    print("Creating Tables...")
    db.create_all()
    print("Tables Created!")
    print("Importing Books...")
    import_books("books.csv")
    print("Books Imported!")

if __name__ == "__main__":
    with app.app_context():
        main()