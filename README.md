# 首尔地铁Twitter数据爬取工具

这个工具使用Scweet库来爬取与首尔地铁相关的Twitter/X数据，支持按关键词和地理位置筛选。

## 功能特点

- 🚇 **专注首尔地铁**: 使用韩语关键词搜索首尔地铁相关推文
- 📍 **地理定位**: 使用geocode限制在首尔市范围内
- 🔄 **避免重复**: 支持断点续传，避免重复爬取相同数据
- 🚫 **无需登录**: 不需要Twitter账号登录
- 📊 **数据过滤**: 支持按点赞数、转发数、回复数过滤
- 💾 **自动保存**: 数据自动保存为CSV格式

## 安装依赖

首先安装所需的Python包：

```bash
git clone 
```

```bash
pip install -r requirements.txt
```

```bash
pip install zendriver
```

```bash
conda install typing_extensions  
```

```bash
pip install nodriver
```

## 使用方法

### 基础使用

直接运行脚本：

```bash
python test.py
```

### 参数配置

可以在`test.py`文件中修改以下配置：

#### 1. 搜索关键词
```python
metro_keywords = [
    '지하철',      # 地铁
    '서울지하철',   # 首尔地铁
    '전철',       # 电车
    # 可以添加更多关键词
]
```

#### 2. 地理范围
```python
# 首尔市中心，半径25公里
seoul_geocode = "37.5665,126.9780,25km"
```

#### 3. 时间范围
```python
since_date = "2024-01-01"  # 开始日期
until_date = "2024-12-31"  # 结束日期
```

#### 4. 过滤条件
```python
min_likes = 5      # 最少点赞数
min_retweets = 2   # 最少转发数
min_replies = 1    # 最少回复数
```

#### 5. 性能配置
```python
n_splits = 30        # 时间分割数 (影响爬取精度)
concurrency = 3      # 并发数 (建议2-5)
headless = True      # 无头模式 (提高效率)
```

## 输出数据

数据将保存在`seoul_metro_data/seoul_metro_tweets.csv`文件中，包含以下字段：

- `tweetId`: 推文ID
- `UserScreenName`: 用户名
- `UserName`: 显示名称
- `Timestamp`: 发布时间
- `Text`: 推文内容
- `Embedded_text`: 嵌入文本
- `Emojis`: 表情符号
- `Comments`: 评论数
- `Likes`: 点赞数
- `Retweets`: 转发数
- `Image link`: 图片链接
- `Tweet URL`: 推文链接

## 注意事项

1. **合法使用**: 请遵守Twitter的使用条款和相关法律法规
2. **爬取频率**: 不要设置过高的并发数，避免被限制
3. **时间范围**: 建议不要设置过长的时间范围，以免触发API限制
4. **断点续传**: 使用`resume=True`可以从上次中断处继续，避免重复爬取
5. **网络稳定**: 确保网络连接稳定，爬取过程可能需要较长时间

## 常见问题

### Q: 爬取速度很慢怎么办？
A: 可以适当增加`concurrency`参数（建议不超过5），或调整`scroll_ratio`参数。

### Q: 如何避免重复爬取？
A: 设置`resume=True`，脚本会自动检查已有数据并从断点继续。

### Q: 如何扩展到其他城市？
A: 修改`geocode`参数为其他城市的坐标，并调整相应的关键词。

### Q: 遇到错误怎么办？
A: 检查网络连接，降低并发数，或查看错误信息进行相应调整。

## 技术细节

- 使用nodriver作为浏览器驱动
- 支持代理配置
- 自动处理反爬虫机制
- 智能滚动和页面解析
- 并发处理提高效率

## 许可证

遵循Scweet库的MIT许可证。 