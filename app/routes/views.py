from flask import Blueprint, render_template

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
    return render_template('courses.html')

@views_bp.route('/enrollments')
def enrollments():
    return render_template('enrollments.html') 