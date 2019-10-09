import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


# Initialize SQLAlchemy for db functions
db = SQLAlchemy()

# Initialise mail extension with settings
mail = Mail()

# Hash password class
bcrypt = Bcrypt()

# Set login manager
login_manager = LoginManager()

# Set login route
login_manager.login_view = 'users.login'

# Set flash message from login failer message
login_manager.login_message_category = 'info'


# Define a create app function to make the application more modular, configure all extensions before creating app, then use the __init function within the craete_app
# function to config extensions to use the app
def create_app():
    # Application variable assigned to Flask object
    app = Flask(__name__)
    # Configure app from Config class defined in config.py module
    app.config.from_object(Config)

    # Initialize extensions with init_app to configure to use app
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    # Blueprints used to make modules more modular wtihin app
    # The blueprints are llocated withhhin their own directory within the flaskblog main app
    # each blueprint is the imported into each other module which needs it
    # be sure to import the Blueprint module from flask extension
    # inside each sub module an __init__.py file needs to be created to be seen as a module
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    from flaskblog.sites.routes import sites

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(sites)

    return app

