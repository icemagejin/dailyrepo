#!/bin/bash
# 使用飞书 API 上传并发送海报到群聊

FEISHU_APP_ID="cli_a907edcff0785cb5"
FEISHU_APP_SECRET="t2229c0w2naILX2CoIneefjeuaSxpYo6"
CHAT_ID="oc_95076f564f595dc80ae416c8221ad806"
IMAGE_PATH="/workspace/projects/workspace-aesthetic/posters/poster-2026-04-13.jpg"

echo "📤 获取 tenant_access_token..."
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"$FEISHU_APP_ID\",
    \"app_secret\": \"$FEISHU_APP_SECRET\"
  }")

TENANT_ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.tenant_access_token')

if [ "$TENANT_ACCESS_TOKEN" == "null" ]; then
  echo "❌ 获取 token 失败: $TOKEN_RESPONSE"
  exit 1
fi

echo "✅ tenant_access_token 获取成功"

echo "📤 上传图片到飞书..."
UPLOAD_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -F "image_type=message" \
  -F "image=@$IMAGE_PATH")

IMAGE_KEY=$(echo $UPLOAD_RESPONSE | jq -r '.data.image_key')

if [ "$IMAGE_KEY" == "null" ]; then
  echo "❌ 图片上传失败: $UPLOAD_RESPONSE"
  exit 1
fi

echo "✅ 图片上传成功: image_key=$IMAGE_KEY"

echo "📤 发送图片到群聊..."
SEND_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"$CHAT_ID\",
    \"msg_type\": \"image\",
    \"content\": \"{\\\"image_key\\\": \\\"$IMAGE_KEY\\\"}\"
  }")

MESSAGE_ID=$(echo $SEND_RESPONSE | jq -r '.data.message_id')

if [ "$MESSAGE_ID" == "null" ]; then
  echo "❌ 消息发送失败: $SEND_RESPONSE"
  exit 1
fi

echo "✅ 图片发送成功: message_id=$MESSAGE_ID"
