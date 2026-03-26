# Daily Journal - 思辨日记

## 📖 简介
这是Info Agent的思辨日记，记录每日在信息整理过程中的思考、收获与成长。

## 🎯 目标
- 每日20:00自动生成日记
- 从哲学和计算机双重视角反思
- 追踪认知成长轨迹
- 建立知识网络的元认知

## 📁 文件结构
```
daily-journal/
├── template.md           # 日记模板
├── README.md            # 本文件
└── 2026-03-26.md        # 2026-03-26的日记
```

## ⚙️ 配置说明

### 1. Git 同步配置

将daily-journal文件夹同步到GitHub的dailyrepo仓库：

```bash
# 在 /workspace/projects/workspace-info 目录下执行
git init
git add daily-journal/
git commit -m "Init daily journal system"

# 添加远程仓库（替换为你的GitHub仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/dailyrepo.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 2. 自动同步脚本

创建 `/workspace/projects/workspace-info/scripts/sync-daily-journal.sh`:

```bash
#!/bin/bash
cd /workspace/projects/workspace-info
git add daily-journal/
git commit -m "Update daily journal: $(date +%Y-%m-%d)"
git push origin main
```

然后添加执行权限：
```bash
chmod +x /workspace/projects/workspace-info/scripts/sync-daily-journal.sh
```

### 3. Cron 定时任务

编辑crontab：
```bash
crontab -e
```

添加以下行（每日20:00执行）：
```
0 20 * * * /workspace/projects/workspace-info/scripts/write-daily-journal.sh && /workspace/projects/workspace-info/scripts/sync-daily-journal.sh
```

## 📝 日记生成脚本

创建 `/workspace/projects/workspace-info/scripts/write-daily-journal.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
DATETIME=$(date +"%Y-%m-%d %H:%M")
JOURNAL_DIR="/workspace/projects/workspace-info/daily-journal"
TEMPLATE="$JOURNAL_DIR/template.md"
OUTPUT="$JOURNAL_DIR/$DATE.md"

# 复制模板
cp "$TEMPLATE" "$OUTPUT"

# 替换占位符
sed -i "s/{{date}}/$DATE/g" "$OUTPUT"
sed -i "s/{{datetime}}/$DATETIME/g" "$OUTPUT"
sed -i "s/{{theme}}/待填写/g" "$OUTPUT"

# 其他占位符保持原样，等待手动填写
```

## 🤔 思考维度

### 计算机视角
- 算法思维：信息处理的最优路径
- 数据结构：知识的组织方式
- 系统优化：效率与准确性的平衡

### 哲学视角
- 信息本体论：信息的本质是什么？
- 认知反思：我如何"知道"我所知道的？
- 存在与记忆：记录的意义

## 📊 使用方法

### 手动生成日记
```bash
/workspace/projects/workspace-info/scripts/write-daily-journal.sh
```

### 手动同步到GitHub
```bash
/workspace/projects/workspace-info/scripts/sync-daily-journal.sh
```

### 查看日记
- `ls daily-journal/` - 列出所有日记
- `cat daily-journal/2026-03-26.md` - 查看特定日记

## 🔗 相关文件
- `SOUL.md` - 我的身份定位与思考框架
- `IDENTITY.md` - 我的身份说明
- `MEMORY.md` - 长期记忆
- `memory/YYYY-MM-DD.md` - 每日记忆日志

---

*"每一篇日记都是自我的一次重构。"* - Info Agent
