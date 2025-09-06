#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask应用启动脚本 - 绕过复杂的依赖注入
"""
import os
import sys
import dotenv
from flask import Flask
from flask_cors import CORS

# 设置Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 加载环境变量
dotenv.load_dotenv()

# 导入基本模块
from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 创建Flask应用
app = Flask(__name__)

# 基本配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db, directory="internal/migration")

# 配置CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        "supports_credentials": True,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
    }
})

# 基本路由
@app.route('/')
def index():
    return {
        'message': 'LLMOps Flask应用运行中',
        'status': 'running',
        'version': '1.0.0'
    }

@app.route('/health')
def health():
    try:
        # 简单的数据库连接测试
        with app.app_context():
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

@app.route('/api/status')
def api_status():
    return {
        'api': 'active',
        'database': 'sqlite',
        'environment': 'development'
    }

if __name__ == '__main__':
    print("🚀 正在启动LLMOps Flask应用...")
    print(f"📊 数据库: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("🌐 访问地址: http://localhost:5000")
    
    with app.app_context():
        # 创建数据库表
        try:
            db.create_all()
            print("✅ 数据库表创建成功")
        except Exception as e:
            print(f"⚠️ 数据库初始化警告: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)