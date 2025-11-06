# 关键词搜索 - 快速开始指南

## 🎯 你的情况
- 有300个关键词
- 需要找相似关键词
- 小企业，预算有限

## ✅ 推荐方案

### 立即开始：方案1（Claude Prompt）

**成本：** ~$0.06/查询
**设置时间：** 5分钟
**适合：** 每天查询 < 20次

```bash
# 1. 安装依赖
pip install anthropic

# 2. 设置API key
export ANTHROPIC_API_KEY="your_key_here"

# 3. 运行
python keyword_finder_claude.py product_keywords.csv "pet feeder"

# 结果：
# - 5个最相似关键词
# - 为什么相似的解释
# - 市场洞察分析
# 成本：$0.06
```

---

### 如果成本成问题：方案2（本地免费）

**成本：** $0（完全免费）
**设置时间：** 首次2小时（之后秒级）
**适合：** 每天查询 > 20次

```bash
# 1. 安装依赖
pip install sentence-transformers scikit-learn

# 2. 首次运行（会下载模型，约80MB）
python keyword_finder_local.py product_keywords.csv "pet feeder"

# 结果：
# - 5个最相似关键词
# - 相似度评分
# 成本：$0
# 速度：<0.1秒
```

---

## 📊 成本对比

### 每月查询100次

| 方案 | 月成本 | 设置成本 | 总成本（第1个月） |
|------|--------|---------|-----------------|
| **Claude Prompt** | $6 | 0小时 | $6 |
| **本地向量** | $0 | 2小时 | $0 |

### 每月查询10次

| 方案 | 月成本 | 设置成本 | 总成本（第1个月） |
|------|--------|---------|-----------------|
| **Claude Prompt** | $0.60 | 0小时 | $0.60 ⭐ |
| **本地向量** | $0 | 2小时 | $0 |

---

## 🎯 决策树

```
你每天查询多少次？
│
├─ < 10次 → 用方案1（Claude）
│           成本可忽略不计
│
├─ 10-50次 → 先用方案1
│            如果月成本>$20，切换方案2
│
└─ > 50次 → 直接用方案2
            一次性投入，永久免费
```

---

## 💡 实际建议

### 对于小企业：

**第1周：** 用Claude方案
- 立即可用
- 成本极低（<$5）
- 测试是否满足需求

**第1个月：** 监控成本
- 如果 <$10/月 → 继续用Claude
- 如果 >$20/月 → 切换本地方案

**长期：**
- 偶尔用 → Claude（简单）
- 频繁用 → 本地（免费）

---

## 🚀 立即开始

### 选项A：5分钟快速测试（Claude）

```bash
# 1. 安装
pip install anthropic

# 2. 运行
export ANTHROPIC_API_KEY="sk-ant-xxx"
python keyword_finder_claude.py product_keywords.csv "smart pet feeder"

# 3. 看结果
# 如果满意 → 继续用
# 如果不满意 → 告诉我，我帮你调整
```

### 选项B：一次性设置（本地免费）

```bash
# 1. 安装（首次需要几分钟）
pip install sentence-transformers scikit-learn

# 2. 运行（首次会下载模型）
python keyword_finder_local.py product_keywords.csv "smart pet feeder"

# 3. 保存embeddings（避免重复计算）
# 下次运行会更快
```

---

## ❓ 常见问题

### Q1: 300个关键词需要用RAG吗？
**A:** ❌ 不需要！300个很小，直接放prompt就够了。

### Q2: 哪个方案更准确？
**A:** Claude方案稍微准确一些，因为它理解语义和意图。
本地方案纯粹基于向量相似度，但对大多数情况够用。

### Q3: 我可以两个都用吗？
**A:** ✅ 可以！
- 日常查询用本地方案（免费快速）
- 需要深度分析时用Claude方案（有解释）

### Q4: 如果我的关键词增加到1000个呢？
**A:** 两个方案都可以应对：
- Claude: 仍然可以放入prompt（10K tokens）
- 本地: 速度几乎不变（<0.2秒）

### Q5: 成本会失控吗？
**A:** ❌ 不会！
- Claude方案上限：假设每天查100次 = $6/天 = $180/月
- 如果达到这个量级，早就该切换本地方案了

---

## 📞 需要帮助？

**如果遇到问题：**

1. **Claude API错误** → 检查API key是否正确
2. **本地模型下载失败** → 检查网络，或换个时间重试
3. **结果不准确** → 告诉我具体情况，我帮你调整
4. **其他问题** → 直接问我

---

## 🎁 Bonus: 高级用法

### Claude方案：批量分析

```python
from keyword_finder_claude import KeywordFinder

finder = KeywordFinder(api_key, "keywords.csv")

# 分组归类
groups = finder.group_keywords([
    "smart pet feeder",
    "automatic pet feeder",
    "wifi pet feeder"
])

# 成本：$0.08
```

### 本地方案：自动聚类

```python
from keyword_finder_local import LocalKeywordFinder

finder = LocalKeywordFinder("keywords.csv")

# 自动分成5组
clusters = finder.cluster_keywords(n_clusters=5)

# 成本：$0
```

---

## ✅ 总结

**对于300个关键词的小企业：**

1. **立即开始：** 用Claude方案（$0.06/查询）
2. **如果成本>$20/月：** 切换本地方案（免费）
3. **不要用RAG：** 数据量太小，过度复杂

**最重要的是：先开始用，根据实际情况调整！**
