#!/bin/bash

# Info Agent Daily Journal Sync Script
# 将思辨日记同步到GitHub

set -e

# 配置
WORKSPACE="/workspace/projects/workspace-info"
JOURNAL_DIR="$WORKSPACE/daily-journal"
COMMIT_MSG="Update daily journal: $(date +%Y-%m-%d)"

# 进入工作目录
cd "$WORKSPACE"

# 检查是否在git仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "⚠️  当前不是git仓库"
    echo "提示: 需要先初始化git并添加远程仓库"
    echo ""
    echo "执行以下命令:"
    echo "  git init"
    echo "  git add daily-journal/"
    echo "  git commit -m 'Init daily journal system'"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/dailyrepo.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    exit 1
fi

# 添加daily-journal目录
git add daily-journal/

# 检查是否有变更
if git diff --cached --quiet; then
    echo "✓ 没有新的变更，无需提交"
    exit 0
fi

# 提交变更
git commit -m "$COMMIT_MSG"

# 推送到远程仓库
if git push origin main 2>&1; then
    echo "✓ 日记已同步到GitHub"
    echo "✓ 提交信息: $COMMIT_MSG"
else
    echo "⚠️  推送失败，请检查网络连接和远程仓库配置"
    echo "提示: 可以手动执行 'git push origin main'"
    exit 1
fi
