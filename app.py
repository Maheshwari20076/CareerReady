"""
CareerReady - Student Career Readiness & Skill Gap Analysis System
Application entry point / factory.
"""

from flask import Flask, render_template
from flask_login import LoginManager

from config import Config
from models import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # --- Register blueprints ---
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.resources import resources_bp
    from routes.interview import interview_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def landing():
        return render_template("landing.html")

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
