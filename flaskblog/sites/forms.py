from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, DataRequired
from flask_wtf import FlaskForm

class SiteForm(FlaskForm):
    sitename = StringField('Site Name', validators=[InputRequired()])
    level = StringField('Required Certification Level', validators=[InputRequired()])
    dive_time = StringField('Dive Time', validators=[InputRequired()])
    depth = StringField('Maximum Depth', validators=[InputRequired()])
    distance = StringField('Boat Travel Time', validators=[InputRequired()])
    marine_life = TextAreaField('Marine Life', validators=[InputRequired()])
    description = TextAreaField('Site Description', validators=[InputRequired()])
    map_image = FileField('Site Map', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Create')