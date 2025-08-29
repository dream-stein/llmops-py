#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的Flask应用启动脚本，用于测试基本功能
"""
import os
import sys
import dotenv
from flask import Flask

# 设置Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 加载环境变量
dotenv.load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 基本配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/')
def hello():
    return {'message': 'LLMOps应用启动成功！', 'status': 'running'}

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    print("正在启动简化版Flask应用...")
    app.run(host='0.0.0.0', port=5000, debug=True)