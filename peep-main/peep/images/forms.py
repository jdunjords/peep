from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ImageForm(FlaskForm):
	picture = FileField('Select Image', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Upload')