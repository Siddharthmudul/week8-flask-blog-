"""Post forms."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired(), Length(max=200)])
	category = StringField("Category", validators=[DataRequired(), Length(max=80)])
	content = TextAreaField("Content", validators=[DataRequired()])
	status = SelectField("Status", choices=[("published", "Published"), ("draft", "Draft")])
	image = FileField("Cover image", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only")])
	submit = SubmitField("Save post")
