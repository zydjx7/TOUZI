#!/usr/bin/env python3
"""
测试特定UP主 - 战国时代_姜汁汽水
验证能否正确提取视频文本内容
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
import hashlib

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.crawler import BilibiliCrawler
from src.core.database import DatabaseManager, VideoContent, DynamicContent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_specific_up():
    """测试特定UP主的数据获取"""
    
    # 目标UP主信息
    test_uid = "1039025435"
    up_name = "战国时代_姜汁汽水"
    
    crawler = BilibiliCrawler()
    db_manager = DatabaseManager("data/test_specific_up.db")
    
    await crawler.init_session()
    
    try:
        print(f"\n{'='*60}")
        print(f"🎯 测试UP主: {up_name} (UID: {test_uid})")
        print(f"{'='*60}\n")
        
        # 1. 获取最新视频列表
        print("📹 获取最新视频...")
        videos = await crawler.get_user_videos(test_uid, page_size=5)
        
        if not videos:
            print("❌ 未能获取到视频列表")
            return
            
        print(f"✅ 成功获取 {len(videos)} 个视频")
        
        # 2. 测试前3个视频的文本提取
        for i, video in enumerate(videos[:3]):
            print(f"\n{'='*50}")
            print(f"📌 处理第 {i+1} 个视频")
            print(f"标题: {video.get('title', 'Unknown')}")
            print(f"BV号: {video.get('bvid', 'Unknown')}")
            
            await asyncio.sleep(2)  # 避免请求过快
            
            # 获取视频详情
            video_info = await crawler.get_video_info(video['bvid'])
            if not video_info:
                print("❌ 无法获取视频详情")
                continue
            
            print(f"播放量: {video_info['stat']['view']:,}")
            print(f"发布时间: {datetime.fromtimestamp(video_info['pubdate']).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 获取视频文本（字幕或描述）
            print("\n📝 提取视频文本...")
            transcript = await crawler.get_video_transcript(video['bvid'])
            
            if transcript:
                print(f"✅ 成功提取文本")
                print(f"文本长度: {len(transcript)} 字符")
                print(f"文本预览: {transcript[:200]}...")
                
                # 判断是字幕还是描述
                if len(transcript) > len(video_info.get('desc', '')):
                    print("📌 来源: 视频字幕")
                else:
                    print("📌 来源: 视频描述")
            else:
                print("⚠️  未能提取到文本内容")
            
            # 保存到数据库
            try:
                content_hash = hashlib.md5(
                    (video_info['title'] + video_info['desc']).encode()
                ).hexdigest()
                
                video_content = VideoContent(
                    bvid=video['bvid'],
                    title=video_info['title'],
                    description=video_info['desc'],
                    transcript=transcript or video_info['desc'],  # 如果没有字幕，使用描述
                    publish_time=datetime.fromtimestamp(video_info['pubdate']),
                    up_name=up_name,
                    view_count=video_info['stat']['view'],
                    like_count=video_info['stat']['like'],
                    coin_count=video_info['stat']['coin'],
                    share_count=video_info['stat']['share'],
                    tags=[tag['tag_name'] for tag in video_info.get('tags', [])],
                    content_hash=content_hash
                )
                
                db_manager.save_video(video_content)
                print("✅ 已保存到数据库")
                
            except Exception as e:
                print(f"❌ 保存失败: {e}")
            
            await asyncio.sleep(1)
        
        # 3. 获取最新动态
        print(f"\n{'='*50}")
        print("💬 获取最新动态...")
        dynamics = await crawler.get_user_dynamics(test_uid)
        
        if dynamics:
            print(f"✅ 成功获取 {len(dynamics)} 条动态")
            
            # 显示前3条动态
            for i, dynamic in enumerate(dynamics[:3]):
                print(f"\n动态 {i+1}:")
                print(f"内容: {dynamic['content'][:100]}...")
                print(f"点赞: {dynamic['like_count']}")
                
                # 保存动态
                try:
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
                    
                    db_manager.save_dynamic(dynamic_content)
                    print("✅ 动态已保存")
                    
                except Exception as e:
                    print(f"❌ 保存动态失败: {e}")
        else:
            print("❌ 未能获取动态")
        
        # 4. 显示统计信息
        print(f"\n{'='*60}")
        print("📊 数据统计")
        print(f"{'='*60}")
        
        stats = db_manager.get_statistics()
        print(f"总视频数: {stats.get('total_videos', 0)}")
        print(f"总动态数: {stats.get('total_dynamics', 0)}")
        
        # 5. 验证数据库中的数据
        print(f"\n📄 数据库中的视频内容示例：")
        saved_videos = db_manager.get_latest_content('video', up_name=up_name)
        if saved_videos:
            for video in saved_videos[:2]:
                print(f"\n标题: {video['title']}")
                print(f"文本内容: {video['transcript'][:150]}...")
        
    except Exception as e:
        logger.error(f"测试过程出错: {e}")
    
    finally:
        await crawler.close_session()
        print(f"\n{'='*60}")
        print("✅ 测试完成！")
        print(f"数据已保存到: data/test_specific_up.db")
        print(f"{'='*60}")

if __name__ == "__main__":
    # 确保数据目录存在
    Path("data").mkdir(exist_ok=True)
    
    # 运行测试
    asyncio.run(test_specific_up())
