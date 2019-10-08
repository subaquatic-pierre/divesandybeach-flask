from flask import Blueprint
from flaskblog.models import User, Post
from flask import request, render_template

main = Blueprint('main', __name__)


# Show home page template
@main.route('/')
@main.route('/home')
def home():    
    return render_template('main/index.html')


# Show about page template
@main.route('/about')
def about():
    return render_template('main/about.html', title='About')


# Show about contact template
@main.route('/contact')
def contact():
    return render_template('main/contact.html', title='Contact Us')


# Show about privacy policy template
@main.route('/policy')
def policy():
    return render_template('main/policy.html', title='Privacy Policy')


# Show about terms and condtions template
@main.route('/terms')
def terms():
    return render_template('main/terms.html', title='Terms and Conditions')


# Show about site map template
@main.route('/site_map')
def site_map():
    return render_template('main/site_map.html', title='Site Map')