import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用程序密钥
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')  # 默认值为'dev'
    
    # 调试模式
    DEBUG = os.getenv('FLASK_ENV') == 'development' 