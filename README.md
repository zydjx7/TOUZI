# 财经智能分析系统 (Financial Intelligence Analysis System)

## 项目简介

这是一个集成化的财经智能分析系统，主要功能包括：

- 🎥 **B站内容爬取**：自动爬取指定UP主的视频、动态和评论
- 🎯 **视频转文字**：将视频内容转换为文本进行分析
- 🤖 **AI智能分析**：基于大语言模型分析财经观点和投资机会
- 📰 **新闻聚合**：实时获取财经和地缘政治新闻
- 📊 **投资信号检测**：智能识别投资机会和风险
- 📧 **自动化报告**：生成分析报告并邮件发送
- 🌐 **Web控制面板**：可视化监控和控制系统运行

## 项目结构

```
TOUZI/
├── README.md                               # 项目说明文档
├── requirements.txt                        # 依赖包列表
├── main.py                                # 主程序入口
├── setup.py                               # 项目安装脚本
├── config.py                              # 系统配置文件
├── .env.example                           # 环境变量示例
├── 
├── src/                                   # 源代码目录
│   ├── __init__.py
│   ├── core/                              # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── crawler.py                     # B站爬虫模块
│   │   ├── analyzer.py                    # 内容分析模块
│   │   ├── database.py                    # 数据库管理
│   │   ├── news_aggregator.py             # 新闻聚合模块
│   │   └── report_generator.py            # 报告生成模块
│   ├── web/                               # Web界面
│   │   ├── __init__.py
│   │   ├── app.py                         # Flask应用
│   │   ├── api.py                         # API接口
│   │   ├── static/                        # 静态资源
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   └── templates/                     # HTML模板
│   │       ├── dashboard.html
│   │       ├── analysis.html
│   │       └── reports.html
│   └── utils/                             # 工具模块
│       ├── __init__.py
│       ├── email_notifier.py              # 邮件通知
│       ├── text_processor.py              # 文本处理
│       └── financial_calculator.py        # 金融计算
├── 
├── data/                                  # 数据存储目录
│   ├── cache/                             # 缓存文件
│   ├── reports/                           # 生成的报告
│   ├── transcripts/                       # 视频转录文本
│   ├── videos/                           # 视频文件
│   └── financial_analysis.db             # SQLite数据库
├── 
├── logs/                                  # 日志文件
├── tests/                                 # 测试文件
│   ├── __init__.py
│   ├── test_crawler.py
│   ├── test_analyzer.py
│   └── test_api.py
└── docs/                                  # 文档
    ├── API.md                             # API文档
    ├── CONFIG.md                          # 配置说明
    └── DEPLOY.md                          # 部署指南
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/zydjx7/TOUZI.git
cd TOUZI

# 运行安装脚本
python setup.py

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的配置信息
```

### 2. 配置系统

编辑 `config.py` 文件：
- 添加要监控的B站UP主信息
- 配置邮件和API密钥
- 调整分析参数

### 3. 运行系统

```bash
# 启动主程序
python main.py

# 启动Web控制面板
python -m src.web.app
```

### 4. 访问控制面板

打开浏览器访问 `http://localhost:5000` 查看系统状态和分析结果。

## 功能特性

### 数据收集
- **视频内容**：自动获取UP主的最新视频及详细信息
- **动态内容**：监控UP主的动态发布
- **评论分析**：收集关键评论数据
- **新闻聚合**：从多个财经新闻源获取信息

### 智能分析
- **情感分析**：识别内容的情感倾向
- **关键词提取**：自动提取重要财经术语
- **投资信号检测**：识别买入/卖出信号
- **风险评估**：评估投资风险等级

### 报告生成
- **日报**：每日投资机会汇总
- **周报**：周度投资趋势分析
- **月报**：月度市场总结

### Web控制面板
- **实时监控**：系统运行状态监控
- **数据可视化**：图表展示分析结果
- **手动控制**：手动触发分析任务
- **历史查询**：查看历史分析数据

## API接口

系统提供RESTful API接口，详见 [API文档](docs/API.md)

### 主要接口：
- `GET /api/status` - 获取系统状态
- `GET /api/analysis/latest` - 获取最新分析结果
- `POST /api/analysis/trigger` - 手动触发分析
- `GET /api/reports/{date}` - 获取指定日期的报告

## 配置说明

详细配置说明请参考 [配置文档](docs/CONFIG.md)

### 主要配置项：
- UP主列表配置
- 邮件服务配置
- API密钥配置
- 分析参数配置

## 部署指南

生产环境部署请参考 [部署文档](docs/DEPLOY.md)

## 注意事项

1. **合规使用**：请遵守B站的使用条款，避免过度频繁的请求
2. **数据隐私**：系统不会存储任何个人敏感信息
3. **投资风险**：本系统仅供参考，投资决策请谨慎
4. **API限制**：请注意各种API的调用限制

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

MIT License