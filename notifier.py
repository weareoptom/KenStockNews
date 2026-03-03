import requests

def send_telegram_message(bot_token, chat_id, message):
    if not bot_token or not chat_id or bot_token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("⚠️ Telegram bot_token 或是 chat_id 未設定或為預設值。跳過發送，改為在畫面印出報告。")
        print("====================== 產生的報告內容 ======================\n")
        print(message.replace("<b>", "").replace("</b>", "").replace("<a href='", "").replace("'>", " \n    連結: ").replace("</a>", ""))
        print("\n============================================================")
        return
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Telegram 訊息發送成功！ [SUCCESS]")
        else:
            print(f"發送失敗，狀態碼：{response.status_code}, 回應：{response.text} [FAILED]")
    except Exception as e:
        print(f"Telegram 發送發生錯誤：{e} [ERROR]")
