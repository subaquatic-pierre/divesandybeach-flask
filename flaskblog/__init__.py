from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Application variable assigned to Flask object
app = Flask(__name__)

# Set secret code for application to prevent CSRF token (cross site request forgery token) used by WTForms, should set environment vairable
app.config['SECRET_KEY'] = 'd30cdb1c8d3e69f91295902e044d5333'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Hash password class
bcrypt = Bcrypt(app)

# Set login manager
login_manager = LoginManager(app)

# Set login route
login_manager.login_view = 'login'

# Set flash message from login failer message
login_manager.login_message_category = 'info'

# Import routes after everything to prevent cricle importing
from flaskblog import routes