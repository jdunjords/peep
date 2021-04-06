from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	picture = MultipleFileField('Select Image', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Post')


class CommentForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')