import pandas as pd
from sqlalchemy.orm import Session
from database_setup import engine, Session as DBSession, Review, Bank  # Import from setup
from datetime import datetime
import pandas as pd  # Already imported, but ensure


def insert_reviews():
    session = DBSession()

    # Load full processed data (MODIFY: Update CSV path if needed)
    csv_path = 'data/processed/reviews_with_sentiment_themes.csv'
    df = pd.read_csv(csv_path)
    print(f"Inserting {len(df)} analyzed reviews...")

    inserted = 0
    skipped = 0
    for _, row in df.iterrows():
        bank = session.query(Bank).filter_by(bank_name=row['bank']).first()
        if not bank:
            skipped += 1
            continue

        # Handle NaNs
        sentiment_score = float(row.get('sentiment_compound', 0)) if pd.notna(
            row.get('sentiment_compound')) else None
        theme = str(row.get('theme', 'Other'))

        review = Review(
            bank_id=bank.bank_id,
            review_text=str(row['review']) if pd.notna(row['review']) else '',
            rating=float(row['rating']),
            review_date=datetime.strptime(str(row['date']), '%Y-%m-%d').date(),
            sentiment_label=str(row['sentiment_label']),
            sentiment_score=sentiment_score,
            source=str(row['source']),
            theme=theme
        )
        session.add(review)
        inserted += 1

    session.commit()
    session.close()
    print(f"Inserted {inserted} reviews ({skipped} skipped).")


def verify_data():
    with engine.connect() as conn:
        # Counts per bank
        counts = conn.execute("""
            SELECT b.bank_name, COUNT(r.review_id) as count 
            FROM banks b LEFT JOIN reviews r ON b.bank_id = r.bank_id 
            GROUP BY b.bank_name;
        """).fetchall()
        print("Reviews per bank:")
        for name, cnt in counts:
            print(f"  {name}: {cnt}")

        # Aggregates
        avg_rating = conn.execute("SELECT AVG(rating) FROM reviews;").scalar()
        total = conn.execute("SELECT COUNT(*) FROM reviews;").scalar()
        print(f"Total reviews: {total}")
        print(f"Avg rating: {avg_rating:.2f}")

        # Sample
        sample = conn.execute(
            "SELECT sentiment_label, theme FROM reviews LIMIT 5;").fetchall()
        print("Sample sentiment/theme:", sample)


if __name__ == "__main__":
    insert_reviews()
    verify_data()
