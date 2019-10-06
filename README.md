# Welcome to flask-scubadivedubai

# Intro

Welcome to flask-scubadivedubai. This app is developed using python and flask framework. It is created for scubadivedivedubai.com.
The bsics of the app it that it is an infomrative website site for Sandy Beach Dive Centre. This is a dive centre based in the UAE.
It offers daily diving trips and PADI scuba diving courses.

This app offers a platform fro users to log in and to post blog posts to the site. The current ittereation will only have one user.
This user will be the admin of the site who will update all posts and load new pages into the site. 

The site has a few static pages such as the landing page, about us page and contact page. All other pages are dynamic pages which are
rendered through the flask framework. The database is based on SQLLite and will be moved over to Prostgress SQL when needed.

Each compenent part is broken down into a Blueprint to alow for more modular and extensibility

### Current functionaility includes:
- User Register
- Log in / out
- Create PADI courses pages, update and delete
- Create Diive Sites, update and delete
- Upload Blog post, update and delete
- Contact form susbmission
- Dive Course request form susbmission
- Fun diving request susbmission

### Components
The component are made into Blueprints to improve molar design and help scaling when needed.
- Main : main functionality including serving statis pages
- Posts : All functionily regarding posts
- Users : all user functionality
- Errors : All error handling

# Technical Overview

### Languages
- Python : Server side controller
- Javascript : Client side functionality and interactivity
- CSS : Originally written in SCSS and compiled to CSS for styling
- HTML : Basic webpage layout

### Frameworks
- [Flask](http://flask.palletsprojects.com/en/1.1.x/) : Server side framework
- [Bootsrap 4](https://getbootstrap.com/docs/4.3/getting-started/introduction/) : Web page styling
- [JQuery](https://api.jquery.com/) : Client side UX

### Flask Extensions
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
- [Its Dangerous](https://pythonhosted.org/itsdangerous/)
- [WTForms](https://wtforms.readthedocs.io/en/stable/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [Jinja 2](https://jinja.palletsprojects.com/en/2.10.x/)


# Architectual Pattern

This appp is developed with the **MVC** arcitechitual design pattern. The details of each componenet is borken down below.

## Model

### SQL Lite
SQL Lite is used as the current database for the application. It is not a large enough amount of data to warrant the use of
a dedicated SQL Server.

### SQL ALchemy
All database queries and submissions are made with SQL Alchemy. 

### Login Manager 
This sets login decorator on all paths that need user login authentication. 

### Model Classes

#### User Model
Model used to store user data. A back reference is created to reference all posts by that user
- UserMixin is imported from flask_login to extend use with login_manager. 
- Methods definied with user class to allow password reset functionality
    - Serializer is imported from itsdangerous to serilaize a token to user email

#### Post Model
Model for posts

## Controller

Because of the apps modular design pattern, the config.py folder contains a create_app function. This function returns
flask as a configured app. This app is the assigned to the main app vairable and main is then called to run in the run.py
within the flaskblog route directory.

### Blueprint
This module is imported from flask. It is used to seperate all compents of the app into their own blueprint.
Each blueprint is import in the main __init.py to be used in the whole app

### Routes
- Some routes are decorated with login requeried to prevent anauthorized user access
- Forms and users are validated and authenticated beofre submission
- SQL Alchemy used to query and return from the Database
- Flash is used to send flash messages to users
- BCrypt used to encryppt password from forms and compared to hashed passwords in DB
- Render Template is used to return html templates after logic has been procceessed

### Users
Users are authenticated using login_manager, current_user method

### Forms
FlaskForms are used to create classes of forms. Thos classes are then passed into temaplates to be rendered as html

- FlaskForm class imported from flask_wtf
    - DataRequired and Fields are imported from WTForms
    - All uploads are done through FlaskForms
    - Form data is validated using validate_ion_sumit method from FlaskForm class

validate_username and email are functions defined within users.forms RegistrationForm to be used
to validate users when queries are made to the database to check if username or email is taken already

validate_email is defined in RequestResetForm to check if email exists to reset the requested password

### Utils

#### User utils : 
- save_picture function is defined to save a new profile picture to the user profile
    - PIL Image module is used to open the image and resize it, it is then saved to the DB
- send_reset_email function is defined to send user a password reset token to their email
    - Message module imported from flask-mail is used to construct and send email to user email

## Views

### Templates
Templates are rendered using jinja 2. All data is returned from routes within the controller. Data passed
onto the templates is the rendered into html using vairables and looks. layout.html is used to extend the layout
of each page to prevent repeating code.

### CSS
All custome styles are writen in SCSS. Ruby SASS is then used to compile SCSS into CSS. Bootstrap is imported with 
CDN to improve site performance. 

### Javascript
Custom JS is imported from static directory. JQuery and Popper are imported via CDN, they are used to query the DOM,
and improve UX.

### Images
Images are stored within the static directory. These images are served onto pages with get_url for module 
Profile pictures are stored within this directory

_________________________________________________________________________________________________________________________

### Created by:
#### Pierre du Toit





