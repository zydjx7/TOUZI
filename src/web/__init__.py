"""
Web界面模块
包含Flask应用、API接口和前端模板
"""

from .app import create_app
from .api import api_bp

__all__ = ['create_app', 'api_bp'] 