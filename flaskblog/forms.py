from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
