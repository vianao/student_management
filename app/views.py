from flask import Blueprint, render_template
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course
from app.models.class_ import Class

views = Blueprint('views', __name__)
 
@views.route('/')
def index():
    """首页路由"""
    stats = {
        'student_count': Student.query.count(),
        'class_count': Class.query.count(),
        'course_count': Course.query.count(),
        'enrollment_count': Enrollment.query.count()
    }
    return render_template('index.html', stats=stats) 