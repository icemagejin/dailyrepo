# DESIGN.md 使用指南

## 什么是 DESIGN.md？

DESIGN.md 是一个对 AI 友好的 Markdown 文件，用于记录和同步设计规则（调色板、字体、间距、组件模式），让 AI 在生成 UI 时能自动保持品牌一致性。

它的逻辑类似于开发领域的 Agents.md：通过一个人类和 AI 都能读写的配置文件，为 AI 设定规则。

---

## 为什么需要 DESIGN.md？

### 问题
没有 DESIGN.md，AI 生成的 10 个页面可能有 10 种不同的按钮样式。你需要在每次生成 UI 时反复描述：
- "品牌色是 #6C5CE7"
- "标题用 32px Bold"
- "按钮圆角是 24px"

### 解决方案
有了 DESIGN.md，你只需要：
1. 创建一次 DESIGN.md 文件
2. 放在项目根目录
3. AI 自动读取并遵循这些规则
4. 所有生成的 UI 保持一致

---

## 如何使用

### 方法 1：复制示例文件
```bash
# 将示例文件复制为你的 DESIGN.md
cp DESIGN.md.example DESIGN.md

# 根据你的品牌需求修改内容
vim DESIGN.md
```

### 方法 2：从 awesome-design-md 仓库获取
awesome-design-md 仓库包含了从真实网站（如 Claude、Linear、Vercel、Stripe、Apple）提取的 DESIGN.md 文件。

```bash
# 克隆仓库（需要 GitHub 访问权限）
git clone https://github.com/awesome-design-md/awesome-design-md.git

# 选择你喜欢的设计系统
cd awesome-design-md/vercel
cp DESIGN.md ../../your-project/
```

### 方法 3：手动编写
参考 `DESIGN.md.example` 的结构，创建你自己的 DESIGN.md 文件。

---

## DESIGN.md 文件结构

### 必需部分
1. **色彩系统** - 定义所有使用的颜色
2. **字体规则** - 字号、字重、行高
3. **间距系统** - 标准间距值
4. **组件规范** - 按钮、卡片等组件样式

### 可选部分
- 圆角半径
- 阴影系统
- 动画效果
- 响应式断点
- 设计原则
- AI 代理提示指南

---

## 实际应用场景

### 场景 1：快速生成营销页面
```python
# 你只需要这样描述
prompt = """
生成一个 SaaS 定价页面，包含：
- 3 个价格层级
- 功能对比表
- 用户评价区域
"""

# AI 会自动：
# 1. 读取 DESIGN.md
# 2. 使用定义的颜色、字体、间距
# 3. 生成风格一致的 UI
```

### 场景 2：跨团队协作
```bash
# 设计师创建 DESIGN.md
# → 开发者读取并生成代码
# → 自动保持视觉一致性
```

### 场景 3：品牌一致性
```bash
# 多个项目使用同一个 DESIGN.md
# → 所有项目保持统一品牌形象
```

---

## 常见错误

### ❌ 错误：模糊描述
```markdown
## 色彩系统
- 主色: 使用品牌蓝色
- 强调色: 使用醒目的颜色
```

### ✅ 正确：具体数值
```markdown
## 色彩系统
- Primary: #6C5CE7
- Secondary: #00B894
- Accent: #FD79A8
```

### ❌ 错误：过度复杂
```markdown
## 所有可能的场景
# 不要试图在一个文件中涵盖所有场景
```

### ✅ 正确：从核心开始
```markdown
# 从核心颜色、字体和间距开始，然后逐步扩展
```

---

## 维护建议

1. **定期更新** - 随着产品迭代同步更新 DESIGN.md
2. **版本控制** - 使用 Git 跟踪 DESIGN.md 的变化
3. **团队协作** - 让设计师和开发者共同维护
4. **文档化** - 记录设计决策的原因

---

## 与 AI 工具集成

### Google Stitch
```bash
# Stitch 可以自动从 URL 提取设计系统并生成 DESIGN.md
# 也可以导入现有的 DESIGN.md 文件
```

### Claude Code / Cursor
```python
# 这些工具会自动读取项目根目录的 DESIGN.md
# 生成代码时自动遵循设计规范
```

### 其他 AI 设计工具
```markdown
# 大多数现代 AI 设计工具都支持 DESIGN.md
# 查看各自文档了解具体用法
```

---

## 示例 DESIGN.md 文件

仓库中提供了一个完整的 `DESIGN.md.example` 文件，包含：
- 完整的色彩系统
- 详细的字体规则
- 标准的间距系统
- 组件规范（按钮、卡片、输入框等）
- 动画效果
- 响应式断点
- 设计原则
- AI 代理提示指南

你可以直接复制并修改为你的设计系统。

---

## 参考资源

- [Google Stitch - DESIGN.md 概览](https://stitch.withgoogle.com/docs/design-md/overview/)
- [awesome-design-md 仓库](https://github.com/awesome-design-md/awesome-design-md)
- [DESIGN.md 深度解析](https://youmind.com/zh-CN/blog/google-stitch-design-md-ai-brand-consistency)

---

## 下一步

1. **阅读** `DESIGN.md.example` 了解标准格式
2. **修改** 为你的品牌创建自定义 DESIGN.md
3. **测试** 让 AI 生成 UI 验证效果
4. **迭代** 根据实际需求调整规范
5. **分享** 让团队成员使用统一的 DESIGN.md

---

## 贡献

如果你有改进建议或发现错误，欢迎提交 Issue 或 Pull Request。

---

_最后更新: 2026-04-06_
