import os, secrets
from flask import url_for, current_app
from PIL import Image
from flask_mail import Message
from flaskblog import mail


# New function to update user profile picture when user uploads new profile picture
def save_profile_picture(form_picture):
    # Change filename to random hex by using secrets module
    random_hex = secrets.token_hex(8)
    # Get file extension with os module using split ext function, returns 2 values: filename and extentsion, use _ to throw away filename variable
    _, f_ext = os.path.splitext(form_picture.filename)
    # Make new filename for picture
    picture_fn = random_hex + f_ext    
    # Create absolue path from os path.join method, root_path gives full path until package directory
    picture_path = os.path.join(current_app.root_path, 'static/uploads/profile_pics', picture_fn)

    # Use Pillow module to resize image before saving it
    output_size = (125, 125) # Create tuple for resize dimernsions
    i = Image.open(form_picture) # Open fill passed into function from form input using Image class from Pillow
    i.thumbnail(output_size) # Set output size to new output size
    # Save file to filesystem
    i.save(picture_path)

    # Return path to picture to be save in db for image_file
    return picture_fn


# Create function to call to send user an email
def send_reset_email(user):
    # Create token to send to the user using the get_reset_token method from User model in models 
    token = user.get_reset_token()
    
    # Use Message module from flask-mail extension
    msg = Message('Password Reset Request', 
                    sender='noreply@demo.com', 
                    recipients=[user.email])

    # Create password message
    msg.body = f''' To reset your password visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not send this request, simply ignore this email and no change will be made    
'''
    mail.send(msg)