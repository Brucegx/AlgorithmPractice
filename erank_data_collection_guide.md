# eRank数据采集指南

## 从eRank获取数据的详细步骤

### ⚠️  重要：eRank没有一键导出功能！

eRank**不提供**CSV导出或API，所有数据需要**手动复制**。

---

## 步骤1: 登录eRank

```
网址: https://erank.com/
登录你的付费账号
```

---

## 步骤2: 进入Keyword Tool

```
导航: eRank首页 → Tools → Keyword Tool
或直接访问: https://erank.com/keyword-tool
```

---

## 步骤3: 搜索关键词

### 示例：搜索 "smart pet feeder"

```
1. 在搜索框输入: smart pet feeder
2. 选择市场: US (或其他目标市场)
3. 点击 "Search"
```

---

## 步骤4: 查看数据（需要记录的字段）

eRank会显示以下数据，**逐个记录到CSV**：

### 📊 关键数据字段

| eRank字段名 | CSV列名 | 示例值 | 说明 |
|------------|---------|--------|------|
| **Search Volume** | Search Volume | 12,500 | 月搜索量 |
| **Competition** | Competition | High/Medium/Low | 竞争程度 |
| **Clicks** | Clicks | 850 | 月点击数 |
| **Engagement** | Engagement | 6.8% | 参与度/点击率 |

### 可选字段（如果你的付费版提供）：

| eRank字段 | 作用 |
|-----------|------|
| **Avg Sales** | 平均销量（如果有） |
| **Trend** | 趋势（上升/下降） |
| **Related Keywords** | 相关关键词建议 |

---

## 步骤5: 复制数据到CSV

### 方法A: 直接填写Excel/Google Sheets

```
1. 打开 product_keywords.csv (或Excel)
2. 填写第一行：
   Product: Smart Pet Feeder
   Keyword: smart pet feeder
   Search Volume: 12500 (去掉逗号)
   Competition: High
   Clicks: 850
   Engagement: 6.8%
   Keyword Type: Primary
```

### 方法B: 用笔记本临时记录

```
关键词: smart pet feeder
搜索量: 12500
竞争: High
点击: 850
参与度: 6.8%

(然后一次性粘贴到CSV)
```

---

## 步骤6: 重复查询其他关键词

**同一个产品的其他关键词变体：**

```
1. 搜索: "automatic pet feeder"
   → 记录数据到CSV第2行（Product名称相同）

2. 搜索: "wifi pet feeder"
   → 记录数据到CSV第3行

3. 搜索: "pet feeder with camera"
   → 记录数据到CSV第4行
```

---

## 实际示例：完整流程

### 产品：Smart Pet Feeder

#### 1. 主关键词
```
eRank搜索: "smart pet feeder"
结果:
- Search Volume: 12,500
- Competition: High
- Clicks: 850
- Engagement: 6.8%

→ 填入CSV:
Smart Pet Feeder,smart pet feeder,12500,High,850,6.8%,Primary
```

#### 2. 变体关键词1
```
eRank搜索: "automatic pet feeder"
结果:
- Search Volume: 8,900
- Competition: Medium
- Clicks: 620
- Engagement: 7.0%

→ 填入CSV:
Smart Pet Feeder,automatic pet feeder,8900,Medium,620,7.0%,Variant
```

#### 3. 变体关键词2
```
eRank搜索: "wifi pet feeder"
结果:
- Search Volume: 5,600
- Competition: Low
- Clicks: 380
- Engagement: 6.8%

→ 填入CSV:
Smart Pet Feeder,wifi pet feeder,5600,Low,380,6.8%,Variant
```

#### 4. 长尾关键词
```
eRank搜索: "pet feeder with camera"
结果:
- Search Volume: 3,200
- Competition: Medium
- Clicks: 210
- Engagement: 6.5%

→ 填入CSV:
Smart Pet Feeder,pet feeder with camera,3200,Medium,210,6.5%,Long-tail
```

---

## 最终CSV文件

```csv
Product,Keyword,Search Volume,Competition,Clicks,Engagement,Keyword Type
Smart Pet Feeder,smart pet feeder,12500,High,850,6.8%,Primary
Smart Pet Feeder,automatic pet feeder,8900,Medium,620,7.0%,Variant
Smart Pet Feeder,wifi pet feeder,5600,Low,380,6.8%,Variant
Smart Pet Feeder,pet feeder with camera,3200,Medium,210,6.5%,Long-tail
```

---

## 时间估算

**单个关键词：**
- eRank搜索: 10秒
- 复制数据: 20秒
- 填入CSV: 10秒
- **总计: ~40秒/关键词**

**一个产品（4个关键词）：**
- **总计: ~3分钟**

**效率提升技巧：**
1. 用两个屏幕：一个显示eRank，一个显示CSV
2. 用键盘快捷键复制粘贴
3. 一次性查询多个关键词，然后批量填写

---

## 常见问题

### Q: eRank有没有导出功能？
**A:** ❌ 没有。即使付费版也不提供CSV导出。

### Q: 能用Selenium自动化吗？
**A:** 技术上可行，但：
- ⚠️ 违反eRank TOS
- ⚠️ 账号可能被封
- ⚠️ 不推荐

### Q: 如果数据字段名不一样怎么办？
**A:** eRank界面可能更新，以下是常见的别名：

| 我们的CSV列名 | eRank可能的叫法 |
|-------------|---------------|
| Search Volume | Searches, Monthly Searches |
| Competition | Comp, Competition Level |
| Clicks | Monthly Clicks |
| Engagement | CTR, Click Rate, Eng% |

### Q: 必须填所有字段吗？
**A:** 最少需要：
- Keyword ✅ 必须
- Search Volume ✅ 必须
- Competition ✅ 必须
- Clicks ⚠️ 推荐
- Engagement ⚠️ 推荐
- Keyword Type ⚠️ 推荐（帮助分析）

---

## 下一步

数据收集完成后，运行分析：

```bash
# 仅分析eRank数据
python improved_product_validator.py analyze product_keywords.csv

# 同时调用Etsy API获取竞品数据
python improved_product_validator.py analyze product_keywords.csv your_etsy_api_key
```
