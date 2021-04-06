from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, MultipleFileField

class ImageForm(FlaskForm):
	picture = MultipleFileField('Select Image', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Upload')