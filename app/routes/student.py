from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.student import Student
from app.models.class_ import Class

student_bp = Blueprint('student', __name__, url_prefix='/students')

@student_bp.route('/')
def list_students():
    """显示学生列表页面"""
    students = Student.query.all()
    classes = Class.query.all()
    return render_template('students.html', students=students, classes=classes)

@student_bp.route('/add', methods=['POST'])
def add_student():
    """添加新学生"""
    try:
        student = Student(
            student_id=request.form['student_id'],
            name=request.form['name'],
            gender=request.form['gender'],
            age=int(request.form['age']),
            class_id=request.form['class_id'] if request.form['class_id'] else None
        )
        db.session.add(student)
        db.session.commit()
        flash('学生添加成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'添加学生失败：{str(e)}', 'danger')
    return redirect(url_for('student.list_students'))

@student_bp.route('/edit', methods=['POST'])
def edit_student():
    """编辑学生信息"""
    try:
        student = Student.query.get_or_404(request.form['id'])
        student.student_id = request.form['student_id']
        student.name = request.form['name']
        student.gender = request.form['gender']
        student.age = int(request.form['age'])
        student.class_id = request.form['class_id'] if request.form['class_id'] else None
        db.session.commit()
        flash('学生信息更新成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'更新学生信息失败：{str(e)}', 'danger')
    return redirect(url_for('student.list_students'))

@student_bp.route('/delete/<int:id>')
def delete_student(id):
    """删除学生"""
    try:
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        flash('学生删除成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除学生失败：{str(e)}', 'danger')
    return redirect(url_for('student.list_students')) 