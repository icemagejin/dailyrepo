#!/bin/bash

# Info Agent Daily Journal Sync Script
# 将思辨日记同步到GitHub

set -e

# 配置
WORKSPACE="/workspace/projects/workspace-info"
JOURNAL_DIR="$WORKSPACE/daily-journal"
COMMIT_MSG="Update daily journal: $(date +%Y-%m-%d)"
GITHUB_TOKEN="${GITHUB_TOKEN:-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}"

# 进入工作目录
cd "$WORKSPACE"

# 检查是否在git仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "⚠️  当前不是git仓库"
    exit 1
fi

# 配置Git用户信息
git config user.email "info-agent@openclaw.ai" 2>/dev/null || true
git config user.name "Info Agent" 2>/dev/null || true

# 确保远程URL包含token（如果环境变量中有token）
if [ -n "$GITHUB_TOKEN" ]; then
    REMOTE_URL=$(git remote get-url origin)
    if [[ ! "$REMOTE_URL" =~ ^https://ghp_ ]]; then
        # 提取URL中的username@部分并替换
        REMOTE_URL_WITH_TOKEN=$(echo "$REMOTE_URL" | sed "s|https://github.com/|https://${GITHUB_TOKEN}@github.com/|")
        git remote set-url origin "$REMOTE_URL_WITH_TOKEN"
    fi
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
    echo "✓ 仓库: https://github.com/icemagejin/dailyrepo"
else
    echo "⚠️  推送失败，请检查网络连接"
    exit 1
fi
