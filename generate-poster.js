const { createCanvas, loadImage, registerFont } = require('canvas');
const fs = require('fs');

async function generatePoster() {
  // 加载背景图
  const bgImage = await loadImage('/tmp/aesthetic/background.jpg');

  // 创建画布（1080x1920）
  const canvas = createCanvas(1080, 1920);
  const ctx = canvas.getContext('2d');

  // 绘制背景图
  ctx.drawImage(bgImage, 0, 0, 1080, 1920);

  // 添加半透明白色遮罩（上半部分）
  ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
  ctx.fillRect(0, 0, 1080, 900);

  // 添加半透明白色遮罩（下半部分，文字区域）
  ctx.fillStyle = 'rgba(255, 255, 255, 0.25)';
  ctx.fillRect(0, 800, 1080, 1120);

  // 配色方案（今日四元素）
  const colors = {
    fire: '#E67E22',    // 暖橙色
    earth: '#D4A574',   // 土黄色
    metal: '#D4AF37',   // 金色
    water: '#87CEEB',   // 淡蓝色
    wood: '#2ECC71',    // 木绿色
    dark: '#2C3E50'     // 深色文字
  };

  // 设置文字样式
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // 标题 - 八字合盘
  ctx.font = 'bold 64px "Microsoft YaHei", sans-serif';
  ctx.fillStyle = colors.fire;
  ctx.fillText('八字合盘', 540, 150);

  // 日期
  ctx.font = '32px "Microsoft YaHei", sans-serif';
  ctx.fillStyle = colors.dark;
  ctx.fillText('2026年4月11日 · 丙午年', 540, 220);

  // 分割线
  ctx.strokeStyle = colors.earth;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(240, 270);
  ctx.lineTo(840, 270);
  ctx.stroke();

  // 四柱八字
  const pillars = [
    { name: '年柱', gan: '丙', zhi: '午', element: '火火' },
    { name: '月柱', gan: '壬', zhi: '辰', element: '水土' },
    { name: '日柱', gan: '乙', zhi: '巳', element: '木火' },
    { name: '时柱', gan: '壬', zhi: '午', element: '水火' }
  ];

  // 绘制四柱
  pillars.forEach((pillar, index) => {
    const y = 380 + index * 140;

    // 柱名称
    ctx.font = '24px "Microsoft YaHei", sans-serif';
    ctx.fillStyle = colors.dark;
    ctx.fillText(pillar.name, 200, y);

    // 天干（大）
    ctx.font = 'bold 72px "Microsoft YaHei", serif';
    ctx.fillStyle = colors.fire;
    ctx.fillText(pillar.gan, 350, y + 10);

    // 地支（大）
    ctx.fillStyle = colors.earth;
    ctx.fillText(pillar.zhi, 470, y + 10);

    // 五行元素（小）
    ctx.font = '20px "Microsoft YaHei", sans-serif';
    ctx.fillStyle = colors.water;
    ctx.fillText(pillar.element, 580, y);

    // 装饰线条
    ctx.strokeStyle = colors.metal;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(220, y + 50);
    ctx.lineTo(280, y + 50);
    ctx.stroke();
  });

  // 底部装饰线
  ctx.strokeStyle = colors.water;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(150, 980);
  ctx.lineTo(930, 980);
  ctx.stroke();

  // 美学说明
  ctx.font = '28px "Microsoft YaHei", sans-serif';
  ctx.fillStyle = colors.dark;
  ctx.fillText('今日美学 · 现代国画写意', 540, 1050);

  ctx.font = '20px "Microsoft YaHei", sans-serif';
  ctx.fillStyle = '#7F8C8D';
  ctx.fillText('暖橙色光晕 · 土黄色墨线 · 金色光泽 · 淡蓝水波', 540, 1100);

  // 底部签名
  ctx.font = '16px "Microsoft YaHei", sans-serif';
  ctx.fillStyle = '#95A5A6';
  ctx.fillText('Aesthetics Designer · 小清新美学', 540, 1850);

  // 保存图片
  const buffer = canvas.toBuffer('image/jpeg', { quality: 0.9 });
  fs.writeFileSync('/tmp/aesthetic/bazi_poster.jpg', buffer);

  console.log('✅ 海报生成成功！');
  console.log('📁 保存路径: /tmp/aesthetic/bazi_poster.jpg');
}

generatePoster().catch(console.error);
