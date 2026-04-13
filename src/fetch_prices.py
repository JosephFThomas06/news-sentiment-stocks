import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_prices(tickers, days_back=30):
    print(f"Fetching price data for {len(tickers)} tickers...")
    
    end = datetime.today()
    start = end - timedelta(days=days_back)
    
    # Download all tickers at once
    raw = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=True)
    
    # Pull just Close prices and flatten
    close = raw["Close"].reset_index()
    
    # Melt from wide to long format
    df = close.melt(id_vars="Date", var_name="ticker", value_name="close")
    df.columns = ["date", "ticker", "close"]
    df = df.dropna(subset=["close"])
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    
    print(f"  Fetched {len(df)} price rows for {df['ticker'].nunique()} tickers.")
    return df

if __name__ == "__main__":
    tickers = [
        "AAPL", "TSLA", "NVDA", "MSFT", "AMZN", "META", "GOOGL",
        "AMD", "SPY", "NFLX", "PLTR"
    ]
    df = fetch_stock_prices(tickers)
    df.to_csv("data/processed/stock_prices.csv", index=False)
    print("Saved to data/processed/stock_prices.csv")