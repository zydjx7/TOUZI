#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UP主数据爬取总结报告
"""

import json
import os
from datetime import datetime
from typing import Dict, List

def analyze_crawl_data(filename: str):
    """分析爬取的数据并生成报告"""
    
    if not os.path.exists(filename):
        print(f"❌ 文件不存在: {filename}")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*80)
    print("🎯 B站UP主数据爬取成功报告")
    print("="*80)
    
    # 基本信息
    crawl_info = data.get('crawl_info', {})
    basic_info = data.get('basic_info', {})
    
    print(f"📅 爬取时间: {crawl_info.get('crawl_time', 'Unknown')}")
    print(f"🆔 UP主UID: {crawl_info.get('uid', 'Unknown')}")
    print(f"📝 爬取方法: {crawl_info.get('crawl_method', 'Unknown')}")
    
    print("\n" + "="*60)
    print("👤 UP主基本信息")
    print("="*60)
    print(f"🎭 用户名: {basic_info.get('name', 'Unknown')}")
    print(f"👥 粉丝数: {basic_info.get('follower', 0):,}")
    print(f"➕ 关注数: {basic_info.get('following', 0):,}")
    print(f"⭐ 等级: {basic_info.get('level', 'Unknown')}")
    print(f"📝 签名: {basic_info.get('sign', 'Unknown')}")
    
    # 认证信息
    if basic_info.get('official', {}).get('role') > 0:
        official = basic_info.get('official', {})
        print(f"✅ 认证信息: {official.get('title', 'Unknown')}")
    
    # 视频信息
    videos = data.get('videos', [])
    print(f"\n" + "="*60)
    print("📺 视频数据统计")
    print("="*60)
    print(f"🎬 找到视频数量: {len(videos)}")
    
    if videos:
        # 分析视频数据
        total_plays = sum(video.get('play', 0) for video in videos)
        avg_plays = total_plays / len(videos) if videos else 0
        
        print(f"👁️  总播放量: {total_plays:,}")
        print(f"📊 平均播放量: {avg_plays:,.0f}")
        
        # 最热门视频
        most_popular = max(videos, key=lambda x: x.get('play', 0))
        print(f"🔥 最热门视频: {most_popular.get('title', 'Unknown')}")
        print(f"   播放量: {most_popular.get('play', 0):,}")
        
        print(f"\n📋 视频列表 (前8个):")
        for i, video in enumerate(videos[:8], 1):
            title = video.get('title', 'Unknown')
            plays = video.get('play', 0)
            duration = video.get('duration', 'Unknown')
            bvid = video.get('bvid', 'Unknown')
            
            # 转换时间戳
            try:
                pubdate = video.get('pubdate', 0)
                pub_time = datetime.fromtimestamp(pubdate).strftime('%Y-%m-%d')
            except:
                pub_time = "未知"
                
            print(f"   {i:2d}. {title}")
            print(f"       📺 {plays:,} 次播放 | ⏰ {duration} | 📅 {pub_time} | 🆔 {bvid}")
    
    # 动态信息
    dynamics = data.get('dynamics', [])
    print(f"\n" + "="*60)
    print("📱 动态数据")
    print("="*60)
    print(f"📄 动态数量: {len(dynamics)}")
    
    if dynamics:
        print(f"💬 最新动态:")
        for i, dynamic in enumerate(dynamics[:3], 1):
            content = dynamic.get('content', '')[:60]
            timestamp = dynamic.get('timestamp', 0)
            try:
                time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            except:
                time_str = "未知时间"
            print(f"   {i}. {content}... ({time_str})")
    else:
        print("⚠️  未获取到动态数据（可能是权限限制）")
    
    # 示例视频详情
    sample_video = data.get('sample_video_detail', {})
    if sample_video:
        print(f"\n" + "="*60)
        print("🎬 示例视频详细信息")
        print("="*60)
        print(f"🎯 视频标题: {sample_video.get('title', 'Unknown')}")
        print(f"🆔 BVID: {sample_video.get('bvid', 'Unknown')}")
        
        stat = sample_video.get('stat', {})
        print(f"📊 视频统计:")
        print(f"   👁️  播放量: {stat.get('view', 0):,}")
        print(f"   👍 点赞数: {stat.get('like', 0):,}")
        print(f"   🪙 投币数: {stat.get('coin', 0):,}")
        print(f"   ⭐ 收藏数: {stat.get('favorite', 0):,}")
        print(f"   💬 评论数: {stat.get('reply', 0):,}")
        print(f"   📤 分享数: {stat.get('share', 0):,}")
        
        # 时长
        duration = sample_video.get('duration', 0)
        if duration:
            minutes = duration // 60
            seconds = duration % 60
            print(f"   ⏱️  时长: {minutes}分{seconds}秒")
    
    # 爬取成功总结
    print(f"\n" + "="*60)
    print("✅ 爬取成功总结")
    print("="*60)
    
    success_items = []
    if basic_info: success_items.append("✓ UP主基本信息")
    if videos: success_items.append(f"✓ {len(videos)}个视频信息")
    if dynamics: success_items.append(f"✓ {len(dynamics)}条动态")
    if sample_video: success_items.append("✓ 视频详细信息示例")
    
    for item in success_items:
        print(f"   {item}")
    
    print(f"\n💡 数据使用建议:")
    print(f"   1. 可以分析视频标题中的关键词，了解内容主题")
    print(f"   2. 通过播放量和时间分析内容受欢迎程度趋势")
    print(f"   3. 结合动态和视频，了解UP主的活跃度")
    print(f"   4. 可以进一步获取视频评论进行情感分析")
    
    print(f"\n📁 数据文件位置: {filename}")
    print(f"📊 文件大小: {os.path.getsize(filename) / 1024:.1f} KB")

def main():
    """主函数"""
    # 查找最新的数据文件
    data_dir = "data"
    if not os.path.exists(data_dir):
        print("❌ data目录不存在")
        return
    
    # 找到最新的UP主数据文件
    up_files = [f for f in os.listdir(data_dir) if f.startswith('up_') and f.endswith('.json')]
    
    if not up_files:
        print("❌ 未找到UP主数据文件")
        return
    
    # 按修改时间排序，取最新的
    latest_file = max(up_files, key=lambda f: os.path.getmtime(os.path.join(data_dir, f)))
    filepath = os.path.join(data_dir, latest_file)
    
    print(f"📄 分析最新数据文件: {latest_file}")
    analyze_crawl_data(filepath)

if __name__ == "__main__":
    main() 