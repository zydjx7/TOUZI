# 系统架构文档

## 🏗 整体架构

```
财经智能分析系统
├── 数据采集层 (Data Collection Layer)
│   ├── B站爬虫模块 (Bilibili Crawler)
│   └── 新闻聚合模块 (News Aggregator)
├── 数据存储层 (Data Storage Layer)
│   ├── SQLite数据库 (Database)
│   └── 缓存系统 (Cache)
├── 业务逻辑层 (Business Logic Layer)
│   ├── 内容分析器 (Content Analyzer)
│   ├── 投资信号检测器 (Signal Detector)
│   └── 报告生成器 (Report Generator)
├── 服务层 (Service Layer)
│   ├── Web应用 (Flask App)
│   ├── API接口 (REST API)
│   └── 任务调度器 (Task Scheduler)
└── 表现层 (Presentation Layer)
    ├── Web仪表板 (Dashboard)
    ├── 报告界面 (Reports)
    └── 邮件通知 (Email Notifications)
```

## 📊 数据流架构

### 数据采集流程
```
外部数据源 → 爬虫模块 → 数据清洗 → 数据库存储
    ↓
B站API/网站 → BilibiliCrawler → TextProcessor → Database
新闻网站   → NewsAggregator   → TextProcessor → Database
```

### 数据分析流程
```
数据库 → 内容分析 → 信号检测 → 结果存储 → 报告生成
   ↓        ↓         ↓         ↓         ↓
Database → Analyzer → Detector → Database → ReportGenerator
```

## 🔧 核心模块

### 1. 核心业务模块 (src/core/)
- **database.py** - 数据库管理和数据模型
- **crawler.py** - B站内容爬取（已完成）
- **analyzer.py** - 内容分析和情感分析（框架）
- **news_aggregator.py** - 新闻聚合（框架）
- **report_generator.py** - 报告生成（框架）

### 2. Web应用模块 (src/web/)
- **app.py** - Flask应用主体（框架）
- **api.py** - REST API接口（框架）
- **templates/** - HTML模板（已完成）
- **static/** - 静态资源（已完成）

### 3. 工具模块 (src/utils/)
- **email_notifier.py** - 邮件通知（框架）
- **text_processor.py** - 文本处理（框架）
- **financial_calculator.py** - 金融计算（框架）

## 🗄 数据模型

### 核心数据结构
```python
@dataclass
class VideoContent:
    bvid: str
    title: str
    description: str
    transcript: str
    publish_time: datetime
    up_name: str
    # ... 其他字段

@dataclass  
class AnalysisResult:
    content_id: str
    content_type: str
    sentiment_score: float
    investment_signals: List[Dict]
    risk_level: str
    confidence: float
```

## 🔌 接口设计

### API接口
- `POST /api/analysis/start` - 启动分析
- `POST /api/analysis/stop` - 停止分析
- `GET /api/analysis/status` - 获取状态
- `GET /api/dashboard/data` - 获取仪表板数据
- `POST /api/reports/generate` - 生成报告

### 内部模块接口
- 所有核心模块都有标准化的接口定义
- 异步操作使用 `async/await` 模式
- 错误处理统一使用日志记录

## 🔄 部署架构

### 开发环境
```
本地开发 → Python虚拟环境 → SQLite数据库
```

### 生产环境（规划）
```
服务器 → Docker容器 → PostgreSQL/MySQL → 反向代理(Nginx)
```

## 📁 文件结构
详见项目根目录的文件组织结构，采用标准的Python项目布局。 