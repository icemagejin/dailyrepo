#!/usr/bin/env python3
"""
八字合盘海报 - DESIGN.md 版本
基于 DESIGN.md 视觉设计系统的深色主题海报
遵循标准色彩、字体、间距系统
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import random

# 获取参数
date_str = sys.argv[1] if len(sys.argv) > 1 else None
custom_yi = sys.argv[2] if len(sys.argv) > 2 else None
custom_ji = sys.argv[3] if len(sys.argv) > 3 else None

if not date_str:
    print("Usage: python3 poster_design_system.py YYYY-MM-DD [宜] [忌]")
    sys.exit(1)

# 解析日期
from datetime import datetime
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
year = date_obj.year
month = date_obj.month
day = date_obj.day
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]

# 输出路径
output_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{date_str}.jpg"

# ========== DESIGN.md 设计系统 ==========

# 色彩系统（从 DESIGN.md 映射到 RGB）
BACKGROUND = (26, 26, 46)          # #1A1A2E - 深色背景
TEXT_PRIMARY = (255, 255, 255)     # #FFFFFF - 主文字
TEXT_SECONDARY = (160, 160, 176)   # #A0A0B0 - 次要文字
TEXT_TERTIARY = (107, 114, 128)    # #6B7280 - 辅助文字
TEXTURE_COLOR = (35, 37, 48)       # #232530 - 微纹理（介于背景和表面之间）
PRIMARY = (108, 92, 231)           # #6C5CE7 - 品牌主色（可用于装饰）

# 间距系统（DESIGN.md 标准间距）
XS = 4
SM = 8
MD = 16
LG = 24   # 内边距
XL = 32   # 主要元素间距
XL2 = 48  # 大区块间距

# 配置
width = 1080
height = 1920

# 字体大小（增大字体，确保清晰醒目）
DISPLAY_2_SIZE = int(height * 0.104)  # 日期数字: 200px（大幅增大）
BODY_LARGE_SIZE = int(height * 0.026)  # 日期信息: 50px（增大）
BODY_SIZE = int(height * 0.0208)  # 宜忌文字: 40px（增大）

# 创建背景
img = Image.new('RGB', (width, height), BACKGROUND)
draw = ImageDraw.Draw(img)

def add_subtle_texture(img, draw):
    """添加微妙的纹理效果 - 深色主题版本"""
    width, height = img.size

    # 纹理点配置
    point_color = TEXTURE_COLOR  # 比背景色稍深一点
    num_points = 150  # 点的数量
    point_radius = 2  # 点的半径

    # 随机添加点，避开中间文字区域
    # 文字区域大约在 20%-80% 之间
    text_zone_top = height * 0.20
    text_zone_bottom = height * 0.80

    for _ in range(num_points):
        x = random.randint(0, width)
        y = random.randint(0, height)

        # 跳过中间文字区域
        if text_zone_top < y < text_zone_bottom:
            continue

        # 绘制小圆点
        draw.ellipse([x - point_radius, y - point_radius,
                      x + point_radius, y + point_radius],
                     fill=point_color)

    # 添加几条细微的线条（模拟纸张纹理）
    line_color = (40, 42, 55)  # 比纹理点稍深
    num_lines = 20

    for _ in range(num_lines):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        line_length = random.randint(50, 150)

        # 几乎水平，轻微倾斜
        x2 = x1 + int(line_length * 0.3 * 0.9)
        y2 = y1 + int(line_length * 0.1)

        # 绘制细线
        draw.line([x1, y1, x2, y2], fill=line_color, width=1)

    print("✓ 微纹理背景已添加（深色主题）")

def add_bazi_symbols(img, draw, date_str):
    """不添加图形，保持简洁"""
    pass


# 添加微纹理

# 添加微纹理
add_subtle_texture(img, draw)

# 字体（优先使用 Inter，回退到系统字体）
# 按照 DESIGN.md 的字体家族顺序
font_names = ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Noto Sans", "sans-serif"]

def load_font(size):
    """加载字体，按照 DESIGN.md 优先级"""
    for font_name in font_names:
        # 尝试从系统字体路径加载
        try:
            return ImageFont.truetype(font_name, size)
        except:
            continue

    # 如果都失败，尝试 Noto Sans
    try:
        return ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", size)
    except:
        # 最后回退到默认字体
        return ImageFont.load_default()

# 加载字体
try:
    date_day_font = load_font(DISPLAY_2_SIZE)
    date_info_font = load_font(BODY_LARGE_SIZE)
    yi_ji_font = load_font(BODY_SIZE)
    print(f"✓ 字体加载成功（Display 2: {DISPLAY_2_SIZE}px, Body Large: {BODY_LARGE_SIZE}px, Body: {BODY_SIZE}px）")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")
    date_day_font = ImageFont.load_default()
    date_info_font = ImageFont.load_default()
    yi_ji_font = ImageFont.load_default()

# 内容
date_day = str(day)
date_info = f"{month}月{day}日 · {weekday} · {year}"

# 宜忌（优先使用传入参数）
if custom_yi:
    yi_text = f"宜：{custom_yi}"
else:
    yi_text = "宜：交易立券可成"

if custom_ji:
    ji_text = f"忌：{custom_ji}"
else:
    ji_text = "忌：争执冲突莫起"

# ========== 布局计算 ==========

# 垂直居中计算
total_content_height = 0

# 1. 日期数字
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_height = date_day_bbox[3] - date_day_bbox[1]
total_content_height += date_day_height

# 2. 间距（数字到日期信息）
total_content_height += XL

# 3. 日期信息
date_info_bbox = draw.textbbox((0, 0), date_info, font=date_info_font)
date_info_height = date_info_bbox[3] - date_info_bbox[1]
total_content_height += date_info_height

# 4. 间距（日期信息到宜忌）
total_content_height += XL2

# 5. 宜忌（2行）
yi_ji_bbox = draw.textbbox((0, 0), yi_text, font=yi_ji_font)
yi_ji_height = yi_ji_bbox[3] - yi_ji_bbox[1]
total_content_height += yi_ji_height * 2 + LG  # 2行 + 行间距

# 计算起始Y坐标（居中）
content_start_y = (height - total_content_height) // 2

# ========== 绘制内容 ==========

current_y = content_start_y

# 1. 日期数字（居中，第一层级）
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_x = (width - date_day_width) // 2

draw.text((date_day_x, current_y), date_day, font=date_day_font, fill=TEXT_PRIMARY)
print(f"✓ 绘制日期数字：{date_day} at y={current_y}")

# 更新位置
date_day_rendered_bbox = draw.textbbox((date_day_x, current_y), date_day, font=date_day_font)
date_day_actual_bottom = date_day_rendered_bbox[3]
current_y = date_day_actual_bottom + XL

# 2. 日期信息（居中，第二层级）
date_info_bbox = draw.textbbox((0, 0), date_info, font=date_info_font)
date_info_width = date_info_bbox[2] - date_info_bbox[0]
date_info_x = (width - date_info_width) // 2

draw.text((date_info_x, current_y), date_info, font=date_info_font, fill=TEXT_SECONDARY)
print(f"✓ 绘制日期信息：{date_info} at y={current_y}")

# 更新位置
date_info_rendered_bbox = draw.textbbox((date_info_x, current_y), date_info, font=date_info_font)
date_info_actual_bottom = date_info_rendered_bbox[3]
current_y = date_info_actual_bottom + XL2

# 3. 宜忌（居中，第三层级）
# 宜
yi_bbox = draw.textbbox((0, 0), yi_text, font=yi_ji_font)
yi_width = yi_bbox[2] - yi_bbox[0]
yi_x = (width - yi_width) // 2

draw.text((yi_x, current_y), yi_text, font=yi_ji_font, fill=TEXT_TERTIARY)
print(f"✓ 绘制宜：{yi_text} at y={current_y}")

# 更新位置
yi_rendered_bbox = draw.textbbox((yi_x, current_y), yi_text, font=yi_ji_font)
yi_actual_bottom = yi_rendered_bbox[3]
current_y = yi_actual_bottom + LG

# 忌
ji_bbox = draw.textbbox((0, 0), ji_text, font=yi_ji_font)
ji_width = ji_bbox[2] - ji_bbox[0]
ji_x = (width - ji_width) // 2

draw.text((ji_x, current_y), ji_text, font=yi_ji_font, fill=TEXT_TERTIARY)
print(f"✓ 绘制忌：{ji_text} at y={current_y}")

# ========== 保存 ==========

# 确保输出目录存在
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 保存
img.save(output_path, quality=95)

print(f"\n✓ DESIGN.md 版海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  设计风格：深色主题 + DESIGN.md 规范 + 三层视觉层次")
print(f"  色彩系统：Background #{BACKGROUND[0]:02x}{BACKGROUND[1]:02x}{BACKGROUND[2]:02x}")
print(f"  字体系统：Inter + 系统字体")
print(f"  间距系统：标准间距（xs, sm, md, lg, xl, 2xl）")
print(f"  视觉层次：日期数字(Primary) → 日期信息(Secondary) → 宜忌(Tertiary)")
