#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试B站Cookie认证
"""

import asyncio
import sys
import os
import logging

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

async def test_authentication():
    """测试认证状态"""
    crawler = BilibiliCrawler()
    
    try:
        await crawler.init_session()
        
        # 测试1: 检查登录状态 - 获取个人空间信息
        logger.info("=== 测试1: 检查登录状态 ===")
        url = "https://api.bilibili.com/x/space/myinfo"
        result = await crawler._make_request(url)
        
        if result and result.get('code') == 0:
            data = result.get('data', {})
            logger.info(f"✅ 登录成功！用户: {data.get('name', 'Unknown')}")
            logger.info(f"   用户ID: {data.get('mid', 'Unknown')}")
            logger.info(f"   粉丝数: {data.get('follower', 'Unknown')}")
            logger.info(f"   关注数: {data.get('following', 'Unknown')}")
        else:
            logger.error(f"❌ 登录失败！响应: {result}")
            return False
        
        # 测试2: 获取关注列表（需要登录）
        logger.info("\n=== 测试2: 获取关注列表 ===")
        url = "https://api.bilibili.com/x/relation/followings"
        params = {'vmid': data.get('mid'), 'ps': 5}
        result = await crawler._make_request(url, params)
        
        if result and result.get('code') == 0:
            followings = result.get('data', {}).get('list', [])
            logger.info(f"✅ 成功获取关注列表，共 {len(followings)} 人")
            for following in followings[:3]:  # 显示前3个
                logger.info(f"   - {following.get('uname', 'Unknown')}")
        else:
            logger.warning(f"⚠️  获取关注列表失败: {result}")
        
        # 测试3: 获取历史记录（需要登录）
        logger.info("\n=== 测试3: 获取观看历史 ===")
        url = "https://api.bilibili.com/x/web-interface/history/cursor"
        params = {'ps': 5}
        result = await crawler._make_request(url, params)
        
        if result and result.get('code') == 0:
            history = result.get('data', {}).get('list', [])
            logger.info(f"✅ 成功获取观看历史，共 {len(history)} 条")
            for item in history[:3]:  # 显示前3条
                logger.info(f"   - {item.get('title', 'Unknown')}")
        else:
            logger.warning(f"⚠️  获取观看历史失败: {result}")
        
        # 测试4: 测试需要高权限的接口
        logger.info("\n=== 测试4: 测试收藏夹列表 ===")
        url = "https://api.bilibili.com/x/v3/fav/folder/created/list-all"
        params = {'up_mid': data.get('mid')}
        result = await crawler._make_request(url, params)
        
        if result and result.get('code') == 0:
            folders = result.get('data', {}).get('list', [])
            logger.info(f"✅ 成功获取收藏夹列表，共 {len(folders)} 个")
            for folder in folders[:3]:  # 显示前3个
                logger.info(f"   - {folder.get('title', 'Unknown')} ({folder.get('media_count', 0)}个视频)")
        else:
            logger.warning(f"⚠️  获取收藏夹列表失败: {result}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试过程中发生错误: {e}")
        return False
    finally:
        await crawler.close_session()

async def test_public_api():
    """测试不需要登录的公开API"""
    crawler = BilibiliCrawler()
    
    try:
        await crawler.init_session()
        
        logger.info("\n=== 测试公开API: 获取热门视频 ===")
        videos = await crawler.get_trending_videos(limit=5)
        
        if videos:
            logger.info(f"✅ 成功获取 {len(videos)} 个热门视频:")
            for i, video in enumerate(videos[:3], 1):
                logger.info(f"   {i}. {video.get('title', 'Unknown')}")
                logger.info(f"      作者: {video.get('owner', 'Unknown')}")
                logger.info(f"      BVID: {video.get('bvid', 'Unknown')}")
        else:
            logger.error("❌ 获取热门视频失败")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试公开API时发生错误: {e}")
        return False
    finally:
        await crawler.close_session()

async def main():
    """主测试函数"""
    logger.info("🚀 开始测试B站Cookie认证...")
    
    # 测试公开API
    public_success = await test_public_api()
    
    # 测试认证API
    auth_success = await test_authentication()
    
    logger.info("\n" + "="*50)
    logger.info("📊 测试结果总结:")
    logger.info(f"   公开API: {'✅ 正常' if public_success else '❌ 失败'}")
    logger.info(f"   认证API: {'✅ 正常' if auth_success else '❌ 失败'}")
    
    if auth_success:
        logger.info("🎉 Cookie认证配置成功！可以使用需要登录的功能了。")
    else:
        logger.error("😞 Cookie认证失败，请检查SESSDATA是否有效。")
    
    return auth_success

if __name__ == "__main__":
    asyncio.run(main()) 