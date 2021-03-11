from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed TODO need this for files in posts
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	picture = FileField('Select Image', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Post')