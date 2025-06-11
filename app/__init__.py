from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.views import views
    from app.routes.student import student_bp
    from app.routes.class_ import class_bp
    from app.routes.course import course_bp
    from app.routes.enrollment import enrollment_bp
    from app.routes.analysis import analysis_bp

    app.register_blueprint(views)
    app.register_blueprint(student_bp)
    app.register_blueprint(class_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(enrollment_bp)
    app.register_blueprint(analysis_bp)

    with app.app_context():
        db.create_all()

    return app 