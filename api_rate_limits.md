# API限流（Rate Limiting）详解

## Etsy API v3 限流规则

### 官方限制

```
每小时限制：10,000次请求
每秒限制：无明确说明（建议 < 10 req/s）
```

### 实际影响

#### 场景1：小规模产品验证
```python
验证1个产品类目：
- 搜索关键词：1次请求
- 获取前50个商品：1次请求
- 获取每个商品详情：50次请求
- 获取店铺信息：50次请求

总计：~100次请求
时间：< 1分钟
状态：✅ 完全没问题
```

#### 场景2：中等规模研究
```python
验证10个产品类目：
- 每个类目100次请求
- 总计：1,000次请求

时间：~5-10分钟
状态：✅ 远低于限制（10,000/小时）
```

#### 场景3：大规模数据采集
```python
采集整个类目所有商品：
- 搜索结果可能有10,000+商品
- 每个商品详情：1次请求
- 总计：10,000+次请求

状态：⚠️ 接近或超过限制
解决：分批处理，每小时一批
```

### 限流响应处理

```python
import time
import requests

def call_etsy_api_with_retry(url, headers, max_retries=3):
    """
    带重试的API调用
    """
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 429:  # Too Many Requests
            # 检查Retry-After header
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"⚠️ 限流！等待 {retry_after} 秒...")
            time.sleep(retry_after)

        elif response.status_code == 403:
            print("❌ API Key无效或权限不足")
            return None

        else:
            print(f"❌ 错误 {response.status_code}")
            return None

    print("❌ 重试次数用尽")
    return None
```

### 最佳实践

```python
# 1. 添加延迟（礼貌性）
import time

for listing in listings:
    data = fetch_listing_details(listing_id)
    time.sleep(0.1)  # 100ms延迟，确保 < 10 req/s

# 2. 批量请求
# Etsy API某些端点支持批量获取
# 例如：一次请求获取多个listing

# 3. 缓存结果
import json

cache = {}

def fetch_with_cache(listing_id):
    if listing_id in cache:
        return cache[listing_id]

    data = fetch_from_api(listing_id)
    cache[listing_id] = data
    return data

# 4. 使用数据库存储
# 避免重复请求相同数据
```

## Google Trends 限流

### pytrends（非官方）

```
没有明确的官方限制，但会触发：

429 Too Many Requests：
- 请求太频繁
- 需要添加延迟（2-5秒）
- 可能需要proxy轮换

建议：
- 每次请求间隔 3-5秒
- 一天不超过 50次请求
- 使用随机User-Agent
```

```python
from pytrends.request import TrendReq
import time
import random

pytrends = TrendReq(hl='en-US', tz=360)

keywords_list = [["keyword1"], ["keyword2"], ["keyword3"]]

for keywords in keywords_list:
    try:
        pytrends.build_payload(keywords, timeframe='today 12-m')
        data = pytrends.interest_over_time()

        # 随机延迟 3-5秒
        time.sleep(random.uniform(3, 5))

    except Exception as e:
        print(f"错误：{e}")
        # 如果429错误，等待更长时间
        time.sleep(60)
```

## Google Keyword Planner 限流

```
通过Web界面使用：无明确限制
如果有API访问（需要Google Ads支出）：
- 取决于你的广告支出
- 支出越多，限制越宽松

实际：大多数用户是手动使用，无限流问题
```

## 限流总结

| API | 小时限制 | 实际影响 | 需要担心？ |
|-----|---------|---------|-----------|
| **Etsy API** | 10,000 | 产品验证：几乎无影响 | ❌ 不需要 |
| **Google Trends** | 不明确 | 需要加延迟 | ⚠️ 稍微注意 |
| **Google KWP** | 无（Web） | 手动使用无问题 | ❌ 不需要 |
| **eRank API** | 无（不存在） | N/A | N/A |

### 实际建议

**对于产品验证场景：**

```python
典型使用：
- 每天验证 3-5个产品
- 每个产品查询 50-100个竞品
- 总请求：300-500次/天

Etsy API限制：10,000次/小时
你的使用：< 500次/天

结论：✅ 完全不用担心限流
```

**什么时候需要担心？**

```
只有在以下情况：
1. 构建数据库（一次性采集数万商品）
2. 持续监控（每小时更新数千商品价格）
3. 提供服务（为多个用户提供数据）

对于个人产品验证：永远不会达到限制
```
