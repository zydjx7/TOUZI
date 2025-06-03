#!/usr/bin/env python3
"""
测试是否可以不用SESSDATA
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.crawler import BilibiliCrawler

async def test_current_cookie():
    """测试当前Cookie是否有效"""
    print("🔍 测试当前Cookie（无SESSDATA）")
    print("="*50)
    
    crawler = BilibiliCrawler()
    await crawler.init_session()
    
    try:
        # 1. 先测试一个简单的API
        print("\n1️⃣ 测试用户信息API...")
        user_info = await crawler._make_request("https://api.bilibili.com/x/web-interface/nav")
        
        if user_info and user_info.get('code') == 0:
            print(f"✅ 已登录用户: {user_info['data']['uname']}")
            print(f"   用户ID: {user_info['data']['mid']}")
        else:
            print("❌ 用户信息获取失败")
        
        await asyncio.sleep(2)
        
        # 2. 测试获取自己的投稿视频
        print("\n2️⃣ 测试获取自己的投稿...")
        your_uid = "473105574"  # 你的UID
        videos = await crawler.get_user_videos(your_uid, page_size=5)
        
        if videos:
            print(f"✅ 成功获取到 {len(videos)} 个视频")
            if videos:
                print(f"   最新视频: {videos[0].get('title', 'Unknown')}")
        else:
            print("❌ 获取自己的视频失败")
        
        await asyncio.sleep(3)
        
        # 3. 测试目标UP主
        print("\n3️⃣ 测试目标UP主...")
        target_uid = "1039025435"  # 战国时代_姜汁汽水
        videos = await crawler.get_user_videos(target_uid, page_size=3)
        
        if videos:
            print(f"✅ 成功！获取到 {len(videos)} 个视频")
            for i, video in enumerate(videos):
                print(f"\n视频{i+1}: {video.get('title')}")
                print(f"BV号: {video.get('bvid')}")
        else:
            print("❌ 获取目标UP主视频失败")
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await crawler.close_session()

if __name__ == "__main__":
    asyncio.run(test_current_cookie())
