import pandas as pd
from sqlalchemy import create_engine, text
from database_setup import DB_URL  # Reuse connection

engine = create_engine(DB_URL)


def query_insights():
    """Query DB for aggregates: Sentiment by bank/theme, pain points (negative %)."""
    with engine.connect() as conn:
        # Full reviews DF
        df = pd.read_sql("""
            SELECT b.bank_name, r.rating, r.sentiment_label, r.sentiment_score, r.theme, r.review_date
            FROM banks b JOIN reviews r ON b.bank_id = r.bank_id;
        """, conn)

        # Aggregates
        sentiment_by_bank = df.groupby('bank_name')['sentiment_score'].agg([
            'mean', 'count']).round(2)
        negative_pct = df[df['sentiment_score'] < -0.05].groupby(
            'bank_name').size() / df.groupby('bank_name').size() * 100

        theme_sentiment = df.groupby(['bank_name', 'theme'])[
            'sentiment_score'].mean().unstack(fill_value=0).round(2)

        print("Sentiment by Bank:\n", sentiment_by_bank)
        print("\n% Negative Reviews by Bank:\n", negative_pct.round(1))
        print("\nSentiment by Bank/Theme:\n", theme_sentiment)

        # Save for plots
        df.to_csv('data/insights/full_reviews_db.csv', index=False)
        sentiment_by_bank.to_csv('data/insights/sentiment_summary.csv')
        return df, sentiment_by_bank, theme_sentiment


if __name__ == "__main__":
    df, sent_bank, theme_sent = query_insights()
    print(f"Queried {len(df)} reviews from DB.")
