#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的B站UP主测试
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

async def test_alternative_approach(uid: str, up_name: str):
    """使用替代方法测试UP主信息获取"""
    crawler = BilibiliCrawler()
    
    try:
        await crawler.init_session()
        logger.info(f"🎯 开始测试UP主: {up_name} (UID: {uid})")
        
        # 方法1: 尝试获取UP主基本信息
        logger.info("📋 尝试获取UP主基本信息...")
        url = "https://api.bilibili.com/x/space/acc/info"
        params = {'mid': uid}
        
        # 等待足够的时间
        await asyncio.sleep(10)
        result = await crawler._make_request(url, params)
        
        if result and result.get('code') == 0:
            data = result.get('data', {})
            logger.info("✅ 成功获取UP主信息:")
            logger.info(f"   用户名: {data.get('name', 'Unknown')}")
            logger.info(f"   粉丝数: {data.get('follower', 0):,}")
            logger.info(f"   关注数: {data.get('following', 0):,}")
            logger.info(f"   签名: {data.get('sign', 'Unknown')}")
            
            # 方法2: 尝试使用搜索API来获取视频
            logger.info("\n🔍 尝试搜索该UP主的视频...")
            await asyncio.sleep(10)  # 等待更长时间
            
            search_query = data.get('name', up_name)
            videos = await crawler.search_videos(search_query, page_size=10)
            
            if videos:
                logger.info(f"✅ 通过搜索找到 {len(videos)} 个相关视频:")
                for i, video in enumerate(videos[:3], 1):
                    title = video.get('title', 'Unknown')
                    author = video.get('author', 'Unknown')
                    bvid = video.get('bvid', 'Unknown')
                    logger.info(f"   {i}. {title}")
                    logger.info(f"      作者: {author} | BVID: {bvid}")
            else:
                logger.warning("⚠️  未找到相关视频")
            
            # 方法3: 尝试获取用户动态
            logger.info("\n📱 尝试获取用户动态...")
            await asyncio.sleep(10)
            
            dynamics = await crawler.get_user_dynamics(uid)
            
            if dynamics:
                logger.info(f"✅ 成功获取 {len(dynamics)} 条动态:")
                for i, dynamic in enumerate(dynamics[:3], 1):
                    content = dynamic.get('content', '')[:50]
                    timestamp = dynamic.get('timestamp', 0)
                    try:
                        time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                    except:
                        time_str = "未知时间"
                    logger.info(f"   {i}. {content}... ({time_str})")
            else:
                logger.warning("⚠️  未能获取到用户动态")
                
            return True
            
        else:
            logger.error(f"❌ 获取UP主信息失败: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试过程中发生错误: {e}")
        return False
    finally:
        await crawler.close_session()

async def test_public_data_only():
    """只测试公开数据，不涉及具体UP主"""
    crawler = BilibiliCrawler()
    
    try:
        await crawler.init_session()
        
        logger.info("🌟 测试获取热门视频...")
        videos = await crawler.get_trending_videos(limit=5)
        
        if videos:
            logger.info(f"✅ 成功获取 {len(videos)} 个热门视频")
            
            # 测试获取其中一个视频的详细信息
            first_video = videos[0]
            bvid = first_video.get('bvid', '')
            
            if bvid:
                logger.info(f"\n🔍 测试获取视频详情: {first_video.get('title', 'Unknown')}")
                await asyncio.sleep(8)  # 稍等
                
                video_info = await crawler.get_video_info(bvid)
                
                if video_info:
                    logger.info("✅ 成功获取视频详情:")
                    logger.info(f"   UP主: {video_info.get('owner', {}).get('name', 'Unknown')}")
                    logger.info(f"   UP主UID: {video_info.get('owner', {}).get('mid', 'Unknown')}")
                    logger.info(f"   播放量: {video_info.get('stat', {}).get('view', 0):,}")
                    logger.info(f"   点赞数: {video_info.get('stat', {}).get('like', 0):,}")
                    
                    return video_info.get('owner', {}).get('mid', None)
        
        return None
        
    except Exception as e:
        logger.error(f"❌ 测试公开数据时发生错误: {e}")
        return None
    finally:
        await crawler.close_session()

async def main():
    """主函数"""
    logger.info("🚀 开始简单测试...")
    
    # 先测试公开数据
    logger.info("="*60)
    logger.info("第一步: 测试公开数据获取")
    sample_uid = await test_public_data_only()
    
    # 等待更长时间再进行下一步测试
    logger.info("\n⏳ 等待60秒以避免频率限制...")
    await asyncio.sleep(60)
    
    # 测试指定UP主
    logger.info("\n" + "="*60)
    logger.info("第二步: 测试指定UP主信息获取")
    
    uid = "1039025435"
    up_name = "战国时代_姜汁汽水"
    
    success = await test_alternative_approach(uid, up_name)
    
    logger.info("\n" + "="*60)
    logger.info("📊 测试总结:")
    logger.info(f"   指定UP主测试: {'✅ 成功' if success else '❌ 失败'}")
    
    if not success:
        logger.info("\n💡 建议:")
        logger.info("   1. 等待更长时间再重试（B站有严格的频率限制）")
        logger.info("   2. 考虑使用不同的网络环境")
        logger.info("   3. 检查Cookie是否仍然有效")
        
        if sample_uid:
            logger.info(f"   4. 可以先测试从热门视频中找到的UP主: {sample_uid}")

if __name__ == "__main__":
    asyncio.run(main()) 