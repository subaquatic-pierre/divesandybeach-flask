from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, DataRequired
from flask_wtf import FlaskForm

class CourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[InputRequired()])
    level = StringField('Level', validators=[InputRequired()])
    age = IntegerField('Minimum Age', validators=[InputRequired()])
    duration = IntegerField('Duration', validators=[InputRequired()])
    price_e_learning = IntegerField('E-learning Price')
    price_book_learning = IntegerField('Book Learning Price')
    pool_dives = IntegerField('No. Pool Dives')
    ocean_dives = IntegerField('No. Ocean Dives')
    min_dives = IntegerField('Minimum No. of Dives')
    qualified_to = StringField('Qualified To:')
    basic_info = TextAreaField('Basic Info', validators=[InputRequired()])
    schedule = TextAreaField('Schedule', validators=[InputRequired()])
    image = FileField('Course Image', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Submit')