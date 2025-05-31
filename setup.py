"""
财经智能分析系统安装脚本
Financial Intelligence Analysis System Setup Script
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python版本检查通过: {sys.version}")

def install_requirements():
    """安装依赖包"""
    print("\n🔧 正在安装依赖包...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
    except subprocess.CalledProcessError:
        print("❌ 依赖包安装失败，请检查网络连接和requirements.txt文件")
        sys.exit(1)

def create_env_file():
    """创建环境变量文件"""
    print("\n📝 创建环境变量文件...")
    
    env_content = """# 财经智能分析系统环境变量配置
# 请填入您的实际配置信息

# 数据库配置
DATABASE_PATH=data/financial_analysis.db

# 邮件配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com

# API配置
OPENAI_API_KEY=your_openai_api_key
WHISPER_API_KEY=your_whisper_api_key

# Web应用配置
WEB_HOST=localhost
WEB_PORT=5000
DEBUG=False
SECRET_KEY=your-secret-key-here

# 日志配置
LOG_LEVEL=INFO
"""
    
    if not Path(".env").exists():
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ 已创建 .env 配置文件，请填入您的配置信息")
    else:
        print("⚠️  .env 文件已存在，跳过创建")

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建项目目录...")
    
    directories = [
        "logs", 
        "data/cache", 
        "data/reports", 
        "data/transcripts",
        "data/videos"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def create_gitignore():
    """创建.gitignore文件"""
    print("\n🚫 创建.gitignore文件...")
    
    gitignore_content = """# 环境变量
.env

# 数据文件
data/
logs/
*.db
*.sqlite

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""
    
    if not Path(".gitignore").exists():
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print("✅ 已创建 .gitignore 文件")
    else:
        print("⚠️  .gitignore 文件已存在，跳过创建")

def print_next_steps():
    """打印下一步操作指南"""
    print("\n🎉 安装完成！")
    print("\n📋 下一步操作：")
    print("1. 编辑 .env 文件，填入您的配置信息")
    print("2. 编辑 config.py 文件，配置UP主列表")
    print("3. 运行 python main.py 启动系统")
    print("4. 运行 python -m src.web.app 启动Web控制面板")
    print("5. 访问 http://localhost:5000 查看控制面板")
    print("\n📚 更多信息请查看 README.md 文件")

def main():
    """主安装函数"""
    print("🚀 财经智能分析系统安装程序")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 安装依赖
    install_requirements()
    
    # 创建配置文件
    create_env_file()
    
    # 创建目录
    create_directories()
    
    # 创建.gitignore
    create_gitignore()
    
    # 打印下一步操作
    print_next_steps()

if __name__ == "__main__":
    main() 