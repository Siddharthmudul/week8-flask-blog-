from run import app
from app import db
from app.models import User, Post, Comment

with app.app_context():
    db.create_all()

    user = User.query.filter_by(name="John Doe").first()
    if user is None:
        user = User(name="John Doe", email="john@example.com")
        db.session.add(user)

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

    if not Comment.query.filter_by(post_id=post.id).count():
        jane = User.query.filter_by(name="Jane Smith").first()
        if jane is None:
            jane = User(name="Jane Smith", email="jane@example.com")
            db.session.add(jane)

        alex = User.query.filter_by(name="Alex Johnson").first()
        if alex is None:
            alex = User(name="Alex Johnson", email="alex@example.com")
            db.session.add(alex)

        sarah = User.query.filter_by(name="Sarah Williams").first()
        if sarah is None:
            sarah = User(name="Sarah Williams", email="sarah@example.com")
            db.session.add(sarah)

        db.session.commit()

        db.session.add_all([
            Comment(post_id=post.id, user_id=jane.id, body="Excellent tutorial! The step-by-step approach really helped me understand Flask better."),
            Comment(post_id=post.id, user_id=alex.id, body="Could you add a section about deployment? That would be really helpful!"),
            Comment(post_id=post.id, user_id=sarah.id, body="The database integration section was particularly useful. Thanks!"),
        ])

    db.session.commit()

response = app.test_client().get('/')
print(response.status_code)
body = response.get_data(as_text=True)
print('John Doe' in body)
print('Getting Started with Flask Web Development' in body)
print('Excellent tutorial!' in body)
