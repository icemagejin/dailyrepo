#!/usr/bin/env python3
"""
诧寂风海报 - 水墨意境 + 不对称布局
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import sys
import random
import math

# 获取日期参数
date_str = sys.argv[1] if len(sys.argv) > 1 else None
if not date_str:
    print("Usage: python3 poster_wabi_sabi.py YYYY-MM-DD")
    sys.exit(1)

# 解析日期
from datetime import datetime
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
year = date_obj.year
month = date_obj.month
day = date_obj.day
weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
weekday_en = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][date_obj.weekday()]
month_en = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][month - 1]

# 输出路径
output_path = f"/workspace/projects/workspace-aesthetic/posters/poster-{date_str}-wabi-sabi.jpg"

# 背景图路径（coze-image-gen 生成 - 新版本）
background_url = "https://coze-coding-project.tos.coze.site/coze_storage_7605820374885859379/image/generate_image_da9ef560-1b01-4c53-aa47-d5889bc314a1.jpeg?sign=1807363268-06fb45cefb-0-ac23a6831bc00608a1ab7ff4213cf778099e5240a057aac2fef7e0d828bfd3ff"
background_path = "/tmp/background_2026-04-10_v2.jpg"

# 下载背景图
import urllib.request
print("正在下载背景图...")
urllib.request.urlretrieve(background_url, background_path)
print(f"✓ 背景图已下载：{background_path}")

# 加载背景图
img = Image.open(background_path)
# 调整到 1080x1920
img = img.resize((1080, 1920), Image.LANCZOS)
width, height = img.size
draw = ImageDraw.Draw(img)

# 八字、农历、警语福语
bazi = "丙午·壬辰·甲寅"
lunar = "二月廿三"
warning = "木土相克慎行"
blessing = "静守祈福安康"

# 添加纸质噪声（更细腻的质感）
def add_paper_texture(img):
    """添加纸质纹理 - 更细腻"""
    width, height = img.size
    pixels = img.load()
    
    # 添加非常细微的纹理
    for i in range(width):
        for j in range(height):
            # 更低概率，更细微的噪声
            if random.random() < 0.01:
                noise = random.randint(-2, 2)
                r = max(0, min(255, pixels[i, j][0] + noise))
                g = max(0, min(255, pixels[i, j][1] + noise))
                b = max(0, min(255, pixels[i, j][2] + noise))
                pixels[i, j] = (r, g, b)
    
    return img

# 添加水墨晕染（细腻、自然）
def add_ink_wash(img, width, height):
    """添加水墨晕染 - 细腻、自然、有层次"""
    
    # 创建临时图像用于绘制晕染
    temp_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 左上角淡墨晕染（营造不对称感）
    for _ in range(8):
        center_x = random.randint(0, width // 4)
        center_y = random.randint(0, height // 4)
        max_radius = random.randint(100, 300)
        
        # 绘制多个同心圆，模拟晕染扩散
        for i in range(5):
            radius = max_radius - (i * 30)
            if radius > 0:
                alpha = random.randint(8, 20) - (i * 3)
                if alpha > 0:
                    temp_draw.ellipse([center_x - radius, center_y - radius,
                                      center_x + radius, center_y + radius],
                                  fill=(ink_light[0], ink_light[1], ink_light[2], alpha))
    
    # 右下角极淡墨痕
    for _ in range(5):
        center_x = random.randint(width * 2 // 3, width)
        center_y = random.randint(height * 2 // 3, height)
        max_radius = random.randint(80, 150)
        
        # 绘制淡墨痕
        for i in range(3):
            radius = max_radius - (i * 20)
            if radius > 0:
                alpha = random.randint(3, 10) - (i * 2)
                if alpha > 0:
                    temp_draw.ellipse([center_x - radius, center_y - radius,
                                      center_x + radius, center_y + radius],
                                  fill=(ink_pale[0], ink_pale[1], ink_pale[2], alpha))
    
    # 添加不规则的墨点（模拟墨汁滴落）- 更少、更自然
    for _ in range(8):
        center_x = random.randint(0, width)
        center_y = random.randint(0, height)
        max_radius = random.randint(3, 6)
        
        # 绘制不规则的墨点（不是完美的圆）
        radius_x = max_radius + random.randint(-1, 1)
        radius_y = max_radius + random.randint(-1, 1)
        
        alpha = random.randint(15, 40)
        temp_draw.ellipse([center_x - radius_x, center_y - radius_y,
                          center_x + radius_x, center_y + radius_y],
                      fill=(ink_dark[0], ink_dark[1], ink_dark[2], alpha))
    
    # 叠加到主图
    img.paste(Image.alpha_composite(img.convert('RGBA'), temp_img), (0, 0))

# 背景图已经包含了水墨晕染和纸质纹理，不需要再添加
# 跳过 add_paper_texture 和 add_ink_wash

# 字体（诧寂风 - 支持中文）
font_regular_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font_bold_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

# 字号配置（诧寂风 - 克制、优雅，避免重叠）
month_week_size = int(width * 0.035)  # 英文月周 - 更小
date_day_size = int(height * 0.18)  # 主日期 - 减小，避免重叠
lunar_size = int(width * 0.040)  # 农历 - 稍微减小
bazi_size = int(width * 0.048)  # 八字 - 稍微减小
warning_size = int(width * 0.036)  # 警语 - 减小
blessing_size = int(width * 0.036)  # 福语 - 减小

# 加载字体
try:
    month_week_font = ImageFont.truetype(font_regular_path, month_week_size)
    date_day_font = ImageFont.truetype(font_bold_path, date_day_size)  # 粗体
    lunar_font = ImageFont.truetype(font_regular_path, lunar_size)
    bazi_font = ImageFont.truetype(font_regular_path, bazi_size)
    warning_font = ImageFont.truetype(font_regular_path, warning_size)
    blessing_font = ImageFont.truetype(font_regular_path, blessing_size)
    print("✓ 字体加载成功（Noto SansCJK - 支持中文）")
except Exception as e:
    print(f"✗ 字体加载失败：{e}")
    month_week_font = ImageFont.load_default()
    date_day_font = ImageFont.load_default()
    lunar_font = ImageFont.load_default()
    bazi_font = ImageFont.load_default()
    warning_font = ImageFont.load_default()
    blessing_font = ImageFont.load_default()

# 内容
month_week = f"{month_en} {weekday_en}"
date_day = str(day)

# 配色（诧寂风 - 更淡雅，克制）
month_week_color = (120, 115, 110)  # 极淡墨
date_day_color = (80, 75, 70)  # 中墨（不再那么深）
lunar_color = (130, 125, 118)  # 浅墨
bazi_color = (110, 105, 98)  # 中浅墨
warning_color = (150, 145, 138)  # 极淡墨
blessing_color = (165, 160, 155)  # 更浅

# 布局 - 根据新 VL 分析调整（避开顶部图形，使用右侧和下方）
# VL分析：顶部35.9%（图形最多），右侧21.2%（相对较少），下部21.5%（相对较少）
# 策略：文字放在下方和中下部，尽量使用右侧（图形较少）

# 英文月周：中下部，右侧
month_week_bbox = draw.textbbox((0, 0), month_week, font=month_week_font)
month_week_width = month_week_bbox[2] - month_week_bbox[0]
month_week_x = width - month_week_width - (width * 0.12)  # 右侧 12%
month_week_y = height * 0.45  # 45% 位置（避开顶部图形）
month_week_rendered_bbox = draw.textbbox((month_week_x, month_week_y), month_week, font=month_week_font)
month_week_actual_bottom = month_week_rendered_bbox[3]

# 主日期：中下部，右侧
date_day_bbox = draw.textbbox((0, 0), date_day, font=date_day_font)
date_day_width = date_day_bbox[2] - date_day_bbox[0]
date_day_x = width - date_day_width - (width * 0.15)  # 右侧 15%
date_day_y = month_week_actual_bottom + height * 0.15  # 增加间距（0.10 → 0.15）
date_day_rendered_bbox = draw.textbbox((date_day_x, date_day_y), date_day, font=date_day_font)
date_day_actual_bottom = date_day_rendered_bbox[3]

# 农历：中下部，右侧
lunar_bbox = draw.textbbox((0, 0), lunar, font=lunar_font)
lunar_width = lunar_bbox[2] - lunar_bbox[0]
lunar_x = width - lunar_width - (width * 0.12)  # 右侧 12%
lunar_y = date_day_actual_bottom + height * 0.12  # 增加间距（0.08 → 0.12）
lunar_rendered_bbox = draw.textbbox((lunar_x, lunar_y), lunar, font=lunar_font)
lunar_actual_bottom = lunar_rendered_bbox[3]

# 八字：中下部，右侧
bazi_bbox = draw.textbbox((0, 0), bazi, font=bazi_font)
bazi_width = bazi_bbox[2] - bazi_bbox[0]
bazi_x = width - bazi_width - (width * 0.12)  # 右侧 12%
bazi_y = lunar_actual_bottom + height * 0.12  # 增加间距（0.08 → 0.12）
bazi_rendered_bbox = draw.textbbox((bazi_x, bazi_y), bazi, font=bazi_font)
bazi_actual_bottom = bazi_rendered_bbox[3]

# 警语：底部，右侧（避开顶部和中部图形）
warning_y = height * 0.80  # 80% 位置（底部）
warning_bbox = draw.textbbox((0, 0), warning, font=warning_font)
warning_width = warning_bbox[2] - warning_bbox[0]
warning_x = width - warning_width - (width * 0.12)  # 右侧 12%
warning_rendered_bbox = draw.textbbox((warning_x, warning_y), warning, font=warning_font)
warning_actual_bottom = warning_rendered_bbox[3]

# 福语：底部，右侧，警语下方
blessing_y = warning_actual_bottom + height * 0.06
blessing_bbox = draw.textbbox((0, 0), blessing, font=blessing_font)
blessing_width = blessing_bbox[2] - blessing_bbox[0]
blessing_x = width - blessing_width - (width * 0.12)  # 右侧 12%

# 绘制所有文字（不对称布局）
draw.text((month_week_x, month_week_y), month_week, font=month_week_font, fill=month_week_color)
draw.text((date_day_x, date_day_y), date_day, font=date_day_font, fill=date_day_color)
draw.text((lunar_x, lunar_y), lunar, font=lunar_font, fill=lunar_color)
draw.text((bazi_x, bazi_y), bazi, font=bazi_font, fill=bazi_color)
draw.text((warning_x, warning_y), warning, font=warning_font, fill=warning_color)
draw.text((blessing_x, blessing_y), blessing, font=blessing_font, fill=blessing_color)

# 保存
img.save(output_path, quality=95)

print(f"\n✓ 诧寂风海报已生成：{output_path}")
print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
print(f"  设计风格：极简诧寂 + 水墨意境 + 衬线体 + 克制字号")
print(f"  特点：细腻晕染 + 纸质纹理 + 大面积留白 + 东方美学")
