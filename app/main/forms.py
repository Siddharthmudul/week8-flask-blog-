"""Main application forms."""

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired(), Length(max=120)])
	email = EmailField("Email", validators=[DataRequired(), Email()])
	subject = StringField("Subject", validators=[Length(max=200)])
	message = TextAreaField("Message", validators=[DataRequired(), Length(max=5000)])
	submit = SubmitField("Send message")
