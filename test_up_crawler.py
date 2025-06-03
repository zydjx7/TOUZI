#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试B站UP主视频爬取
"""

import asyncio
import sys
import os
import logging
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.crawler import BilibiliCrawler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def test_up_videos(uid: str, up_name: str, max_videos: int = 10):
    """测试获取指定UP主的视频"""
    crawler = BilibiliCrawler()
    
    try:
        await crawler.init_session()
        
        logger.info(f"🎯 开始爬取UP主: {up_name} (UID: {uid})")
        logger.info("="*60)
        
        # 1. 获取UP主的视频列表
        logger.info(f"📺 获取UP主视频列表（最多{max_videos}个）...")
        videos = await crawler.get_user_videos(uid, page_size=max_videos)
        
        if not videos:
            logger.error(f"❌ 未能获取到UP主 {up_name} 的视频列表")
            return False
        
        logger.info(f"✅ 成功获取到 {len(videos)} 个视频")
        
        # 显示视频列表
        logger.info("\n📋 视频列表概览:")
        for i, video in enumerate(videos[:5], 1):  # 只显示前5个
            title = video.get('title', 'Unknown')
            bvid = video.get('bvid', 'Unknown')
            play_count = video.get('play', 0)
            pubdate = video.get('created', 0)
            
            # 转换时间戳
            try:
                pub_time = datetime.fromtimestamp(pubdate).strftime('%Y-%m-%d %H:%M')
            except:
                pub_time = "未知时间"
            
            logger.info(f"   {i}. {title}")
            logger.info(f"      BVID: {bvid} | 播放量: {play_count:,} | 发布: {pub_time}")
        
        if len(videos) > 5:
            logger.info(f"   ... 还有 {len(videos) - 5} 个视频")
        
        # 2. 获取第一个视频的详细信息
        if videos:
            first_video = videos[0]
            bvid = first_video.get('bvid', '')
            
            if bvid:
                logger.info(f"\n🔍 获取视频详细信息: {first_video.get('title', 'Unknown')}")
                video_info = await crawler.get_video_info(bvid)
                
                if video_info:
                    logger.info("✅ 视频详细信息:")
                    logger.info(f"   标题: {video_info.get('title', 'Unknown')}")
                    logger.info(f"   描述: {video_info.get('desc', 'Unknown')[:100]}...")
                    logger.info(f"   时长: {video_info.get('duration', 0)} 秒")
                    logger.info(f"   点赞数: {video_info.get('stat', {}).get('like', 0):,}")
                    logger.info(f"   投币数: {video_info.get('stat', {}).get('coin', 0):,}")
                    logger.info(f"   收藏数: {video_info.get('stat', {}).get('favorite', 0):,}")
                    logger.info(f"   分享数: {video_info.get('stat', {}).get('share', 0):,}")
                
                # 3. 尝试获取视频转录/字幕
                logger.info(f"\n📝 获取视频转录内容...")
                transcript = await crawler.get_video_transcript(bvid)
                
                if transcript:
                    logger.info(f"✅ 成功获取转录内容 ({len(transcript)} 字符)")
                    logger.info(f"   前200字符: {transcript[:200]}...")
                else:
                    logger.warning("⚠️  未能获取到视频转录内容")
                
                # 4. 获取视频评论
                logger.info(f"\n💬 获取视频评论（前10条）...")
                comments = await crawler.get_video_comments(bvid, limit=10)
                
                if comments:
                    logger.info(f"✅ 成功获取到 {len(comments)} 条评论")
                    for i, comment in enumerate(comments[:3], 1):
                        content = comment.get('content', '').replace('\n', ' ')[:50]
                        author = comment.get('author', 'Unknown')
                        likes = comment.get('like_count', 0)
                        logger.info(f"   {i}. {author}: {content}... (👍 {likes})")
                else:
                    logger.warning("⚠️  未能获取到视频评论")
        
        # 5. 保存数据到文件
        logger.info(f"\n💾 保存数据到文件...")
        data = {
            'up_info': {
                'uid': uid,
                'name': up_name,
                'crawl_time': datetime.now().isoformat()
            },
            'videos': videos,
            'sample_video_detail': video_info if 'video_info' in locals() else None,
            'sample_transcript': transcript if 'transcript' in locals() else None,
            'sample_comments': comments if 'comments' in locals() else None
        }
        
        filename = f"data/up_{uid}_{up_name}_videos.json"
        os.makedirs("data", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 数据已保存到: {filename}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 爬取过程中发生错误: {e}")
        return False
    finally:
        await crawler.close_session()

async def test_multiple_ups():
    """测试多个UP主的数据获取"""
    from config import config
    
    logger.info("🚀 开始批量测试UP主视频爬取...")
    
    # 从配置文件获取UP主列表
    up_list = config.UP_LIST
    
    results = {}
    
    for up in up_list[:2]:  # 只测试前2个UP主
        uid = up['uid']
        name = up['name']
        
        logger.info(f"\n{'='*60}")
        success = await test_up_videos(uid, name, max_videos=5)
        results[name] = success
        
        # 添加延迟避免请求过于频繁
        await asyncio.sleep(3)
    
    # 输出总结
    logger.info(f"\n{'='*60}")
    logger.info("📊 批量爬取结果总结:")
    for name, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        logger.info(f"   {name}: {status}")

async def main():
    """主函数"""
    print("请选择测试模式:")
    print("1. 测试单个UP主 - 战国时代_姜汁汽水")
    print("2. 测试配置文件中的多个UP主")
    
    try:
        choice = input("请输入选择 (1或2): ").strip()
        
        if choice == "1":
            # 测试指定的UP主
            uid = "1039025435"
            name = "战国时代_姜汽水"
            await test_up_videos(uid, name, max_videos=10)
            
        elif choice == "2":
            # 测试多个UP主
            await test_multiple_ups()
            
        else:
            logger.info("无效选择，默认测试战国时代_姜汁汽水")
            uid = "1039025435"
            name = "战国时代_姜汁汽水"
            await test_up_videos(uid, name, max_videos=10)
            
    except KeyboardInterrupt:
        logger.info("\n用户中断测试")
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 