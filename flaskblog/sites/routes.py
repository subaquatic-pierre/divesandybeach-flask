from flask import Blueprint, redirect, url_for, flash, render_template, abort, request
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.sites.models import Site
from flaskblog.sites.forms import SiteForm
from flaskblog.sites.utils import save_map, build_slug

sites = Blueprint('sites', __name__)

# Show all dive sites
@sites.route('/fujairah-dive-sites')
def all_sites():
    sites = Site.query.all()
    return render_template('sites/all_sites.html', sites=sites, title='Fujairah Dive Sites')


# Show new dive site form or create new dive site if POST
@sites.route('/fujairah-dive-sites/new', methods=['GET', 'POST'])
def new_site():
    form = SiteForm()

    if form.validate_on_submit():
           

        slug = build_slug(form.sitename.data)
        site = Site(sitename=form.sitename.data, level=form.level.data, 
                    dive_time=form.dive_time.data, depth=form.depth.data, 
                    distance=form.distance.data, marine_life=form.marine_life.data, 
                    description=form.description.data, slug=slug)

        # Check if new map was uploaded, update new image, save the map and return url to file    
        if form.map_image.data:
            map_fn = save_map(form.sitename.data, form.map_image.data)
            site.map_image = map_fn

        db.session.add(site)
        db.session.commit()

        return redirect(url_for('sites.all_sites'))


    return render_template('sites/create_update_site.html', form=form, title='New Site', legend='Create a Dive Site')


# Display individual dive sites
@sites.route('/fujairah-dive-sites/<string:slug>')
def dive_site(slug):
    site = Site.query.filter_by(slug=slug).first_or_404()
    return render_template('sites/dive_site.html', site=site, title=site.sitename)

# Update dive site or display update form
@sites.route('/fujairah-dive-sites/<string:slug>/update', methods=['GET', 'POST'])
def update_site(slug):
    site = Site.query.filter_by(slug=slug).first_or_404()

    form = SiteForm()
    
    if form.validate_on_submit():
        # Build a new slug for site
        slug = build_slug(form.sitename.data)

        # Check if new map was uploaded, update new image
        if form.map_image.data:
            map_fn = save_map(form.sitename.data, form.map_image.data)
            site.map_image = map_fn
        
        
        site.sitename = form.sitename.data
        site.level = form.level.data
        site.dive_time = form.dive_time.data
        site.depth = form.depth.data
        site.distance = form.distance.data
        site.marine_life = form.marine_life.data
        site.description = form.description.data        
        site.slug = slug

        db.session.commit()

        flash('The dive site has benn updated', 'success')


        return redirect(url_for('sites.dive_site', slug=slug))

    elif request.method == 'GET':

        form.sitename.data = site.sitename
        form.level.data = site.level
        form.dive_time.data = site.dive_time
        form.depth.data = site.depth
        form.distance.data = site.distance
        form.marine_life.data = site.marine_life
        form.description.data = site.description
        form.map_image.data = site.map_image

    return render_template('sites/create_update_site.html', title='Update Site', 
                            form=form, legend='Update Site')


# Delete dive site from the delete post modal form
@sites.route('/post/<string:slug>/delete', methods=['POST']) # Describe wether argument will be int or string with : infront of variable
def delete_site(slug):
    # Get the post from the db from the post id passed into the url args
    site = Site.query.filter_by(slug=slug).first_or_404() # Get the post with this id, if not found return with 404 page not found error, SQLAlchemy methods

    # Delete the post from the db
    db.session.delete(site)
    db.session.commit()

    # Flash message too the user to let them know post has been deleted
    flash('Your dive site has been deleted', 'success')

    # Redirect back to home
    return redirect(url_for('sites.all_sites'))

