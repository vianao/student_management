from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def index():
    """首页路由"""
    return render_template('index.html') 