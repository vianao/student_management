from flask import Blueprint, render_template
from sqlalchemy import func, case
from app import db
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/')
def index():
    # 检查是否有成绩数据
    has_grades = db.session.query(Enrollment).filter(Enrollment.grade != None).first() is not None

    if not has_grades:
        # 如果没有成绩数据，返回空的统计数据
        return render_template('analysis.html',
                            course_stats=[],
                            student_stats=[],
                            passing_rate=0,
                            grade_distribution={
                                '优秀(90-100)': 0,
                                '良好(80-89)': 0,
                                '中等(70-79)': 0,
                                '及格(60-69)': 0,
                                '不及格(0-59)': 0
                            })

    # 获取所有课程的平均分
    course_stats = db.session.query(
        Course.name,
        func.coalesce(func.avg(case((Enrollment.grade != None, Enrollment.grade))), 0).label('avg_grade'),
        func.coalesce(func.min(case((Enrollment.grade != None, Enrollment.grade))), 0).label('min_grade'),
        func.coalesce(func.max(case((Enrollment.grade != None, Enrollment.grade))), 0).label('max_grade'),
        func.count(Enrollment.id).label('student_count')
    ).join(Enrollment).group_by(Course.id).all()

    # 获取学生总成绩和平均分排名
    student_stats = db.session.query(
        Student.name,
        Student.student_id,
        func.coalesce(func.avg(case((Enrollment.grade != None, Enrollment.grade))), 0).label('avg_grade'),
        func.count(Enrollment.id).label('course_count')
    ).join(Enrollment).group_by(Student.id)\
    .having(func.count(Enrollment.id) > 0)\
    .order_by(func.avg(case((Enrollment.grade != None, Enrollment.grade))).desc()).all()

    # 计算及格率
    total_grades = db.session.query(Enrollment.grade).filter(Enrollment.grade != None).count()
    passing_grades = db.session.query(Enrollment.grade).filter(Enrollment.grade >= 60).count()
    passing_rate = (passing_grades / total_grades * 100) if total_grades > 0 else 0

    # 成绩分布
    grade_distribution = {
        '优秀(90-100)': db.session.query(Enrollment).filter(Enrollment.grade >= 90).count(),
        '良好(80-89)': db.session.query(Enrollment).filter(Enrollment.grade >= 80, Enrollment.grade < 90).count(),
        '中等(70-79)': db.session.query(Enrollment).filter(Enrollment.grade >= 70, Enrollment.grade < 80).count(),
        '及格(60-69)': db.session.query(Enrollment).filter(Enrollment.grade >= 60, Enrollment.grade < 70).count(),
        '不及格(0-59)': db.session.query(Enrollment).filter(Enrollment.grade < 60, Enrollment.grade != None).count()
    }

    return render_template('analysis.html',
                         course_stats=course_stats,
                         student_stats=student_stats,
                         passing_rate=passing_rate,
                         grade_distribution=grade_distribution) 