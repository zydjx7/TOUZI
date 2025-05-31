# 开发指南

## 🚀 新开发者快速上手

### 1. 环境准备
```bash
# 1. 克隆项目
git clone <repository_url>
cd TOUZI

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的配置信息

# 5. 运行安装脚本
python setup.py
```

### 2. 项目启动
```bash
# 启动主程序
python main.py

# 启动Web界面
python -m src.web.app

# 运行测试
python -m pytest tests/
```

---

## 📝 开发约定

### 代码风格
- **Python PEP 8** - 遵循Python官方代码规范
- **类型提示** - 所有函数都要有类型提示
- **文档字符串** - 所有类和函数都要有详细的docstring
- **异步优先** - I/O操作统一使用异步模式

### 示例代码风格
```python
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ExampleClass:
    """示例类的描述
    
    这里是更详细的类说明，包括使用场景、注意事项等。
    """
    
    def __init__(self, config: Dict[str, Any]):
        """初始化方法
        
        Args:
            config: 配置字典
        """
        self.config = config
        
    async def async_method(self, param: str) -> Optional[List[str]]:
        """异步方法示例
        
        Args:
            param: 输入参数
            
        Returns:
            Optional[List[str]]: 返回结果列表，可能为None
            
        Raises:
            ValueError: 当参数无效时抛出
        """
        try:
            # 实现逻辑
            result = await some_async_operation(param)
            logger.info(f"操作完成: {param}")
            return result
        except Exception as e:
            logger.error(f"操作失败: {e}")
            raise
```

### 文件命名规范
- **模块名**: 小写，用下划线分隔 (`user_manager.py`)
- **类名**: 大驼峰命名 (`UserManager`)
- **函数名**: 小写，用下划线分隔 (`get_user_info`)
- **常量**: 全大写，用下划线分隔 (`MAX_RETRY_COUNT`)

---

## 🏗 模块开发流程

### 新模块开发步骤
1. **设计阶段**
   - 确定模块职责和接口
   - 更新 `docs/ARCHITECTURE.md`
   - 在 `docs/INTERFACE_SPECS.md` 中定义接口

2. **实现阶段**
   - 创建模块文件
   - 实现核心功能
   - 添加错误处理和日志

3. **测试阶段**
   - 编写单元测试
   - 进行集成测试
   - 性能测试（如需要）

4. **文档阶段**
   - 更新API文档
   - 更新进度跟踪
   - 编写使用示例

### 代码提交规范
```bash
# 提交格式
git commit -m "feat(模块名): 添加新功能的描述"
git commit -m "fix(模块名): 修复问题的描述"
git commit -m "docs: 更新文档"
git commit -m "test: 添加测试用例"
```

---

## 🧪 测试指南

### 测试文件结构
```
tests/
├── __init__.py
├── test_crawler.py          # 爬虫模块测试
├── test_analyzer.py         # 分析模块测试
├── test_database.py         # 数据库模块测试
├── test_api.py              # API接口测试
└── fixtures/                # 测试数据
    ├── sample_videos.json
    └── sample_news.json
```

### 测试模板
```python
import unittest
import asyncio
from unittest.mock import Mock, patch

class TestModuleName(unittest.TestCase):
    """模块测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.module = ModuleName()
    
    def tearDown(self):
        """测试清理"""
        pass
    
    def test_sync_method(self):
        """测试同步方法"""
        result = self.module.sync_method("test_input")
        self.assertEqual(result, "expected_output")
    
    def test_async_method(self):
        """测试异步方法"""
        async def run_test():
            result = await self.module.async_method("test_input")
            self.assertIsNotNone(result)
        
        asyncio.run(run_test())
    
    @patch('module_name.external_api')
    def test_with_mock(self, mock_api):
        """使用Mock测试外部依赖"""
        mock_api.return_value = "mocked_response"
        result = self.module.method_with_external_call()
        self.assertEqual(result, "expected_result")

if __name__ == '__main__':
    unittest.main()
```

---

## 🔧 调试指南

### 日志配置
```python
import logging

# 设置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 使用示例
logger.info("信息级别日志")
logger.warning("警告级别日志")
logger.error("错误级别日志")
```

### 常用调试技巧
```python
# 1. 使用断点调试
import pdb; pdb.set_trace()

# 2. 异步调试
import asyncio
import logging

# 启用asyncio调试模式
asyncio.get_event_loop().set_debug(True)

# 3. 性能分析
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时: {end - start:.2f}秒")
        return result
    return wrapper
```

---

## 📊 性能优化指南

### 异步编程最佳实践
```python
# ✅ 正确的异步使用
async def good_async_example():
    # 并发执行多个任务
    tasks = [
        fetch_data_1(),
        fetch_data_2(),
        fetch_data_3()
    ]
    results = await asyncio.gather(*tasks)
    return results

# ❌ 错误的异步使用
async def bad_async_example():
    # 顺序执行，没有利用异步优势
    result1 = await fetch_data_1()
    result2 = await fetch_data_2()  
    result3 = await fetch_data_3()
    return [result1, result2, result3]
```

### 数据库优化
```python
# ✅ 批量操作
def batch_insert(self, items: List[Dict]):
    """批量插入数据"""
    query = "INSERT INTO table (col1, col2) VALUES (?, ?)"
    data = [(item['col1'], item['col2']) for item in items]
    self.cursor.executemany(query, data)

# ✅ 使用索引
def create_indexes(self):
    """创建必要的索引"""
    self.cursor.execute("CREATE INDEX idx_publish_time ON videos(publish_time)")
    self.cursor.execute("CREATE INDEX idx_content_type ON analysis(content_type)")
```

---

## 🚨 错误处理最佳实践

### 异常处理模板
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class CustomError(Exception):
    """自定义异常类"""
    pass

async def robust_function(param: str) -> Optional[str]:
    """健壮的函数示例"""
    try:
        # 参数验证
        if not param or not isinstance(param, str):
            raise ValueError("参数必须是非空字符串")
        
        # 主要逻辑
        result = await some_operation(param)
        
        # 结果验证
        if not result:
            logger.warning(f"操作返回空结果: {param}")
            return None
            
        return result
        
    except ValueError as e:
        logger.error(f"参数错误: {e}")
        raise
    except asyncio.TimeoutError:
        logger.error(f"操作超时: {param}")
        return None
    except Exception as e:
        logger.error(f"未知错误: {e}", exc_info=True)
        raise CustomError(f"处理失败: {param}") from e
```

---

## 📋 发布检查清单

### 功能完成检查
- [ ] 功能实现完整
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 错误处理完善
- [ ] 日志记录充分

### 代码质量检查  
- [ ] 代码风格符合规范
- [ ] 类型提示完整
- [ ] 文档字符串完整
- [ ] 无安全漏洞
- [ ] 性能满足要求

### 文档更新检查
- [ ] API文档更新
- [ ] 架构文档更新
- [ ] 进度跟踪更新
- [ ] 使用说明更新

---

## 📞 获取帮助

### 常见问题排查
1. **导入错误**: 检查PYTHONPATH和模块结构
2. **数据库错误**: 检查数据库文件权限和路径
3. **网络错误**: 检查网络连接和API限制
4. **异步错误**: 检查是否正确使用await关键字

### 联系方式
- 项目文档: `docs/` 目录
- 问题反馈: GitHub Issues
- 技术讨论: 项目讨论区

记住：**好的代码不仅要能工作，还要容易理解和维护！** 