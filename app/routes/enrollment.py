from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course

enrollment_bp = Blueprint('enrollment', __name__, url_prefix='/enrollments')

@enrollment_bp.route('/')
def list_enrollments():
    """显示选课列表页面"""
    enrollments = Enrollment.query.all()
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('enrollments.html', enrollments=enrollments, students=students, courses=courses)

@enrollment_bp.route('/add', methods=['POST'])
def add_enrollment():
    """添加新选课"""
    try:
        # 检查是否已经选过这门课
        existing = Enrollment.query.filter_by(
            student_id=request.form['student_id'],
            course_id=request.form['course_id']
        ).first()
        
        if existing:
            flash('该学生已经选过这门课程！', 'danger')
            return redirect(url_for('enrollment.list_enrollments'))

        enrollment = Enrollment(
            student_id=request.form['student_id'],
            course_id=request.form['course_id']
        )
        
        if request.form.get('grade'):
            enrollment.grade = int(request.form['grade'])
            
        db.session.add(enrollment)
        db.session.commit()
        flash('选课成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'选课失败：{str(e)}', 'danger')
    return redirect(url_for('enrollment.list_enrollments'))

@enrollment_bp.route('/edit', methods=['POST'])
def edit_enrollment():
    """编辑选课信息"""
    try:
        enrollment = Enrollment.query.get_or_404(request.form['id'])
        
        # 如果更改了学生或课程，检查是否存在重复选课
        if (int(request.form['student_id']) != enrollment.student_id or 
            int(request.form['course_id']) != enrollment.course_id):
            existing = Enrollment.query.filter_by(
                student_id=request.form['student_id'],
                course_id=request.form['course_id']
            ).first()
            if existing:
                flash('该学生已经选过这门课程！', 'danger')
                return redirect(url_for('enrollment.list_enrollments'))

        enrollment.student_id = request.form['student_id']
        enrollment.course_id = request.form['course_id']
        if request.form.get('grade'):
            enrollment.grade = int(request.form['grade'])
        else:
            enrollment.grade = None
            
        db.session.commit()
        flash('选课信息更新成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'更新选课信息失败：{str(e)}', 'danger')
    return redirect(url_for('enrollment.list_enrollments'))

@enrollment_bp.route('/delete/<int:id>')
def delete_enrollment(id):
    """删除选课"""
    try:
        enrollment = Enrollment.query.get_or_404(id)
        db.session.delete(enrollment)
        db.session.commit()
        flash('退课成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'退课失败：{str(e)}', 'danger')
    return redirect(url_for('enrollment.list_enrollments')) 