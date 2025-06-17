from flask import Blueprint, render_template, request, send_file, make_response
from sqlalchemy import func, case
from app import db
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.class_ import Class
import pandas as pd
from io import BytesIO
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/')
def analysis_page():
    """分析页面"""
    classes = Class.query.all()
    courses = Course.query.all()

    # 检查是否有成绩数据
    has_grades = db.session.query(Enrollment).filter(Enrollment.grade != None).first() is not None

    if not has_grades:
        # 如果没有成绩数据，返回空的统计数据
        return render_template('analysis.html',
                            classes=classes,
                            courses=courses,
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
        func.avg(Enrollment.grade).label('avg_grade'),
        func.min(Enrollment.grade).label('min_grade'),
        func.max(Enrollment.grade).label('max_grade'),
        func.count(Enrollment.id).label('student_count')
    ).join(Enrollment).group_by(Course.id).all()

    # 获取学生总成绩和平均分排名
    student_stats = db.session.query(
        Student.name,
        Student.student_id,
        func.avg(Enrollment.grade).label('avg_grade'),
        func.count(Enrollment.id).label('course_count')
    ).join(Enrollment).group_by(Student.id)\
    .having(func.count(Enrollment.id) > 0)\
    .order_by(func.avg(Enrollment.grade).desc()).all()

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
                        classes=classes,
                        courses=courses,
                        course_stats=course_stats,
                        student_stats=student_stats,
                        passing_rate=passing_rate,
                        grade_distribution=grade_distribution)

@analysis_bp.route('/export_scores', methods=['POST'])
def export_scores():
    """导出成绩"""
    try:
        # 获取筛选条件
        class_id = request.form.get('class_id')
        course_id = request.form.get('course_id')
        min_grade = request.form.get('min_grade')
        max_grade = request.form.get('max_grade')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        selected_fields = request.form.getlist('fields')  # 获取选中的字段

        if not selected_fields:
            return make_response('请至少选择一个导出字段', 400)

        # 定义字段映射
        field_mapping = {
            'student_id': (Student.student_id, '学号'),
            'name': (Student.name, '姓名'),
            'class_name': (Class.name, '班级'),
            'course_code': (Course.course_id, '课程代码'),
            'course_name': (Course.name, '课程名称'),
            'grade': (Enrollment.grade, '成绩'),
            'enrollment_date': (Enrollment.enrollment_date, '选课日期'),
            'credits': (Course.credits, '学分')
        }

        # 构建查询字段
        query_fields = []
        column_names = {}
        for field in selected_fields:
            if field in field_mapping:
                db_field, display_name = field_mapping[field]
                labeled_field = db_field.label(field)
                query_fields.append(labeled_field)
                column_names[field] = display_name

        # 构建基础查询
        query = db.session.query(*query_fields)\
            .select_from(Student)\
            .join(Class, Student.class_id == Class.id)\
            .join(Enrollment, Student.id == Enrollment.student_id)\
            .join(Course, Enrollment.course_id == Course.id)

        # 应用筛选条件
        if class_id:
            query = query.filter(Class.id == class_id)
        if course_id:
            query = query.filter(Course.id == course_id)
        if min_grade:
            query = query.filter(Enrollment.grade >= float(min_grade))
        if max_grade:
            query = query.filter(Enrollment.grade <= float(max_grade))
        if start_date:
            query = query.filter(Enrollment.enrollment_date >= start_date)
        if end_date:
            query = query.filter(Enrollment.enrollment_date <= end_date + ' 23:59:59')

        # 执行查询
        results = query.all()

        # 转换为DataFrame
        data = []
        for r in results:
            row = {}
            for field in selected_fields:
                value = getattr(r, field)
                if field == 'enrollment_date' and value:
                    value = value.strftime('%Y-%m-%d')
                row[column_names[field]] = value
            data.append(row)

        df = pd.DataFrame(data)

        # 创建Excel文件
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='成绩单')
            # 调整列宽
            worksheet = writer.sheets['成绩单']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length

        output.seek(0)
        
        # 生成文件名
        filename = f'成绩单_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return make_response(str(e), 500) 