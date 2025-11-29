import pandas as pd
from sqlalchemy.orm import Session
from database_setup import engine, Session as DBSession, Review, Bank  # From above
from datetime import datetime


def insert_reviews():
    session = DBSession()

    # Load processed data (Task 2 output; adjust path)
    csv_path = 'data/processed/reviews_with_sentiment_themes.csv'
    df = pd.read_csv(csv_path)
    print(f"Inserting {len(df)} reviews...")

    inserted = 0
    for _, row in df.iterrows():
        # Map to model
        bank = session.query(Bank).filter_by(bank_name=row['bank']).first()
        if not bank:
            print(f"Skipping review for unknown bank: {row['bank']}")
            continue

        review = Review(
            bank_id=bank.bank_id,
            review_text=str(row['review']),
            rating=float(row['rating']),
            review_date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
            sentiment_label=str(row['sentiment_label']),
            sentiment_score=float(
                row['sentiment_compound']) if 'sentiment_compound' in row else None,
            source=str(row['source'])
        )
        session.add(review)
        inserted += 1

    session.commit()
    session.close()
    print(f"Inserted {inserted} reviews successfully.")

# Verify integrity


def verify_data():
    with engine.connect() as conn:
        result = conn.execute("SELECT COUNT(*) FROM reviews GROUP BY bank_id;")
        print("Reviews per bank:", result.fetchall())

        avg_rating = conn.execute("SELECT AVG(rating) FROM reviews;").scalar()
        print(f"Avg rating in DB: {avg_rating:.2f}")

        review_count = conn.execute("SELECT COUNT(*) FROM reviews;").scalar()
        print(f"Total reviews in DB: {review_count}")


if __name__ == "__main__":
    insert_reviews()
    verify_data()
