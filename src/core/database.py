"""
数据库管理模块
包含数据结构定义和数据库操作类
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class VideoContent:
    """视频内容数据结构"""
    bvid: str
    title: str
    description: str
    transcript: str  # 视频转文字内容
    publish_time: datetime
    up_name: str
    view_count: int
    like_count: int
    coin_count: int
    share_count: int
    tags: List[str]
    content_hash: str
    
@dataclass
class DynamicContent:
    """动态内容数据结构"""
    dynamic_id: str
    content: str
    publish_time: datetime
    up_name: str
    like_count: int
    forward_count: int
    comment_count: int
    content_hash: str

@dataclass
class CommentContent:
    """评论内容数据结构"""
    comment_id: str
    content: str
    author: str
    like_count: int
    publish_time: datetime
    parent_id: str  # 视频或动态ID
    parent_type: str  # 'video' or 'dynamic'

@dataclass
class NewsContent:
    """新闻内容数据结构"""
    title: str
    content: str
    source: str
    publish_time: datetime
    url: str
    category: str  # 财经、地缘等
    content_hash: str

@dataclass
class AnalysisResult:
    """分析结果数据结构"""
    content_id: str
    content_type: str
    sentiment_score: float  # 情感分数 -1到1
    key_points: List[str]  # 关键观点
    investment_signals: List[Dict]  # 投资信号
    risk_level: str  # 风险等级
    confidence: float  # 置信度
    analysis_time: datetime

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "data/financial_analysis.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建视频表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                bvid TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                transcript TEXT,
                publish_time TIMESTAMP,
                up_name TEXT,
                view_count INTEGER,
                like_count INTEGER,
                coin_count INTEGER,
                share_count INTEGER,
                tags TEXT,
                content_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建动态表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dynamics (
                dynamic_id TEXT PRIMARY KEY,
                content TEXT,
                publish_time TIMESTAMP,
                up_name TEXT,
                like_count INTEGER,
                forward_count INTEGER,
                comment_count INTEGER,
                content_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建评论表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                comment_id TEXT PRIMARY KEY,
                content TEXT,
                author TEXT,
                like_count INTEGER,
                publish_time TIMESTAMP,
                parent_id TEXT,
                parent_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建新闻表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                source TEXT,
                publish_time TIMESTAMP,
                url TEXT UNIQUE,
                category TEXT,
                content_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建分析结果表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT,
                content_type TEXT,
                sentiment_score REAL,
                key_points TEXT,
                investment_signals TEXT,
                risk_level TEXT,
                confidence REAL,
                analysis_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("数据库初始化完成")
    
    def save_video(self, video: VideoContent):
        """保存视频数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO videos 
                (bvid, title, description, transcript, publish_time, up_name,
                 view_count, like_count, coin_count, share_count, tags, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video.bvid, video.title, video.description, video.transcript,
                video.publish_time, video.up_name, video.view_count,
                video.like_count, video.coin_count, video.share_count,
                json.dumps(video.tags, ensure_ascii=False), video.content_hash
            ))
            conn.commit()
            logger.info(f"保存视频数据: {video.bvid}")
        except Exception as e:
            logger.error(f"保存视频数据失败: {e}")
        finally:
            conn.close()
    
    def save_dynamic(self, dynamic: DynamicContent):
        """保存动态数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO dynamics 
                (dynamic_id, content, publish_time, up_name, like_count,
                 forward_count, comment_count, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dynamic.dynamic_id, dynamic.content, dynamic.publish_time,
                dynamic.up_name, dynamic.like_count, dynamic.forward_count,
                dynamic.comment_count, dynamic.content_hash
            ))
            conn.commit()
            logger.info(f"保存动态数据: {dynamic.dynamic_id}")
        except Exception as e:
            logger.error(f"保存动态数据失败: {e}")
        finally:
            conn.close()

    def save_comment(self, comment: CommentContent):
        """保存评论数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO comments 
                (comment_id, content, author, like_count, publish_time,
                 parent_id, parent_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                comment.comment_id, comment.content, comment.author,
                comment.like_count, comment.publish_time, comment.parent_id,
                comment.parent_type
            ))
            conn.commit()
            logger.info(f"保存评论数据: {comment.comment_id}")
        except Exception as e:
            logger.error(f"保存评论数据失败: {e}")
        finally:
            conn.close()

    def save_news(self, news: NewsContent):
        """保存新闻数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO news 
                (title, content, source, publish_time, url, category, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                news.title, news.content, news.source, news.publish_time,
                news.url, news.category, news.content_hash
            ))
            conn.commit()
            logger.info(f"保存新闻数据: {news.title}")
        except Exception as e:
            logger.error(f"保存新闻数据失败: {e}")
        finally:
            conn.close()

    def save_analysis_result(self, result: AnalysisResult):
        """保存分析结果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO analysis_results 
                (content_id, content_type, sentiment_score, key_points,
                 investment_signals, risk_level, confidence, analysis_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result.content_id, result.content_type, result.sentiment_score,
                json.dumps(result.key_points, ensure_ascii=False),
                json.dumps(result.investment_signals, ensure_ascii=False),
                result.risk_level, result.confidence, result.analysis_time
            ))
            conn.commit()
            logger.info(f"保存分析结果: {result.content_id}")
        except Exception as e:
            logger.error(f"保存分析结果失败: {e}")
        finally:
            conn.close()
    
    def get_latest_content(self, content_type: str, up_name: str = None, days: int = 30) -> List[Dict]:
        """获取最近的内容"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            if content_type == 'video':
                if up_name:
                    cursor.execute('''
                        SELECT * FROM videos 
                        WHERE up_name = ? AND publish_time >= ?
                        ORDER BY publish_time DESC
                    ''', (up_name, since_date))
                else:
                    cursor.execute('''
                        SELECT * FROM videos 
                        WHERE publish_time >= ?
                        ORDER BY publish_time DESC
                    ''', (since_date,))
            elif content_type == 'dynamic':
                if up_name:
                    cursor.execute('''
                        SELECT * FROM dynamics 
                        WHERE up_name = ? AND publish_time >= ?
                        ORDER BY publish_time DESC
                    ''', (up_name, since_date))
                else:
                    cursor.execute('''
                        SELECT * FROM dynamics 
                        WHERE publish_time >= ?
                        ORDER BY publish_time DESC
                    ''', (since_date,))
            elif content_type == 'news':
                cursor.execute('''
                    SELECT * FROM news 
                    WHERE publish_time >= ?
                    ORDER BY publish_time DESC
                ''', (since_date,))
            
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in results]
            
        except Exception as e:
            logger.error(f"获取最近内容失败: {e}")
            return []
        finally:
            conn.close()

    def get_analysis_results(self, content_type: str = None, days: int = 30) -> List[Dict]:
        """获取分析结果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            if content_type:
                cursor.execute('''
                    SELECT * FROM analysis_results 
                    WHERE content_type = ? AND analysis_time >= ?
                    ORDER BY analysis_time DESC
                ''', (content_type, since_date))
            else:
                cursor.execute('''
                    SELECT * FROM analysis_results 
                    WHERE analysis_time >= ?
                    ORDER BY analysis_time DESC
                ''', (since_date,))
            
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in results]
            
        except Exception as e:
            logger.error(f"获取分析结果失败: {e}")
            return []
        finally:
            conn.close()

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        try:
            # 视频统计
            cursor.execute("SELECT COUNT(*) FROM videos")
            stats['total_videos'] = cursor.fetchone()[0]
            
            # 动态统计
            cursor.execute("SELECT COUNT(*) FROM dynamics")
            stats['total_dynamics'] = cursor.fetchone()[0]
            
            # 新闻统计
            cursor.execute("SELECT COUNT(*) FROM news")
            stats['total_news'] = cursor.fetchone()[0]
            
            # 分析结果统计
            cursor.execute("SELECT COUNT(*) FROM analysis_results")
            stats['total_analysis'] = cursor.fetchone()[0]
            
            # 今日新增统计
            today = datetime.now().date().isoformat()
            cursor.execute("SELECT COUNT(*) FROM videos WHERE DATE(created_at) = ?", (today,))
            stats['today_videos'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM dynamics WHERE DATE(created_at) = ?", (today,))
            stats['today_dynamics'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM news WHERE DATE(created_at) = ?", (today,))
            stats['today_news'] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {}
        finally:
            conn.close() 