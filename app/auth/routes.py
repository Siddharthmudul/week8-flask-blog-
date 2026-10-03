"""Authentication routes."""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(
			username=form.username.data,
			name=form.username.data,
			email=form.email.data,
			password_hash=generate_password_hash(form.password.data),
		)
		db.session.add(user)
		db.session.commit()
		flash("Your account has been created. You can now sign in.", "success")
		return redirect(url_for("auth.login"))
	return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password_hash, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for("main.index"))
		flash("Invalid email or password.", "danger")
	return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
	logout_user()
	flash("You have been signed out.", "info")
	return redirect(url_for("main.index"))
