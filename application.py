from flask import Flask, render_template, url_for, flash, redirect
from forms import  RegistrationForm, LoginForm

# Application variable assigned to Flask object
app = Flask(__name__)

# Set secret code for appliaction to prevent CSRF token (cross site request forgery token) used by WTForms, should set environment vairable
app.config['SECRET_KEY'] = 'd30cdb1c8d3e69f91295902e044d5333'

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

    if form.validate_on_submit():
        flash(f'Acount created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessfull. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)