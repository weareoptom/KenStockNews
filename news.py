import feedparser
import urllib.parse
from datetime import datetime
import re

# 定義信任的新聞來源 (網域)
TRUSTED_SOURCES_ZH = [
    "hket.com",
    "aastocks.com",
    "hk.finance.yahoo.com",
    "hkej.com",
    "news.rthk.hk"
]

TRUSTED_SOURCES_EN = [
    "reuters.com",
    "bloomberg.com",
    "cnbc.com",
    "ft.com",
    "wsj.com"
]

def clean_html_tags(text):
    """移除 HTML 標籤"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def fetch_latest_news(symbol, limit=3, name=None):
    """
    透過 Google News RSS 抓取指定關鍵字的最新新聞，
    並限制在信任的來源當中。
    """
    try:
        # 如果有傳入公司名稱，用公司名稱搭配代號搜尋準確率較高；若無，直接用代號搜尋
        query_term = name if name else symbol
        
        # 建立 source 過濾字串 (例如 site:hket.com OR site:aastocks.com ...)
        # 這裡示範預設中英文來源都包進去，讓 Google 自己去配對相關度最高的新聞
        all_sources = TRUSTED_SOURCES_ZH + TRUSTED_SOURCES_EN
        source_query = " OR ".join([f"site:{s}" for s in all_sources])
        
        # 組合完整的搜尋字串
        search_query = f"{query_term} ({source_query})"
        
        # URL encode
        encoded_query = urllib.parse.quote(search_query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            # 嘗試只用代號搜看看
            encoded_query = urllib.parse.quote(f"{symbol} ({source_query})")
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
            feed = feedparser.parse(rss_url)
            
        if not feed.entries:
            return []
            
        results = []
        for article in feed.entries[:limit]:
            # Google News 的 title 通常格式為 "新聞標題 - 來源網站明稱"
            raw_title = article.title
            
            # 嘗試切出真正的標題和來源
            title_parts = raw_title.rsplit(" - ", 1)
            if len(title_parts) == 2:
                title, publisher = title_parts
            else:
                title = raw_title
                publisher = article.get("source", {}).get("title", "Unknown")
            
            results.append({
                "title": clean_html_tags(title),
                "link": article.link,
                "publisher": publisher
            })
            
        return results
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []

if __name__ == "__main__":
    # 簡單測試
    print("Testing fetch: 騰訊 (0700.HK)")
    news = fetch_latest_news("0700.HK", limit=3, name="騰訊")
    for n in news:
        print(f"[{n['publisher']}] {n['title']}\n -> {n['link']}")
