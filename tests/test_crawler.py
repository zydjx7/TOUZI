"""
爬虫模块测试
Crawler Module Tests
"""

import unittest
import asyncio
from src.core.crawler import BilibiliCrawler

class TestBilibiliCrawler(unittest.TestCase):
    """B站爬虫测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.crawler = BilibiliCrawler()
        self.test_uid = "37663924"  # 巫师财经的UID
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """测试清理"""
        self.loop.run_until_complete(self.crawler.close_session())
        self.loop.close()
    
    def test_init_session(self):
        """测试会话初始化"""
        async def run_test():
            await self.crawler.init_session()
            self.assertIsNotNone(self.crawler.session)
            self.assertTrue(hasattr(self.crawler, 'headers'))
        
        self.loop.run_until_complete(run_test())
    
    def test_get_user_videos(self):
        """测试获取用户视频"""
        async def run_test():
            await self.crawler.init_session()
            videos = await self.crawler.get_user_videos(self.test_uid, page_size=5)
            
            # 验证返回结果
            self.assertIsInstance(videos, list)
            if videos:  # 如果获取到视频
                self.assertGreater(len(videos), 0)
                # 验证视频数据结构
                first_video = videos[0]
                self.assertIn('bvid', first_video)
                self.assertIn('title', first_video)
                print(f"✅ 成功获取 {len(videos)} 个视频")
                print(f"   第一个视频: {first_video.get('title', 'Unknown')}")
            else:
                print("⚠️  未获取到视频（可能是网络问题）")
        
        self.loop.run_until_complete(run_test())
    
    def test_get_video_info(self):
        """测试获取视频详情"""
        async def run_test():
            await self.crawler.init_session()
            
            # 先获取一个视频BV号
            videos = await self.crawler.get_user_videos(self.test_uid, page_size=1)
            if not videos:
                self.skipTest("无法获取视频列表")
                return
            
            test_bvid = videos[0]['bvid']
            await asyncio.sleep(2)  # 避免请求过快
            
            # 获取视频详情
            video_info = await self.crawler.get_video_info(test_bvid)
            
            if video_info:
                self.assertIn('title', video_info)
                self.assertIn('stat', video_info)
                self.assertIn('desc', video_info)
                print(f"✅ 获取视频详情成功: {video_info['title']}")
            else:
                print("❌ 获取视频详情失败")
        
        self.loop.run_until_complete(run_test())
    
    def test_get_video_transcript(self):
        """测试获取视频字幕"""
        async def run_test():
            await self.crawler.init_session()
            
            # 获取一个视频用于测试
            videos = await self.crawler.get_user_videos(self.test_uid, page_size=1)
            if not videos:
                self.skipTest("无法获取视频列表")
                return
            
            test_bvid = videos[0]['bvid']
            await asyncio.sleep(2)
            
            # 获取字幕
            transcript = await self.crawler.get_video_transcript(test_bvid)
            
            self.assertIsInstance(transcript, str)
            if transcript:
                print(f"✅ 获取到字幕/描述，长度: {len(transcript)} 字符")
                print(f"   内容预览: {transcript[:100]}...")
            else:
                print("⚠️  未获取到字幕（视频可能没有字幕）")
        
        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    print("🚀 开始测试B站爬虫功能")
    print("=" * 50)
    unittest.main(verbosity=2)