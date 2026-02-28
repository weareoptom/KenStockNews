import json
import os
from fetcher import fetch_data, get_latest_price
from analysis import compute_indicators
from news import fetch_latest_news
from notifier import send_telegram_message

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"讀取 config.json 失敗: {e}")
        return None

def build_report():
    config = load_config()
    if not config:
        return None, None
        
    targets = config.get("targets", [])
    if not targets:
        print("沒有設定追蹤目標。")
        return None, None
        
    report = "📊 <b>每日投資精華報告</b>\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for t in targets:
        symbol = t.get("symbol")
        name = t.get("name")
        
        print(f"正在擷取 {name} ({symbol}) 的資料...")
        hist = fetch_data(symbol)
        price_info = get_latest_price(hist)
        
        if not price_info:
            report += f"❌ <b>{name} ({symbol})</b>: 無法取得價格資料\n\n"
            continue
            
        p = price_info["price"]
        c_pct = price_info["change_pct"]
        sign = "+" if c_pct > 0 else ""
        
        report += f"🔹 <b>{name} ({symbol})</b>\n"
        report += f"最新價格: {p:.2f} ({sign}{c_pct:.2f}%)\n"
        
        indicators = compute_indicators(hist)
        if indicators:
            rsi = indicators.get("rsi")
            ma20 = indicators.get("ma20")
            if rsi and ma20:
                report += f"RSI(14): {rsi:.1f} | 20MA: {ma20:.2f}\n"
            for sig in indicators.get("signals", []):
                report += f"{sig}\n"
                
        # 抓取新聞
        news_list = fetch_latest_news(symbol, limit=2)
        if news_list:
            report += "📰 相關新聞:\n"
            for n in news_list:
                report += f" - <a href='{n['link']}'>{n['title']}</a>\n"
                
        report += "\n"
        
    return report, config.get("telegram", {})

if __name__ == "__main__":
    print("=" * 40)
    print("開始擷取每日投資資料...")
    print("=" * 40)
    report, tg_config = build_report()
    if report:
        print("\n資料匯總完成，準備發送...")
        send_telegram_message(
            tg_config.get("bot_token", ""),
            tg_config.get("chat_id", ""),
            report
        )
    else:
        print("無法產生報告。")
