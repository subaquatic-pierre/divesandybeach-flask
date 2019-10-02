from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Bradley Cooper',
        'title': 'Opening night',
        'content': 'The best night of our lives',
        'date_posted': 'January 1, 2019'
    },
    {
        'author': 'Pierre du Toit',
        'title': 'A New World',
        'content': 'The world is an amazing place, full of amazing people and amazing things to see',
        'date_posted': 'October 19, 2019'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Check if user is already logged in with current_user variable from flask login module downloaded
    if current_user.is_authenticated:
        return redirect('home') 

    # WTForms checks if request is POST
    if form.validate_on_submit():
        # Hash users password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create new instance of user with User class declared in models
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)

        # Add user to the database using SQLAlchemy
        db.session.add(user)
        db.session.commit()

        # Show user successful registration message
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))

    # If method is GET return register form template
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in with current_user variable from flask login module downloaded
    if current_user.is_authenticated:
        return redirect('home')
    
    # Get data from login form
    form = LoginForm()

    if form.validate_on_submit():
        # Check if user is in database with SQLAlchmey function
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exits and check passwaord, use bcrypt to check password received from user in db and data passed in from the form
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # Get user login function from flask_login module downloaded
            login_user(user, remember=form.remember.data)

            # Get next page parameter from argument parameter from request module from flask
            next_page = request.args.get('next')
            
            # Use turnery operator to check if next_page exists in args from previous request and return to page
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # Checked username and password failed which means email is correct but password is wrong
            flash('Login unsuccessful. Please check email and password', 'danger')

    # Render login form if request is GET 
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    # Use logout function from flask_login module downloaded
    logout_user()
    return redirect('home')


@app.route('/account')
@login_required # Imported from flask login module downloaded
def account():
    return render_template('account.html', title='Account')