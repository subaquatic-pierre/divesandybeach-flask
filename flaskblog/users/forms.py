from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

# Use WTForms to make a form which can be rendered to html in the template form used on the register route
class RegistrationForm(FlaskForm):
    # StingField class used from wtforms module downlaoded
    # Create fields with WTForm fields
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)]) # Use wtforms.validator module to validate inputs from the user
    email = StringField('Email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password', 
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Username validator function
    def validate_username(self, username):
        # Check if username is in the DB with SQLAlchemy query function
        user = User.query.filter_by(username=username.data).first()
        # If user is found in DB then user will be True
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # Email validation check
    def validate_email(self, email):
    # Check if email is in the DB with SQLAlchemy query function
        user = User.query.filter_by(email=email.data).first()
        # If email is found in DB then user will be True
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# Use WTForms to make a form which can be rendered to html in the template form used on the login route
class LoginForm(FlaskForm):
    # StingField class used from wtforms module downlaoded
    # Create fields with WTForm fields
    email = StringField('Email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Use WTForms to make a form which can be rendered to html in the template form used on the account route to update profile info
class UpdateAccountForm(FlaskForm):
    # StingField class used from wtforms module downlaoded
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # Username validator function
    def validate_username(self, username):
        # Check that current logged in user matches account update information, get username.data from LoginForm class
        if username.data != current_user.username:
            # Check if username is in the DB with SQLAlchemy query function
            user = User.query.filter_by(username=username.data).first()
            # If user is found in DB then user will be True
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # Email validation check
    def validate_email(self, email):
        # Check that current logged in user matches account update information, get email.data from login form class
        if email.data != current_user.email:
            # Check if email is in the DB with SQLAlchemy query function
            user = User.query.filter_by(email=email.data).first()
            # If email is found in DB then user will be True
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# Create user reset class to be used as form to request reset user details
class RequestResetForm(FlaskForm):
    # Create fields with WTForm fields
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # Email validation check, if no user exits in the database let the user know they have to create an account first
    def validate_email(self, email):
    # Check if email is in the DB with SQLAlchemy query function
        user = User.query.filter_by(email=email.data).first()
        # If email is found in DB then user will be True
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')


# Reset password class for reset password form
class ResetPasswordForm(FlaskForm):
    # Create fields with WTForm fields
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password', 
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')