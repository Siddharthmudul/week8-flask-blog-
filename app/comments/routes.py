"""Comment routes."""

from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.comments.forms import CommentForm
from app.models import Comment, Post


comments = Blueprint("comments", __name__)


@comments.route("/posts/<int:post_id>/comments", methods=["POST"])
@login_required
def create(post_id):
	post = Post.query.get_or_404(post_id)
	form = CommentForm()
	if form.validate_on_submit():
		db.session.add(Comment(body=form.body.data, user_id=current_user.id, post_id=post.id, approved=False))
		db.session.commit()
		flash("Comment submitted for moderation.", "success")
	return redirect(url_for("posts.detail", post_id=post.id))


@comments.route("/comments/<int:comment_id>/approve", methods=["POST"])
@login_required
def approve(comment_id):
	if not current_user.is_admin:
		abort(403)
	comment = Comment.query.get_or_404(comment_id)
	comment.approved = True
	db.session.commit()
	return redirect(url_for("posts.detail", post_id=comment.post_id))


@comments.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	if not current_user.is_admin and comment.user_id != current_user.id:
		abort(403)
	post_id = comment.post_id
	db.session.delete(comment)
	db.session.commit()
	return redirect(url_for("posts.detail", post_id=post_id))
