Week 8 Flask Blog - Project Documentation
1. Project Overview
This project is a Flask-based blog application designed to support user registration, authentication, blog post management, comments, and a contact form. The application follows a modular blueprint architecture and uses SQLAlchemy for database management and Flask-Login for user sessions.
The blog is structured to provide a clean and scalable starting point for building a publishing platform or content management site with authentication and content moderation features.
2. Objectives
•	Create a simple but functional blog platform using Flask.
•	Support user accounts with registration, login, and logout.
•	Allow authenticated users to create, edit, and delete posts.
•	Enable users to submit comments and administrators to moderate them.
•	Provide an attractive homepage, contact form, and RSS feed.
•	Use a modular structure for maintainability and future expansion.
3. Key Features
•	User registration and login using Flask-Login and password hashing.
•	Authentication-aware routes to restrict unauthorized access.
•	Blog post listing with searching and pagination.
•	Create, edit, and delete posts for the author or admin.
•	Comment submission with approval workflow.
•	Admin moderation for approving or deleting comments.
•	Contact page for sending messages to the site owner.
•	RSS feed generation for published posts.
•	Database initialization with default admin user and sample content.
4. Technology Stack
Framework: Flask
Database: Flask-SQLAlchemy with SQLite by default
Authentication: Flask-Login
Forms and validation: Flask-WTF
Email validation: email-validator
Template engine: Jinja2
Security: CSRF protection and hashed passwords
5. Application Architecture
The application uses Flask blueprints to separate major functionality into independent modules. This keeps the project organized and makes it easier to extend with new features.
Blueprints used in this project:
•	- auth
•	- posts
•	- comments
•	- main
6. Project Structure

app/
    __init__.py
    models.py
    auth/
    comments/
    main/
    posts/
    static/
    templates/
config.py
run.py
requirements.txt
README.md
instance/
migrations/
tests/

7. Main Modules
app/__init__.py
Initializes the Flask app, database instance, login manager, CSRF protection, and default data setup.
app/models.py
Defines the user, post, comment, and contact message database models.
app/auth/routes.py
Handles registration, login, logout, and authentication workflows.
app/posts/routes.py
Handles listing, creating, editing, deleting, and viewing posts.
app/comments/routes.py
Creates, approves, and deletes comments for moderation.
app/main/routes.py
Provides the homepage, contact form, and RSS feed functionality.
config.py
Contains the application configuration settings, including secret key and database URL.
run.py
Runs the Flask application.
8. Database Model Overview
The application uses SQLAlchemy models to store blog content and user information.
•	User: stores username, email, password hash, admin flag, and timestamps.
•	Post: stores title, content, category, image, status, author, and related metadata.
•	Comment: stores comment body, author, post reference, and approval status.
•	ContactMessage: stores contact form submissions from users or visitors.
9. Setup and Run Instructions
1. Create a virtual environment: python -m venv .venv
2. Activate the environment: .venv\Scripts\activate
3. Install dependencies: pip install -r requirements.txt
4. Run the app: python run.py
5. Open the app in a browser: http://127.0.0.1:5000
10. Security Features
•	Passwords are stored as secure hashes using Werkzeug.
•	Routes use Flask-Login to restrict access to protected views.
•	CSRF protection is enabled with Flask-WTF.
•	Admin-only actions are enforced for moderation and administrative tasks.
11. Deployment and Future Improvements
This project is configured for local development using SQLite. For production deployment, it can later be upgraded to PostgreSQL or MySQL, with environment variables for secure configuration and a production WSGI server such as Gunicorn or uWSGI.
Potential future improvements include user profiles, category filters, image resizing, email notifications, and a richer admin dashboard.

Prepared for the Week 8 Flask Blog project.
