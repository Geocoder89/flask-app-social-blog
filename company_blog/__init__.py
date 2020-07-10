############################################
# IMPORTS
#############################################
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Bootstrapping the app
######################################
app = Flask(__name__)

############################

#####################################
# forms secret-key
####################################
app.config['SECRET_KEY'] = 'positivity10'

#####################################
# DATABASE CONFIGURATION
##########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)


#########################################
# LOGIN CONFIGURATION
########################################

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'users.login'

#######################################
# blueprint set up
#######################################
from company_blog.core.views import core
from company_blog.error_pages.handlers import error_pages
from company_blog.users.views import users
from company_blog.blog_posts.views import blog_posts


#######################################

########################################
# BLUE PRINTS REGISTRATION
########################################
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
