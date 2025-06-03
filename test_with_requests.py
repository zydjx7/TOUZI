#!/usr/bin/env python3
"""
使用requests库测试B站API
"""
import requests
import json
from pathlib import Path

def test_with_requests():
    """使用requests库测试"""
    print("🔍 使用requests库测试")
    print("="*50)
    
    # 读取Cookie
    cookie_file = Path("config/cookies.json")
    if cookie_file.exists():
        with open(cookie_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cookie_str = data.get('bilibili', {}).get('cookie', '')
    else:
        print("❌ 未找到Cookie配置")
        return
    
    # 设置请求头
    headers = {
        'Cookie': cookie_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.bilibili.com/',
    }
    
    # 1. 测试登录状态
    print("\n1️⃣ 测试登录状态...")
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
    data = resp.json()
    
    if data.get('code') == 0:
        print(f"✅ 已登录: {data['data']['uname']}")
    else:
        print(f"❌ 未登录: {data}")
    
    # 2. 测试获取UP主视频
    print("\n2️⃣ 测试获取UP主视频...")
    params = {
        'mid': '1039025435',  # 战国时代_姜汁汽水
        'ps': 5,
        'pn': 1,
        'order': 'pubdate'
    }
    
    resp = requests.get(
        'https://api.bilibili.com/x/space/arc/search',
        params=params,
        headers=headers
    )
    
    data = resp.json()
    print(f"响应状态码: {resp.status_code}")
    print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    if data.get('code') == 0:
        videos = data.get('data', {}).get('list', {}).get('vlist', [])
        print(f"\n✅ 获取到 {len(videos)} 个视频")
        for video in videos[:3]:
            print(f"- {video['title']}")
    else:
        print(f"\n❌ 获取失败: {data.get('message')}")

if __name__ == "__main__":
    test_with_requests()
