import { LarkClient } from '/workspace/projects/extensions/openclaw-lark/src/core/lark-client.js';
import { uploadImageLark, sendImageLark, sendTextLark } from '/workspace/projects/extensions/openclaw-lark/src/messaging/outbound/media.js';
import { sendTextLark as sendText } from '/workspace/projects/extensions/openclaw-lark/src/messaging/outbound/deliver.js';
import fs from 'fs';

// 飞书群聊 ID
const chatId = 'oc_95076f564f595dc80ae416c8221ad806';

// 图片路径
const imagePath = '/workspace/projects/workspace-aesthetic/temp/bazi_poster.png';

// 文本消息
const textMessage = `🎨 今日美学设计日报

**日期**：2026年4月15日（星期三）
**干支**：丙午年 壬辰月 己亥日 戊辰时

✅ 完成八字合盘海报设计
✅ 创作现代国画写意风格背景图
✅ 合成1080x1920尺寸海报
✅ 发送到美学群

**设计元素**：
- 🌅 配色：暖橙色光晕 + 土黄色墨线 + 金色光泽 + 淡蓝水波纹
- 🖊️ 线条：简约国画墨线，留白克制
- ✨ 氛围：极简诧寂风，东方美学，温暖治愈

**五行统计**：
- 土 ×4（主导）
- 火 ×2（温暖）
- 水 ×2（流动）

💡 美学建议
- 土元素为主，适合沉稳、内敛的设计风格
- 火水相济，动静结合，营造温暖而灵动的氛围
- 留白充足，意境深远，符合诧寂风美学

🖼️ 设计作品
- 作品名称：丙午 壬辰 己亥 戊辰 八字合盘海报
- 作品风格：现代国画写意，小清新美学
- 设计思路：以土为底，火暖金耀，水流灵动，留白为韵

愿今日的设计作品能为你带来温暖与灵感~ 🌸✨`;

async function main() {
  try {
    console.log('开始上传图片...');

    // 读取图片文件
    const imageBuffer = fs.readFileSync(imagePath);
    console.log(`图片大小: ${imageBuffer.length} bytes`);

    // 获取飞书配置
    // 注意：这里需要实际的飞书配置
    // 暂时跳过，因为我们需要正确的配置

    console.log('脚本准备完成，但需要飞书配置才能执行');
    console.log('请确保已配置飞书 API 凭据');

  } catch (error) {
    console.error('错误:', error);
    process.exit(1);
  }
}

main();
