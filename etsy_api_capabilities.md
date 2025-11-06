# Etsy API能力分析

## Etsy官方API v3 - 详细数据清单

### ✅ 可以获取的数据

#### 1. 商品信息（Listing）
```json
{
  "listing_id": 123456,
  "title": "Handmade Leather Wallet",
  "description": "Full product description...",
  "price": {
    "amount": 4500,  // 单位：分（cents）
    "currency_code": "USD"
  },
  "quantity": 10,
  "state": "active",
  "tags": ["wallet", "leather", "handmade"],
  "materials": ["leather", "thread"],
  "who_made": "i_did",
  "when_made": "made_to_order",
  "taxonomy_id": 123,
  "url": "https://www.etsy.com/listing/123456"
}
```

#### 2. 用户互动数据
```json
{
  "num_favorers": 1250,      // ✅ 收藏数
  "views": 8540,             // ✅ 浏览数（仅限自己店铺）
  "creation_timestamp": 1234567890
}
```

#### 3. 店铺信息（Shop）
```json
{
  "shop_id": 123,
  "shop_name": "CoolLeatherShop",
  "title": "Handmade Leather Goods",
  "announcement": "Welcome to my shop",
  "currency_code": "USD",
  "listing_active_count": 45,
  "digital_listing_count": 0
}
```

#### 4. 评论（Reviews）
```json
{
  "rating": 5,
  "review": "Great quality!",
  "created_timestamp": 1234567890,
  "buyer": {
    "user_id": 456
  }
}
```

#### 5. 图片
```json
{
  "url_75x75": "https://...",
  "url_170x135": "https://...",
  "url_570xN": "https://...",
  "url_fullxfull": "https://..."
}
```

### ❌ 不能获取的数据

```
❌ 销量数据（Sales Volume）
   - Etsy严格保密
   - API完全不提供

❌ 店铺收入（Revenue）
   - 只有店主能看到

❌ 其他店铺的浏览数（Views）
   - 只能看自己店铺的

❌ 转化率（Conversion Rate）
   - 商业机密

❌ 广告数据（Ads Performance）
   - 只有店主可见

❌ 精确搜索排名
   - 搜索结果是动态的
```

### 🔢 销量估算方法（非官方）

由于API不提供销量，只能通过间接数据估算：

```python
# 方法1：收藏数估算
月销量 ≈ 收藏数 ÷ 10

# 方法2：评论数估算
总销量 ≈ 评论数 × 50
# 假设：2%的买家会留评论

# 方法3：综合估算
if 收藏数 > 1000:
    估算月销量 = 收藏数 ÷ 8
elif 收藏数 > 100:
    估算月销量 = 收藏数 ÷ 12
else:
    估算月销量 = 收藏数 ÷ 15

# 准确度：±50%（仅供参考）
```

### 💡 Etsy API的实际价值

#### 对产品验证有用的数据：

1. **价格分布分析** ✅
   - 获取竞品价格
   - 计算平均价、价格区间
   - 制定定价策略

2. **市场需求指标** ✅
   - 收藏数 = 用户喜爱度
   - 收藏数高 = 需求旺盛
   - 可以排序找出爆款

3. **竞争程度** ✅
   - 搜索关键词返回多少商品
   - 商品数量 = 竞争激烈程度

4. **标签/关键词研究** ✅
   - 看热门商品用什么tags
   - 优化自己的listing

5. **评论分析** ✅
   - 提取痛点/卖点
   - 了解用户需求
   - 改进产品描述

#### 对产品验证价值有限：

1. **无法验证销量** ❌
   - 这是最关键的指标
   - 只能靠估算
   - 误差较大

2. **无法评估利润率** ❌
   - 不知道别人成本
   - 只能猜测

### 🆚 Etsy API vs eRank

| 数据类型 | Etsy API | eRank |
|---------|----------|-------|
| **关键词搜索量** | ❌ 无 | ✅ 有（估算） |
| **商品价格** | ✅ 精确 | ⚠️ 需手动查看 |
| **收藏数** | ✅ 精确 | ⚠️ 需手动查看 |
| **销量** | ❌ 无 | ✅ 有（估算） |
| **竞争度** | ⚠️ 间接计算 | ✅ 直接显示 |
| **趋势** | ❌ 无 | ✅ 有 |
| **SEO建议** | ❌ 无 | ✅ 有 |

### 结论：最佳组合

```python
完整的产品验证工具链：

1. eRank（手动）
   → 关键词搜索量
   → 竞争度评分
   → 趋势分析

2. Etsy API（自动）
   → 竞品价格采集
   → 收藏数统计
   → 标签分析

3. Google Trends（自动）
   → 趋势验证
   → 季节性分析

三者结合 = 最完整的市场洞察
```
