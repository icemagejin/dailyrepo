#!/usr/bin/env python3
"""
八字合盘海报生成器 - 完整版
包含干支计算、八字合盘分析、宜忌生成、海报绘制
现代国画写意风格
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import sys
from datetime import datetime
import math

# ==================== 干支计算系统 ====================

class GanZhi:
    """干支计算"""

    # 天干
    GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

    # 地支
    ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 五行
    WUXING = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水",
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }

    @staticmethod
    def get_year_ganzhi(year):
        """计算年柱干支（基于立春）"""
        # 1984年是甲子年
        base_year = 1984
        offset = year - base_year

        # 天干偏移
        gan_offset = offset % 10
        # 地支偏移
        zhi_offset = offset % 12

        gan = GanZhi.GAN[gan_offset]
        zhi = GanZhi.ZHI[zhi_offset]

        return gan + zhi

    @staticmethod
    def get_month_ganzhi(year, month):
        """计算月柱干支（基于节气，简化版按月计算）"""
        # 年干决定月干的起始
        year_gan = GanZhi.get_year_ganzhi(year)[0]

        # 月干起始偏移
        month_gan_start = {
            "甲": 2, "乙": 4, "丙": 6, "丁": 8, "戊": 0,
            "己": 2, "庚": 4, "辛": 6, "壬": 8, "癸": 0
        }[year_gan]

        # 月支（寅月是农历一月，对应公历2月）
        month_zhi_start = 2  # 寅

        # 计算偏移
        month_offset = month - 1  # 1月偏移0

        gan_offset = (month_gan_start + month_offset) % 10
        zhi_offset = (month_zhi_start + month_offset) % 12

        gan = GanZhi.GAN[gan_offset]
        zhi = GanZhi.ZHI[zhi_offset]

        return gan + zhi

    @staticmethod
    def get_day_ganzhi(date_obj):
        """计算日柱干支"""
        # 基准日期：1900-01-01 是甲戌日
        base_date = datetime(1900, 1, 1)
        delta = (date_obj - base_date).days

        # 甲戌的偏移量：甲是0，戌是10
        base_gan_offset = 0  # 甲
        base_zhi_offset = 10  # 戌

        gan_offset = (base_gan_offset + delta) % 10
        zhi_offset = (base_zhi_offset + delta) % 12

        gan = GanZhi.GAN[gan_offset]
        zhi = GanZhi.ZHI[zhi_offset]

        return gan + zhi

    @staticmethod
    def get_hour_ganzhi(day_ganzhi, hour):
        """计算时柱干支"""
        # 日干决定时干的起始
        day_gan = day_ganzhi[0]

        # 时干起始偏移
        hour_gan_start = {
            "甲": 0, "乙": 2, "丙": 4, "丁": 6, "戊": 8,
            "己": 0, "庚": 2, "辛": 4, "壬": 6, "癸": 8
        }[day_gan]

        # 时辰
        hour_zhi_map = {
            (23, 1): 0, (1, 3): 1, (3, 5): 2, (5, 7): 3,
            (7, 9): 4, (9, 11): 5, (11, 13): 6, (13, 15): 7,
            (15, 17): 8, (17, 19): 9, (19, 21): 10, (21, 23): 11
        }

        zhi_offset = 0
        for (start, end), offset in hour_zhi_map.items():
            if start <= hour < end or (hour >= 23 or hour < 1 and start == 23):
                zhi_offset = offset
                break

        gan_offset = (hour_gan_start + zhi_offset) % 10

        gan = GanZhi.GAN[gan_offset]
        zhi = GanZhi.ZHI[zhi_offset]

        return gan + zhi

    @staticmethod
    def get_wuxing(ganzhi):
        """获取干支五行"""
        wuxing = GanZhi.WUXING
        gan_wuxing = wuxing[ganzhi[0]]
        zhi_wuxing = wuxing[ganzhi[1]]
        return gan_wuxing, zhi_wuxing

# ==================== 八字合盘分析 ====================

def analyze_bazi_compatibility(user_ganzhi, day_ganzhi):
    """
    八字合盘分析
    user_ganzhi: 用户八字 ["乙丑", "丙戌", "戊申"] (年月日)
    day_ganzhi: 今日干支 [年柱, 月柱, 日柱, 时柱]
    """
    # 五行统计
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}

    # 用户八字五行
    for ganzhi in user_ganzhi:
        gan_wuxing, zhi_wuxing = GanZhi.get_wuxing(ganzhi)
        wuxing_count[gan_wuxing] += 1
        wuxing_count[zhi_wuxing] += 1

    # 今日五行
    for ganzhi in day_ganzhi:
        gan_wuxing, zhi_wuxing = GanZhi.get_wuxing(ganzhi)
        wuxing_count[gan_wuxing] += 1
        wuxing_count[zhi_wuxing] += 1

    # 找出最旺和最弱的五行
    sorted_wuxing = sorted(wuxing_count.items(), key=lambda x: x[1], reverse=True)

    most_strong = sorted_wuxing[0][0]
    weakest = sorted_wuxing[-1][0]

    # 日柱五行
    day_gan_wuxing, day_zhi_wuxing = GanZhi.get_wuxing(day_ganzhi[2])
    primary_wuxing = day_gan_wuxing

    return {
        "wuxing_count": wuxing_count,
        "most_strong": most_strong,
        "weakest": weakest,
        "primary_wuxing": primary_wuxing,
        "day_gan": day_ganzhi[2][0],
        "day_zhi": day_ganzhi[2][1]
    }

# ==================== 宜忌生成 ====================

def generate_yi_ji(analysis):
    """
    根据合盘分析生成对仗宜忌
    analysis: 合盘分析结果
    """
    day_gan = analysis["day_gan"]
    primary_wuxing = analysis["primary_wuxing"]
    most_strong = analysis["most_strong"]
    weakest = analysis["weakest"]

    # 宜忌库（根据日干和五行生成）
    yi_ji_map = {
        "甲": {
            "木": ("宜栽种植木", "忌破伐山林"),
            "火": ("宜点火炊煮", "忌寒凉不食"),
            "土": ("宜筑墙垒土", "忌开掘动土"),
            "金": ("宜铸造锻打", "忌损毁器皿"),
            "水": ("宜引流灌溉", "忌枯竭水源"),
        },
        "乙": {
            "木": ("宜修剪草木", "忌摧残嫩芽"),
            "火": ("宜燃香拜佛", "忌烟火熏灼"),
            "土": ("宜培土施肥", "忌翻动根基"),
            "金": ("宜修整农具", "忌砍伐树木"),
            "水": ("宜灌溉浇花", "忌水淹花木"),
        },
        "丙": {
            "木": ("宜焚香祭祀", "忌焚烧草木"),
            "火": ("宜炼丹制药", "忌灭火断炊"),
            "土": ("宜铸造铜器", "忌焚烧田地"),
            "金": ("宜冶炼锻打", "忌熔化珍宝"),
            "水": ("宜晒干物事", "忌受潮变质"),
        },
        "丁": {
            "木": ("宜点灯照明", "忌火烧山林"),
            "火": ("宜烹饪膳食", "忌熄灭炉火"),
            "土": ("宜陶冶瓷器", "忌火烧屋舍"),
            "金": ("宜打造首饰", "忌熔化金属"),
            "水": ("宜烘烤衣物", "忌淋湿生火"),
        },
        "戊": {
            "木": ("宜耕种土地", "忌毁坏林木"),
            "火": ("宜筑炉开灶", "忌烧毁庄稼"),
            "土": ("宜建屋立柱", "忌破土动工"),
            "金": ("宜开矿采石", "忌挖掘坟墓"),
            "水": ("宜筑堤防洪", "忌决堤泄洪"),
        },
        "己": {
            "木": ("宜种植花卉", "忌砍伐苗木"),
            "火": ("宜修缮灶台", "忌火烧房屋"),
            "土": ("宜培土养花", "忌翻动田地"),
            "金": ("宜挖掘地基", "忌破坏土壤"),
            "水": ("宜疏通水渠", "忌堵塞河道"),
        },
        "庚": {
            "木": ("宜伐木取材", "忌摧残幼苗"),
            "火": ("宜锻打兵器", "忌熔化铜铁"),
            "土": ("宜开矿凿井", "忌损毁山石"),
            "金": ("宜铸造器物", "忌损毁刀兵"),
            "水": ("宜疏通河道", "忌泛滥成灾"),
        },
        "辛": {
            "木": ("宜修剪枝叶", "忌砍伐大树"),
            "火": ("宜打磨玉石", "忌火烧珍宝"),
            "土": ("宜开凿石材", "忌破坏风水"),
            "金": ("宜打造首饰", "忌熔化金银"),
            "水": ("宜清洗器物", "忌沉入水中"),
        },
        "壬": {
            "木": ("宜灌溉农田", "忌淹没庄稼"),
            "火": ("宜煮药熬汤", "忌水火相克"),
            "土": ("宜水利建设", "忌冲毁堤坝"),
            "金": ("宜淘洗金矿", "忌金属锈蚀"),
            "水": ("宜行船航运", "忌逆水行舟"),
        },
        "癸": {
            "木": ("宜浇灌花草", "忌水涝成灾"),
            "火": ("宜温药煎汤", "忌水火不容"),
            "土": ("宜灌溉田地", "忌冲刷土壤"),
            "金": ("宜清洗金属", "忌水蚀生锈"),
            "水": ("宜饮用甘泉", "忌污水伤身"),
        },
    }

    # 获取宜忌
    yi_ji = yi_ji_map.get(day_gan, yi_ji_map["甲"]).get(primary_wuxing, ("宜吉祥如意", "忌凶险莫为"))

    return yi_ji

# ==================== 海报绘制 ====================

class BaziPoster:
    """八字合盘海报生成器 - 现代国画写意风格"""

    def __init__(self, date_str, user_ganzhi, day_ganzhi, yi_ji):
        self.date_str = date_str
        self.user_ganzhi = user_ganzhi
        self.day_ganzhi = day_ganzhi
        self.yi_ji = yi_ji

        # 配置
        self.width = 1080
        self.height = 1920

        # 现代国画写意风格配色
        self.bg_color = (30, 28, 35)  # 深色背景
        self.warm_orange = (255, 165, 100)  # 暖橙色光晕
        self.earth_yellow = (218, 165, 32)  # 土黄色墨线
        self.gold = (255, 215, 0)  # 金色光泽
        self.light_blue = (173, 216, 230)  # 淡蓝水波纹
        self.text_white = (245, 245, 245)  # 文字白色
        self.text_grey = (180, 180, 190)  # 次要文字灰色

        # 字体大小
        self.title_size = 48
        self.ganzhi_size = 52
        self.yi_ji_size = 46
        self.footer_size = 36

    def create_poster(self):
        """创建海报"""
        # 创建基础背景
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # 添加微纹理背景
        self._add_texture(img, draw)

        # 添加暖橙色光晕
        self._add_orange_glow(img)

        # 添加淡蓝水波纹
        self._add_water_ripple(draw)

        # 添加半透明白色遮罩（提升文字可读性）
        mask = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 20))
        img.paste(Image.alpha_composite(img.convert('RGBA'), mask), (0, 0))

        # 重新创建 Draw 对象
        draw = ImageDraw.Draw(img)

        # 加载字体
        fonts = self._load_fonts()

        # 绘制内容
        self._draw_header(draw, fonts)
        self._draw_bazi(draw, fonts)
        self._draw_yi_ji(draw, fonts)
        self._draw_footer(draw, fonts)

        # 添加金色光泽装饰
        self._add_gold_accents(draw)

        return img

    def _add_texture(self, img, draw):
        """添加微纹理背景"""
        import random

        # 150个小圆点
        for _ in range(150):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            # 避开中间文字区域（20%-80%）
            if self.height * 0.20 < y < self.height * 0.80:
                continue
            radius = random.randint(1, 3)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius],
                        fill=(40, 38, 45))

        # 20条细线（模拟墨线）
        for _ in range(20):
            x1 = random.randint(0, self.width)
            y1 = random.randint(0, int(self.height * 0.20))
            length = random.randint(50, 150)
            x2 = x1 + random.randint(-30, 30)
            y2 = y1 + random.randint(5, 20)
            draw.line([x1, y1, x2, y2], fill=self.earth_yellow, width=1)

    def _add_orange_glow(self, img):
        """添加暖橙色光晕"""
        # 在右上角和左下角添加渐变光晕
        glow = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)

        # 右上角光晕
        for i in range(50, 0, -5):
            alpha = int(15 * (1 - i/50))
            glow_draw.ellipse(
                [self.width-400-i, -100-i, self.width+100+i, 300+i],
                fill=(self.warm_orange[0], self.warm_orange[1], self.warm_orange[2], alpha)
            )

        # 左下角光晕
        for i in range(40, 0, -5):
            alpha = int(12 * (1 - i/40))
            glow_draw.ellipse(
                [-150-i, self.height-300-i, 250+i, self.height+100+i],
                fill=(self.warm_orange[0], self.warm_orange[1], self.warm_orange[2], alpha)
            )

        # 模糊光晕
        glow = glow.filter(ImageFilter.GaussianBlur(30))
        img.paste(Image.alpha_composite(img.convert('RGBA'), glow), (0, 0))

    def _add_water_ripple(self, draw):
        """添加淡蓝水波纹"""
        import random

        # 添加几条水平波浪线
        base_y = self.height * 0.15
        for i in range(3):
            points = []
            y = base_y + i * 25
            for x in range(0, self.width, 20):
                offset = random.randint(-8, 8)
                points.append((x, y + offset))

            # 绘制平滑曲线
            for j in range(len(points) - 1):
                draw.line([points[j], points[j+1]],
                         fill=self.light_blue, width=2)

    def _add_gold_accents(self, draw):
        """添加金色光泽装饰"""
        # 在标题下方添加金色线条
        draw.line([self.width*0.2, self.height*0.20, self.width*0.8, self.height*0.20],
                 fill=self.gold, width=2)

        # 在底部添加金色装饰
        draw.line([self.width*0.3, self.height*0.85, self.width*0.7, self.height*0.85],
                 fill=self.gold, width=1)

    def _load_fonts(self):
        """加载字体"""
        def load_font(size, bold=False):
            font_names = ["Inter-Bold" if bold else "Inter",
                         "-apple-system", "Noto Sans", "sans-serif"]
            for font_name in font_names:
                try:
                    return ImageFont.truetype(font_name, size)
                except:
                    continue
            # 回退到系统字体
            try:
                font_path = "/usr/share/fonts/opentype/noto/"
                font_file = "NotoSansCJK-Bold.ttc" if bold else "NotoSansCJK-Regular.ttc"
                return ImageFont.truetype(font_path + font_file, size)
            except:
                return ImageFont.load_default()

        return {
            "title_bold": load_font(self.title_size, bold=True),
            "ganzhi": load_font(self.ganzhi_size, bold=True),
            "ganzhi_regular": load_font(self.ganzhi_size, bold=False),
            "yi_ji": load_font(self.yi_ji_size, bold=False),
            "footer": load_font(self.footer_size, bold=False),
        }

    def _draw_header(self, draw, fonts):
        """绘制标题"""
        title = "八字合盘"
        title_bbox = draw.textbbox((0, 0), title, font=fonts["title_bold"])
        title_width = title_bbox[2] - title_bbox[0]
        x = (self.width - title_width) // 2
        y = self.height * 0.08

        draw.text((x, y), title, font=fonts["title_bold"], fill=self.gold)

    def _draw_bazi(self, draw, fonts):
        """绘制八字信息"""
        # 今日八字
        today_label = f"今日八字"
        today_ganzhi = " · ".join(self.day_ganzhi[:3])  # 年月日

        y_start = self.height * 0.25

        # 今日八字标题
        label_bbox = draw.textbbox((0, 0), today_label, font=fonts["ganzhi_regular"])
        label_width = label_bbox[2] - label_bbox[0]
        x = (self.width - label_width) // 2
        draw.text((x, y_start), today_label, font=fonts["ganzhi_regular"], fill=self.text_grey)

        # 今日八字内容
        y_start += 60
        ganzhi_bbox = draw.textbbox((0, 0), today_ganzhi, font=fonts["ganzhi"])
        ganzhi_width = ganzhi_bbox[2] - ganzhi_bbox[0]
        x = (self.width - ganzhi_width) // 2
        draw.text((x, y_start), today_ganzhi, font=fonts["ganzhi"], fill=self.text_white)

        # 用户八字
        y_start += 100
        user_label = f"您的八字"
        user_ganzhi = " · ".join(self.user_ganzhi)

        label_bbox = draw.textbbox((0, 0), user_label, font=fonts["ganzhi_regular"])
        label_width = label_bbox[2] - label_bbox[0]
        x = (self.width - label_width) // 2
        draw.text((x, y_start), user_label, font=fonts["ganzhi_regular"], fill=self.text_grey)

        y_start += 60
        ganzhi_bbox = draw.textbbox((0, 0), user_ganzhi, font=fonts["ganzhi"])
        ganzhi_width = ganzhi_bbox[2] - ganzhi_bbox[0]
        x = (self.width - ganzhi_width) // 2
        draw.text((x, y_start), user_ganzhi, font=fonts["ganzhi"], fill=self.text_white)

    def _draw_yi_ji(self, draw, fonts):
        """绘制宜忌"""
        yi_text, ji_text = self.yi_ji

        y_start = self.height * 0.65

        # 宜
        yi_full = f"宜 {yi_text}"
        yi_bbox = draw.textbbox((0, 0), yi_full, font=fonts["yi_ji"])
        yi_width = yi_bbox[2] - yi_bbox[0]
        x = (self.width - yi_width) // 2
        draw.text((x, y_start), yi_full, font=fonts["yi_ji"], fill=self.warm_orange)

        y_start += 70

        # 忌
        ji_full = f"忌 {ji_text}"
        ji_bbox = draw.textbbox((0, 0), ji_full, font=fonts["yi_ji"])
        ji_width = ji_bbox[2] - ji_bbox[0]
        x = (self.width - ji_width) // 2
        draw.text((x, y_start), ji_full, font=fonts["yi_ji"], fill=self.text_grey)

    def _draw_footer(self, draw, fonts):
        """绘制底部信息"""
        date_info = self.date_str

        footer_bbox = draw.textbbox((0, 0), date_info, font=fonts["footer"])
        footer_width = footer_bbox[2] - footer_bbox[0]
        x = (self.width - footer_width) // 2
        y = self.height * 0.90

        draw.text((x, y), date_info, font=fonts["footer"], fill=self.text_grey)


# ==================== 主流程 ====================

def main():
    # 获取参数
    date_str = sys.argv[1] if len(sys.argv) > 1 else None

    if not date_str:
        print("Usage: python3 bazi_hepan_poster.py YYYY-MM-DD")
        sys.exit(1)

    # 解析日期
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # 用户八字（年月日）
    user_ganzhi = ["乙丑", "丙戌", "戊申"]

    # 计算今日干支（年月日时）
    year_ganzhi = GanZhi.get_year_ganzhi(date_obj.year)
    month_ganzhi = GanZhi.get_month_ganzhi(date_obj.year, date_obj.month)
    day_ganzhi = GanZhi.get_day_ganzhi(date_obj)
    hour_ganzhi = GanZhi.get_hour_ganzhi(day_ganzhi, 8)  # 8点为辰时

    day_ganzhi_list = [year_ganzhi, month_ganzhi, day_ganzhi, hour_ganzhi]

    print(f"📊 今日干支计算：")
    print(f"  年柱：{year_ganzhi}")
    print(f"  月柱：{month_ganzhi}")
    print(f"  日柱：{day_ganzhi}")
    print(f"  时柱（8点）：{hour_ganzhi}")

    # 八字合盘分析
    analysis = analyze_bazi_compatibility(user_ganzhi, day_ganzhi_list)
    print(f"\n🔮 八字合盘分析：")
    print(f"  主五行：{analysis['primary_wuxing']}")
    print(f"  最旺五行：{analysis['most_strong']}")
    print(f"  最弱五行：{analysis['weakest']}")

    # 生成宜忌
    yi_ji = generate_yi_ji(analysis)
    print(f"\n✨ 宜忌生成：")
    print(f"  宜：{yi_ji[0]}")
    print(f"  忌：{yi_ji[1]}")

    # 生成海报
    print(f"\n🎨 生成海报...")
    poster = BaziPoster(date_str, user_ganzhi, day_ganzhi_list, yi_ji)
    img = poster.create_poster()

    # 保存海报
    output_path = f"/workspace/projects/workspace-aesthetic/posters/bazi-hepan-{date_str}.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)

    print(f"\n✓ 海报已生成：{output_path}")
    print(f"  文件大小：{os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

    return output_path


if __name__ == "__main__":
    main()
