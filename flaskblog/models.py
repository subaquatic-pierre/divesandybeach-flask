from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

# Set login manager decorator
@login_manager.user_loader
def load_user(user_id):
    # Get user id from database query
    return User.query.get(int(user_id))

# Create user model which is used to populate the db
class User(db.Model, UserMixin): # UserMixin is a class imported from flask_login that creates attributes to be used with login_manager
    # Use SQLAlchemy to create User table within site.db
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Create back reference for user to be linked to posts
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# Create Post model to be used when a user creates new posts
class Post(db.Model):
    # Use SQLAlchemy to create Post table within site.db
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # User id column to back reference authors of the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"