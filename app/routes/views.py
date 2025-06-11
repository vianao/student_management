from flask import Blueprint, render_template
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/students')
def students():
    return render_template('students.html')

@views_bp.route('/classes')
def classes():
    return render_template('classes.html')

@views_bp.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@views_bp.route('/enrollments')
def enrollments():
    enrollments = Enrollment.query.all()
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('enrollments.html', enrollments=enrollments, students=students, courses=courses) 