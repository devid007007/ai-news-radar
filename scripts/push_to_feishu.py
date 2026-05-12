import json
import requests
import os

# 读取最新24小时新闻
with open("data/latest-24h.json", "r", encoding="utf-8") as f:
    news_data = json.load(f)

# 取出新闻列表
news = news_data.get("items", [])

if not news:
    print("无新新闻，不推送")
    exit()

# 飞书 Webhook
feishu_webhook = os.getenv("FEISHU_WEBHOOK_URL")
if not feishu_webhook:
    print("未配置 FEISHU_WEBHOOK_URL")
    exit()

# 构造纯文本消息（飞书自定义机器人只支持这个！）
msg = "🤖 AI 最新资讯（24小时）\n\n"
for item in news[:5]:
    title = item.get("title", "无标题")
    url = item.get("url", "")
    msg += f"• {title}\n{url}\n\n"

# 发送到飞书（关键：必须用 text 格式）
payload = {
    "msg_type": "text",
    "content": {
        "text": msg
    }
}

resp = requests.post(feishu_webhook, json=payload)
print("推送成功！返回结果：", resp.text)
