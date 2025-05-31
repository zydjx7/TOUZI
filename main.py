#!/usr/bin/env python3
"""
财经智能分析系统 - 主程序入口
Financial Intelligence Analysis System - Main Entry Point
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from src.core.database import DatabaseManager
from src.core.analyzer import ContentAnalyzer
from src.core.crawler import BilibiliCrawler
from src.core.news_aggregator import NewsAggregator
from src.core.report_generator import ReportGenerator
from src.utils.email_notifier import EmailNotifier

# 配置日志
def setup_logging():
    """配置日志系统"""
    log_config = config.LOG_CONFIG
    
    # 确保日志目录存在
    Path(log_config['file']).parent.mkdir(parents=True, exist_ok=True)
    
    # 配置日志格式
    logging.basicConfig(
        level=getattr(logging, log_config['level']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_config['file'], encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成")
    return logger

class FinancialAnalysisSystem:
    """财经智能分析系统主类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # 初始化组件
        self.db_manager = DatabaseManager(config.DATABASE_PATH)
        self.crawler = BilibiliCrawler()
        self.analyzer = ContentAnalyzer()
        self.news_aggregator = NewsAggregator()
        self.report_generator = ReportGenerator(self.db_manager)
        self.email_notifier = EmailNotifier(
            **config.EMAIL_CONFIG
        ) if config.EMAIL_CONFIG['email'] else None
        
        self.logger.info("财经智能分析系统初始化完成")
    
    async def start(self):
        """启动系统"""
        self.logger.info("🚀 启动财经智能分析系统...")
        self.running = True
        
        # 初始化爬虫会话
        await self.crawler.init_session()
        
        try:
            # 启动主循环
            await self.main_loop()
        except asyncio.CancelledError:
            self.logger.info("系统收到停止信号")
        except Exception as e:
            self.logger.error(f"系统运行出错: {e}")
            raise
        finally:
            await self.cleanup()
    
    async def main_loop(self):
        """主要业务循环"""
        self.logger.info("开始主要业务循环")
        
        while self.running:
            try:
                # 执行一轮分析
                await self.run_analysis_cycle()
                
                # 等待下一轮
                await asyncio.sleep(300)  # 5分钟间隔
                
            except Exception as e:
                self.logger.error(f"分析循环出错: {e}")
                await asyncio.sleep(60)  # 出错后等待1分钟再重试
    
    async def run_analysis_cycle(self):
        """执行一轮完整的分析周期"""
        self.logger.info("开始新的分析周期")
        
        # 1. 爬取UP主内容
        for up_info in config.UP_LIST:
            if not self.running:
                break
                
            try:
                await self.crawl_up_content(up_info['uid'], up_info['name'])
            except Exception as e:
                self.logger.error(f"爬取UP主 {up_info['name']} 内容失败: {e}")
        
        # 2. 爬取新闻
        try:
            await self.crawl_news()
        except Exception as e:
            self.logger.error(f"爬取新闻失败: {e}")
        
        # 3. 分析内容
        try:
            await self.analyze_content()
        except Exception as e:
            self.logger.error(f"分析内容失败: {e}")
        
        # 4. 生成报告（每小时一次）
        import time
        if int(time.time()) % 3600 < 300:  # 每小时的前5分钟
            try:
                await self.generate_and_send_report()
            except Exception as e:
                self.logger.error(f"生成报告失败: {e}")
        
        self.logger.info("分析周期完成")
    
    async def crawl_up_content(self, uid: str, up_name: str):
        """爬取UP主内容"""
        self.logger.info(f"开始爬取UP主内容: {up_name}")
        
        # 获取视频列表
        videos = await self.crawler.get_user_videos(uid)
        
        for video in videos[:10]:  # 只处理最新的10个视频
            try:
                # 获取详细信息
                video_info = await self.crawler.get_video_info(video['bvid'])
                if not video_info:
                    continue
                
                # 获取转录文本
                transcript = await self.crawler.get_video_transcript(video['bvid'])
                
                # 保存到数据库
                from src.core.database import VideoContent
                import hashlib
                from datetime import datetime
                
                content_hash = hashlib.md5(
                    (video_info['title'] + video_info['desc']).encode()
                ).hexdigest()
                
                video_content = VideoContent(
                    bvid=video['bvid'],
                    title=video_info['title'],
                    description=video_info['desc'],
                    transcript=transcript,
                    publish_time=datetime.fromtimestamp(video_info['pubdate']),
                    up_name=up_name,
                    view_count=video_info['stat']['view'],
                    like_count=video_info['stat']['like'],
                    coin_count=video_info['stat']['coin'],
                    share_count=video_info['stat']['share'],
                    tags=[tag['tag_name'] for tag in video_info.get('tags', [])],
                    content_hash=content_hash
                )
                
                self.db_manager.save_video(video_content)
                
                # 添加延迟避免过于频繁的请求
                await asyncio.sleep(config.CRAWLER_CONFIG['rate_limit_delay'])
                
            except Exception as e:
                self.logger.error(f"处理视频 {video.get('bvid', 'unknown')} 失败: {e}")
        
        # 获取动态
        dynamics = await self.crawler.get_user_dynamics(uid)
        
        for dynamic in dynamics[:20]:  # 只处理最新的20条动态
            try:
                from src.core.database import DynamicContent
                
                content_hash = hashlib.md5(
                    dynamic['content'].encode()
                ).hexdigest()
                
                dynamic_content = DynamicContent(
                    dynamic_id=str(dynamic['id']),
                    content=dynamic['content'],
                    publish_time=datetime.fromtimestamp(dynamic['timestamp']),
                    up_name=up_name,
                    like_count=dynamic.get('like_count', 0),
                    forward_count=dynamic.get('forward_count', 0),
                    comment_count=dynamic.get('comment_count', 0),
                    content_hash=content_hash
                )
                
                self.db_manager.save_dynamic(dynamic_content)
                
            except Exception as e:
                self.logger.error(f"处理动态失败: {e}")
    
    async def crawl_news(self):
        """爬取新闻"""
        self.logger.info("开始爬取新闻")
        
        for category in ['financial', 'geopolitical']:
            try:
                news_list = await self.news_aggregator.fetch_latest_news(category)
                
                for news in news_list:
                    self.db_manager.save_news(news)
                    
            except Exception as e:
                self.logger.error(f"爬取 {category} 新闻失败: {e}")
    
    async def analyze_content(self):
        """分析内容"""
        self.logger.info("开始分析内容")
        
        # 获取最近的未分析内容
        recent_videos = self.db_manager.get_latest_content('video', days=1)
        recent_dynamics = self.db_manager.get_latest_content('dynamic', days=1)
        recent_news = self.db_manager.get_latest_content('news', days=1)
        
        # 分析视频
        for video in recent_videos[:50]:  # 限制处理数量
            await self.analyze_single_content(
                video['bvid'], 'video', 
                f"{video['title']} {video['description']} {video['transcript']}"
            )
        
        # 分析动态
        for dynamic in recent_dynamics[:100]:
            await self.analyze_single_content(
                dynamic['dynamic_id'], 'dynamic', dynamic['content']
            )
        
        # 分析新闻
        for news in recent_news[:50]:
            await self.analyze_single_content(
                str(news['id']), 'news', 
                f"{news['title']} {news['content']}"
            )
    
    async def analyze_single_content(self, content_id: str, content_type: str, text: str):
        """分析单个内容"""
        try:
            # 情感分析
            sentiment_score = self.analyzer.analyze_sentiment(text)
            
            # 提取关键点
            key_points = self.analyzer.extract_key_points(text)
            
            # 检测投资信号
            investment_signals = self.analyzer.detect_investment_signals(text)
            
            # 评估风险等级
            risk_level = self.analyzer.assess_risk_level(sentiment_score, investment_signals)
            
            # 计算置信度
            confidence = self.analyzer.calculate_confidence(text, investment_signals)
            
            # 保存分析结果
            from src.core.database import AnalysisResult
            from datetime import datetime
            
            result = AnalysisResult(
                content_id=content_id,
                content_type=content_type,
                sentiment_score=sentiment_score,
                key_points=key_points,
                investment_signals=investment_signals,
                risk_level=risk_level,
                confidence=confidence,
                analysis_time=datetime.now()
            )
            
            self.db_manager.save_analysis_result(result)
            
        except Exception as e:
            self.logger.error(f"分析内容 {content_id} 失败: {e}")
    
    async def generate_and_send_report(self):
        """生成并发送报告"""
        self.logger.info("开始生成报告")
        
        try:
            # 生成报告
            report_content = self.report_generator.generate_daily_report()
            
            # 发送邮件
            if self.email_notifier and config.RECIPIENT_EMAIL:
                from datetime import date
                subject = f"财经智能分析日报 - {date.today()}"
                self.email_notifier.send_report(
                    config.RECIPIENT_EMAIL, subject, report_content
                )
                self.logger.info("报告发送完成")
            else:
                self.logger.warning("邮件配置不完整，跳过发送")
                
        except Exception as e:
            self.logger.error(f"生成或发送报告失败: {e}")
    
    async def cleanup(self):
        """清理资源"""
        self.logger.info("开始清理资源...")
        
        try:
            await self.crawler.close_session()
            self.logger.info("清理完成")
        except Exception as e:
            self.logger.error(f"清理资源时出错: {e}")
    
    def stop(self):
        """停止系统"""
        self.logger.info("收到停止信号")
        self.running = False

# 全局系统实例
system = None

def signal_handler(signum, frame):
    """信号处理器"""
    if system:
        system.stop()

async def main():
    """主函数"""
    global system
    
    # 设置日志
    logger = setup_logging()
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # 创建并启动系统
        system = FinancialAnalysisSystem()
        await system.start()
        
    except KeyboardInterrupt:
        logger.info("收到键盘中断信号")
    except Exception as e:
        logger.error(f"系统运行失败: {e}")
        return 1
    
    logger.info("系统已停止")
    return 0

if __name__ == "__main__":
    # 运行主程序
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 