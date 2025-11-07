# Etsy API完整解决方案 - 告别截图的时代

## 🎯 你的痛点 vs 解决方案

### ❌ 之前的痛苦流程：
```
1. 在Etsy网站创建listing
2. 遇到一堆属性选项
3. 逐个截图
4. 发给GPT询问
5. 手动填写
6. 重复N次...
```

**时间消耗**: 30-60分钟/listing
**错误率**: 高（容易遗漏）
**可扩展性**: 差（无法批量处理）

### ✅ 现在的自动化流程：
```
1. 运行脚本获取类目的所有属性要求（一次性）
2. AI自动分析产品描述并填充属性
3. API自动创建listing
4. API自动上传图片
5. 完成！
```

**时间消耗**: 2-3分钟/listing
**错误率**: 低（AI智能填充）
**可扩展性**: 高（可批量处理）

---

## 📋 答案：Etsy确实提供完整的API！

### ✅ Etsy API v3 支持的功能：

| 功能 | API端点 | 你的用途 |
|------|---------|---------|
| **获取类目属性** | `GET /seller-taxonomy/nodes/{id}/properties` | 一次性获取所有属性要求，保存为JSON |
| **创建listing** | `POST /shops/{shop_id}/listings` | 通过代码上传listing |
| **上传图片** | `POST /shops/{shop_id}/listings/{listing_id}/images` | 自动上传产品图片 |
| **更新listing** | `PUT /shops/{shop_id}/listings/{listing_id}` | 修改listing信息 |
| **批量操作** | 循环调用API | 批量创建多个listing |

---

## 🚀 完整工作流程

### Phase 1: 一次性设置（获取API访问权限）

#### 1.1 创建Etsy App

```
访问: https://www.etsy.com/developers/your-apps
→ "Create a New App"
→ 填写信息
→ 获得API Key (Keystring)
```

#### 1.2 设置OAuth 2.0

Etsy使用OAuth 2.0认证，需要：

**Scopes（权限）**:
- `listings_r` - 读取listings
- `listings_w` - 创建/编辑listings
- `listings_d` - 删除listings（可选）

**获取Access Token**:
```python
# Etsy OAuth 2.0流程（简化版）
# 1. 重定向用户到Etsy授权页面
# 2. 用户授权
# 3. Etsy回调你的redirect_uri
# 4. 用code换取access_token

# 详细流程见Etsy官方文档：
# https://developer.etsy.com/documentation/essentials/authentication
```

**注意**: Access Token会过期，需要用refresh token刷新。

---

### Phase 2: 获取类目的所有属性要求（解决截图问题）

#### 2.1 搜索你的产品类目

```python
from etsy_listing_automation import EtsyListingAutomation

automation = EtsyListingAutomation(
    etsy_api_key="your_api_key",
    etsy_access_token="your_access_token"
)

# 搜索类目
categories = automation.search_taxonomy("pet supplies")

for cat in categories:
    print(f"{cat['name']} (ID: {cat['id']})")

# 输出示例：
# Pet Supplies (ID: 1234)
# Pet Bowls & Feeders (ID: 5678)
# Automatic Pet Feeders (ID: 9012)
```

#### 2.2 获取类目的所有属性

```python
# 选择taxonomy_id
taxonomy_id = 9012  # Automatic Pet Feeders

# 获取所有属性要求
metadata = automation.get_taxonomy_properties(taxonomy_id)

# 保存到文件（以后就不需要截图了！）
automation.save_taxonomy_metadata(
    taxonomy_id,
    "pet_feeder_attributes.json"
)
```

**输出文件内容示例**:
```json
{
  "taxonomy_id": 9012,
  "taxonomy_name": "Automatic Pet Feeders",
  "properties": [
    {
      "property_id": 46803063641,
      "name": "primary_color",
      "display_name": "Primary color",
      "is_required": true,
      "is_multivalued": false,
      "possible_values": [
        {"value_id": 1, "name": "Beige"},
        {"value_id": 2, "name": "Black"},
        {"value_id": 3, "name": "Blue"},
        ...
      ]
    },
    {
      "property_id": 46803063642,
      "name": "material",
      "display_name": "Material",
      "is_required": true,
      "is_multivalued": true,
      "max_values_allowed": 3,
      "possible_values": [
        {"value_id": 100, "name": "Plastic"},
        {"value_id": 101, "name": "Stainless Steel"},
        {"value_id": 102, "name": "Ceramic"},
        ...
      ]
    },
    ...
  ],
  "required_count": 5,
  "optional_count": 12
}
```

**关键信息**:
- `is_required`: 是否必填
- `is_multivalued`: 能否选多个值
- `max_values_allowed`: 最多选几个
- `possible_values`: 所有可选值

**现在你有了完整的属性清单，不需要再截图了！**

---

### Phase 3: AI自动填充属性（解决手动填写问题）

#### 3.1 准备产品描述

```python
product_description = """
Smart Pet Feeder with WiFi

Features:
- Automatic feeding schedule via smartphone app
- Stainless steel bowl (dishwasher safe)
- Holds up to 6 cups of dry food
- Black color with silver accents
- Made from BPA-free plastic
- Size: 12" x 8" x 10"
- Perfect for cats and small dogs
- 1-year warranty

Package includes:
- 1x Smart feeder base
- 1x Stainless steel bowl
- 1x Power adapter
- 1x User manual
"""
```

#### 3.2 AI自动分析并填充

```python
# AI会自动：
# 1. 阅读产品描述
# 2. 分析每个属性的要求
# 3. 从可选值中选择最合适的
# 4. 给出置信度和理由

filled_properties = automation.ai_fill_properties(
    product_description,
    metadata['properties']
)

# 输出示例：
# {
#   "primary_color": {
#     "value_ids": [2],
#     "values": ["Black"],
#     "confidence": "high",
#     "reasoning": "Product explicitly states 'Black color'"
#   },
#   "material": {
#     "value_ids": [100, 101],
#     "values": ["Plastic", "Stainless Steel"],
#     "confidence": "high",
#     "reasoning": "Base is plastic, bowl is stainless steel"
#   },
#   "size": {
#     "value_ids": [205],
#     "values": ["Medium"],
#     "confidence": "medium",
#     "reasoning": "12x8x10 inches suggests medium size"
#   }
# }
```

**AI的优势**:
- 理解上下文（"black color with silver accents" → primary: black, secondary: silver）
- 自动选择合适的value_id
- 处理多值属性（material可以是plastic + stainless steel）
- 给出置信度（你可以review低置信度的）

---

### Phase 4: 通过API创建listing

#### 4.1 创建draft listing

```python
listing = automation.create_draft_listing(
    shop_id=12345678,  # 你的店铺ID
    taxonomy_id=9012,
    title="Smart Pet Feeder with WiFi - Automatic Feeding",
    description=product_description,
    price=49.99,
    quantity=10,
    who_made="i_did",          # 或"someone_else", "collective"
    when_made="made_to_order", # 或"2020_2024", "2010_2019"等
    properties=filled_properties
)

# 返回：
# {
#   'listing_id': 987654321,
#   'state': 'draft',
#   'url': 'https://www.etsy.com/listing/987654321',
#   ...
# }
```

#### 4.2 上传图片

```python
# 上传主图
automation.upload_listing_image(
    shop_id=12345678,
    listing_id=listing['listing_id'],
    image_path="product_main.jpg",
    rank=1  # 第1张图片
)

# 上传更多图片
for i, image_path in enumerate(['angle1.jpg', 'angle2.jpg', 'detail.jpg'], 2):
    automation.upload_listing_image(
        shop_id=12345678,
        listing_id=listing['listing_id'],
        image_path=image_path,
        rank=i
    )
```

#### 4.3 发布listing

```python
# Draft listing创建后，你可以：
# 1. 在Etsy后台review
# 2. 通过API直接发布

# 发布API（需要listings_w权限）：
# PUT /shops/{shop_id}/listings/{listing_id}
# Body: {"state": "active"}
```

---

## 💡 高级用法

### 批量创建listings

```python
# 假设你有一个产品列表
products = [
    {
        "title": "Smart Pet Feeder - Black",
        "description": "...",
        "price": 49.99,
        "images": ["black_main.jpg", "black_angle.jpg"]
    },
    {
        "title": "Smart Pet Feeder - White",
        "description": "...",
        "price": 49.99,
        "images": ["white_main.jpg", "white_angle.jpg"]
    },
    # ... 更多产品
]

# 批量创建
for product in products:
    # 1. AI填充属性
    properties = automation.ai_fill_properties(
        product['description'],
        metadata['properties']
    )

    # 2. 创建listing
    listing = automation.create_draft_listing(
        shop_id=SHOP_ID,
        taxonomy_id=taxonomy_id,
        title=product['title'],
        description=product['description'],
        price=product['price'],
        quantity=10,
        properties=properties
    )

    # 3. 上传图片
    for rank, image_path in enumerate(product['images'], 1):
        automation.upload_listing_image(
            shop_id=SHOP_ID,
            listing_id=listing['listing_id'],
            image_path=image_path,
            rank=rank
        )

    print(f"✅ {product['title']} created!")
```

**结果**: 10个产品 → 20分钟完成（vs 5-10小时手动）

---

### 使用eRank数据自动生成描述

```python
# 结合你之前的eRank分析工具

# 1. 从eRank获取热门关键词
keywords = ["smart pet feeder", "automatic feeder", "wifi pet feeder"]

# 2. 生成SEO优化的描述
seo_description = f"""
{keywords[0].title()}

Perfect {keywords[1]} for busy pet parents!

Features:
- WiFi enabled ({keywords[2]})
- Automatic scheduling
- Smartphone control

🐾 Keep your pets fed on schedule, even when you're away!
"""

# 3. AI填充属性
properties = automation.ai_fill_properties(seo_description, metadata['properties'])

# 4. 创建listing
listing = automation.create_draft_listing(..., description=seo_description)
```

---

## 🔧 完整代码示例

### 示例1: 快速创建单个listing

```python
#!/usr/bin/env python3
import os
from etsy_listing_automation import EtsyListingAutomation

# 配置
ETSY_API_KEY = os.environ['ETSY_API_KEY']
ETSY_ACCESS_TOKEN = os.environ['ETSY_ACCESS_TOKEN']
CLAUDE_API_KEY = os.environ['ANTHROPIC_API_KEY']
SHOP_ID = int(os.environ['ETSY_SHOP_ID'])

# 初始化
automation = EtsyListingAutomation(
    etsy_api_key=ETSY_API_KEY,
    etsy_access_token=ETSY_ACCESS_TOKEN,
    claude_api_key=CLAUDE_API_KEY
)

# 产品信息
product = {
    "taxonomy_id": 9012,  # Automatic Pet Feeders
    "title": "Smart Pet Feeder with WiFi - Black",
    "description": """
    Smart Pet Feeder with WiFi
    - Automatic feeding schedule
    - Stainless steel bowl
    - Black color
    - Holds 6 cups
    - Perfect for cats and dogs
    """,
    "price": 49.99,
    "quantity": 10,
    "images": ["main.jpg", "angle1.jpg", "detail.jpg"]
}

# 1. 获取属性要求
metadata = automation.get_taxonomy_properties(product['taxonomy_id'])

# 2. AI填充属性
properties = automation.ai_fill_properties(
    product['description'],
    metadata['properties']
)

# 3. 创建listing
listing = automation.create_draft_listing(
    shop_id=SHOP_ID,
    taxonomy_id=product['taxonomy_id'],
    title=product['title'],
    description=product['description'],
    price=product['price'],
    quantity=product['quantity'],
    who_made="i_did",
    when_made="made_to_order",
    properties=properties
)

# 4. 上传图片
for rank, image_path in enumerate(product['images'], 1):
    automation.upload_listing_image(
        shop_id=SHOP_ID,
        listing_id=listing['listing_id'],
        image_path=image_path,
        rank=rank
    )

print(f"✅ Listing created: {listing['url']}")
```

---

## 📊 API限制和成本

### API Rate Limits

```
Etsy API v3限制：
- 每秒：10次请求
- 每天：10,000次请求（免费）

建议：
- 添加延迟（0.1-0.2秒/请求）
- 使用exponential backoff处理429错误
```

### OAuth Access Token

```
- Access Token有效期：3600秒（1小时）
- Refresh Token有效期：90天
- 需要实现token自动刷新机制
```

### 成本分析

```
Etsy API：免费（在限制内）
Claude API：
- 每个listing约5K tokens（属性填充）
- 成本：$0.02-0.03/listing
- 100个listing：$2-3

vs 手动：
- 时间成本：100 listings × 30分钟 = 50小时
- 按$20/小时计 = $1000

ROI：节省$997+
```

---

## ⚠️ 重要注意事项

### 1. OAuth认证复杂性

Etsy的OAuth 2.0流程较复杂，需要：
- 注册应用获得client_id和client_secret
- 实现OAuth回调处理
- 管理token刷新

**建议**: 使用现成的OAuth库（如`requests-oauthlib`）

### 2. 属性验证

```python
# AI填充的属性可能需要验证
# 建议添加validation层

def validate_properties(filled_properties, property_definitions):
    """验证AI填充的属性是否符合要求"""
    for prop_name, prop_data in filled_properties.items():
        # 检查value_ids是否在possible_values中
        # 检查multivalued限制
        # 检查required属性是否都填写
        pass
```

### 3. 图片要求

```
Etsy图片要求：
- 最小尺寸：2000 × 2000 px
- 格式：JPEG, PNG, GIF
- 大小：<10MB
- 至少1张图片
```

### 4. 分类选择

```python
# Taxonomy ID很重要，选错类目会导致：
# - 属性不匹配
# - 搜索排名低
# - 可能被Etsy标记

# 建议：
# 1. 仔细搜索类目
# 2. 查看类目的完整路径
# 3. 确认属性要求匹配你的产品
```

---

## 🎯 vs 你之前的方法

| 方面 | 之前（截图+手动） | 现在（API+AI） |
|------|----------------|---------------|
| **获取属性** | 逐个截图 | 一次性API调用 |
| **时间** | 10-15分钟 | 2秒 |
| **准确性** | 依赖人眼 | JSON格式，完整 |
| **可复用** | 需要重复截图 | 保存JSON，永久使用 |
| **填充属性** | 逐个判断 | AI自动分析 |
| **时间** | 15-20分钟 | 3-5秒 |
| **错误率** | 高 | 低（AI理解上下文） |
| **创建listing** | 手动网页操作 | API自动创建 |
| **时间** | 10-15分钟 | 5秒 |
| **批量处理** | ❌ 不可能 | ✅ 轻松批量 |
| **总时间/listing** | 35-50分钟 | 2-3分钟 |
| **可扩展性** | 无法扩展 | 可处理成百上千 |

---

## 🚀 立即开始

### Step 1: 设置环境

```bash
# 安装依赖
pip install requests anthropic

# 设置环境变量
export ETSY_API_KEY="your_api_key"
export ETSY_ACCESS_TOKEN="your_access_token"
export ANTHROPIC_API_KEY="your_claude_key"
export ETSY_SHOP_ID="12345678"
```

### Step 2: 获取你的第一个类目的属性

```bash
python etsy_listing_automation.py get-properties 9012
```

### Step 3: 运行完整demo

```bash
python etsy_listing_automation.py demo
```

---

## 📞 下一步

我可以帮你：

1. **设置OAuth认证**
   - 详细的OAuth 2.0流程
   - Token管理和刷新

2. **定制化脚本**
   - 针对你的产品类型
   - 集成你的eRank数据

3. **批量上传工具**
   - CSV输入 → 批量创建listings
   - 图片批处理

4. **测试和调试**
   - 测试API调用
   - 处理错误情况

**告诉我你想从哪里开始！**
