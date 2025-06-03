#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试B站UP主信息获取
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
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def quick_test_up_info(uid: str, up_name: str):
    """快速测试UP主基本信息"""
    crawler = BilibiliCrawler()
    
    try:
        await crawler.init_session()
        
        logger.info(f"🎯 测试UP主: {up_name} (UID: {uid})")
        
        # 只测试基本信息接口
        url = "https://api.bilibili.com/x/space/acc/info"
        params = {'mid': uid}
        
        logger.info("📋 获取UP主基本信息...")
        result = await crawler._make_request(url, params)
        
        if result and result.get('code') == 0:
            data = result.get('data', {})
            logger.info("✅ 成功！UP主信息:")
            logger.info(f"   用户名: {data.get('name', 'Unknown')}")
            logger.info(f"   UID: {data.get('mid', 'Unknown')}")
            logger.info(f"   粉丝数: {data.get('follower', 0):,}")
            logger.info(f"   关注数: {data.get('following', 0):,}")
            logger.info(f"   等级: {data.get('level', 'Unknown')}")
            logger.info(f"   签名: {data.get('sign', 'Unknown')}")
            
            return True
        else:
            error_msg = result.get('message', 'Unknown error') if result else 'No response'
            logger.error(f"❌ 失败: {error_msg}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 错误: {e}")
        return False
    finally:
        await crawler.close_session()

async def main():
    """主函数"""
    logger.info("🚀 快速测试开始...")
    
    # 测试指定的UP主
    uid = "1039025435"
    up_name = "战国时代_姜汁汽水"
    
    success = await quick_test_up_info(uid, up_name)
    
    logger.info("="*50)
    if success:
        logger.info("🎉 测试成功！爬虫可以获取UP主基本信息")
        logger.info("💡 接下来可以尝试:")
        logger.info("   1. 获取视频列表")
        logger.info("   2. 获取用户动态")
        logger.info("   3. 搜索相关视频")
    else:
        logger.info("😞 测试失败，可能需要:")
        logger.info("   1. 等待更长时间（避免频率限制）")
        logger.info("   2. 检查网络连接")
        logger.info("   3. 验证Cookie是否有效")

if __name__ == "__main__":
    asyncio.run(main()) 