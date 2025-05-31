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
financial_intelligence_system/
├── README.md                    # 项目说明文档
├── requirements.txt             # 依赖包列表
├── config.py                   # 系统配置
├── main.py                     # 主程序入口
├── 
├── core/                       # 核心模块
├── web/                        # Web界面
├── utils/                      # 工具模块
├── data/                       # 数据存储
└── logs/                       # 日志文件
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/zydjx7/TOUZI.git
cd TOUZI

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的配置信息
```

### 2. 运行系统

```bash
# 启动主程序
python main.py

# 启动Web控制面板
python web/app.py
```

### 3. 访问控制面板

打开浏览器访问 `http://localhost:5000` 查看系统状态和分析结果。

## 注意事项

1. **合规使用**：请遵守B站的使用条款，避免过度频繁的请求
2. **数据隐私**：系统不会存储任何个人敏感信息
3. **投资风险**：本系统仅供参考，投资决策请谨慎
4. **API限制**：请注意各种API的调用限制

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

MIT License