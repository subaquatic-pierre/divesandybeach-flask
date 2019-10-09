from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm

# Create post form class to be used to create a form to create a post 
class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')