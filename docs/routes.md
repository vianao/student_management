# 路由目录结构说明

## 目录结构

```
app/routes/
├── __init__.py        # 路由包初始化文件
├── analysis.py        # 成绩分析相关路由
├── course.py          # 课程管理相关路由
├── enrollment.py      # 选课管理相关路由
├── class_.py          # 班级管理相关路由
└── student.py         # 学生管理相关路由
```

## 路由模块说明

### 1. __init__.py
- 路由包的初始化文件
- 导入并收集所有蓝图（Blueprint）
- 便于在应用程序中统一注册路由
```python
from .student import student_bp
from .class_ import class_bp
from .course import course_bp
from .enrollment import enrollment_bp

__all__ = ['student_bp', 'class_bp', 'course_bp', 'enrollment_bp']
```

### 2. student.py（学生管理路由）
- URL前缀：`/students`
- 主要功能：
  * 学生列表展示
  * 添加新学生
  * 编辑学生信息
  * 删除学生记录
- 关键路由：
  ```python
  @student_bp.route('/')              # 学生列表页面
  @student_bp.route('/add')           # 添加学生
  @student_bp.route('/edit')          # 编辑学生
  @student_bp.route('/delete/<int:id>')# 删除学生
  ```

### 3. class_.py（班级管理路由）
- URL前缀：`/classes`
- 主要功能：
  * 班级列表展示
  * 创建新班级
  * 编辑班级信息
  * 删除班级
- 关键路由：
  ```python
  @class_bp.route('/')               # 班级列表页面
  @class_bp.route('/add')            # 添加班级
  @class_bp.route('/edit')           # 编辑班级
  @class_bp.route('/delete/<int:id>') # 删除班级
  ```

### 4. course.py（课程管理路由）
- URL前缀：`/courses`
- 主要功能：
  * 课程列表展示
  * 添加新课程
  * 编辑课程信息
  * 删除课程
- 关键路由：
  ```python
  @course_bp.route('/')              # 课程列表页面
  @course_bp.route('/add')           # 添加课程
  @course_bp.route('/edit')          # 编辑课程
  @course_bp.route('/delete/<int:id>')# 删除课程
  ```

### 5. enrollment.py（选课管理路由）
- URL前缀：`/enrollments`
- 主要功能：
  * 选课记录列表
  * 学生选课
  * 成绩录入
  * 退课处理
- 关键路由：
  ```python
  @enrollment_bp.route('/')          # 选课列表页面
  @enrollment_bp.route('/add')       # 添加选课记录
  @enrollment_bp.route('/edit')      # 编辑选课/录入成绩
  @enrollment_bp.route('/delete/<int:id>') # 退课
  ```

### 6. analysis.py（成绩分析路由）
- URL前缀：`/analysis`
- 主要功能：
  * 成绩统计分析
  * 课程平均分计算
  * 成绩分布展示
  * 及格率统计
  * 成绩数据导出
- 关键路由：
  ```python
  @analysis_bp.route('/')                # 成绩分析主页
  @analysis_bp.route('/export_scores', methods=['POST'])  # 成绩导出
  ```
- 导出功能特点：
  * 支持多种筛选条件：
    - 按班级筛选
    - 按课程筛选
    - 按成绩范围筛选
    - 按选课时间筛选
  * 自定义导出字段：
    - 学号
    - 姓名
    - 班级
    - 课程代码
    - 课程名称
    - 成绩
    - 选课日期
    - 学分
  * Excel格式导出
  * 自动列宽调整

## 路由特点

1. **蓝图组织**
   - 使用Flask蓝图（Blueprint）组织路由
   - 模块化路由管理
   - 清晰的URL结构

2. **RESTful设计**
   - 符合REST风格的API设计
   - 统一的URL命名规范
   - 标准的HTTP方法使用

3. **错误处理**
   - 统一的错误处理机制
   - 友好的错误提示
   - 数据验证和异常捕获

4. **数据交互**
   - 表单数据处理
   - 数据库操作封装
   - Flash消息反馈

## 安全特性

1. **输入验证**
   - 表单数据验证
   - SQL注入防护
   - XSS攻击防护

2. **权限控制**
   - 路由访问控制
   - 操作权限验证
   - 敏感数据保护

## 开发规范

1. **命名规范**
   - 路由函数使用下划线命名法
   - URL使用短横线分隔
   - 变量名清晰易懂

2. **注释规范**
   - 每个路由函数都有文档字符串
   - 关键逻辑有注释说明
   - 复杂操作有详细说明

3. **代码组织**
   - 相关功能集中管理
   - 代码结构清晰
   - 易于维护和扩展

## 使用示例

```python
# 添加学生示例
@student_bp.route('/add', methods=['POST'])
def add_student():
    """添加新学生"""
    try:
        student = Student(
            student_id=request.form['student_id'],
            name=request.form['name'],
            gender=request.form['gender'],
            age=int(request.form['age']),
            class_id=request.form['class_id']
        )
        db.session.add(student)
        db.session.commit()
        flash('学生添加成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'添加学生失败：{str(e)}', 'danger')
    return redirect(url_for('student.list_students'))
``` 