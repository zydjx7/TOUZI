# 项目摘要 - 快速上手指南

> 🚀 **新对话必读**：这是财经智能分析系统的核心信息摘要，帮助AI快速了解项目状态。

## 📋 项目基本信息

**项目名称**: 财经智能分析系统 (Financial Intelligence Analysis System)  
**技术栈**: Python 3.8+ | Flask | SQLite | AsyncIO | Chart.js  
**当前版本**: v1.0.0-dev  
**开发阶段**: 基础框架完成，进入核心功能开发

## 🏗 核心架构 (5分钟速览)

```python
# 主要模块结构
src/
├── core/           # 核心业务逻辑
│   ├── crawler.py     # ✅ B站爬虫 (已完成)
│   ├── database.py    # ✅ 数据库管理 (已完成)
│   ├── analyzer.py    # 🔄 内容分析 (框架完成，待实现)
│   ├── news_aggregator.py  # 📋 新闻聚合 (待实现)
│   └── report_generator.py # 📋 报告生成 (待实现)
├── web/            # Web界面
│   ├── app.py         # ✅ Flask应用 (框架完成)
│   ├── api.py         # 🔄 API接口 (框架完成，待实现)
│   └── templates/     # ✅ 前端模板 (已完成)
└── utils/          # 工具模块
    ├── email_notifier.py    # 📋 邮件通知 (待实现)
    ├── text_processor.py    # 📋 文本处理 (待实现)
    └── financial_calculator.py # 📋 金融计算 (待实现)
```

## 🎯 核心功能清单

### ✅ 已完成功能
- **B站数据爬取**: 视频、动态、评论获取
- **数据库架构**: 完整的数据模型和存储结构
- **Web仪表板**: 响应式界面，实时数据展示
- **项目架构**: 模块化设计，标准Python包结构

### 🔄 进行中功能
- **内容分析模块**: 情感分析、关键词提取算法设计

### 📋 待实现功能
- **AI分析引擎**: 投资信号检测、风险评估
- **新闻聚合**: 财经新闻自动获取和分析
- **报告生成**: 自动化日报/周报/月报
- **通知系统**: 邮件推送和警报

## 🔧 关键类和接口

### 数据模型
```python
@dataclass
class VideoContent:
    bvid: str; title: str; transcript: str; up_name: str
    publish_time: datetime; view_count: int; tags: List[str]

@dataclass
class AnalysisResult:
    content_id: str; sentiment_score: float
    investment_signals: List[Dict]; risk_level: str
```

### 核心接口
```python
class ContentAnalyzer:
    def analyze_sentiment(text: str) -> float  # 待实现
    def detect_investment_signals(text: str) -> List[Dict]  # 待实现

class NewsAggregator:
    async def fetch_latest_news(category: str) -> List[NewsContent]  # 待实现
```

## 📊 API接口 (REST)
- `POST /api/analysis/start` - 启动分析
- `GET /api/dashboard/data` - 获取仪表板数据
- `POST /api/reports/generate` - 生成报告

## 🗃 配置和环境

### 必要的配置文件
- `config.py` - 系统配置 (UP主列表、API密钥等)
- `requirements.txt` - Python依赖包
- `.env` - 环境变量 (邮箱、API密钥等敏感信息)

### 关键配置项
```python
# config.py 重要配置
UP_LIST = [{"uid": "37663924", "name": "巫师财经"}]  # B站UP主列表
DATABASE_PATH = "data/financial_analysis.db"        # 数据库路径
EMAIL_CONFIG = {...}                                # 邮件配置
```

## 🎯 当前开发重点

**优先级1**: 实现内容分析模块 (`src/core/analyzer.py`)
- 情感分析算法
- 投资信号检测逻辑
- 关键词提取功能

**优先级2**: 完善API接口实现 (`src/web/api.py`)
- 业务逻辑连接
- 数据获取和处理
- 错误处理

## 💡 开发约定

### 代码风格
- 使用异步编程 (`async/await`)
- 统一日志记录 (`logging`)
- 类型提示 (`typing`)
- 数据类 (`@dataclass`)

### 文件命名
- 蛇形命名法 (`snake_case`)
- 模块名简洁明确
- 测试文件以 `test_` 开头

## 🚨 已知问题和注意事项

1. **API限制**: B站API有速率限制，需要合理控制请求频率
2. **数据库**: 当前使用SQLite，生产环境需要考虑升级
3. **异步处理**: 确保所有I/O操作都使用异步模式
4. **错误处理**: 网络请求需要完善的超时和重试机制

## 📞 快速启动新任务

### 如果你要实现新功能：
1. 检查 `docs/PROGRESS_TRACKING.md` 了解当前状态
2. 参考 `docs/ARCHITECTURE.md` 了解系统设计
3. 查看对应模块的TODO注释了解需要实现的接口
4. 更新进度文档记录你的修改

### 如果你要修复问题：
1. 检查日志输出和错误信息
2. 参考 `tests/` 目录中的测试用例
3. 使用 `main.py` 作为调试入口点

---

**📋 使用建议**: 建议AI在开始新任务前，先阅读相关的具体模块代码和注释，了解当前的实现状态和预期接口。 