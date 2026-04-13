import pandas as pd
import sqlite3
import plotly.express as px

DB_PATH = "data/sentiment.db"

def load(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Chart 1 — Sentiment by ticker
sentiment = load("""
    SELECT
        ticker,
        ROUND(AVG(sentiment_score), 3) as avg_sentiment,
        COUNT(*) as article_count
    FROM sentiment_articles
    GROUP BY ticker
    ORDER BY avg_sentiment DESC
""")

fig1 = px.bar(
    sentiment,
    x="ticker",
    y="avg_sentiment",
    color="avg_sentiment",
    color_continuous_scale="RdYlGn",
    title="Average News Sentiment by Ticker",
    labels={"avg_sentiment": "Avg Sentiment Score", "ticker": "Ticker"},
    text="article_count"
)
fig1.write_html("data/sentiment_by_ticker.html")
print("Saved sentiment_by_ticker.html")

# Chart 2 — Sentiment vs Returns
returns = load("""
    SELECT
        s.ticker,
        ROUND(AVG(s.sentiment_score), 3) as avg_sentiment,
        ROUND(AVG(p.daily_return) * 100, 2) as avg_return
    FROM sentiment_articles s
    JOIN stock_prices p ON s.ticker = p.ticker
    GROUP BY s.ticker
""")

fig2 = px.scatter(
    returns,
    x="avg_sentiment",
    y="avg_return",
    text="ticker",
    title="News Sentiment vs Stock Returns",
    labels={
        "avg_sentiment": "Avg Sentiment Score",
        "avg_return": "Avg Daily Return (%)"
    },
    trendline="ols"
)
fig2.write_html("data/sentiment_vs_returns.html")
print("Saved sentiment_vs_returns.html")

print("\nDone! Open the HTML files in your browser to see the charts.")