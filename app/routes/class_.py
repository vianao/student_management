from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.class_ import Class

class_bp = Blueprint('class_', __name__, url_prefix='/classes')

@class_bp.route('/')
def list_classes():
    """显示班级列表页面"""
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)

@class_bp.route('/add', methods=['POST'])
def add_class():
    """添加新班级"""
    try:
        class_ = Class(name=request.form['name'])
        db.session.add(class_)
        db.session.commit()
        flash('班级添加成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'添加班级失败：{str(e)}', 'danger')
    return redirect(url_for('class_.list_classes'))

@class_bp.route('/edit', methods=['POST'])
def edit_class():
    """编辑班级信息"""
    try:
        class_ = Class.query.get_or_404(request.form['id'])
        class_.name = request.form['name']
        db.session.commit()
        flash('班级信息更新成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'更新班级信息失败：{str(e)}', 'danger')
    return redirect(url_for('class_.list_classes'))

@class_bp.route('/delete/<int:id>')
def delete_class(id):
    """删除班级"""
    try:
        class_ = Class.query.get_or_404(id)
        if class_.students:
            flash('无法删除班级：该班级还有学生！', 'danger')
        else:
            db.session.delete(class_)
            db.session.commit()
            flash('班级删除成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除班级失败：{str(e)}', 'danger')
    return redirect(url_for('class_.list_classes')) 