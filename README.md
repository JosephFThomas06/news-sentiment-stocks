cat > README.md << 'EOF'
# Financial News Sentiment vs Stock Returns

I built this to explore whether the tone of financial news headlines actually lines up with how stocks perform. Spoiler: it kind of does.

## What It Does
Pulls live news headlines for 11 tickers, runs sentiment analysis on each article using VADER, grabs 30 days of price data, stores everything in SQLite, and generates interactive charts showing how sentiment maps to returns.

## Tech Stack
Python, VADER NLP, NewsAPI, yfinance, SQLite, Plotly

## Tickers
AAPL, TSLA, NVDA, MSFT, AMZN, META, GOOGL, AMD, SPY, NFLX, PLTR

## How to Run
```bash
pip install requests pandas vaderSentiment yfinance plotly statsmodels
mkdir -p data/raw data/processed
python3 src/fetch_news.py
python3 src/score_sentiment.py
python3 src/fetch_prices.py
python3 src/load_to_db.py
python3 src/visualize.py
```

## Output
- `data/sentiment_by_ticker.html` — sentiment breakdown by ticker
- `data/sentiment_vs_returns.html` — scatter plot with trendline showing sentiment vs avg daily return

## What I Found
Tickers with more positive news coverage tended to have better average daily returns over the same period. AMZN had the highest sentiment score and one of the strongest returns. PLTR sat at the bottom on both. Not a trading signal, but an interesting pattern.
EOF
git add README.md
git commit -m "Add README"
git push
