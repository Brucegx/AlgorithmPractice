# PowerPoint技能使用指南

## 📦 来源
- **仓库**: https://github.com/anthropics/skills
- **位置**: `document-skills/pptx/`
- **许可**: Proprietary (见LICENSE.txt)

---

## 🎯 这个技能可以做什么？

这是Anthropic官方的PowerPoint技能，支持：

1. ✅ **创建新的PowerPoint** - 从零开始或使用模板
2. ✅ **编辑现有PowerPoint** - 修改内容、格式
3. ✅ **分析PowerPoint** - 提取文本、分析结构

---

## 📚 三种主要工作流程

### 1. 创建新PowerPoint（无模板）

**使用场景**: 从头创建全新演示文稿

**工作流程**:
```bash
1. 设计选择（颜色、字体、布局）
2. 创建HTML文件（每个幻灯片一个）
3. 使用html2pptx.js转换为PPTX
4. 生成缩略图验证
```

**特色**:
- 18种预设配色方案（从经典蓝到复古彩虹）
- 支持图表、表格
- 自动布局优化
- 视觉验证工具

**阅读文档**:
- `html2pptx.md` - HTML转PPTX的详细语法

---

### 2. 使用模板创建PowerPoint

**使用场景**: 使用现有模板创建新演示文稿

**工作流程**:
```bash
1. 分析模板（提取文本+生成缩略图）
   python -m markitdown template.pptx > template-content.md
   python scripts/thumbnail.py template.pptx

2. 创建模板清单（template-inventory.md）
   - 列出所有幻灯片（0-indexed）
   - 标注每个幻灯片的用途

3. 设计演示文稿大纲（outline.md）
   - 映射内容到模板幻灯片
   - 注意：幻灯片索引从0开始

4. 重新排列幻灯片
   python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52

5. 提取文本清单
   python scripts/inventory.py working.pptx text-inventory.json

6. 生成替换文本JSON
   - 基于text-inventory.json
   - 创建replacement-text.json

7. 应用替换
   python scripts/replace.py working.pptx replacement-text.json output.pptx
```

---

### 3. 编辑现有PowerPoint

**使用场景**: 修改现有PPTX文件

**工作流程**:
```bash
1. 解包PPTX（它是个ZIP文件）
   python ooxml/scripts/unpack.py input.pptx output_dir

2. 编辑XML文件
   - ppt/slides/slide1.xml（幻灯片内容）
   - ppt/notesSlides/notesSlide1.xml（演讲者备注）
   - ppt/theme/theme1.xml（主题）

3. 验证修改
   python ooxml/scripts/validate.py output_dir --original input.pptx

4. 重新打包
   python ooxml/scripts/pack.py output_dir final.pptx
```

**阅读文档**:
- `ooxml.md` - OOXML格式详细指南

---

## 🛠️ 实用工具

### 缩略图生成器
```bash
# 生成幻灯片缩略图网格（快速预览）
python scripts/thumbnail.py presentation.pptx

# 自定义列数
python scripts/thumbnail.py presentation.pptx --cols 4

# 自定义输出前缀
python scripts/thumbnail.py presentation.pptx my-analysis
```

**输出**:
- `thumbnails.jpg`（或`thumbnails-1.jpg`等）
- 默认5列，最多30张/网格
- 幻灯片标注为0-indexed（Slide 0, Slide 1...）

---

### 文本提取
```bash
# 提取所有文本为Markdown
python -m markitdown presentation.pptx > content.md
```

---

### 幻灯片转图片
```bash
# 1. 转PDF
soffice --headless --convert-to pdf presentation.pptx

# 2. PDF转JPEG
pdftoppm -jpeg -r 150 presentation.pdf slide

# 输出: slide-1.jpg, slide-2.jpg, ...
```

---

## 🎨 设计资源

### 18种预设配色方案

1. **Classic Blue**: 深海军蓝 + 银灰
2. **Teal & Coral**: 青绿 + 珊瑚红
3. **Bold Red**: 红色系渐变
4. **Warm Blush**: 淡紫 + 腮红粉
5. **Burgundy Luxury**: 酒红 + 金色
6. **Deep Purple & Emerald**: 紫色 + 翠绿
7. **Cream & Forest Green**: 奶油 + 森林绿
8. **Pink & Purple**: 粉色系
9. **Lime & Plum**: 酸橙 + 梅子
10. **Black & Gold**: 黑金配色
11. **Sage & Terracotta**: 鼠尾草绿 + 赤陶
12. **Charcoal & Red**: 炭灰 + 红
13. **Vibrant Orange**: 活力橙
14. **Forest Green**: 森林绿系
15. **Retro Rainbow**: 复古彩虹
16. **Vintage Earthy**: 复古大地色
17. **Coastal Rose**: 海岸玫瑰
18. **Orange & Turquoise**: 橙 + 青绿

### 布局建议

**图表/表格幻灯片**:
- ✅ **推荐**: 两栏布局（文字40% + 图表60%）
- ✅ **备选**: 全屏布局（图表占满）
- ❌ **避免**: 垂直堆叠（文字在上，图表在下）

**文字密集型**:
- 使用清晰的视觉层次
- 强对比度
- 一致的间距

---

## 📦 依赖安装

```bash
# Python包
pip install "markitdown[pptx]"
pip install defusedxml

# Node.js包
npm install -g pptxgenjs
npm install -g playwright
npm install -g react-icons react react-dom
npm install -g sharp

# 系统工具
sudo apt-get install libreoffice      # PDF转换
sudo apt-get install poppler-utils    # PDF转图片
```

---

## 💡 使用建议

### 对于你的电商产品验证项目

**场景1: 产品策略演示文稿**
```
1. 使用html2pptx创建新演示文稿
2. 选择合适的配色（如Teal & Coral for现代感）
3. 包含：
   - 封面（产品名称）
   - 市场分析（图表）
   - 竞品对比（表格）
   - 定价策略（数字展示）
   - 行动计划（时间线）
```

**场景2: 每周进度报告**
```
1. 创建模板（第一次）
2. 每周使用template工作流
3. 只替换文本和数据
4. 快速生成报告
```

---

## 🚀 快速开始

### 示例1: 创建简单演示文稿

```bash
# 1. 创建HTML幻灯片
# slide1.html
<div style="width: 720pt; height: 405pt; background: #1C2833; color: white;">
  <h1 style="text-align: center; padding-top: 150pt;">
    我的产品验证报告
  </h1>
</div>

# 2. 使用html2pptx.js转换（需要先阅读html2pptx.md了解详细语法）
# 3. 生成缩略图验证
python scripts/thumbnail.py output.pptx
```

---

## 📖 必读文档

在使用前，**必须**完整阅读相关文档：

1. **SKILL.md** (已读) - 总览和工作流程
2. **html2pptx.md** (~500行) - 创建新PPTX
3. **ooxml.md** (~500行) - 编辑现有PPTX

---

## ⚠️ 重要注意事项

1. **幻灯片索引从0开始**
   - 第1张幻灯片 = Slide 0
   - 第2张幻灯片 = Slide 1
   - 以此类推

2. **使用web-safe字体**
   - Arial, Helvetica, Times New Roman
   - Georgia, Courier New, Verdana
   - Tahoma, Trebuchet MS, Impact

3. **设计先行**
   - 先分析内容和受众
   - 选择合适的配色方案
   - 说明设计选择理由

4. **验证是关键**
   - 总是生成缩略图检查
   - 验证文本是否被截断
   - 检查对比度和可读性

---

## 🔗 相关资源

- **完整仓库**: https://github.com/anthropics/skills
- **PPTX技能路径**: `document-skills/pptx/`
- **脚本位置**: `document-skills/pptx/scripts/`

---

## 💬 想要什么帮助？

我可以帮你：

1. **立即创建演示文稿**
   - 给我内容，我用html2pptx创建
   - 选择配色方案和布局

2. **编辑现有PPTX**
   - 修改文本、格式
   - 添加幻灯片

3. **使用模板**
   - 分析模板
   - 创建基于模板的演示文稿

4. **为你的产品验证项目创建专用模板**
   - 设计符合你品牌的模板
   - 可重复使用的报告格式

**告诉我你需要什么样的演示文稿！**
