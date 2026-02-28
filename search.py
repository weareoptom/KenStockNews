import requests
import sys
import json

def search_symbol(query):
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=10&newsCount=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"網路連線錯誤: {e}")
        return
    
    if response.status_code != 200:
        print(f"讀取資料錯誤 (狀態碼: {response.status_code})")
        return
        
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("解析資料失敗。")
        return

    quotes = data.get("quotes", [])
    
    if not quotes:
        print(f"\n=> 找不到與 '{query}' 相關的投資產品或股票代號。")
        return
        
    print(f"\n找到以下與 '{query}' 相關的項目：\n")
    print(f"{'代號 (Symbol)':<15} | {'交易所':<15} | {'類型':<15} | {'名稱 (Name)'}")
    print("-" * 90)
    for q in quotes:
        symbol = q.get("symbol", "N/A")
        exch = q.get("exchange", "N/A")
        type_Disp = q.get("quoteType", "N/A")
        shortname = q.get("shortname", q.get("longname", "N/A"))
        print(f"{symbol:<15} | {exch:<15} | {type_Disp:<15} | {shortname}")
    print("\n提示：請將上方的「代號 (Symbol)」加入到 config.json 進行追蹤。\n")

if __name__ == "__main__":
    print("=" * 60)
    print("股票、外匯與加密貨幣代號搜尋工具")
    print("來源: Yahoo Finance 搜尋 API")
    print("=" * 60)
    
    # 如果有帶參數直接搜尋
    if len(sys.argv) > 1:
        search_symbol(" ".join(sys.argv[1:]))
    else:
        while True:
            query = input("請輸入想搜尋的公司名稱或代號 (例如 'Apple', 'HSBC', '2800'，輸入 'q' 離開): ")
            if query.lower().strip() == 'q':
                break
            if query.strip():
                search_symbol(query.strip())
