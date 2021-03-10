from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired #TODO need this for files in posts
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	filename = FileField(
			label="file",
			validators=[
				# 文件必须选择;
				FileRequired(),
				# 指定文件上传的格式;
				FileAllowed(['png', 'jpg'], 'png&jpg')
			]
	)
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')
