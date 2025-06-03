#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的UP主数据爬取脚本
"""

import asyncio
import sys
import os
import logging
import json
from datetime import datetime
from typing import Optional, Dict, List

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.crawler import BilibiliCrawler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class UPMasterCrawler:
    """UP主数据爬取器"""
    
    def __init__(self, delay_between_requests: int = 10):
        self.crawler = BilibiliCrawler()
        self.delay = delay_between_requests
        
    async def get_up_basic_info(self, uid: str) -> Optional[Dict]:
        """获取UP主基本信息"""
        url = "https://api.bilibili.com/x/space/acc/info"
        params = {'mid': uid}
        
        logger.info(f"📋 获取UP主基本信息 (UID: {uid})...")
        result = await self.crawler._make_request(url, params)
        
        if result and result.get('code') == 0:
            return result.get('data', {})
        else:
            logger.warning(f"获取UP主基本信息失败: {result}")
            return None
    
    async def get_up_videos_by_search(self, up_name: str, max_videos: int = 20) -> List[Dict]:
        """通过搜索获取UP主视频"""
        logger.info(f"🔍 通过搜索获取UP主 '{up_name}' 的视频...")
        await asyncio.sleep(self.delay)
        
        videos = await self.crawler.search_videos(up_name, page_size=max_videos)
        
        # 过滤出该UP主的视频
        filtered_videos = []
        for video in videos:
            if up_name in video.get('author', ''):
                filtered_videos.append(video)
        
        logger.info(f"找到 {len(filtered_videos)} 个该UP主的视频")
        return filtered_videos
    
    async def get_up_dynamics(self, uid: str) -> List[Dict]:
        """获取UP主动态"""
        logger.info(f"📱 获取UP主动态 (UID: {uid})...")
        await asyncio.sleep(self.delay)
        
        dynamics = await self.crawler.get_user_dynamics(uid)
        return dynamics
    
    async def get_video_details(self, bvid: str) -> Optional[Dict]:
        """获取视频详细信息"""
        logger.info(f"🎬 获取视频详情 (BVID: {bvid})...")
        await asyncio.sleep(self.delay)
        
        return await self.crawler.get_video_info(bvid)
    
    async def crawl_up_complete_data(self, uid: str, up_name: str = None) -> Dict:
        """爬取UP主完整数据"""
        try:
            await self.crawler.init_session()
            
            logger.info(f"🎯 开始爬取UP主完整数据 (UID: {uid})")
            logger.info("="*60)
            
            # 1. 获取基本信息
            basic_info = await self.get_up_basic_info(uid)
            if not basic_info:
                logger.error("无法获取UP主基本信息，停止爬取")
                return {}
            
            actual_name = basic_info.get('name', up_name or 'Unknown')
            logger.info(f"✅ UP主: {actual_name}")
            logger.info(f"   粉丝数: {basic_info.get('follower', 0):,}")
            logger.info(f"   等级: {basic_info.get('level', 'Unknown')}")
            
            # 2. 通过搜索获取视频
            videos = await self.get_up_videos_by_search(actual_name, max_videos=15)
            
            # 3. 获取动态
            dynamics = await self.get_up_dynamics(uid)
            
            # 4. 获取第一个视频的详细信息作为示例
            sample_video_detail = None
            if videos:
                first_video = videos[0]
                bvid = first_video.get('bvid', '')
                if bvid:
                    sample_video_detail = await self.get_video_details(bvid)
            
            # 5. 整理数据
            result = {
                'crawl_info': {
                    'uid': uid,
                    'crawl_time': datetime.now().isoformat(),
                    'crawl_method': 'search_based'  # 标记使用搜索方式获取
                },
                'basic_info': basic_info,
                'videos': videos,
                'dynamics': dynamics,
                'sample_video_detail': sample_video_detail,
                'statistics': {
                    'videos_found': len(videos),
                    'dynamics_found': len(dynamics)
                }
            }
            
            logger.info("\n📊 爬取结果统计:")
            logger.info(f"   基本信息: {'✅' if basic_info else '❌'}")
            logger.info(f"   视频数量: {len(videos)}")
            logger.info(f"   动态数量: {len(dynamics)}")
            logger.info(f"   视频详情示例: {'✅' if sample_video_detail else '❌'}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ 爬取过程中发生错误: {e}")
            return {}
        finally:
            await self.crawler.close_session()
    
    async def save_data(self, data: Dict, filename: str = None):
        """保存数据到文件"""
        if not data:
            logger.warning("没有数据可保存")
            return
        
        if not filename:
            uid = data.get('crawl_info', {}).get('uid', 'unknown')
            name = data.get('basic_info', {}).get('name', 'unknown')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/up_{uid}_{name}_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 数据已保存到: {filename}")

async def main():
    """主函数"""
    logger.info("🚀 UP主数据爬取工具")
    logger.info("="*50)
    
    # 配置
    uid = "1039025435"
    up_name = "战国时代_姜汁汽水"
    
    # 创建爬虫实例（15秒延迟，更保守）
    crawler = UPMasterCrawler(delay_between_requests=15)
    
    # 爬取数据
    logger.info(f"开始爬取UP主: {up_name}")
    data = await crawler.crawl_up_complete_data(uid, up_name)
    
    if data:
        # 保存数据
        await crawler.save_data(data)
        
        logger.info("\n🎉 爬取完成！")
        logger.info("📁 数据已保存到data目录")
        logger.info("\n💡 获取的数据包括:")
        logger.info("   ✓ UP主基本信息（姓名、粉丝数、等级等）")
        logger.info("   ✓ 视频列表（通过搜索获取）")
        logger.info("   ✓ 用户动态")
        logger.info("   ✓ 示例视频详情")
        
    else:
        logger.error("😞 爬取失败！")
        logger.info("💡 可能的原因:")
        logger.info("   1. 网络问题")
        logger.info("   2. B站API限制")
        logger.info("   3. Cookie失效")

if __name__ == "__main__":
    asyncio.run(main()) 