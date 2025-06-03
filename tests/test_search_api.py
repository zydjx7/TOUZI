#!/usr/bin/env python3
"""
使用B站搜索API测试 - 绕过用户视频API限制
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.crawler import BilibiliCrawler

async def test_search_api():
    """使用搜索API获取UP主视频"""
    crawler = BilibiliCrawler()
    await crawler.init_session()
    
    try:
        # 通过搜索UP主名字获取视频
        up_name = "战国时代_姜汁汽水"
        print(f"🔍 搜索UP主: {up_name}")
        
        # 使用搜索功能
        videos = await crawler.search_videos(up_name, page_size=10)
        
        if videos:
            print(f"\n✅ 搜索到 {len(videos)} 个相关视频")
            
            # 筛选该UP主的视频
            up_videos = [v for v in videos if up_name in v.get('author', '')]
            print(f"✅ 其中 {len(up_videos)} 个来自目标UP主")
            
            for i, video in enumerate(up_videos[:3]):
                print(f"\n视频 {i+1}:")
                print(f"标题: {video['title']}")
                print(f"作者: {video['author']}")
                print(f"BV号: {video['bvid']}")
                print(f"播放量: {video.get('play', 0)}")
                
                # 延迟避免频率限制
                await asyncio.sleep(3)
                
                # 获取视频详情
                print("\n获取视频详情...")
                video_info = await crawler.get_video_info(video['bvid'])
                
                if video_info:
                    print(f"✅ 描述: {video_info['desc'][:100]}...")
                    
                    # 获取字幕
                    await asyncio.sleep(3)
                    transcript = await crawler.get_video_transcript(video['bvid'])
                    
                    if transcript:
                        print(f"✅ 文本长度: {len(transcript)} 字符")
                        print(f"文本预览: {transcript[:150]}...")
                    else:
                        print("⚠️  无字幕，仅有视频描述")
        else:
            print("❌ 搜索失败")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        await crawler.close_session()

if __name__ == "__main__":
    print("使用搜索API测试（避开用户API限制）")
    print("="*50)
    asyncio.run(test_search_api())
