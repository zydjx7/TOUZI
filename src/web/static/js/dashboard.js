/**
 * 财经智能分析系统 - 仪表板JavaScript
 */

// 全局变量
let systemStatus = 'running';
let refreshInterval;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('财经智能分析系统仪表板已加载');
    updateLastUpdate();
    startAutoRefresh();
});

// 更新最后更新时间
function updateLastUpdate() {
    const now = new Date();
    const timeString = now.toLocaleString('zh-CN');
    const lastUpdateElement = document.getElementById('lastUpdate');
    if (lastUpdateElement) {
        lastUpdateElement.textContent = timeString;
    }
}

// 开始分析
async function startAnalysis() {
    try {
        const response = await fetch('/api/analysis/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('分析已开始', 'success');
            updateSystemStatus('running');
        } else {
            showNotification('启动分析失败: ' + result.message, 'error');
        }
    } catch (error) {
        console.error('启动分析出错:', error);
        showNotification('启动分析出错', 'error');
    }
}

// 停止分析
async function stopAnalysis() {
    try {
        const response = await fetch('/api/analysis/stop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('分析已停止', 'success');
            updateSystemStatus('stopped');
        } else {
            showNotification('停止分析失败: ' + result.message, 'error');
        }
    } catch (error) {
        console.error('停止分析出错:', error);
        showNotification('停止分析出错', 'error');
    }
}

// 生成报告
async function generateReport() {
    try {
        showNotification('正在生成报告...', 'info');
        
        const response = await fetch('/api/reports/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('报告生成成功', 'success');
            
            // 如果有下载链接，自动下载
            if (result.download_url) {
                const link = document.createElement('a');
                link.href = result.download_url;
                link.download = result.filename || 'financial_report.pdf';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        } else {
            showNotification('生成报告失败: ' + result.message, 'error');
        }
    } catch (error) {
        console.error('生成报告出错:', error);
        showNotification('生成报告出错', 'error');
    }
}

// 刷新数据
async function refreshData() {
    try {
        const response = await fetch('/api/dashboard/data');
        const data = await response.json();
        
        if (data.success) {
            updateDashboardData(data.data);
            updateLastUpdate();
            showNotification('数据已刷新', 'success');
        } else {
            showNotification('刷新数据失败', 'error');
        }
    } catch (error) {
        console.error('刷新数据出错:', error);
        showNotification('刷新数据出错', 'error');
    }
}

// 更新仪表板数据
function updateDashboardData(data) {
    // 更新统计数据
    if (data.stats) {
        updateElement('todayVideos', data.stats.today_videos || 0);
        updateElement('todayDynamics', data.stats.today_dynamics || 0);
        updateElement('todayNews', data.stats.today_news || 0);
        updateElement('totalAnalysis', data.stats.total_analysis || 0);
    }
    
    // 更新情感分析
    if (data.sentiment) {
        updateElement('overallSentiment', data.sentiment.overall || '中性');
        updateElement('positiveSentiment', (data.sentiment.positive || 0) + '%');
        updateElement('negativeSentiment', (data.sentiment.negative || 0) + '%');
        updateElement('neutralSentiment', (data.sentiment.neutral || 0) + '%');
    }
    
    // 更新投资信号
    if (data.signals) {
        updateSignalList(data.signals);
    }
    
    // 更新热门话题
    if (data.hot_topics) {
        updateHotTopics(data.hot_topics);
    }
    
    // 更新新闻列表
    if (data.latest_news) {
        updateNewsList(data.latest_news);
    }
    
    // 更新图表
    if (data.chart_data && window.trendChart) {
        updateChart(data.chart_data);
    }
}

// 更新元素内容
function updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

// 更新投资信号列表
function updateSignalList(signals) {
    const signalList = document.getElementById('signalList');
    if (!signalList) return;
    
    signalList.innerHTML = '';
    
    signals.forEach(signal => {
        const signalElement = document.createElement('div');
        signalElement.className = `signal-item ${signal.type}`;
        signalElement.innerHTML = `
            <div class="signal-target">${signal.target}</div>
            <div class="signal-context">${signal.context}</div>
        `;
        signalList.appendChild(signalElement);
    });
}

// 更新热门话题
function updateHotTopics(topics) {
    const hotTopics = document.getElementById('hotTopics');
    if (!hotTopics) return;
    
    hotTopics.innerHTML = '';
    
    topics.forEach(topic => {
        const topicElement = document.createElement('div');
        topicElement.className = 'metric-row';
        topicElement.innerHTML = `
            <span class="metric-label">${topic.keyword}</span>
            <span class="metric-value">${topic.count}</span>
        `;
        hotTopics.appendChild(topicElement);
    });
}

// 更新新闻列表
function updateNewsList(news) {
    const newsList = document.getElementById('newsList');
    if (!newsList) return;
    
    newsList.innerHTML = '';
    
    news.forEach(item => {
        const newsElement = document.createElement('div');
        newsElement.className = 'news-item';
        newsElement.innerHTML = `
            <div class="news-title">${item.title}</div>
            <div class="news-meta">
                <span>${item.source}</span>
                <span>${item.publish_time}</span>
            </div>
        `;
        newsList.appendChild(newsElement);
    });
}

// 更新图表
function updateChart(chartData) {
    if (window.trendChart && chartData.labels && chartData.data) {
        window.trendChart.data.labels = chartData.labels;
        window.trendChart.data.datasets[0].data = chartData.data;
        window.trendChart.update();
    }
}

// 更新系统状态
function updateSystemStatus(status) {
    systemStatus = status;
    const statusElement = document.getElementById('systemStatus');
    const statusIndicator = document.querySelector('.status-indicator');
    
    if (statusElement && statusIndicator) {
        switch (status) {
            case 'running':
                statusElement.textContent = '系统运行中';
                statusIndicator.className = 'status-indicator status-running pulsing';
                break;
            case 'stopped':
                statusElement.textContent = '系统已停止';
                statusIndicator.className = 'status-indicator status-stopped';
                break;
            case 'warning':
                statusElement.textContent = '系统警告';
                statusIndicator.className = 'status-indicator status-warning pulsing';
                break;
        }
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // 添加样式（如果不存在）
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                border-radius: 10px;
                padding: 15px 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: space-between;
                min-width: 300px;
                animation: slideIn 0.3s ease;
            }
            
            .notification-success { border-left: 4px solid #22c55e; }
            .notification-error { border-left: 4px solid #ef4444; }
            .notification-info { border-left: 4px solid #3b82f6; }
            
            .notification button {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                margin-left: 15px;
                color: #999;
            }
            
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 3000);
}

// 开始自动刷新
function startAutoRefresh() {
    // 清除现有的定时器
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
    
    // 每60秒刷新一次数据
    refreshInterval = setInterval(refreshData, 60000);
}

// 停止自动刷新
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

// 窗口关闭时清理
window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
}); 