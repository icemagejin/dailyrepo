#!/usr/bin/env python3
"""
八字合盘海报 - 背景图案版
在 DESIGN.md 基础上添加中式背景图案
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import random
import math

# 获取日期参数
date_str = sys.argv[1] if len(sys.argv) > 1 else "2026-04-06"

# 解析日期
from datetime import datetime
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
year = date_obj.year
month = date_obj.month
day = date_obj.day
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]

# 输出路径
output_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{date_str}-with-bg.jpg"

# ========== DESIGN.md 设计系统 ==========

# 色彩系统
BACKGROUND = (26, 26, 46)          # #1A1A2E
TEXT_PRIMARY = (255, 255, 255)     # #FFFFFF
TEXT_SECONDARY = (160, 160, 176)   # #A0A0B0
TEXT_TERTIARY = (107, 114, 128)    # #6B7280
TEXTURE_COLOR = (35, 37, 48)       # #232530
PRIMARY = (108, 92, 231)           # #6C5CE7
BG_PATTERN = (40, 42, 55)           # 背景图案颜色

# 间距系统
XS = 4
SM = 8
MD = 16
LG = 24
XL = 32
XL2 = 48

# 配置
width = 1080
height = 1920

# 字体大小
DISPLAY_2_SIZE = int(height * 0.025)
BODY_LARGE_SIZE = int(height * 0.009375)
BODY_SIZE = int(height * 0.00833)

# 创建背景
img = Image.new('RGB', (width, height), BACKGROUND)
draw = ImageDraw.Draw(img)

def add_chinese_pattern(draw, width, height):
    """添加中式背景图案"""
    
    # 1. 边框装饰（中式回纹风格）
    border_width = 3
    margin = 60
    
    # 外框
    draw.rectangle([margin, margin, width - margin, height - margin],
                 outline=BG_PATTERN, width=border_width)
    
    # 内框（双线效果）
    inner_margin = margin + 10
    draw.rectangle([inner_margin, inner_margin, width - inner_margin, height - inner_margin],
                 outline=BG_PATTERN, width=1)
    
    # 2. 四角装饰（云纹风格）
    corner_size = 80
    for x, y in [(margin, margin), (width - margin - corner_size, margin),
                 (margin, height - margin - corner_size), (width - margin - corner_size, height - margin - corner_size)]:
        # 云纹曲线
        for i in range(3):
            offset = i * 15
            draw.arc([x + offset, y + offset, x + corner_size - offset, y + corner_size - offset],
                     0, 360, fill=BG_PATTERN, width=2)
    
    # 3. 圆形八卦图案（背景装饰）
    center_x = width // 2
    center_y = height // 2
    radius = 400
    
    # 外圈
    draw.ellipse([center_x - radius, center_y - radius,
                  center_x + radius, center_y + radius],
                 outline=BG_PATTERN, width=1)
    
    # 中圈
    draw.ellipse([center_x - radius * 0.7, center_y - radius * 0.7,
                  center_x + radius * 0.7, center_y + radius * 0.7],
                 outline=BG_PATTERN, width=1)
    
    # 内圈
    draw.ellipse([center_x - radius * 0.4, center_y - radius * 0.4,
                  center_x + radius * 0.4, center_y + radius * 0.4],
                 outline=BG_PATTERN, width=1)
    
    # 4. 八字符号（八角形）
    octagon_points = []
    for i in range(8):
        angle = (i * 45 + 22.5) * math.pi / 180
        x = center_x + radius * 0.85 * math.cos(angle)
        y = center_y + radius * 0.85 * math.sin(angle)
        octagon_points.append((x, y))
    
    draw.polygon(octagon_points, outline=BG_PATTERN, width=2)
    
    # 5. 天干地支符号（简化）
    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 在外圈周围放置天干地支
    radius_text = radius + 30
    font_small = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 24)
    
    # 天干（偶数位置）
    for i, char in enumerate(tiangan):
        if i % 2 == 0:
            angle = (i * 36) * math.pi / 180
            x = center_x + radius_text * math.cos(angle) - 12
            y = center_y + radius_text * math.sin(angle) - 12
            draw.text((x, y), char, font=font_small, fill=TEXT_TERTIARY)
    
    # 地支（奇数位置）
    for i, char in enumerate(dizhi):
        if i % 2 == 1:
            angle = (i * 30 + 15) * math.pi / 180
            x = center_x + radius_text * math.cos(angle) - 12
            y = center_y + radius_text * math.sin(angle) - 12
            draw.text((x, y), char, font=font_small, fill=TEXT_TERTIARY)
    
    print("✓ 中式背景图案已添加")

# 添加背景图案
add_chinese_pattern(draw, width, height)

# 字体加载
def load_font(size):
    font_names = ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Noto Sans", "sans-serif"]
    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except:
            continue
    try:
        return ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", size)
    except:
        return ImageFont.load_default()

date_day_font = load_font(DISPLAY_2_SIZE)
date_info_font = load_font(BODY_LARGE_SIZE)
yi_ji_font = load_font(BODY_SIZE)

print(f"✓ 字体加载成功")

# 内容
date_day = str(day)
date_info = f"{month}月{day}日 · {weekday} · {year}"
yi_text = "宜：交易立券可成"
ji_text = "忌：争执冲突莫起"

# 布局计算
total_content_height = 0

date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_height = date_day_bbox[3] - date_day_bbox[1]
total_content_height += date_day_height + XL

date_info_bbox = draw.textbbox((0, 0), date_info, font=date_info_font)
date_info_height = date_info_bbox[3] - date_info_bbox[1]
total_content_height += date_info_height + XL2

yi_ji_bbox = draw.textbbox((0, 0), yi_text, font=yi_ji_font)
yi_ji_height = yi_ji_bbox[3] - yi_ji_bbox[1]
total_content_height += yi_ji_height * 2 + LG

content_start_y = (height - total_content_height) // 2

# 绘制内容
current_y = content_start_y

# 日期数字
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_x = (width - date_day_width) // 2

draw.text((date_day_x, current_y), date_day, font=date_day_font, fill=TEXT_PRIMARY)

date_day_rendered_bbox = draw.textbbox((date_day_x, current_y), date_day, font=date_day_font)
date_day_actual_bottom = date_day_rendered_bbox[3]
current_y = date_day_actual_bottom + XL

# 日期信息
date_info_bbox = draw.textbbox((0, 0), date_info, font=date_info_font)
date_info_width = date_info_bbox[2] - date_info_bbox[0]
date_info_x = (width - date_info_width) // 2

draw.text((date_info_x, current_y), date_info, font=date_info_font, fill=TEXT_SECONDARY)

date_info_rendered_bbox = draw.textbbox((date_info_x, current_y), date_info, font=date_info_font)
date_info_actual_bottom = date_info_rendered_bbox[3]
current_y = date_info_actual_bottom + XL2

# 宜忌
yi_bbox = draw.textbbox((0, 0), yi_text, font=yi_ji_font)
yi_width = yi_bbox[2] - yi_bbox[0]
yi_x = (width - yi_width) // 2

draw.text((yi_x, current_y), yi_text, font=yi_ji_font, fill=TEXT_TERTIARY)

yi_rendered_bbox = draw.textbbox((yi_x, current_y), yi_text, font=yi_ji_font)
yi_actual_bottom = yi_rendered_bbox[3]
current_y = yi_actual_bottom + LG

ji_bbox = draw.textbbox((0, 0), ji_text, font=yi_ji_font)
ji_width = ji_bbox[2] - ji_bbox[0]
ji_x = (width - ji_width) // 2

draw.text((ji_x, current_y), ji_text, font=yi_ji_font, fill=TEXT_TERTIARY)

# 保存
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path, quality=95)

print(f"\n✓ 带背景图案的海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  背景元素：中式回纹边框 + 云纹四角 + 八卦图案 + 天干地支符号")
print(f"  设计风格：中式元素 + 深色主题 + DESIGN.md 规范")
