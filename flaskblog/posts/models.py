from datetime import datetime
from flaskblog import db

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