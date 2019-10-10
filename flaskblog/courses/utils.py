import os, string
from flask import url_for, current_app
from PIL import Image

# New function to update user profile picture when user uploads new profile picture
def save_image(course_name, course_image):
    # Get file extension with os module using split ext function, returns 2 values: filename and extentsion, use _ to throw away filename variable
    _, f_ext = os.path.splitext(course_image.filename)
    # Make new filename for picture
    picture_fn = course_name + '_image' + f_ext    
    # Create absolue path from os path.join method, root_path gives full path until package directory
    picture_path = os.path.join(current_app.root_path, 'static/uploads/courses', picture_fn)

    # Use Pillow module to resize image before saving it
    # output_size = (125, 125) # Create tuple for resize dimernsions
    i = Image.open(course_image) # Open fill passed into function from form input using Image class from Pillow
    # i.thumbnail(output_size) # Set output size to new output size
    # Save file to filesystem
    i.save(picture_path)

    # Return path to picture to be save in db for image_file
    return picture_fn


# Build url for dive sites

def build_slug(course_name):
    i = course_name.lower().split()
    slug = '-'.join(i)
    return slug

def build_level_slug(course_name):
    i = course_name.lower().split()
    level_slug = '-'.join(i)
    return level_slug