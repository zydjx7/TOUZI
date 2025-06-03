#!/usr/bin/env python3
"""
增强版B站爬虫测试 - 处理反爬虫
"""

import asyncio
import logging
import sys
import time
import random
from pathlib import Path
from datetime import datetime
import hashlib

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.crawler import BilibiliCrawler
from src.core.database import DatabaseManager, VideoContent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedBilibiliCrawler(BilibiliCrawler):
    """增强版爬虫，添加反爬虫处理"""
    
    def __init__(self):
        super().__init__()
        # 增加更真实的请求头
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        })
        
    async def _make_request_with_retry(self, url: str, params: dict = None, max_retries: int = 3):
        """带重试的请求"""
        for attempt in range(max_retries):
            try:
                # 添加随机延迟
                if attempt > 0:
                    delay = random.uniform(3, 5) * (attempt + 1)
                    logger.info(f"等待 {delay:.1f} 秒后重试...")
                    await asyncio.sleep(delay)
                
                result = await self._make_request(url, params)
                
                if result and result.get('code') == 0:
                    return result
                elif result and result.get('code') == -799:
                    logger.warning(f"请求频繁，第 {attempt + 1} 次尝试失败")
                    continue
                else:
                    return result
                    
            except Exception as e:
                logger.error(f"请求异常: {e}")
                if attempt == max_retries - 1:
                    raise
        
        return None

async def test_with_cookie_approach():
    """使用Cookie方式测试"""
    print("\n" + "="*60)
    print("📋 使用Cookie方式访问")
    print("="*60)
    
    # 检查是否有Cookie配置
    cookie_file = Path("config/cookies.json")
    if cookie_file.exists():
        print("✅ 发现Cookie配置文件")
    else:
        print("❌ 未找到Cookie配置")
        print("\n建议操作：")
        print("1. 在浏览器中登录B站")
        print("2. 使用浏览器开发者工具获取Cookie")
        print("3. 运行: python src/utils/cookie_helper.py")
        print("4. 将Cookie粘贴到提示中")
        
        # 提供快速配置选项
        cookie = input("\n现在配置Cookie吗？(直接粘贴Cookie或按回车跳过): ").strip()
        if cookie:
            from src.utils.cookie_helper import CookieHelper
            helper = CookieHelper()
            helper.save_bilibili_cookie(cookie)
            print("✅ Cookie已保存")

async def test_with_delays():
    """使用延迟策略测试"""
    print("\n" + "="*60)
    print("🐢 使用延迟策略测试")
    print("="*60)
    
    # 目标UP主信息
    test_uid = "1039025435"
    up_name = "战国时代_姜汁汽水"
    
    # 使用增强版爬虫
    crawler = EnhancedBilibiliCrawler()
    db_manager = DatabaseManager("data/test_with_delays.db")
    
    await crawler.init_session()
    
    try:
        # 先等待一段时间
        print("⏳ 等待5秒以避免频率限制...")
        await asyncio.sleep(5)
        
        print(f"\n📹 获取UP主视频: {up_name}")
        
        # 修改请求方式，使用更长的延迟
        crawler.rate_limit_delay = 5  # 增加到5秒
        
        videos = await crawler._make_request_with_retry(
            "https://api.bilibili.com/x/space/arc/search",
            params={
                'mid': test_uid,
                'ps': 3,  # 只获取3个视频
                'pn': 1,
                'order': 'pubdate',
                'tid': 0,
                'keyword': '',
                'jsonp': 'jsonp'
            }
        )
        
        if videos and videos.get('code') == 0:
            video_list = videos.get('data', {}).get('list', {}).get('vlist', [])
            print(f"✅ 成功获取 {len(video_list)} 个视频")
            
            for i, video in enumerate(video_list):
                print(f"\n视频 {i+1}:")
                print(f"标题: {video['title']}")
                print(f"BV号: {video['bvid']}")
                print(f"播放量: {video['play']:,}")
                
                # 获取视频详情
                print("⏳ 等待5秒...")
                await asyncio.sleep(5)
                
                video_info = await crawler._make_request_with_retry(
                    "https://api.bilibili.com/x/web-interface/view",
                    params={'bvid': video['bvid']}
                )
                
                if video_info and video_info.get('code') == 0:
                    info = video_info['data']
                    print(f"✅ 获取详情成功")
                    print(f"描述: {info['desc'][:100]}...")
                    
                    # 尝试获取字幕
                    print("\n📝 尝试获取字幕...")
                    await asyncio.sleep(5)
                    
                    transcript = await crawler.get_video_transcript(video['bvid'])
                    if transcript:
                        print(f"✅ 获取到文本内容")
                        print(f"长度: {len(transcript)} 字符")
                        print(f"预览: {transcript[:150]}...")
                    else:
                        print("⚠️  未获取到字幕，使用视频描述")
                        
        else:
            print(f"❌ 获取失败: {videos}")
            
    except Exception as e:
        logger.error(f"测试失败: {e}")
    finally:
        await crawler.close_session()

async def test_alternative_methods():
    """测试替代方案"""
    print("\n" + "="*60)
    print("🔄 替代方案建议")
    print("="*60)
    
    print("\n1. 使用搜索API代替用户视频API：")
    print("   - 搜索UP主名称获取视频")
    print("   - 限制较少，更容易成功")
    
    print("\n2. 使用Web端接口：")
    print("   - 模拟浏览器访问")
    print("   - 需要更复杂的请求头")
    
    print("\n3. 使用MCP方案：")
    print("   - Bilibili MCP (需要Apify token)")
    print("   - Browser-Tools MCP (自动化浏览器)")
    
    print("\n4. 手动方式：")
    print("   - 使用哔哩君等浏览器插件")
    print("   - 手动下载后批量处理")

async def main():
    """主测试函数"""
    print("🔍 B站爬虫问题诊断")
    print("="*60)
    
    # 1. 先尝试使用延迟策略
    await test_with_delays()
    
    # 2. 提供Cookie方案
    await test_with_cookie_approach()
    
    # 3. 显示替代方案
    await test_alternative_methods()
    
    print("\n" + "="*60)
    print("📌 推荐解决方案：")
    print("1. 短期：配置Cookie + 增加请求延迟")
    print("2. 长期：考虑使用MCP或其他自动化方案")
    print("="*60)

if __name__ == "__main__":
    # 确保必要的目录存在
    Path("data").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)
    
    # 运行测试
    asyncio.run(main())
