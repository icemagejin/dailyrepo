#!/usr/bin/env python3
"""
每日八字合盘海报 - 完整流程
自动生成并发送到美学群
"""

import subprocess
import os
from datetime import datetime

def run_command(cmd):
    """执行命令并返回结果"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ 命令失败：{cmd}")
        print(f"  错误：{result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"📊 八字合盘海报生成 - {today}")
    print("=" * 50)

    # 1. 生成海报
    print("\n1️⃣ 生成海报...")
    poster_script = "/workspace/projects/workspace-aesthetic/scripts/generate-daily-poster.sh"
    if not run_command(f"bash {poster_script}"):
        return False

    # 2. 发送到飞书群
    print("\n2️⃣ 准备发送到美学群...")
    poster_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{today}.jpg"

    if not os.path.exists(poster_path):
        print(f"✗ 海报不存在：{poster_path}")
        return False

    print(f"✓ 海报已生成：{poster_path}")
    print(f"✓ 文件大小：{os.path.getsize(poster_path) / 1024:.1f} KB")

    # 返回海报路径，让OpenClaw的delivery机制处理发送
    return poster_path

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n✓ 任务完成！海报路径：{result}")
    else:
        print("\n✗ 任务失败")
