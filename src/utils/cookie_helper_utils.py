"""
B站Cookie管理工具
用于管理和加载B站登录凭据
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class CookieHelper:
    """Cookie管理助手"""
    
    def __init__(self, config_path: str = "config/cookies.json"):
        self.config_path = Path(config_path)
        self.cookies = self._load_cookies()
    
    def _load_cookies(self) -> Dict:
        """加载Cookie配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载Cookie失败: {e}")
        return {}
    
    def get_bilibili_cookie(self) -> Optional[str]:
        """获取B站Cookie"""
        return self.cookies.get('bilibili', {}).get('cookie')
    
    def save_bilibili_cookie(self, cookie: str):
        """保存B站Cookie"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.cookies['bilibili'] = {
            'cookie': cookie,
            'updated_at': str(Path.ctime(Path.cwd()))
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.cookies, f, indent=2, ensure_ascii=False)
        
        logger.info("Cookie已保存")
        
        # 更新.gitignore
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if 'config/cookies.json' not in content:
                with open(gitignore_path, 'a') as f:
                    f.write("\n# Cookie配置\nconfig/cookies.json\n")

def setup_cookie_interactive():
    """交互式设置Cookie"""
    print("\n📋 B站Cookie配置向导")
    print("=" * 50)
    print("获取Cookie的步骤：")
    print("1. 在浏览器中登录B站")
    print("2. 按F12打开开发者工具")
    print("3. 切换到Network标签页")
    print("4. 刷新B站页面")
    print("5. 找到任意bilibili.com的请求")
    print("6. 在Request Headers中找到Cookie字段")
    print("7. 复制完整的Cookie值")
    print("=" * 50)
    
    cookie = input("\n请粘贴Cookie（直接回车跳过）: ").strip()
    
    if cookie:
        helper = CookieHelper()
        helper.save_bilibili_cookie(cookie)
        print("✅ Cookie配置成功！")
        print("\n下一步：")
        print("1. 运行爬虫测试: python tests/test_crawler.py")
        print("2. Cookie会自动加载到爬虫中")
    else:
        print("⚠️  跳过Cookie配置，将只能访问公开内容")

if __name__ == "__main__":
    setup_cookie_interactive()
