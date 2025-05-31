"""
B站爬虫模块
Bilibili Crawler Module
"""

import aiohttp
import asyncio
import json
import logging
import re
import hashlib
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import config

logger = logging.getLogger(__name__)

class BilibiliCrawler:
    """B站爬虫类"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.rate_limit_delay = config.CRAWLER_CONFIG.get('rate_limit_delay', 2)
        self.timeout = config.CRAWLER_CONFIG.get('timeout', 30)
        
    async def init_session(self):
        """初始化会话"""
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=timeout
            )
            logger.info("B站爬虫会话初始化完成")
    
    async def close_session(self):
        """关闭会话"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("B站爬虫会话已关闭")
    
    async def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """发起HTTP请求"""
        if not self.session:
            await self.init_session()
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"请求失败: {url}, 状态码: {response.status}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error(f"请求超时: {url}")
            return None
        except Exception as e:
            logger.error(f"请求出错: {url}, 错误: {e}")
            return None
    
    async def get_user_videos(self, uid: str, page_size: int = 50) -> List[Dict]:
        """获取用户视频列表"""
        url = "https://api.bilibili.com/x/space/arc/search"
        
        params = {
            'mid': uid,
            'ps': page_size,
            'pn': 1,
            'order': 'pubdate',
            'tid': 0,
            'keyword': '',
            'jsonp': 'jsonp'
        }
        
        try:
            data = await self._make_request(url, params)
            
            if data and data.get('code') == 0:
                videos = data.get('data', {}).get('list', {}).get('vlist', [])
                logger.info(f"获取到 {len(videos)} 个视频")
                return videos
            else:
                logger.warning(f"获取用户视频失败: {data}")
                return []
                
        except Exception as e:
            logger.error(f"获取用户视频出错: {e}")
            return []
    
    async def get_video_info(self, bvid: str) -> Optional[Dict]:
        """获取视频详细信息"""
        url = "https://api.bilibili.com/x/web-interface/view"
        
        params = {
            'bvid': bvid
        }
        
        try:
            data = await self._make_request(url, params)
            
            if data and data.get('code') == 0:
                video_info = data.get('data', {})
                logger.debug(f"获取视频信息: {video_info.get('title', 'Unknown')}")
                return video_info
            else:
                logger.warning(f"获取视频信息失败: {bvid}")
                return None
                
        except Exception as e:
            logger.error(f"获取视频信息出错: {e}")
            return None
    
    async def get_video_transcript(self, bvid: str) -> str:
        """获取视频转录文本（字幕）"""
        try:
            # 先获取视频的基本信息
            video_info = await self.get_video_info(bvid)
            if not video_info:
                return ""
            
            cid = video_info.get('cid')
            if not cid:
                return ""
            
            # 获取字幕信息
            subtitle_url = f"https://api.bilibili.com/x/player/v2"
            params = {
                'bvid': bvid,
                'cid': cid
            }
            
            subtitle_data = await self._make_request(subtitle_url, params)
            
            if not subtitle_data or subtitle_data.get('code') != 0:
                return ""
            
            # 提取字幕URL
            subtitle_list = subtitle_data.get('data', {}).get('subtitle', {}).get('subtitles', [])
            
            if not subtitle_list:
                # 如果没有字幕，尝试从视频描述中提取有用信息
                return video_info.get('desc', '')
            
            # 获取第一个字幕文件
            subtitle_info = subtitle_list[0]
            subtitle_file_url = subtitle_info.get('subtitle_url', '')
            
            if not subtitle_file_url:
                return video_info.get('desc', '')
            
            # 下载字幕文件
            if subtitle_file_url.startswith('//'):
                subtitle_file_url = 'https:' + subtitle_file_url
            
            subtitle_content = await self._make_request(subtitle_file_url)
            
            if not subtitle_content:
                return video_info.get('desc', '')
            
            # 解析字幕内容
            transcript = ""
            if 'body' in subtitle_content:
                for item in subtitle_content['body']:
                    text = item.get('content', '').strip()
                    if text:
                        transcript += text + " "
            
            return transcript.strip() or video_info.get('desc', '')
            
        except Exception as e:
            logger.error(f"获取视频字幕失败: {bvid}, 错误: {e}")
            # 返回视频描述作为备选
            try:
                video_info = await self.get_video_info(bvid)
                return video_info.get('desc', '') if video_info else ""
            except:
                return ""
    
    async def get_user_dynamics(self, uid: str, offset: str = "0") -> List[Dict]:
        """获取用户动态"""
        url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
        
        params = {
            'host_mid': uid,
            'offset': offset,
            'timezone_offset': -480,
            'platform': 'web'
        }
        
        try:
            data = await self._make_request(url, params)
            
            if data and data.get('code') == 0:
                items = data.get('data', {}).get('items', [])
                dynamics = []
                
                for item in items:
                    try:
                        dynamic_info = self._parse_dynamic_item(item)
                        if dynamic_info:
                            dynamics.append(dynamic_info)
                    except Exception as e:
                        logger.error(f"解析动态项目失败: {e}")
                        continue
                
                logger.info(f"获取到 {len(dynamics)} 条动态")
                return dynamics
            else:
                logger.warning(f"获取用户动态失败: {data}")
                return []
                
        except Exception as e:
            logger.error(f"获取用户动态出错: {e}")
            return []
    
    def _parse_dynamic_item(self, item: Dict) -> Optional[Dict]:
        """解析动态项目"""
        try:
            basic = item.get('basic', {})
            modules = item.get('modules', {})
            
            # 动态ID
            dynamic_id = item.get('id_str', '')
            
            # 发布时间
            timestamp = basic.get('pub_ts', 0)
            
            # 动态内容
            content = ""
            
            # 从不同模块提取内容
            if 'module_dynamic' in modules:
                desc = modules['module_dynamic'].get('desc', {})
                if 'text' in desc:
                    content = desc['text']
                elif 'rich_text_nodes' in desc:
                    # 富文本内容
                    for node in desc['rich_text_nodes']:
                        if node.get('type') == 'RICH_TEXT_NODE_TYPE_TEXT':
                            content += node.get('text', '')
            
            # 获取互动数据
            stat = modules.get('module_stat', {})
            like_count = stat.get('like', {}).get('count', 0)
            forward_count = stat.get('forward', {}).get('count', 0)
            comment_count = stat.get('comment', {}).get('count', 0)
            
            if not content.strip():
                return None
            
            return {
                'id': dynamic_id,
                'content': content.strip(),
                'timestamp': timestamp,
                'like_count': like_count,
                'forward_count': forward_count,
                'comment_count': comment_count
            }
            
        except Exception as e:
            logger.error(f"解析动态项目出错: {e}")
            return None
    
    async def get_video_comments(self, bvid: str, limit: int = 100) -> List[Dict]:
        """获取视频评论"""
        try:
            # 先获取视频信息以获得aid
            video_info = await self.get_video_info(bvid)
            if not video_info:
                return []
            
            aid = video_info.get('aid')
            if not aid:
                return []
            
            url = "https://api.bilibili.com/x/v2/reply/main"
            params = {
                'type': 1,  # 视频类型
                'oid': aid,
                'mode': 3,  # 按热度排序
                'next': 0,
                'ps': min(limit, 49)  # B站API限制
            }
            
            data = await self._make_request(url, params)
            
            if data and data.get('code') == 0:
                replies = data.get('data', {}).get('replies', [])
                comments = []
                
                for reply in replies:
                    try:
                        comment_info = {
                            'comment_id': str(reply.get('rpid', '')),
                            'content': reply.get('content', {}).get('message', ''),
                            'author': reply.get('member', {}).get('uname', ''),
                            'like_count': reply.get('like', 0),
                            'timestamp': reply.get('ctime', 0)
                        }
                        
                        if comment_info['content'].strip():
                            comments.append(comment_info)
                            
                    except Exception as e:
                        logger.error(f"解析评论失败: {e}")
                        continue
                
                logger.info(f"获取到 {len(comments)} 条评论")
                return comments
                
            else:
                logger.warning(f"获取视频评论失败: {data}")
                return []
                
        except Exception as e:
            logger.error(f"获取视频评论出错: {e}")
            return []
    
    async def search_videos(self, keyword: str, page_size: int = 50) -> List[Dict]:
        """搜索视频"""
        url = "https://api.bilibili.com/x/web-interface/search/type"
        
        params = {
            'search_type': 'video',
            'keyword': keyword,
            'page': 1,
            'page_size': page_size,
            'order': 'pubdate',
            'duration': 0,
            'tids': 0
        }
        
        try:
            data = await self._make_request(url, params)
            
            if data and data.get('code') == 0:
                videos = data.get('data', {}).get('result', [])
                
                # 简化视频信息
                simplified_videos = []
                for video in videos:
                    simplified_video = {
                        'bvid': video.get('bvid', ''),
                        'title': video.get('title', ''),
                        'author': video.get('author', ''),
                        'duration': video.get('duration', ''),
                        'play': video.get('play', 0),
                        'pubdate': video.get('pubdate', 0)
                    }
                    simplified_videos.append(simplified_video)
                
                logger.info(f"搜索到 {len(simplified_videos)} 个视频")
                return simplified_videos
                
            else:
                logger.warning(f"搜索视频失败: {data}")
                return []
                
        except Exception as e:
            logger.error(f"搜索视频出错: {e}")
            return []
    
    async def get_trending_videos(self, limit: int = 100) -> List[Dict]:
        """获取热门视频"""
        url = "https://api.bilibili.com/x/web-interface/popular"
        
        params = {
            'ps': min(limit, 100),
            'pn': 1
        }
        
        try:
            data = await self._make_request(url, params)
            
            if data and data.get('code') == 0:
                videos = data.get('data', {}).get('list', [])
                
                # 简化视频信息
                simplified_videos = []
                for video in videos:
                    simplified_video = {
                        'bvid': video.get('bvid', ''),
                        'title': video.get('title', ''),
                        'owner': video.get('owner', {}).get('name', ''),
                        'stat': video.get('stat', {}),
                        'pubdate': video.get('pubdate', 0)
                    }
                    simplified_videos.append(simplified_video)
                
                logger.info(f"获取到 {len(simplified_videos)} 个热门视频")
                return simplified_videos
                
            else:
                logger.warning(f"获取热门视频失败: {data}")
                return []
                
        except Exception as e:
            logger.error(f"获取热门视频出错: {e}")
            return [] 