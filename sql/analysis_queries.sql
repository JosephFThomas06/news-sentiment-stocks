-- 1. Average sentiment per ticker
SELECT
    ticker,
    COUNT(*) as post_count,
    ROUND(AVG(sentiment_score), 3) as avg_sentiment,
    SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END) as positive_posts,
    SUM(CASE WHEN sentiment_label = 'negative' THEN 1 ELSE 0 END) as negative_posts
FROM sentiment_posts
GROUP BY ticker
ORDER BY avg_sentiment DESC;


-- 2. Most discussed tickers
SELECT
    ticker,
    COUNT(*) as mentions,
    ROUND(AVG(sentiment_score), 3) as avg_sentiment,
    SUM(score) as total_upvotes
FROM sentiment_posts
GROUP BY ticker
ORDER BY mentions DESC;


-- 3. Highest upvoted posts per ticker
SELECT
    ticker,
    title,
    score as upvotes,
    sentiment_label,
    ROUND(sentiment_score, 3) as sentiment_score
FROM sentiment_posts
ORDER BY score DESC
LIMIT 20;


-- 4. Sentiment vs next day return
-- Join sentiment with price data by ticker and date
SELECT
    s.ticker,
    DATE(s.created_utc) as post_date,
    ROUND(AVG(s.sentiment_score), 3) as avg_daily_sentiment,
    ROUND(AVG(p.daily_return) * 100, 2) as next_day_return_pct
FROM sentiment_posts s
JOIN stock_prices p ON s.ticker = p.ticker
    AND DATE(s.created_utc) = DATE(p.date)
GROUP BY s.ticker, DATE(s.created_utc)
ORDER BY s.ticker, post_date;