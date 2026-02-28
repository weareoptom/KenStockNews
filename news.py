import yfinance as yf

def fetch_latest_news(symbol, limit=3):
    """
    使用 yfinance 抓取相關股票的最新新聞
    """
    try:
        ticker = yf.Ticker(symbol)
        news_list = ticker.news
        
        if not news_list:
            return []
            
        # 整理出標題與連結
        results = []
        for article in news_list[:limit]:
            results.append({
                "title": article.get("title", "無標題"),
                "link": article.get("link", "#"),
                "publisher": article.get("publisher", "Unknown")
            })
            
        return results
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []
