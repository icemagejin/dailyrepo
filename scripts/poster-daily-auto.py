#!/usr/bin/env python3
"""
每日八字合盘海报 - 完整自动化流程
自动生成并发送到飞书美学群
"""

import subprocess
import os
import sys
from datetime import datetime

def run_command(cmd):
    """执行命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ 命令失败：{cmd}")
        print(f"  错误：{result.stderr}")
        return None
    return result.stdout.strip()

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]

    print(f"📊 八字合盘海报 - {today} {weekday}")

    # 生成海报
    poster_script = "/workspace/projects/workspace-aesthetic/scripts/generate-daily-poster.sh"
    output = run_command(f"bash {poster_script}")

    if not output:
        return False

    poster_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{today}.jpg"

    if not os.path.exists(poster_path):
        print(f"✗ 海报不存在：{poster_path}")
        return False

    file_size = os.path.getsize(poster_path) / 1024
    print(f"✓ 海报已生成：{poster_path} ({file_size:.1f} KB)")

    # 返回海报路径和描述信息
    return {
        "poster_path": poster_path,
        "file_size": file_size,
        "date": today,
        "weekday": weekday,
        "yi": "交易立券可成",
        "ji": "争执冲突莫起"
    }

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n✓ 任务完成！")
        print(f"  日期：{result['date']} {result['weekday']}")
        print(f"  宜：{result['yi']}")
        print(f"  忌：{result['ji']}")
        print(f"  海报：{result['poster_path']}")
    else:
        print("\n✗ 任务失败")
        sys.exit(1)
