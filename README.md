# 学生信息管理系统

这是一个基于Flask和MySQL的学生信息管理系统，提供学生信息、班级、课程和选课等功能的管理。
展示地址：https://yun1.anevol.cn

# 学生信息管理系统

这是一个基于Flask和MySQL的学生信息管理系统，提供学生信息、班级、课程和选课等功能的管理。

## 系统分析

### 1. 功能需求

#### 1.1 学生信息管理
- 学生基本信息的录入、修改、删除和查询
  * 录入学生基本信息：学号、姓名、性别、年龄、所属班级
  * 支持按学号、姓名查询学生信息
  * 支持修改学生个人信息
  * 支持删除学生记录（同时删除相关的选课记录）
- 学生信息的批量导入导出
- 学生列表的分页显示和排序

#### 1.2 班级信息管理
- 班级信息的增删改查
  * 创建新班级并设置班级名称
  * 修改班级信息
  * 查看班级学生名单
  * 删除空班级
- 班级学生统计
  * 显示各班级的学生人数
  * 查看班级学生详细信息

#### 1.3 课程信息管理
- 课程基本信息的维护
  * 录入课程信息：课程编号、课程名称、学分、课程描述
  * 修改课程信息
  * 删除未被选修的课程
- 课程信息的查询和统计
  * 按课程编号、名称查询
  * 显示课程选修人数和平均成绩

#### 1.4 选课管理
- 学生选课功能
  * 学生选择课程
  * 查看已选课程
  * 退选课程
- 成绩管理
  * 录入课程成绩
  * 修改成绩
  * 成绩统计分析
  * 成绩数据导出功能：
    - 支持多种筛选条件（班级、课程、成绩范围、时间范围）
    - 自定义导出字段选择
    - Excel格式导出
    - 自动列宽调整

### 2. 系统实体及属性

#### 2.1 学生(Student)
- 主要属性：
  * id: 系统唯一标识（主键）
  * student_id: 学号（唯一）
  * name: 姓名
  * gender: 性别
  * age: 年龄
  * class_id: 所属班级ID（外键）
- 关联关系：
  * 与班级(Class)是多对一关系
  * 与选课(Enrollment)是一对多关系

#### 2.2 班级(Class)
- 主要属性：
  * id: 系统唯一标识（主键）
  * name: 班级名称（唯一）
- 关联关系：
  * 与学生(Student)是一对多关系

#### 2.3 课程(Course)
- 主要属性：
  * id: 系统唯一标识（主键）
  * course_id: 课程编号（唯一）
  * name: 课程名称
  * credits: 学分
  * description: 课程描述
- 关联关系：
  * 与选课(Enrollment)是一对多关系

#### 2.4 选课(Enrollment)
- 主要属性：
  * id: 系统唯一标识（主键）
  * student_id: 学生ID（外键）
  * course_id: 课程ID（外键）
  * grade: 成绩
- 关联关系：
  * 与学生(Student)是多对一关系
  * 与课程(Course)是多对一关系

### 3. 实体关系及业务规则

#### 3.1 核心业务规则
1. 学生管理规则：
   - 每个学生必须有唯一的学号
   - 学生可以属于一个班级
   - 学生可以选修多门课程
   - 删除学生时会自动删除其选课记录

2. 班级管理规则：
   - 班级名称必须唯一
   - 一个班级可以包含多名学生
   - 班级可以没有学生

3. 课程管理规则：
   - 课程编号必须唯一
   - 一门课程可以被多名学生选修
   - 课程学分必须大于0

4. 选课管理规则：
   - 一个学生只能选修同一门课程一次
   - 选课记录包含学生成绩信息
   - 成绩可以为空（表示尚未录入）
   - 删除课程或学生时，相关的选课记录会自动删除

#### 3.2 关系约束
1. 学生-班级关系：
   - 多对一关系
   - 学生可以不属于任何班级
   - 班级可以没有学生

2. 学生-课程关系：
   - 多对多关系，通过选课表实现
   - 一个学生可以选修多门课程
   - 一门课程可以被多名学生选修
   - 选课记录通过外键关联学生和课程

3. 级联规则：
   - 删除学生时，级联删除其选课记录
   - 删除课程时，级联删除相关选课记录
   - 删除班级时，需确保班级内没有学生


## 技术栈

- 后端：Flask + MySQL
- 前端：Bootstrap 5 + JavaScript
- 数据库：MySQL

## 数据库设计

### ER 图设计

```mermaid
erDiagram
    Class ||--o{ Student : has
    Student ||--o{ Enrollment : includes
    Course ||--o{ Enrollment : includes

    Class {
        int id
        string name UK
    }

    Student {
        int id
        string student_id UK
        string name
        string gender
        int age
        int class_id FK
    }

    Course {
        int id
        string course_id UK
        string name
        float credits
        text description
    }

    Enrollment {
        int id
        int student_id FK
        int course_id FK
        int grade
        datetime enrollment_date
    }
```

### ER 图设计说明

#### 1. 实体说明

1. 班级(Class)
   - 主实体，代表学校的基本组织单位
   - 包含基本班级信息
   - 与学生形成一对多关系

2. 学生(Student)
   - 核心实体，系统的主要管理对象
   - 包含学生的基本信息
   - 通过外键关联班级
   - 通过选课关系与课程相关联

3. 课程(Course)
   - 独立实体，代表教学内容单元
   - 包含课程的基本信息和学分设置
   - 通过选课关系与学生相关联

4. 选课(Enrollment)
   - 关系实体，连接学生和课程
   - 记录选课信息和成绩
   - 作为学生和课程多对多关系的中间表

#### 2. 属性说明

1. 班级(Class)属性：
   - id：整型，主键，自增
   - name：字符串，唯一约束，班级名称

2. 学生(Student)属性：
   - id：整型，主键，自增
   - student_id：字符串，唯一约束，学号
   - name：字符串，学生姓名
   - gender：字符串，性别
   - age：整型，年龄
   - class_id：整型外键，关联班级

3. 课程(Course)属性：
   - id：整型，主键，自增
   - course_id：字符串，唯一约束，课程编号
   - name：字符串，课程名称
   - credits：浮点型，学分
   - description：文本，课程描述

4. 选课(Enrollment)属性：
   - id：整型，主键，自增
   - student_id：整型，外键，关联学生
   - course_id：整型外键，关联课程
   - grade：整型，成绩

#### 3. 关系及约束说明

1. 主键约束：
   - 所有实体表都使用 id 作为主键
   - 主键自增，确保唯一性

2. 唯一约束：
   - 班级名称(Class.name)唯一
   - 学号(Student.student_id)唯一
   - 课程编号(Course.course_id)唯一

3. 外键约束：
   - Student.class_id 引用 Class.id
   - Enrollment.student_id 引用 Student.id
   - Enrollment.course_id 引用 Course.id

4. 实体关系：
   - 班级-学生：一对多关系
     * 一个班级可以有多个学生
     * 一个学生只能属于一个班级
     * 外键可以为空，表示学生可以不属于任何班级

   - 学生-课程：多对多关系
     * 通过 Enrollment 表实现
     * 一个学生可以选修多门课程
     * 一门课程可以被多个学生选修
     * 包含成绩信息

#### 4. 设计合理性分析

1. 实体划分合理性：
   - 符合实际业务场景的实体划分
   - 实体之间关系清晰，职责分明
   - 避免了数据冗余

2. 关系设计合理性：
   - 使用中间表处理多对多关系
   - 合理使用外键约束保证数据完整性
   - 支持级联删除，维护数据一致性

3. 扩展性考虑：
   - 预留了课程描述等扩展字段
   - 字段类型选择合理，预留了足够空间
   - 支持未来功能扩展

4. 性能考虑：
   - 合理使用索引（主键、外键、唯一约束）
   - 避免过多的外键约束
   - 适当的字段类型选择

### 数据库创建SQL语句

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS student_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE student_management;

-- 创建班级表
CREATE TABLE classes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL COMMENT '班级名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班级表';

-- 创建学生表
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender VARCHAR(10) COMMENT '性别',
    age INT COMMENT '年龄',
    class_id INT COMMENT '班级ID',
    FOREIGN KEY (class_id) REFERENCES classes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生表';

-- 创建课程表
CREATE TABLE courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id VARCHAR(20) UNIQUE NOT NULL COMMENT '课程编号',
    name VARCHAR(100) NOT NULL COMMENT '课程名称',
    credits FLOAT NOT NULL COMMENT '学分',
    description TEXT COMMENT '课程描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程表';

-- 创建选课表
CREATE TABLE enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL COMMENT '学生ID',
    course_id INT NOT NULL COMMENT '课程ID',
    grade INT COMMENT '成绩',
    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '选课日期',
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY `unique_enrollment` (student_id, course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='选课表';

-- 添加索引
CREATE INDEX idx_student_id ON students(student_id);
CREATE INDEX idx_course_id ON courses(course_id);
CREATE INDEX idx_enrollment_grade ON enrollments(grade);
CREATE INDEX idx_enrollment_date ON enrollments(enrollment_date);
```

## 安装步骤

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd student_management
```

2. 创建虚拟环境并激活：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置数据库：
   - 创建MySQL数据库
   - 复制`.env.example`为`.env`
   - 修改`.env`中的数据库配置



## 运行项目

```bash
python run.py
```

修改了数据库模型，需要进行数据库迁移
```
flask db migrate -m "Add enrollment_date to Enrollment model"
```

访问 http://localhost:5000 即可使用系统。

## API接口

### 学生管理
- GET /api/students - 获取所有学生
- GET /api/students/<id> - 获取单个学生
- POST /api/students - 创建学生
- PUT /api/students/<id> - 更新学生
- DELETE /api/students/<id> - 删除学生

### 班级管理
- GET /api/classes - 获取所有班级
- GET /api/classes/<id> - 获取单个班级
- POST /api/classes - 创建班级
- PUT /api/classes/<id> - 更新班级
- DELETE /api/classes/<id> - 删除班级

### 课程管理
- GET /api/courses - 获取所有课程
- GET /api/courses/<id> - 获取单个课程
- POST /api/courses - 创建课程
- PUT /api/courses/<id> - 更新课程
- DELETE /api/courses/<id> - 删除课程

### 选课和成绩管理
- GET /api/enrollments/student/<student_id> - 获取学生的选课
- GET /api/enrollments/course/<course_id> - 获取课程的选课学生
- POST /api/enrollments - 创建选课记录
- PUT /api/enrollments/<id>/grade - 更新成绩
- DELETE /api/enrollments/<id> - 删除选课记录

## 贡献指南

1. Fork 本仓库
2. 创建新的分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License

### 测试数据集与查询测试

#### 1. 扩展测试数据集

```sql
-- 清空现有数据（按照外键关系的反序删除）
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE enrollments;
TRUNCATE TABLE students;
TRUNCATE TABLE courses;
TRUNCATE TABLE classes;
SET FOREIGN_KEY_CHECKS = 1;

-- 1.1 插入班级数据
INSERT INTO classes (id, name) VALUES 
(1, '计算机科学2021级1班'),
(2, '软件工程2021级1班'),
(3, '网络工程2021级1班'),
(4, '数据科学2022级1班'),
(5, '人工智能2022级1班');

-- 1.2 插入学生数据
INSERT INTO students (id, student_id, name, gender, age, class_id) VALUES
(1, '2021001', '张三', '男', 20, 1),
(2, '2021002', '李四', '女', 19, 1),
(3, '2021003', '王五', '男', 21, 2),
(4, '2021004', '赵六', '女', 20, 2),
(5, '2021005', '周七', '男', 20, 3),
(6, '2021006', '吴八', '女', 19, 3),
(7, '2022001', '郑九', '男', 19, 4),
(8, '2022002', '冯十', '女', 18, 4),
(9, '2022003', '陈百', '男', 19, 5),
(10, '2022004', '褚千', '女', 18, 5);

-- 1.3 插入课程数据
INSERT INTO courses (id, course_id, name, credits, description) VALUES
(1, 'CS101', '计算机导论', 3.0, '计算机科学与技术导论课程'),
(2, 'CS102', '数据结构', 4.0, '数据结构与算法基础'),
(3, 'CS103', '算法分析', 4.0, '算法设计与复杂度分析'),
(4, 'CS104', '数据库系统', 3.0, '数据库原理与应用'),
(5, 'CS105', '操作系统', 3.0, '操作系统原理与设计');

-- 1.4 插入选课数据
INSERT INTO enrollments (student_id, course_id, grade, enrollment_date) VALUES
(1, 1, 85, '2023-09-01 10:00:00'),
(1, 2, 90, '2023-09-01 10:30:00'),
(2, 1, 78, '2023-09-01 11:00:00'),
(2, 3, 88, '2023-09-01 14:00:00'),
(3, 2, 92, '2023-09-02 09:00:00'),
(3, 4, 76, '2023-09-02 10:00:00'),
(4, 3, 81, '2023-09-02 11:00:00'),
(4, 5, 95, '2023-09-02 14:00:00'),
(5, 1, 89, '2023-09-03 09:00:00'),
(5, 5, 84, '2023-09-03 10:00:00'),
(6, 2, 77, '2023-09-03 11:00:00'),
(6, 4, 93, '2023-09-03 14:00:00'),
(7, 1, 82, '2023-09-04 09:00:00'),
(7, 3, 87, '2023-09-04 10:00:00'),
(8, 2, 94, '2023-09-04 11:00:00'),
(8, 5, 79, '2023-09-04 14:00:00'),
(9, 1, 88, '2023-09-05 09:00:00'),
(9, 3, 91, '2023-09-05 10:00:00'),
(10, 2, 76, '2023-09-05 11:00:00'),
(10, 4, 85, '2023-09-05 14:00:00');

-- 2. 测试查询语句

-- 2.1 查询学生总人数和班级分布
SELECT c.name as class_name, COUNT(s.id) as student_count 
FROM classes c 
LEFT JOIN students s ON c.id = s.class_id 
GROUP BY c.id, c.name 
ORDER BY c.name;

-- 2.2 查询各课程的平均分、最高分、最低分
SELECT 
    c.course_id,
    c.name as course_name,
    COUNT(e.id) as student_count,
    ROUND(AVG(e.grade), 2) as avg_grade,
    MAX(e.grade) as max_grade,
    MIN(e.grade) as min_grade
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
GROUP BY c.id, c.course_id, c.name
ORDER BY c.course_id;

-- 2.3 查询学生成绩排名（按平均分）
SELECT 
    s.student_id,
    s.name,
    c.name as class_name,
    COUNT(e.id) as course_count,
    ROUND(AVG(e.grade), 2) as avg_grade
FROM students s
JOIN classes c ON s.class_id = c.id
LEFT JOIN enrollments e ON s.id = e.student_id
GROUP BY s.id, s.student_id, s.name, c.name
ORDER BY avg_grade DESC;

-- 2.4 查询各班级的及格率
SELECT 
    c.name as class_name,
    COUNT(e.id) as total_courses,
    SUM(CASE WHEN e.grade >= 60 THEN 1 ELSE 0 END) as passed_courses,
    ROUND(SUM(CASE WHEN e.grade >= 60 THEN 1 ELSE 0 END) * 100.0 / COUNT(e.id), 2) as pass_rate
FROM classes c
JOIN students s ON c.id = s.class_id
JOIN enrollments e ON s.id = e.student_id
GROUP BY c.id, c.name
ORDER BY pass_rate DESC;

-- 2.5 查询最近一周的选课记录
SELECT 
    s.student_id,
    s.name as student_name,
    c.course_id,
    c.name as course_name,
    e.enrollment_date
FROM enrollments e
JOIN students s ON e.student_id = s.id
JOIN courses c ON e.course_id = c.id
WHERE e.enrollment_date >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
ORDER BY e.enrollment_date DESC;
```

```