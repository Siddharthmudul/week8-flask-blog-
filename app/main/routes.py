"""Main application routes."""

from flask import Blueprint, Response, flash, redirect, render_template, url_for
from flask_login import current_user

from app import db
from app.main.forms import ContactForm
from app.models import Comment, ContactMessage, Post, User


main = Blueprint("main", __name__)


@main.route("/")
def index():
    user = User.query.filter_by(name="John Doe").first()
    if user is None:
        user = User(username="john", name="John Doe", email="john@example.com", password_hash="")
        db.session.add(user)
        db.session.commit()

    post = Post.query.filter_by(title="Getting Started with Flask Web Development").first()
    if post is None:
        post = Post(
            title="Getting Started with Flask Web Development",
            content="In this comprehensive guide, we'll explore how to build your first Flask application...",
            category="Web Development",
            views=1245,
            likes=45,
            user_id=user.id,
        )
        db.session.add(post)
        db.session.commit()

    comments = Comment.query.filter_by(post_id=post.id, approved=True).all()
    if not comments:
        jane = User.query.filter_by(name="Jane Smith").first()
        if jane is None:
            jane = User(name="Jane Smith", email="jane@example.com")
            db.session.add(jane)
            db.session.commit()

        alex = User.query.filter_by(name="Alex Johnson").first()
        if alex is None:
            alex = User(name="Alex Johnson", email="alex@example.com")
            db.session.add(alex)
            db.session.commit()

        sarah = User.query.filter_by(name="Sarah Williams").first()
        if sarah is None:
            sarah = User(name="Sarah Williams", email="sarah@example.com")
            db.session.add(sarah)
            db.session.commit()

        db.session.add_all(
            [
                    Comment(post_id=post.id, user_id=jane.id, body="Excellent tutorial! The step-by-step approach really helped me understand Flask better.", approved=True),
                    Comment(post_id=post.id, user_id=alex.id, body="Could you add a section about deployment? That would be really helpful!", approved=True),
                    Comment(post_id=post.id, user_id=sarah.id, body="The database integration section was particularly useful. Thanks!", approved=True),
            ]
        )
        db.session.commit()
        comments = Comment.query.filter_by(post_id=post.id).all()

    active_users = [
        ("John Doe", 15),
        ("Jane Smith", 8),
        ("Mike Brown", 5),
    ]

    return render_template(
        "main/index.html",
        user=user,
        post=post,
        comments=comments,
        published_date="January 25, 2024",
        comment_dates=["Jan 25, 2024", "Jan 26, 2024", "Jan 27, 2024"],
        comment_total=12,
        active_users=active_users,
        total_posts=25,
        total_comments=156,
        categories=8,
        most_popular_post='Python for Data Science',
    )


@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data, email=form.email.data, subject=form.subject.data, message=form.message.data,
            user_id=current_user.id if current_user.is_authenticated else None,
        )
        db.session.add(message)
        db.session.commit()
        flash("Your message has been sent.", "success")
        return redirect(url_for("main.contact"))
    return render_template("main/contact.html", form=form)


@main.route("/feed.xml")
def feed():
    posts = Post.query.filter_by(status="published").order_by(Post.created_at.desc()).limit(20).all()
    items = "".join(
        f"<item><title>{post.title}</title><link>{url_for('posts.detail', post_id=post.id, _external=True)}</link>"
        f"<description><![CDATA[{post.content}]]></description></item>" for post in posts
    )
    return Response(f"<?xml version='1.0'?><rss version='2.0'><channel><title>Flask Blog</title>{items}</channel></rss>", mimetype="application/rss+xml")
