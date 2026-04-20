#!/bin/bash
# 每日八字合盘海报生成（简化版）

set -e

# 获取今天日期
TODAY=$(date +%Y-%m-%d)

# 生成海报
cd /workspace/projects/workspace-aesthetic
python3 poster_design_system.py "$TODAY" "交易立券可成" "争执冲突莫起"

echo "✓ 海报已生成：posters/poster-$TODAY.jpg"
