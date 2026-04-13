import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def score_sentiment(df):
    analyzer = SentimentIntensityAnalyzer()
    df = df.copy()
    
    print("Scoring sentiment...")
    
    def get_score(row):
        text = str(row.get("title", "")) + " " + str(row.get("text", ""))
        if text.strip() == "":
            return 0.0
        return analyzer.polarity_scores(text)["compound"]
    
    df["sentiment_score"] = df.apply(get_score, axis=1)
    df["sentiment_label"] = df["sentiment_score"].apply(
        lambda x: "positive" if x >= 0.05 else ("negative" if x <= -0.05 else "neutral")
    )
    
    df["published_at"] = pd.to_datetime(df["published_at"], utc=True)
    df["date"] = df["published_at"].dt.date
    
    print(f"  Scored {len(df)} articles.")
    print(df["sentiment_label"].value_counts())
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/raw/news_articles.csv")
    df = score_sentiment(df)
    df.to_csv("data/processed/articles_with_sentiment.csv", index=False)
    print("Saved to data/processed/articles_with_sentiment.csv")