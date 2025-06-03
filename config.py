"""
系统配置文件
Financial Intelligence Analysis System Configuration
"""

import os
from typing import Dict, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """系统配置类"""
    
    # 数据库配置
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/financial_analysis.db")
    
    # B站UP主列表 - 请替换为实际的UID和名称
    UP_LIST = [
        {"uid": "1039025435", "name": "战国时代_姜汁汽水"},
        {"uid": "37663924", "name": "巫师财经"},  # 示例UID，请替换
        {"uid": "456664753", "name": "温义飞的频道"},  # 示例UID，请替换
        {"uid": "1266132762", "name": "老蛮数据透析站"},  # 示例UID，请替换
        # 添加更多UP主
    ]
    
    # 邮件配置
    EMAIL_CONFIG = {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "email": os.getenv("SENDER_EMAIL", ""),
        "password": os.getenv("EMAIL_PASSWORD", ""),  # 使用应用密码
    }
    
    # 收件人邮箱
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")
    
    # 新闻源配置
    NEWS_SOURCES = {
        "financial": [
            "https://finance.sina.com.cn/",
            "https://www.jiemian.com/",
            "https://wallstreetcn.com/",
            "https://www.yicai.com/",
        ],
        "geopolitical": [
            "https://world.huanqiu.com/",
            "https://news.sina.com.cn/world/",
        ]
    }
    
    # API配置
    API_KEYS = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),  # 用于更高级的文本分析
        "whisper_api_key": os.getenv("WHISPER_API_KEY", ""),  # 用于视频转文字
    }
    
    # 分析参数
    ANALYSIS_CONFIG = {
        "sentiment_threshold": 0.3,  # 情感分析阈值
        "confidence_threshold": 0.6,  # 置信度阈值
        "max_daily_videos": 100,  # 每日最大分析视频数
        "lookback_days": 7,  # 历史数据回看天数
    }
    
    # 爬虫配置
    CRAWLER_CONFIG = {
        "rate_limit_delay": 5,  # 请求间隔（秒）- 增加到5秒避免频率限制
        "max_retries": 3,  # 最大重试次数
        "timeout": 30,  # 请求超时时间
    }
    
    # Web应用配置
    WEB_CONFIG = {
        "host": os.getenv("WEB_HOST", "localhost"),
        "port": int(os.getenv("WEB_PORT", "5000")),
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "secret_key": os.getenv("SECRET_KEY", "your-secret-key-here"),
    }
    
    # 日志配置
    LOG_CONFIG = {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "file": "logs/financial_analysis.log",
        "max_bytes": 10 * 1024 * 1024,  # 10MB
        "backup_count": 5,
    }

# 导出配置实例
config = Config() 