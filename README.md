<p align="center"><img src="https://github.com/guryaniv/book-reviews/blob/master/app/static/img/logo.png" width="170" title="Book Reviews"></p>

Project 1 for Harvard's CS50's Web Programming with Python and JavaScript Course, with some Extras.<br>
See- [Project Instructions](https://docs.cs50.net/web/2019/x/projects/1/project1.html).

Book-Reviews web app, created using flask, postgreSQL, Goodreads API.
<h3>Implemented Components:</h3>
<ul>
  <li><strong>Registration</strong>: Users are able to register to the website, providing a username, password and Email address.</li>
  <li><strong>Login</strong>: Users, once registered, are able to log in to the website with their username and password. Also implemented a "remember me" option, sessions.</li>
  <li><strong>Create and Import</strong>: Using the <a href="https://github.com/guryaniv/book-reviews/blob/master/create.py">create.py</a> file, the database tabels and relationships are automatically created and books are imported to the database from a given  <a href="https://github.com/guryaniv/book-reviews/blob/master/books.csv">books.csv</a> file.</li>
  <li><strong>Search</strong>: Once a user has logged in, they can search for a bookby ISBN number, title, or author. After performing the search, the website displays a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, the search page finds matches for those as well.</li>
  <li><strong>Book Page</strong>: When users click on a book from the results of the search page, they are taken to a book page, with details about the book and any reviews that users have left for the book on your website.</li>
  <li><strong>Review Submission</strong>: On the book page, users are able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users are not able to submit multiple reviews for the same book.</li>
  <li><strong>Goodreads Review Data</strong>: On the book page, we also display (if available) the average rating and number of ratings the work has received from Goodreads.</li>
  <li><Strong>API Access</strong>: If users make a GET request to the website’s /api/<isbn> route, where <isbn> is an ISBN number of a book, the website returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.</li>
</ul>

<h3>prerequisites:</h3>

See ```requirements.txt```.



