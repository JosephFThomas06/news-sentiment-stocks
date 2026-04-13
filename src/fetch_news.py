import requests
import pandas as pd
from datetime import datetime

def fetch_news(api_key, tickers):
    all_articles = []
    
    queries = {
        "AAPL": "Apple stock",
        "TSLA": "Tesla stock",
        "NVDA": "Nvidia stock",
        "MSFT": "Microsoft stock",
        "AMZN": "Amazon stock",
        "META": "Meta stock",
        "GOOGL": "Google stock",
        "AMD": "AMD stock",
        "SPY": "S&P 500",
        "NFLX": "Netflix stock",
        "PLTR": "Palantir stock"
    }
    
    for ticker, query in queries.items():
        print(f"Fetching news for {ticker}...")
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&"
            f"language=en&"
            f"sortBy=publishedAt&"
            f"pageSize=50&"
            f"apiKey={api_key}"
        )
        response = requests.get(url)
        data = response.json()
        
        if data.get("status") != "ok":
            print(f"  Error for {ticker}: {data.get('message')}")
            continue
            
        for article in data.get("articles", []):
            all_articles.append({
                "ticker": ticker,
                "title": article.get("title", ""),
                "text": article.get("description", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", ""),
                "url": article.get("url", "")
            })
    
    df = pd.DataFrame(all_articles)
    print(f"\nFetched {len(df)} total articles across {df['ticker'].nunique()} tickers.")
    return df

if __name__ == "__main__":
    API_KEY = "b3b405575874434bb8b5535d09baad9a"  
    
    tickers = list({
        "AAPL", "TSLA", "NVDA", "MSFT", "AMZN",
        "META", "GOOGL", "AMD", "SPY", "NFLX", "PLTR"
    })
    
    df = fetch_news(API_KEY, tickers)
    df.to_csv("data/raw/news_articles.csv", index=False)
    print("Saved to data/raw/news_articles.csv")