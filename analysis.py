import pandas as pd
import ta

def compute_indicators(hist):
    """
    給定包含至少一個月資料的 DataFrame，計算最新的 RSI, 10MA, 20MA，並給出簡單訊號
    """
    if hist is None or len(hist) < 20:
        # 資料天數不足以計算全部指標，回傳空指標
        return None
        
    close = hist["Close"]
    
    # 計算 RSI (14天)
    rsi_series = ta.momentum.RSIIndicator(close, window=14).rsi()
    latest_rsi = rsi_series.iloc[-1]
    
    # 計算均線 MA10, MA20
    ma10_series = close.rolling(window=10).mean()
    ma20_series = close.rolling(window=20).mean()
    
    ma10 = ma10_series.iloc[-1]
    ma20 = ma20_series.iloc[-1]
    
    latest_price = close.iloc[-1]
    prev_price = close.iloc[-2]
    prev_ma20 = ma20_series.iloc[-2]
    
    signals = []
    
    # RSI 訊號判斷
    if pd.notna(latest_rsi):
        if latest_rsi > 70:
            signals.append("RSI 超買 (>70)，短期可能回調")
        elif latest_rsi < 30:
            signals.append("RSI 超賣 (<30)，短期可能反彈")
            
    # 均線多空判斷
    if pd.notna(ma20) and pd.notna(prev_ma20):
        if latest_price > ma20 and prev_price <= prev_ma20:
            signals.append("⚡ 價格剛向上突破 20MA (轉強)")
        elif latest_price < ma20 and prev_price >= prev_ma20:
            signals.append("⚠️ 價格剛向下測試 20MA (轉弱)")
            
    return {
        "rsi": float(latest_rsi) if pd.notna(latest_rsi) else None,
        "ma10": float(ma10) if pd.notna(ma10) else None,
        "ma20": float(ma20) if pd.notna(ma20) else None,
        "signals": signals
    }
