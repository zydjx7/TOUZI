#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def main():
    filename = "data/up_1039025435_战国时代_姜汁汽水_20250602_095714.json"
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("🎯 B站UP主数据爬取成功！")
    print("="*50)
    
    # 基本信息
    basic = data.get('basic_info', {})
    print(f"UP主: {basic.get('name', 'Unknown')}")
    print(f"UID: {basic.get('mid', 'Unknown')}")
    print(f"等级: {basic.get('level', 'Unknown')}")
    print(f"签名: {basic.get('sign', 'Unknown')}")
    
    # 认证信息
    official = basic.get('official', {})
    if official.get('role', 0) > 0:
        print(f"认证: {official.get('title', 'Unknown')}")
    
    # 视频统计
    videos = data.get('videos', [])
    print(f"\n📺 视频数据:")
    print(f"找到视频: {len(videos)} 个")
    
    if videos:
        total_plays = sum(v.get('play', 0) for v in videos)
        avg_plays = total_plays / len(videos)
        print(f"总播放量: {total_plays:,}")
        print(f"平均播放量: {avg_plays:,.0f}")
        
        # 最热门视频
        top_video = max(videos, key=lambda x: x.get('play', 0))
        print(f"最热门: {top_video.get('title', 'Unknown')}")
        print(f"播放量: {top_video.get('play', 0):,}")
        
        print(f"\n视频列表:")
        for i, video in enumerate(videos[:5], 1):
            title = video.get('title', 'Unknown')
            plays = video.get('play', 0)
            print(f"{i}. {title} ({plays:,} 播放)")
    
    # 示例视频详情
    sample = data.get('sample_video_detail', {})
    if sample:
        stat = sample.get('stat', {})
        print(f"\n🎬 示例视频详情:")
        print(f"标题: {sample.get('title', 'Unknown')}")
        print(f"播放: {stat.get('view', 0):,}")
        print(f"点赞: {stat.get('like', 0):,}")
        print(f"投币: {stat.get('coin', 0):,}")
        print(f"收藏: {stat.get('favorite', 0):,}")
        print(f"评论: {stat.get('reply', 0):,}")
    
    print(f"\n✅ 爬取成功！数据已保存到: {filename}")
    print(f"文件大小: {os.path.getsize(filename)/1024:.1f} KB")

if __name__ == "__main__":
    main() 