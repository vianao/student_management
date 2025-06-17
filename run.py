from dotenv import load_dotenv
from app import create_app, db

load_dotenv()
app = create_app()

# 确保应用上下文存在
app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True) 