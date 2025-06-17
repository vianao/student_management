# 数据模型目录结构说明

## 目录结构

```
app/models/
├── __init__.py        # 模型包初始化文件
├── models.py          # 基础模型和共享功能
├── student.py         # 学生模型
├── course.py          # 课程模型
├── enrollment.py      # 选课模型
└── class_.py          # 班级模型
```

## 数据模型说明

### 1. models.py（基础模型）
- 包含共享的基础模型类和功能
- 定义数据库连接和基本配置
- 提供通用的模型方法和工具函数
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """基础模型类"""
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
```

### 2. student.py（学生模型）
- 定义学生相关的数据结构
- 主要字段：
  * student_id：学号
  * name：姓名
  * gender：性别
  * age：年龄
  * class_id：班级ID（外键）
```python
class Student(BaseModel):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
```

### 3. class_.py（班级模型）
- 定义班级相关的数据结构
- 主要字段：
  * name：班级名称
  * students：与学生的关联关系
```python
class Class(BaseModel):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    students = db.relationship('Student', backref='class_')
```

### 4. course.py（课程模型）
- 定义课程相关的数据结构
- 主要字段：
  * course_id：课程编号
  * name：课程名称
  * credit：学分
  * teacher：任课教师
```python
class Course(BaseModel):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    credit = db.Column(db.Float, default=0.0)
    teacher = db.Column(db.String(50))
```

### 5. enrollment.py（选课模型）
- 定义选课记录的数据结构
- 主要字段：
  * student_id：学生ID（外键）
  * course_id：课程ID（外键）
  * grade：成绩
  * enrollment_date：选课日期
```python
class Enrollment(BaseModel):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    grade = db.Column(db.Float, default=0.0)
    enrollment_date = db.Column(db.DateTime, default=datetime.now)
```

## 模型关系

1. **学生-班级关系**
   - 一对多关系：一个班级可以有多个学生
   - 外键：`Student.class_id` -> `Class.id`
   - 反向引用：`Class.students`

2. **学生-课程关系**
   - 多对多关系：通过选课表（enrollments）关联
   - 中间表：`Enrollment`
   - 关联字段：`student_id`, `course_id`

## 数据库特性

1. **字段约束**
   - 主键自增：`id`字段
   - 唯一约束：`student_id`, `course_id`
   - 非空约束：关键信息字段
   - 默认值：特定字段如`credit`, `grade`

2. **时间戳**
   - 创建时间：`created_at`
   - 更新时间：`updated_at`
   - 自动更新：使用`onupdate`触发器

3. **关系定义**
   - 外键约束
   - 级联操作
   - 反向引用（backref）

## 使用示例

```python
# 创建新学生
new_student = Student(
    student_id='2024001',
    name='张三',
    gender='男',
    age=20,
    class_id=1
)
db.session.add(new_student)
db.session.commit()

# 查询选课记录
enrollments = Enrollment.query.filter_by(student_id=1).all()
for enrollment in enrollments:
    print(f"课程：{enrollment.course.name}, 成绩：{enrollment.grade}")
```

## 开发规范

1. **命名规范**
   - 模型类名使用大驼峰命名法
   - 表名使用小写复数形式
   - 字段名使用下划线命名法

2. **注释规范**
   - 模型类必须有文档字符串
   - 重要字段需要注释说明
   - 复杂关系需要详细说明

3. **代码组织**
   - 相关模型放在同一文件
   - 共用功能放在基类中
   - 保持代码简洁清晰 