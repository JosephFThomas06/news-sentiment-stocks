import pandas as pd
import sqlite3
import os

DB_PATH = "data/sentiment.db"

def load_table(df, table_name, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    count = pd.read_sql(f"SELECT COUNT(*) as n FROM {table_name}", conn).iloc[0]["n"]
    print(f"  Loaded {count} rows into '{table_name}'")
    conn.close()

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    sentiment = pd.read_csv("data/processed/articles_with_sentiment.csv")
    prices = pd.read_csv("data/processed/stock_prices.csv")
    load_table(sentiment, "sentiment_articles")
    load_table(prices, "stock_prices")
    print("Done. Database saved to:", DB_PATH)