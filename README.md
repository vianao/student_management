# 学生信息管理系统

这是一个基于Flask和MySQL的学生信息管理系统，提供学生信息、班级、课程和选课等功能的管理。

## 功能特点

- 学生信息管理（增删改查）
- 班级信息管理
- 课程信息管理
- 成绩录入与查询
- 学生选课管理

## 技术栈

- 后端：Flask + MySQL
- 前端：Bootstrap 5 + JavaScript
- 数据库：MySQL

## 安装步骤

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd student-management-system
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

5. 初始化数据库：
```bash
flask db upgrade
```

## 运行项目

```bash
python run.py
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