from flaskblog import db

# Create dive site model
class Course(db.Model):
    course_name = db.Column(db.String(100), primary_key=True)
    level = db.Column(db.String(100))
    level_slug = db.Column(db.String(100))
    age = db.Column(db.Integer)
    duration = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    price_e_learning = db.Column(db.Integer)
    price_book_learning = db.Column(db.Integer)
    pool_dives = db.Column(db.Integer)
    ocean_dives = db.Column(db.Integer)
    min_dives = db.Column(db.String(100))
    qualified_to = db.Column(db.String(255))
    basic_info = db.Column(db.Text)
    schedule = db.Column(db.Text)
    image = db.Column(db.String(100), default='default_course.jpg')


    def __repr__(self):
        return f"Site('{self.course_name}', '{self.level}')"