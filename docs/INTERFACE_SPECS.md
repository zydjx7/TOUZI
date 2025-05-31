# 接口规范文档

## 📋 模块间接口定义

### 🗄 数据结构规范

#### VideoContent (视频内容)
```python
@dataclass
class VideoContent:
    bvid: str                    # B站视频ID
    title: str                   # 视频标题
    description: str             # 视频描述
    transcript: str              # 视频转录文本
    publish_time: datetime       # 发布时间
    up_name: str                # UP主名称
    view_count: int             # 播放数
    like_count: int             # 点赞数
    coin_count: int             # 投币数
    share_count: int            # 分享数
    tags: List[str]             # 标签列表
    content_hash: str           # 内容哈希
```

#### AnalysisResult (分析结果)
```python
@dataclass  
class AnalysisResult:
    content_id: str             # 内容ID
    content_type: str           # 内容类型 (video/dynamic/news)
    sentiment_score: float      # 情感分数 (-1到1)
    key_points: List[str]       # 关键观点
    investment_signals: List[Dict]  # 投资信号
    risk_level: str             # 风险等级 (低/中/高)
    confidence: float           # 置信度 (0到1)
    analysis_time: datetime     # 分析时间
```

#### InvestmentSignal (投资信号)
```python
@dataclass
class InvestmentSignal:
    signal_type: str            # 信号类型 (bullish/bearish/neutral)
    target: str                 # 目标对象 (股票/行业/市场)
    strength: float             # 信号强度 (0到1)
    reasoning: str              # 判断理由
    time_horizon: str           # 时间范围 (short/medium/long)
    confidence: float           # 置信度
```

---

## 🔌 核心模块接口

### ContentAnalyzer (内容分析器)
```python
class ContentAnalyzer:
    def analyze_sentiment(self, text: str) -> float:
        """
        情感分析
        参数: text - 待分析文本
        返回: float - 情感分数 (-1:极度负面, 0:中性, 1:极度正面)
        """
        
    def extract_key_points(self, text: str) -> List[str]:
        """
        提取关键观点
        参数: text - 待分析文本
        返回: List[str] - 关键观点列表
        """
        
    def detect_investment_signals(self, text: str) -> List[Dict]:
        """
        检测投资信号
        参数: text - 待分析文本
        返回: List[Dict] - 投资信号列表
        """
        
    def assess_risk_level(self, sentiment_score: float, signals: List[Dict]) -> str:
        """
        评估风险等级
        参数: sentiment_score - 情感分数, signals - 投资信号
        返回: str - 风险等级 ("低"/"中"/"高")
        """
```

### NewsAggregator (新闻聚合器)
```python
class NewsAggregator:
    async def fetch_latest_news(self, category: str) -> List[NewsContent]:
        """
        获取最新新闻
        参数: category - 新闻分类 ("financial"/"geopolitical")
        返回: List[NewsContent] - 新闻列表
        """
        
    async def fetch_financial_news(self) -> List[NewsContent]:
        """获取财经新闻"""
        
    async def fetch_geopolitical_news(self) -> List[NewsContent]:
        """获取地缘政治新闻"""
```

### ReportGenerator (报告生成器)
```python
class ReportGenerator:
    def generate_daily_report(self) -> str:
        """
        生成日报
        返回: str - HTML格式的报告内容
        """
        
    def generate_summary_statistics(self) -> Dict:
        """
        生成统计摘要
        返回: Dict - 包含各种统计数据的字典
        """
```

---

## 🌐 Web API接口规范

### 分析控制接口
```typescript
// 启动分析
POST /api/analysis/start
Request: {}
Response: {
    success: boolean,
    message: string
}

// 停止分析  
POST /api/analysis/stop
Request: {}
Response: {
    success: boolean,
    message: string
}

// 获取分析状态
GET /api/analysis/status
Response: {
    success: boolean,
    status: "running" | "stopped" | "error",
    last_update: string
}
```

### 数据获取接口
```typescript
// 获取仪表板数据
GET /api/dashboard/data
Response: {
    success: boolean,
    data: {
        stats: {
            today_videos: number,
            today_dynamics: number,
            today_news: number,
            total_analysis: number
        },
        sentiment: {
            overall: string,
            positive: number,
            negative: number,
            neutral: number
        },
        signals: Array<{
            type: "bullish" | "bearish",
            target: string,
            context: string
        }>,
        hot_topics: Array<{
            keyword: string,
            count: number
        }>,
        latest_news: Array<{
            title: string,
            source: string,
            publish_time: string
        }>,
        chart_data: {
            labels: string[],
            data: number[]
        }
    }
}
```

### 报告生成接口
```typescript
// 生成报告
POST /api/reports/generate
Request: {
    type?: "daily" | "weekly" | "monthly",
    format?: "html" | "pdf"
}
Response: {
    success: boolean,
    message: string,
    download_url?: string,
    filename?: string
}
```

---

## 🔄 数据流接口

### 爬虫 → 数据库
```python
# BilibiliCrawler 输出格式
VideoInfo = {
    "bvid": str,
    "title": str, 
    "desc": str,
    "pubdate": int,
    "stat": {
        "view": int,
        "like": int,
        "coin": int,
        "share": int
    },
    "tags": List[Dict]
}
```

### 数据库 → 分析器
```python
# DatabaseManager 查询输出格式
ContentRecord = {
    "id": str,
    "type": str,  # "video" | "dynamic" | "news"
    "title": str,
    "content": str,
    "publish_time": str,
    "metadata": Dict  # 扩展字段
}
```

### 分析器 → 报告生成器
```python
# ContentAnalyzer 分析结果格式
AnalysisOutput = {
    "content_id": str,
    "sentiment_score": float,
    "key_points": List[str],
    "signals": List[InvestmentSignal],
    "risk_level": str,
    "confidence": float
}
```

---

## 📧 通知接口规范

### EmailNotifier
```python
class EmailNotifier:
    def send_report(self, to_email: str, subject: str, 
                   content: str, attachments: List[str] = None) -> bool:
        """发送报告邮件"""
        
    def send_alert(self, to_email: str, message: str) -> bool:
        """发送警报邮件"""
```

---

## 🔧 工具模块接口

### TextProcessor
```python
class TextProcessor:
    def clean_text(self, text: str) -> str:
        """清理文本，去除无用字符"""
        
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """提取关键词"""
        
    def segment_text(self, text: str) -> List[str]:
        """中文分词"""
```

### FinancialCalculator  
```python
class FinancialCalculator:
    def calculate_return_rate(self, initial: float, final: float) -> float:
        """计算收益率"""
        
    def calculate_volatility(self, prices: List[float]) -> float:
        """计算波动率"""
```

---

## ⚠️ 错误处理规范

### 异常类型
```python
class AnalysisError(Exception):
    """分析过程中的错误"""
    
class CrawlerError(Exception):
    """爬虫错误"""
    
class DatabaseError(Exception):
    """数据库操作错误"""
```

### 错误响应格式
```typescript
ErrorResponse = {
    success: false,
    error: {
        code: string,     // 错误代码
        message: string,  // 错误信息
        details?: any     // 详细信息
    }
}
```

---

## 📝 接口版本控制

- 当前API版本: `v1`
- 接口URL前缀: `/api/v1/`
- 向后兼容性: 保持至少2个版本的兼容
- 废弃通知: 提前30天通知接口变更 