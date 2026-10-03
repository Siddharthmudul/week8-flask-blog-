"""Authentication forms."""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=3, max=120)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Create account")

	def validate_username(self, username):
		if User.query.filter_by(username=username.data).first():
			raise ValidationError("That username is already taken.")

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError("That email is already registered.")


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember me")
	submit = SubmitField("Sign in")
