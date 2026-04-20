#!/usr/bin/env python3
"""
发送海报到飞书美学群
"""

import sys
import os
import subprocess
from datetime import datetime

def send_poster_to_feishu(date_str):
    """发送海报到飞书群"""
    poster_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{date_str}.jpg"

    if not os.path.exists(poster_path):
        print(f"✗ 海报不存在：{poster_path}")
        return False

    # 使用 sessions_send 发送消息（这是OpenClaw内置的跨会话消息功能）
    # 但这个需要在OpenClaw环境中运行，不能单独作为脚本
    # 所以我们只打印路径，由cron任务的delivery配置来处理发送

    print(f"✓ 海报已准备发送：{poster_path}")
    return True

if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    send_poster_to_feishu(date_str)
