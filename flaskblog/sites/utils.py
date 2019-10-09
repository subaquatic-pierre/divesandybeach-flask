import os, string
from flask import url_for, current_app
from PIL import Image

# New function to update user profile picture when user uploads new profile picture
def save_map(site_name, form_picture):
    # Get file extension with os module using split ext function, returns 2 values: filename and extentsion, use _ to throw away filename variable
    _, f_ext = os.path.splitext(form_picture.filename)
    # Make new filename for picture
    picture_fn = site_name + '_map' + f_ext    
    # Create absolue path from os path.join method, root_path gives full path until package directory
    picture_path = os.path.join(current_app.root_path, 'static/uploads/maps', picture_fn)

    # Use Pillow module to resize image before saving it
    # output_size = (125, 125) # Create tuple for resize dimernsions
    i = Image.open(form_picture) # Open fill passed into function from form input using Image class from Pillow
    # i.thumbnail(output_size) # Set output size to new output size
    # Save file to filesystem
    i.save(picture_path)

    # Return path to picture to be save in db for image_file
    return picture_fn


# Build url for dive sites

def build_slug(sitename):
    i = sitename.lower().split()
    slug = '-'.join(i)
    return slug