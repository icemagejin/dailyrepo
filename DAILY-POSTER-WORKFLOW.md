# 八字合盘海报工作流 - DESIGN.md 版本

## 概述
根据 DESIGN.md 视觉设计系统重新设计的八字合盘海报，采用深色主题，遵循标准色彩、字体、间距系统。

## 设计系统映射

### 色彩系统
- **背景色**: #1A1A2E (Background) - 深色背景
- **表面色**: #16213E (Surface) - 卡片容器
- **主文字**: #FFFFFF (Text Primary) - 核心信息
- **次要文字**: #A0A0B0 (Text Secondary) - 日期信息
- **辅助文字**: #6B7280 (Text Tertiary) - 宜忌信息
- **强调色**: #6C5CE7 (Primary) - 可用于装饰元素
- **微纹理**: #232530 (介于 Background 和 Surface 之间)

### 字体系统
- **字体家族**: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- **超大数字**: Display 2: 48px / SemiBold / Line-height 1.2
- **日期信息**: Body Large: 18px / Regular / Line-height 1.6
- **宜忌文字**: Body: 16px / Regular / Line-height 1.6

### 间距系统
- **元素间距**: xl (32px) - 主要元素之间
- **区块间距**: 2xl (48px) - 大区块之间
- **内边距**: lg (24px) - 内容区域内边距

### 视觉层次
- **第一层级**: 日期数字 - #FFFFFF, SemiBold
- **第二层级**: 日期信息 - #A0A0B0, Regular
- **第三层级**: 宜忌信息 - #6B7280, Regular

---

## 完整工作流

### 1. 获取今日干支
- 计算年柱、月柱、日柱
- 从运势网站获取宜忌
- 提取关键词

### 2. 八字合盘分析
- 弗尼八字：乙丑 丙戌 戊申
- 将今日八字与弗尼八字合盘
- 分析五行相生相克
- 生成针对性宜忌

### 3. 生成对仗宜忌
- 根据合盘结果，改写成对仗的宜忌
- 要求：字数相等（6-8字），结构相同，对仗工整
- 示例：
  - 宜：交易立券可成
  - 忌：争执冲突莫起

### 4. 生成海报（核心！）
**工具**: `python3 /workspace/projects/workspace-aesthetic/poster_design_system.py YYYY-MM-DD`

**输出路径**: `posters/poster-{date}.jpg`

**尺寸**: 1080x1920

### 5. 发送到美学群
- 目标: `oc_95076f564f595dc80ae416c8221ad806`

---

## 设计规范

### 布局策略
- **居中对齐**: 所有信息居中对齐
- **纵向层次**: 日期数字 → 日期信息 → 宜忌
- **信息聚合**: 日期信息聚合在一起（月份+星期+年份）
- **微纹理背景**: 深色背景 + 微妙纹理

### 色彩方案
- **背景**: #1A1A2E - 深色背景
- **微纹理**: #232530 - 比背景稍深
- **日期数字**: #FFFFFF - 主文字
- **日期信息**: #A0A0B0 - 次要文字
- **宜忌文字**: #6B7280 - 辅助文字

### 字体大小
- **日期数字**: 根据容器高度动态计算，建议 48px (Display 2)
- **日期信息**: 18px (Body Large)
- **宜忌文字**: 16px (Body)

### 间距规则
- **数字到日期**: 32px (xl)
- **日期到宜忌**: 48px (2xl)
- **宜忌内部**: 24px (lg)

---

## 与微纹理版本的对比

| 维度 | 微纹理版 | **DESIGN.md 版** |
|------|---------|-----------------|
| 背景 | 暖白 (245, 243, 240) | **深色 (#1A1A2E)** |
| 主题 | 浅色系 | **深色系** |
| 文字色 | 深色文字 | **浅色文字** |
| 字体 | Noto Sans | **Inter + 系统字体** |
| 字号体系 | 自定义 | **标准字号体系** |
| 间距 | 自定义像素值 | **标准间距系统** |
| 视觉层次 | 简单 | **三层级清晰** |
| 设计系统 | 无 | **遵循 DESIGN.md** |
| 一致性 | 单次设计 | **全局一致** |

---

## 技术要点

### 色彩转换
```python
# DESIGN.md 色彩到 RGB
BACKGROUND = (26, 26, 46)  # #1A1A2E
TEXT_PRIMARY = (255, 255, 255)  # #FFFFFF
TEXT_SECONDARY = (160, 160, 176)  # #A0A0B0
TEXT_TERTIARY = (107, 114, 128)  # #6B7280
TEXTURE_COLOR = (35, 37, 48)  # #232530
```

### 字体加载
```python
# 优先使用 Inter，回退到系统字体
font_names = ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"]
```

### 间距计算
```python
# 使用 DESIGN.md 间距系统
XL = 32  # 主要元素间距
XL2 = 48  # 大区块间距
LG = 24  # 内边距
```

### 文字定位
```python
# 使用 textbbox 获取实际位置
bbox = draw.textbbox((x, y), text, font=font)
actual_bottom = bbox[3]
next_y = actual_bottom + XL  # 使用标准间距
```

---

## AI 代理提示指南

### 生成海报时
1. **使用 DESIGN.md 色彩系统**，不要随意创造新颜色
2. **遵循标准字号体系**（Display 2, Body Large, Body）
3. **使用标准间距值**（xl, 2xl, lg）
4. **保持三层视觉层次**清晰
5. **信息聚合**，避免分散
6. **使用 Inter 字体**，保持一致性

### 生成代码时
1. **使用常量**定义颜色和间距
2. **遵循 DESIGN.md 的命名约定**
3. **保持可维护性**，易于调整
4. **遵循响应式设计原则**

---

_创建时间: 2026-04-06_
_基于: DESIGN.md v1.0_
