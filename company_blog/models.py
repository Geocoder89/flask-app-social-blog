# models.py
# this imports the db class we intend to inherit
from company_blog import db, login_manager

# the werkzeug security packages provides options to generate a hashed password and also checked existing hashed
# passwords

from werkzeug.security import generate_password_hash, check_password_hash

# this helps generate user login checked functions e.g is_authenticated etc
from flask_login import UserMixin

# import the inbuilt datetime module of python to set up the datetime
from datetime import datetime


# the user authentication pattern we used the user loader decorator of the login manager and call the load_user
# function passing in the user id and return a query result of the user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# basic set up of the user model which inherits from the db model class and the usermixin class which we use to
# construct models and also sets up custom user login functions or functionality respectively
class User(db.Model, UserMixin):
    # setting the name to 'users'
    __tablename__ = 'users'
    # setting the user id to an integer and making it to a unique primary key which auto-increments
    id = db.Column(db.Integer, primary_key=True)
    # setting the profile image to a string of 64 characters using the nullable to false to force the user to insert
    # an image and if they have none they are given a static preloaded image
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    # emails and username are strings of 64 characters which are unique and indexed
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # passwords are 128 character strings
    password_hash = db.Column(db.String(128))
    # relationships are set to blog posts by mentioning the particular model they have relationships with,
    # they are given a reference called author which we use for reference to this relationship to template and they
    # are lazily loaded

    posts = db.relationship('BlogPost', backref='author', lazy=True)

    # we instantiate the User model class
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        # here the password_hashed is set to a werkzeug generated representation of the password
        self.password_hash = generate_password_hash(password)

    # check password function checks the hashed password and also that we inputted
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # we produce a printed version or representative for debugging purposes
    def __repr__(self):
        return f"Username {self.username}"


# setting up the blog post model
class BlogPost(db.Model):
    # we set up and reference the relationship between the blog post and a User
    users = db.relationship(User)

    # we set up a column for the id of the blog post which is a primary key
    id = db.Column(db.Integer, primary_key=True)
    # we set up the user_id which is an integer which is an integer which is a foreign key referencing the id of the
    # users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # we set it to a date time column with the default set to the present date and time
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # we set the title to a string of 140 characters which must be filled
    title = db.Column(db.String(140), nullable=False)

    # text set to a db text and must be inputted
    text = db.Column(db.Text, nullable=False)

    #   we then set the title text and userid as a representation attributes of the blog post class
    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    # we then set up a representation of this class which can be used for debugging or testing purposes
    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"