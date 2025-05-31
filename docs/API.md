# API 文档

## 接口概览

### 分析控制
- `POST /api/analysis/start` - 启动分析
- `POST /api/analysis/stop` - 停止分析
- `GET /api/analysis/status` - 获取分析状态

### 数据获取
- `GET /api/dashboard/data` - 获取仪表板数据

### 报告生成
- `POST /api/reports/generate` - 生成报告

## 详细说明

### 启动分析
```
POST /api/analysis/start
```

返回:
```json
{
  "success": true,
  "message": "分析已启动"
}
```

### 获取仪表板数据
```
GET /api/dashboard/data
```

返回:
```json
{
  "success": true,
  "data": {
    "stats": {},
    "sentiment": {},
    "signals": [],
    "hot_topics": [],
    "latest_news": []
  }
}
``` 