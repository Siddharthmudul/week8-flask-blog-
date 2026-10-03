"""Post routes."""

import os

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.comments.forms import CommentForm
from app.models import Post
from app.posts.forms import PostForm


posts = Blueprint("posts", __name__)


def can_manage(post):
	return current_user.is_authenticated and (post.user_id == current_user.id or current_user.is_admin)


@posts.route("/posts")
def list_posts():
	query = request.args.get("q", "").strip()
	page = request.args.get("page", 1, type=int)
	posts_query = Post.query.filter_by(status="published").order_by(Post.created_at.desc())
	if query:
		posts_query = posts_query.filter(Post.title.ilike(f"%{query}%") | Post.content.ilike(f"%{query}%"))
	pagination = posts_query.paginate(page=page, per_page=5, error_out=False)
	return render_template("posts/list.html", pagination=pagination, query=query)


@posts.route("/posts/new", methods=["GET", "POST"])
@login_required
def create_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, category=form.category.data, content=form.content.data,
					status=form.status.data, user_id=current_user.id)
		if form.image.data:
			filename = secure_filename(form.image.data.filename)
			form.image.data.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
			post.image_file = filename
		db.session.add(post)
		db.session.commit()
		flash("Post saved.", "success")
		return redirect(url_for("posts.detail", post_id=post.id))
	return render_template("posts/form.html", form=form, title="New post")


@posts.route("/posts/<int:post_id>")
def detail(post_id):
	post = Post.query.get_or_404(post_id)
	if post.status != "published" and not can_manage(post):
		abort(404)
	return render_template("posts/detail.html", post=post, comment_form=CommentForm())


@posts.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit(post_id):
	post = Post.query.get_or_404(post_id)
	if not can_manage(post):
		abort(403)
	form = PostForm(obj=post)
	if form.validate_on_submit():
		form.populate_obj(post)
		if form.image.data:
			filename = secure_filename(form.image.data.filename)
			form.image.data.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
			post.image_file = filename
		db.session.commit()
		flash("Post updated.", "success")
		return redirect(url_for("posts.detail", post_id=post.id))
	return render_template("posts/form.html", form=form, title="Edit post", post=post)


@posts.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
	post = Post.query.get_or_404(post_id)
	if not can_manage(post):
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Post deleted.", "info")
	return redirect(url_for("posts.list_posts"))
