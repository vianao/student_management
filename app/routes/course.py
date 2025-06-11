from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.course import Course

course_bp = Blueprint('course', __name__, url_prefix='/courses')

@course_bp.route('/')
def list_courses():
    """显示课程列表页面"""
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@course_bp.route('/add', methods=['POST'])
def add_course():
    """添加新课程"""
    try:
        course = Course(
            course_id=request.form['course_id'],
            name=request.form['name'],
            credits=float(request.form['credits']),
            description=request.form.get('description')
        )
        db.session.add(course)
        db.session.commit()
        flash('课程添加成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'添加课程失败：{str(e)}', 'danger')
    return redirect(url_for('course.list_courses'))

@course_bp.route('/edit', methods=['POST'])
def edit_course():
    """编辑课程信息"""
    try:
        course = Course.query.get_or_404(request.form['id'])
        course.course_id = request.form['course_id']
        course.name = request.form['name']
        course.credits = float(request.form['credits'])
        course.description = request.form.get('description')
        db.session.commit()
        flash('课程信息更新成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'更新课程信息失败：{str(e)}', 'danger')
    return redirect(url_for('course.list_courses'))

@course_bp.route('/delete/<int:id>')
def delete_course(id):
    """删除课程"""
    try:
        course = Course.query.get_or_404(id)
        if course.enrollments:
            flash('无法删除课程：该课程还有学生选修！', 'danger')
        else:
            db.session.delete(course)
            db.session.commit()
            flash('课程删除成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除课程失败：{str(e)}', 'danger')
    return redirect(url_for('course.list_courses')) 