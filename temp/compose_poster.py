from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

# 打开背景图
bg = Image.open('/workspace/projects/workspace-aesthetic/temp/background.png')

# 转换为RGB（如果需要）
if bg.mode != 'RGB':
    bg = bg.convert('RGB')

width, height = bg.size
print(f"背景图尺寸: {width}x{height}")

# 创建半透明白色遮罩
overlay = Image.new('RGBA', (width, height), (255, 255, 255, 0))
draw = ImageDraw.Draw(overlay)

# 添加半透明白色渐变遮罩到文字区域（底部和顶部）
for y in range(0, 300):
    alpha = int(30 * (y / 300))  # 顶部淡入
    for x in range(width):
        overlay.putpixel((x, y), (255, 255, 255, alpha))

for y in range(height-400, height):
    alpha = int(60 * ((y - (height-400)) / 400))  # 底部淡入
    for x in range(width):
        overlay.putpixel((x, y), (255, 255, 255, alpha))

# 合成遮罩
bg_composite = Image.alpha_composite(bg.convert('RGBA'), overlay)

# 准备绘制
draw = ImageDraw.Draw(bg_composite)

# 配色方案（基于今日五行）
colors = {
    'earth': '#8B7355',      # 土黄色
    'fire': '#FFA07A',       # 暖橙色
    'water': '#87CEEB',      # 淡蓝色
    'gold': '#D4AF37',       # 金色
    'white': '#FFFFFF',      # 白色
    'dark': '#2C2C2C'        # 深灰色
}

# 八字信息
bazi_info = {
    'year': '丙午',
    'month': '壬辰',
    'day': '己亥',
    'hour': '戊辰'
}

date_text = '2026年4月15日 · 壬辰月 · 己亥日'

# 尝试加载中文字体
def get_font(size, bold=False):
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 文泉驿正黑
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微米黑
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]

    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue

    # 如果都失败了，使用默认字体
    return ImageFont.load_default()

# 获取字体
title_font = get_font(64, bold=True)
subtitle_font = get_font(40)
text_font = get_font(48)
small_font = get_font(32)

# 绘制日期（顶部居中）
date_bbox = draw.textbbox((0, 0), date_text, font=subtitle_font)
date_width = date_bbox[2] - date_bbox[0]
date_x = (width - date_width) // 2
draw.text((date_x, 120), date_text, fill=colors['white'], font=subtitle_font)

# 绘制八字（中部）
bazi_y_start = 400
bazi_spacing = 180

# 四柱标题
pillar_names = ['年柱', '月柱', '日柱', '时柱']
pillar_x_positions = [width//2 - 360, width//2 - 120, width//2 + 120, width//2 + 360]

for i, (name, pillar) in enumerate(zip(pillar_names, [bazi_info['year'], bazi_info['month'], bazi_info['day'], bazi_info['hour']])):
    x = pillar_x_positions[i]

    # 绘制柱名称
    name_bbox = draw.textbbox((0, 0), name, font=small_font)
    name_width = name_bbox[2] - name_bbox[0]
    draw.text((x - name_width//2, bazi_y_start), name, fill=colors['gold'], font=small_font)

    # 绘制干支
    pillar_bbox = draw.textbbox((0, 0), pillar, font=text_font)
    pillar_width = pillar_bbox[2] - pillar_bbox[0]
    draw.text((x - pillar_width//2, bazi_y_start + 50), pillar, fill=colors['white'], font=text_font)

    # 绘制小竖线装饰
    draw.line([(x, bazi_y_start - 10), (x, bazi_y_start + 130)], fill=colors['gold'], width=2)

# 绘制五行说明（底部）
五行_text = '土 ×4  火 ×2  水 ×2'
five_y_start = height - 320

# 绘制五行统计
elements_y = height - 350
draw.text((width//2, elements_y), '今日五行', fill=colors['gold'], font=small_font, anchor='mt')

# 绘制五行统计详情
element_details = [
    ('土', colors['earth'], '4'),
    ('火', colors['fire'], '2'),
    ('水', colors['water'], '2'),
]

element_x_start = width//2 - 150
element_spacing = 150

for i, (elem, color, count) in enumerate(element_details):
    x = element_x_start + i * element_spacing
    text = f'{elem}×{count}'
    text_bbox = draw.textbbox((0, 0), text, font=text_font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text((x - text_width//2, elements_y + 40), text, fill=color, font=text_font)

# 绘制装饰性墨线（国画风格）
# 底部山脉轮廓
draw.line([(0, height-400), (width//3, height-450), (2*width//3, height-430), (width, height-470)],
          fill=colors['earth'], width=3)

# 顶部小云纹
draw.arc([width-200, 50, width-50, 150], start=0, end=180, fill=colors['gold'], width=2)
draw.arc([width-180, 70, width-70, 130], start=0, end=180, fill=colors['gold'], width=1)

# 添加装饰性印章风格
seal_size = 60
seal_x = width - 120
seal_y = 150
draw.rectangle([seal_x, seal_y, seal_x + seal_size, seal_y + seal_size],
               outline=colors['fire'], width=2)
seal_text = '甲辰'
seal_bbox = draw.textbbox((0, 0), seal_text, font=small_font)
seal_width = seal_bbox[2] - seal_bbox[0]
seal_height = seal_bbox[3] - seal_bbox[1]
draw.text((seal_x + seal_size//2 - seal_width//2, seal_y + seal_size//2 - seal_height//2),
          seal_text, fill=colors['fire'], font=small_font)

# 保存最终图片
output_path = '/workspace/projects/workspace-aesthetic/temp/bazi_poster.png'
bg_composite.save(output_path, 'PNG', optimize=True, quality=95)
print(f"海报已保存到: {output_path}")

# 转换回RGB用于显示
bg_final = bg_composite.convert('RGB')
bg_final.save(output_path, 'PNG', optimize=True, quality=95)
print("海报合成完成！")
