import yfinance as yf
import pandas as pd

def fetch_data(symbol, period="2mo"):
    """
    抓取指定代號的歷史資料
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        if hist.empty:
            return None
        return hist
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def get_latest_price(hist):
    """
    從歷史 K 線中取得最新收盤價與漲幅
    """
    if hist is None or hist.empty:
        return None
        
    latest = hist.iloc[-1]
    
    # 假日或資料缺失可能導致只有一筆，如果有兩筆以上再比對前一天
    if len(hist) > 1:
        prev = hist.iloc[-2]
    else:
        prev = latest
    
    price = latest["Close"]
    prev_price = prev["Close"]
    change = price - prev_price
    
    # 避免分母為0
    if prev_price != 0:
        change_pct = (change / prev_price) * 100
    else:
        change_pct = 0
        
    return {
        "price": price,
        "change": change,
        "change_pct": change_pct,
        "date": hist.index[-1].strftime('%Y-%m-%d')
    }
