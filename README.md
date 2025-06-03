# 财经智能分析系统 (Financial Intelligence Analysis System)

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Development Status](https://img.shields.io/badge/status-40%25%20Complete-orange)
![Framework](https://img.shields.io/badge/framework-Flask-red)

**🚀 AI驱动的智能财经分析平台**

*通过自动化数据采集、AI内容分析和智能信号检测，为投资决策提供数据支持*

</div>

---

## 📋 项目概览

这是一个**模块化、智能化**的财经分析系统，整合了多种先进技术：

- 🎥 **智能内容爬取** - 自动化采集B站财经UP主的视频、动态和评论数据
- 🧠 **AI内容分析** - 基于大语言模型的情感分析和投资观点提取
- 📰 **实时新闻聚合** - 多源财经和地缘政治新闻的智能聚合
- 📊 **投资信号检测** - 智能识别市场机会和风险预警
- 📈 **可视化仪表板** - 现代化Web界面，实时展示分析结果
- 📧 **自动化报告** - 定时生成并推送投资分析报告

## 🏗 系统架构

```
财经智能分析系统
├── 📁 src/                    # 核心源代码
│   ├── 🔧 core/              # 业务逻辑层
│   │   ├── crawler.py        # ✅ B站爬虫 (已完成)
│   │   ├── database.py       # ✅ 数据库管理 (已完成)
│   │   ├── analyzer.py       # 🔄 内容分析 (开发中)
│   │   ├── news_aggregator.py # 📋 新闻聚合 (规划中)
│   │   └── report_generator.py # 📋 报告生成 (规划中)
│   ├── 🌐 web/               # Web应用层
│   │   ├── app.py           # ✅ Flask应用 (框架完成)
│   │   ├── api.py           # 🔄 REST API (开发中)
│   │   ├── templates/       # ✅ 前端模板 (已完成)
│   │   └── static/          # ✅ 静态资源 (已完成)
│   └── 🛠 utils/             # 工具模块
│       ├── email_notifier.py    # 📋 邮件通知
│       ├── text_processor.py    # 📋 文本处理
│       └── financial_calculator.py # 📋 金融计算
├── 📚 docs/                   # 完整文档体系
├── 🧪 tests/                  # 测试框架
├── 📊 data/                   # 数据存储
└── 📝 logs/                   # 系统日志
```

**图例**: ✅ 已完成 | 🔄 开发中 | 📋 规划中

## 🚀 快速开始

### 1. 环境配置

```bash
# 克隆项目
git clone https://github.com/zydjx7/TOUZI.git
cd TOUZI

# 创建虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 自动安装依赖和配置
python setup.py
```

### 2. 配置参数

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件 (必须配置)
# - UP主列表信息
# - 邮箱服务配置  
# - API密钥设置
nano .env
```

### 3. 启动系统

```bash
# 方式一：启动完整系统
python main.py

# 方式二：仅启动Web界面
python -m src.web.app
```

### 4. 访问界面

打开浏览器访问 **http://localhost:5000** 查看智能仪表板

---

## 💡 核心功能

### 🎯 数据采集
- **B站爬虫**: 支持视频列表、详情、字幕、评论的全量采集
- **新闻聚合**: 多平台财经资讯的实时获取和去重
- **数据管道**: 异步处理，高效稳定的数据流水线

### 🧠 智能分析  
- **情感分析**: AI驱动的多维度情感倾向分析
- **关键词提取**: 智能识别投资热点和主题
- **信号检测**: 基于语义分析的投资机会识别
- **风险评估**: 智能化的风险等级评估体系

### 📊 可视化展示
- **实时仪表板**: 现代化响应式设计，支持移动端
- **数据图表**: 基于Chart.js的交互式数据可视化
- **趋势分析**: 多时间维度的趋势展示和对比

### 📈 报告系统
- **自动化报告**: 日报/周报/月报的智能生成
- **邮件推送**: 定时推送个性化分析报告
- **PDF导出**: 专业格式的报告文档生成

## 🔧 技术栈

| 分类 | 技术 | 用途 |
|------|------|------|
| **后端** | Python 3.8+, AsyncIO | 主要开发语言和异步框架 |
| **Web框架** | Flask, Jinja2 | Web应用和模板引擎 |
| **数据库** | SQLite | 轻量级数据存储 |
| **前端** | Bootstrap, Chart.js | 响应式UI和数据可视化 |
| **AI/ML** | OpenAI API, jieba | 大语言模型和中文分词 |
| **数据处理** | pandas, numpy | 数据分析和数值计算 |

## 📊 项目进度

| 模块 | 完成度 | 状态 | 说明 |
|------|--------|------|------|
| 🏗 **基础架构** | 100% | ✅ | 项目结构、配置、日志系统 |
| 🕷 **数据爬取** | 80% | ✅ | B站爬虫核心功能完成 |
| 🗄 **数据存储** | 90% | ✅ | 数据模型和基础操作完成 |
| 🌐 **Web界面** | 70% | ✅ | 仪表板UI和前端交互完成 |
| 🧠 **内容分析** | 20% | 🔄 | 算法框架完成，核心逻辑开发中 |
| 📰 **新闻聚合** | 10% | 📋 | 架构设计完成，待实现 |
| 📊 **报告生成** | 0% | 📋 | 框架设计中 |
| 📧 **邮件通知** | 0% | 📋 | 待开发 |
| 🧪 **测试框架** | 10% | 📋 | 基础框架搭建 |

**总体完成度**: 40%

## 📖 文档指南

我们提供了完整的文档体系，帮助开发者快速上手：

| 文档 | 描述 | 链接 |
|------|------|------|
| 📋 **项目概述** | 项目目标、功能和技术栈 | [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) |
| 🏗 **系统架构** | 整体架构和模块设计 | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 🔌 **接口规范** | API接口和数据结构定义 | [INTERFACE_SPECS.md](docs/INTERFACE_SPECS.md) |
| 📊 **进度跟踪** | 详细的开发进度和计划 | [PROGRESS_TRACKING.md](docs/PROGRESS_TRACKING.md) |
| 💻 **开发指南** | 编码规范和最佳实践 | [DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md) |
| 🤝 **协作模板** | AI助手协作流程 | [COLLABORATION_TEMPLATE.md](docs/COLLABORATION_TEMPLATE.md) |

## 🛡 注意事项

### ⚠️ 合规使用
- 严格遵守B站使用条款，合理控制请求频率
- 尊重内容创作者的知识产权
- 本系统仅供学习和研究用途

### 🔒 数据安全
- 系统不存储任何个人敏感信息
- 所有配置信息通过环境变量管理
- 支持数据加密和访问控制

### ⚖️ 免责声明
- 本系统生成的分析结果仅供参考
- 投资有风险，决策需谨慎
- 不承担任何投资损失责任

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. **Fork** 项目到你的账户
2. **创建** 功能分支: `git checkout -b feature/AmazingFeature`
3. **提交** 你的修改: `git commit -m 'Add some AmazingFeature'`
4. **推送** 到分支: `git push origin feature/AmazingFeature`
5. **创建** Pull Request

### 开发规范
- 遵循 PEP 8 代码风格
- 添加完整的类型提示和文档字符串
- 编写对应的单元测试
- 更新相关文档

## 📞 支持与联系

- 📧 **问题反馈**: [GitHub Issues](https://github.com/zydjx7/TOUZI/issues)
- 💬 **技术讨论**: [GitHub Discussions](https://github.com/zydjx7/TOUZI/discussions)
- 📚 **详细文档**: 查看 `docs/` 目录下的完整文档

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<div align="center">

**🌟 如果这个项目对你有帮助，请给个Star支持！**

Made with ❤️ by AI & Human Collaboration

</div>