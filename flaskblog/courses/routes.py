from flask import Blueprint, redirect, url_for, flash, render_template, abort, request
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.courses.models import Course
from flaskblog.courses.forms import CourseForm
from flaskblog.courses.utils import save_image, build_slug, build_level_slug

courses = Blueprint('courses', __name__)

# Show all courses
@courses.route('/padi-courses')
def all_courses():
    courses = Course.query.all()
    return render_template('courses/all_courses.html', courses=courses, title='PADI Courses')


# Show new course form or create new course if POST
@courses.route('/padi-course/new', methods=['GET', 'POST'])
def new_course():
    form = CourseForm()

    if form.validate_on_submit():
           

        slug = build_slug(form.course_name.data)
        course = Course(course_name=form.course_name.data, level=form.level.data, 
                    age=form.age.data, duration=form.duration.data, 
                    price_e_learning=form.price_e_learning.data, price_book_learning=form.price_book_learning.data, 
                    pool_dives=form.pool_dives.data, slug=slug, ocean_dives=form.ocean_dives.data,
                    min_dives=form.min_dives.data, qualified_to=form.qualified_to.data, 
                    basic_info=form.basic_info.data, schedule=form.schedule.data )

        # Check if new map was uploaded, update new image, save the map and return url to file    
        if form.image.data:
            image_fn = save_image(form.course_name.data, form.image.data)
            course.image = image_fn

        db.session.add(course)
        db.session.commit()

        return redirect(url_for('courses.all_courses'))


    return render_template('courses/create_update_course.html', form=form, title='New Course', legend='Create a PADI Course')


# Display individual dive sites
@courses.route('/padi-course/<string:slug>')
def padi_course(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    return render_template('courses/padi_course.html', course=course, title=course.course_name)

# Update dive site or display update form
@courses.route('/padi-course/<string:slug>/update', methods=['GET', 'POST'])
def update_course(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()

    form = CourseForm()
    
    if form.validate_on_submit():
        # Build a new slug for course
        slug = build_slug(form.course_name.data)

        # Check if new map was uploaded, update new image
        if form.image.data:
            image_fn = save_image(form.course_name.data, form.image.data)
            course.image = image_fn
        
        
        course.course_name = form.course_name.data
        course.level = form.level.data
        course.age = form.age.data
        course.duration = form.duration.data
        course.price_e_learning = form.price_e_learning.data
        course.price_book_learning = form.price_book_learning.data
        course.pool_dives = form.pool_dives.data  
        course.ocean_dives = form.ocean_dives.data  
        course.min_dives = form.min_dives.data  
        course.qualified_to = form.qualified_to.data  
        course.basic_info = form.basic_info.data  
        course.schedule = form.schedule.data  
        course.slug = slug

        db.session.commit()

        flash('The dive course has been updated', 'success')


        return redirect(url_for('courses.padi_course', slug=slug))

    elif request.method == 'GET':

        form.course_name.data = course.course_name
        form.level.data = course.level
        form.age.data = course.age
        form.duration.data = course.duration
        form.price_e_learning.data = course.price_e_learning
        form.price_book_learning.data = course.price_book_learning
        form.pool_dives.data = course.pool_dives  
        form.ocean_dives.data = course.ocean_dives
        form.min_dives.data = course.min_dives
        form.qualified_to.data = course.qualified_to
        form.basic_info.data = course.basic_info
        form.schedule.data = course.schedule
        form.image.data = course.image

    return render_template('courses/create_update_course.html', title='Update Course', 
                            form=form, legend='Update Course')


# Delete dive site from the delete post modal form
@courses.route('/padi-course/<string:slug>/delete', methods=['POST']) # Describe wether argument will be int or string with : infront of variable
def delete_course(slug):
    # Get the post from the db from the post id passed into the url args
    course = Course.query.filter_by(slug=slug).first_or_404() # Get the post with this id, if not found return with 404 page not found error, SQLAlchemy methods

    # Delete the post from the db
    db.session.delete(course)
    db.session.commit()

    # Flash message too the user to let them know post has been deleted
    flash('Your course has been deleted', 'success')

    # Redirect back to home
    return redirect(url_for('courses.all_courses'))

