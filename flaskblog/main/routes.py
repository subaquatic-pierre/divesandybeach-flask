from flask import Blueprint
from flaskblog.models import User, Post
from flask import request, render_template

main = Blueprint('main', __name__)


# Show home page template
@main.route('/')
@main.route('/home')
def home():
    # Set page for SQLAlchemy pagination meythod from request.args
    page = request.args.get('page', 1, type=int) # Use int type to prevent anyone submitting anything other than integer
    # Get posts from db using SQLAlchemy, use paginate method to get only few posts
    # Check sort results from SQLAlchemy **********************************************
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # user order_by to order the posts by newest post at the top
    return render_template('index.html', posts=posts)


# Show about page template
@main.route('/about')
def about():
    return render_template('about.html', title='About')