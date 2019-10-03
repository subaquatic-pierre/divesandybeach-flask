import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


# Show home page template
@app.route('/')
@app.route('/home')
def home():
    # Set page for SQLAlchemy pagination meythod from request.args
    page = request.args.get('page', 1, type=int) # Use int type to prevent anyone submitting anything other than integer
    # Get posts from db using SQLAlchemy, use paginate method to get only few posts
    # Check sort results from SQLAlchemy **********************************************
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # user order_by to order the posts by newest post at the top
    return render_template('index.html', posts=posts)


# Show about page template
@app.route('/about')
def about():
    return render_template('about.html', title='About')


# Show the register form page or register a new user if POST method
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


# Show the login page or log the user into their account if POST request
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


# Log the user out of their acount
@app.route('/logout')
def logout():
    # Use logout function from flask_login module downloaded
    logout_user()
    return redirect('home')


# New function to update user profile picture when user uploads new profile picture
def save_picture(form_picture):
    # Change filename to random hex by using secrets module
    random_hex = secrets.token_hex(8)
    # Get file extension with os module using split ext function, returns 2 values: filename and extentsion, use _ to throw away filename variable
    _, f_ext = os.path.splitext(form_picture.filename)
    # Make new filename for picture
    picture_fn = random_hex + f_ext    
    # Create absolue path from os path.join method, root_path gives full path until package directory
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Use Pillow module to resize image before saving it
    output_size = (125, 125) # Create tuple for resize dimernsions
    i = Image.open(form_picture) # Open fill passed into function from form input using Image class from Pillow
    i.thumbnail(output_size) # Set output size to new output size
    # Save file to filesystem
    i.save(picture_path)

    # Return path to picture to be save in db for image_file
    return picture_fn


# Account page route to view the account, any POST requests will update user profile data
@app.route('/account', methods=['GET', 'POST'])
@login_required # Imported from flask login module downloaded
def account():
    # Create instance on UpdateAccountForm imported from forms module
    form = UpdateAccountForm()

    # Check if POST route and form is valid
    if form.validate_on_submit():
        # Check if profile picture exists, use save_picture function created to pass in information and save file so file system, get new picture filename back
        if form.picture.data:

            # CREATE LOGIC TO REMOVE OLD PROFIILE PICTURE WHEN NEW ONE IS UPLOADED
            # ************************************

            picture_file = save_picture(form.picture.data) # Call save_picture function which returns new picture file name
            current_user.image_file = picture_file

        # Change current data to submitted data from form, using flask_login module, current_user class
        current_user.username = form.username.data
        current_user.email = form.email.data
        # Update db
        db.session.commit()
        # Send flash message to user successful update
        flash('Your account has been updated!', 'success')

        # POST,GET redirect pattern, seen on browser reload, Are your sure you want to reload, prevent POST request to account
        return redirect(url_for('account'))

    elif request.method == 'GET':        
        # Populate account update form with current user data if method is GET
        form.username.data = current_user.username
        form.email.data = current_user.email        

    # Get user profile pic from the db
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                            image_file=image_file, form=form)


# Display new post form or create new post from POST request
@app.route('/post/new', methods=['GET', 'POST'])
@login_required # Imported from flask login module downloaded
def new_post():
    # Create new instance of PostForm from forms module
    form = PostForm()

    if form.validate_on_submit():        

        # Add post to the database using SQLAlchemy
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        # Flash message for successful post created and redirect to home page
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    
    return render_template('create_update_post.html', title='New Post', form=form, legend='Create Post')


# Display page for individual post
@app.route('/post/<int:post_id>') # Describe wether argument will be int or string with : infront of variable
def post(post_id):
    # Get the post from the db from the post id passed into the url args
    post = Post.query.get_or_404(post_id) # Get the post with this id, if not found return with 404 page not found error, SQLAlchemy methods

    return render_template('post.html', title=post.title, post=post)


# Display page for individual post
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST']) # Describe wether argument will be int or string with : infront of variable
@login_required
def update_post(post_id):
    # Get the post from the db from the post id passed into the url args
    post = Post.query.get_or_404(post_id) # Get the post with this id, if not found return with 404 page not found error, SQLAlchemy methods

    #Check only user who created post can update it
    if post.author != current_user:
        # Flask function from abort
        abort(403)

    # Create post form instance
    form = PostForm()     

    if form.validate_on_submit():
        # Update post to new data from the form data which was submmitted
        post.title = form.title.data
        post.content = form.content.data

        # Update database with SQLAlchemy
        db.session.commit()

        # Flash message too the user to let them know post has been updated
        flash('Your post has been updated successfully', 'success')


        # Redirect back to the post page
        return redirect(url_for('post', post_id=post.id))
    
    elif request.method == 'GET':  # User has requested to update the post, populate the form with current db data to the page
        # Pupulate the form with current post data from db
        form.title.data = post.title
        form.content.data = post.content

    # Render update form template with populated form
    return render_template('create_update_post.html', title='Update Post', 
                            form=form, legend='Update Post')


# Delete post route from the delete post modal form
@app.route('/post/<int:post_id>/delete', methods=['POST']) # Describe wether argument will be int or string with : infront of variable
@login_required
def delete_post(post_id):
    # Get the post from the db from the post id passed into the url args
    post = Post.query.get_or_404(post_id) # Get the post with this id, if not found return with 404 page not found error, SQLAlchemy methods

    # Check only user who created post can delete it
    if post.author != current_user:
        # Flask function from abort
        abort(403)

    # Delete the post from the db
    db.session.delete(post)
    db.session.commit()

    # Flash message too the user to let them know post has been deleted
    flash('Your post has been deleted', 'success')

    # Redirect back to home
    return redirect(url_for('home'))


# Show posts from particular user
@app.route('/user/<string:username>') # Set variable as string with : before the variable arg in url
def user_posts(username):
    # Set page for SQLAlchemy pagination meythod from request.args
    page = request.args.get('page', 1, type=int) # Use int type to prevent anyone submitting anything other than integer

    # Get user from db using SQLAchemy
    user = User.query.filter_by(username=username).first_or_404() # Username comes from variable in route, similar to get version from post lookup, return 404 if user not found

    # Get posts from db using SQLAlchemy
    # First filter posts by user set from username query
    # Order by latest posts
    # use paginate method to get only few posts
    posts = Post.query.filter_by(author=user). \
    order_by(Post.date_posted.desc()) \
    .paginate(page=page, per_page=5) # user order_by to order the posts by newest post at the top

    return render_template('user_posts.html', posts=posts, user=user)

# Request reset password route
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # Make sure user is logged out to view this
    # Check if user is already logged in with current_user variable from flask login module downloaded
    if current_user.is_authenticated:
        return redirect('home')

    form = RequestResetForm()
    
    return render_template('reset_request.html', title='Reset Password', form=form)


# Get request form url sent to user email with enrytped timed token sent to their email
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # Make sure user is logged out to view this
    # Check if user is already logged in with current_user variable from flask login module downloaded
    if current_user.is_authenticated:
        return redirect('home')

    # Use the method from the User class created in models
    # Method checks if the toekn is valid and returns user_id from db if valid
    user = user.verify_reset_token(token)

    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    
    return render_template('reset_token.html', title='Reset Password', form=form)
    