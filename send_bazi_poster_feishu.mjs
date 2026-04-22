#!/usr/bin/env node
/**
 * 发送八字合盘海报到飞书美学群
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 动态导入飞书插件
const pluginPath = join(__dirname, '../extensions/openclaw-lark/index.js');
const { uploadImageLark, sendImageLark } = await import(pluginPath);

async function sendPoster(imagePath) {
  const config = {
    appId: process.env.FEISHU_APP_ID || process.env.OPENCLAW_FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET || process.env.OPENCLAW_FEISHU_APP_SECRET,
  };

  const target = 'oc_95076f564f595dc80ae416c8221ad806'; // 美学群

  try {
    console.log('📤 上传图片到飞书...');
    const { imageKey } = await uploadImageLark({
      cfg: config,
      image: imagePath,
      imageType: 'message',
    });
    console.log(`✅ 图片上传成功: image_key=${imageKey}`);

    console.log('📤 发送图片到群聊...');
    const result = await sendImageLark({
      cfg: config,
      to: target,
      imageKey,
    });
    console.log(`✅ 图片发送成功: message_id=${result.messageId}`);
    return result;

  } catch (error) {
    console.error('❌ 发送失败:', error.message);
    throw error;
  }
}

// 导出函数供外部调用
export { sendPoster };
