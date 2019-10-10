import os

class Config:
    # Mail settings to send emails 
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # Set enviroment variables for username and password
    MAIL_USERNAME = os.environ.get['GMAIL_USERNAME']
    MAIL_PASSWORD = os.environ.get['GMAIL_PASSWORD']
    # Set secret code for application to prevent CSRF token (cross site request forgery token) used by WTForms, should set environment vairable
    SECRET_KEY = os.environ.get['FLASKBLOG_SECRET_KEY']

    # Database setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'