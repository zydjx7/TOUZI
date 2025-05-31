"""
Flask Web应用
Web Application Module
"""

from flask import Flask, render_template, jsonify
import logging
from config import config

logger = logging.getLogger(__name__)

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.update(config.WEB_CONFIG)
    
    # 注册蓝图
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def dashboard():
        """仪表板首页"""
        # TODO: 实现仪表板数据获取
        data = {
            'stats': {},
            'sentiment': {},
            'signals': [],
            'hot_topics': [],
            'latest_news': [],
            'chart_labels': [],
            'chart_data': [],
            'last_update': '刚刚'
        }
        return render_template('dashboard.html', **data)
    
    @app.route('/analysis')
    def analysis():
        """分析页面"""
        # TODO: 实现分析页面
        return render_template('analysis.html')
    
    @app.route('/reports')
    def reports():
        """报告页面"""
        # TODO: 实现报告页面
        return render_template('reports.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 