from flask import Blueprint, redirect, url_for, flash, render_template, abort, request
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.posts.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# Display main blog page with alll posts
@posts.route('/blog')
def blog():
    # Set page for SQLAlchemy pagination meythod from request.args
    page = request.args.get('page', 1, type=int) # Use int type to prevent anyone submitting anything other than integer
    # Get posts from db using SQLAlchemy, use paginate method to get only few posts
    # Check sort results from SQLAlchemy **********************************************
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # user order_by to order the posts by newest post at the top
    return render_template('posts/blog.html', posts=posts)


# Display new post form or create new post from POST request
@posts.route('/post/new', methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))

    
    return render_template('posts/create_update_post.html', title='New Post', form=form, legend='Create Post')


# Display page for individual post
@posts.route('/post/<int:post_id>') # Describe wether argument will be int or string with : infront of variable
def post(post_id):
    # Get the post from the db from the post id passed into the url args
    post = Post.query.get_or_404(post_id) # Get the post with this id, if not found return with 404 page not found error, SQLAlchemy methods

    return render_template('posts/post.html', title=post.title, post=post)


# Display page for individual post
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST']) # Describe wether argument will be int or string with : infront of variable
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
        return redirect(url_for('posts.post', post_id=post.id))
    
    elif request.method == 'GET':  # User has requested to update the post, populate the form with current db data to the page
        # Pupulate the form with current post data from db
        form.title.data = post.title
        form.content.data = post.content

    # Render update form template with populated form
    return render_template('posts/create_update_post.html', title='Update Post', 
                            form=form, legend='Update Post')


# Delete post route from the delete post modal form
@posts.route('/post/<int:post_id>/delete', methods=['POST']) # Describe wether argument will be int or string with : infront of variable
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
    return redirect(url_for('main.home'))

