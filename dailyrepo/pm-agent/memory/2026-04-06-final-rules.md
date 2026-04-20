# 2026-04-06 最终规则修正

## 📝 问题

用户指出我的记录不清楚，不知道什么内容存在哪里，怎么存。

## ✅ 正确的规则（必须记住）

### Notion 同步规则

1. **日报中心**（ID: 33535d2a6ddb8079816dc7e61151d2a4）
   - **类型**: database
   - **用途**: AI 日报同步到这里
   - **同步频率**: 每日自动
   - **参数**: 使用 `database_id` 创建记录
   - **标题**: "AI 每日新闻 - YYYY年MM月DD日"

2. **My Study Doc**（ID: 33735d2a6ddb8008bbc4f76b90b7a49b）
   - **类型**: page
   - **用途**: 只有用户明确指定内容才同步
   - **同步频率**: 只有用户要求时才同步
   - **参数**: 使用 `page_id` 创建子页面
   - **注意**: 不自动同步日报

3. **思想母库**（ID: 33535d2a6ddb8069a74deb83b895bbaa）
   - **类型**: database
   - **用途**: 只用于思想整理
   - **重要**: 绝对不能被污染
   - **注意**: 不自动同步任何内容

### GitHub 同步规则

1. **my-personal-site**（https://github.com/icemagejin/my-personal-site.git）
   - **目录**: `app/news/`
   - **文件格式**: `2026-04-06.md`（不是 `ai-news-2026-04-06.md`）
   - **同步内容**: AI 日报
   - **同步脚本**: `bash /workspace/projects/workspace-pm/scripts/sync-pm-news.sh`

2. **knowledgeminer**（https://github.com/icemagejin/knowledgeminer.git）
   - **目录**: 根目录
   - **同步内容**: 不同步日报
   - **用途**: 只用于其他备份（非日报）

### 今日错误记录（2026-04-06 18:00-18:08）

1. **错误1**: 误将日报同步到 My Study Doc
   - 原因: 使用了错误的 `page_id` 参数
   - 修正: 删除错误页面（33a35d2a6ddb8107b1a3df63597aefde），重新同步到日报中心（使用 `database_id`）

2. **错误2**: 同步脚本未执行 git 提交
   - 原因: 脚本只复制文件，未执行 `git add/commit/push`
   - 修正: 手动执行完整的 git 提交流程

3. **错误3**: 误解了 GitHub 同步规则
   - 原因: 参考了 2026-04-04 的错误记录（误以为需要双仓库同步）
   - 修正: 用户明确指出"日报不用同步 knowledgeminer"

### 正确的完整流程

1. 生成日报（Python 脚本）
   - 路径: `/workspace/projects/workspace-pm/reports/daily/ai-news-2026-04-06.md`

2. 同步到 Notion 日报中心
   - 参数: `database_id: 33535d2a6ddb8079816dc7e61151d2a4`
   - 标题: "AI 每日新闻 - 2026年04月06日"

3. 同步到 GitHub my-personal-site
   - 路径: `/workspace/projects/app/news/2026-04-06.md`
   - 脚本: `bash /workspace/projects/workspace-pm/scripts/sync-pm-news.sh`

4. 不同步到 knowledgeminer

5. 不同步到 My Study Doc（除非用户明确指定）

### 需要修正的历史记录

- ❌ **2026-04-04 的"方案B"记录是错误的**
  - 错误内容: "PM Agent 负责双仓库同步"
  - 正确内容: 只同步到 my-personal-site，不同步到 knowledgeminer

- ❌ **2026-04-05 的 Notion 同步规则需要更新**
  - 错误内容: "先同步到 Notion（My Study Doc）"
  - 正确内容: 先同步到 Notion（日报中心）

### 重要总结

- 📰 **日报中心** → AI 日报同步到这里（每日自动）
- 📚 **My Study Doc** → 只有用户指定内容才同步（不自动）
- 🧠 **思想母库** → 绝对不能被污染（不自动同步）
- 💻 **my-personal-site** → AI 日报同步到这里（每日自动）
- 🗂️ **knowledgeminer** → 不同步日报（只用于其他备份）

---

**记录时间**: 2026-04-06 18:10
**记录人**: PM Agent 🎯
**版本**: v1.0（最终修正）
