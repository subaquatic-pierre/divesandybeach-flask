

class Config:
    # Mail settings to send emails 
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # Set enviroment variables for username and password
    MAIL_USERNAME = 'subaquatic.pierre@gmail.com'
    MAIL_PASSWORD = 'M0ther!and'
    # Set secret code for application to prevent CSRF token (cross site request forgery token) used by WTForms, should set environment vairable
    SECRET_KEY = 'd30cdb1c8d3e69f91295902e044d5333'

    # Database setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'