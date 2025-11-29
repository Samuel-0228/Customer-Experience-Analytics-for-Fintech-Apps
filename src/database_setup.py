from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import ENUM
import os
from datetime import date

# Connection (use env for prod; hardcoded for local)
DB_URL = "postgresql://postgres:password@localhost:5432/bank_reviews"  # Update pw/port
engine = create_engine(DB_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Bank(Base):
    __tablename__ = 'banks'

    bank_id = Column(Integer, primary_key=True)
    bank_name = Column(String(50), unique=True)
    app_name = Column(String(100))

    # Relationship
    reviews = relationship("Review", back_populates="bank")


class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.bank_id'))
    review_text = Column(String(1000))  # Text
    rating = Column(Float, nullable=False)  # 1-5
    review_date = Column(Date, nullable=False)
    sentiment_label = Column(SQLEnum(
        'positive', 'negative', 'neutral', name='sentiment_enum'), default='neutral')
    sentiment_score = Column(Float)  # -1 to 1
    source = Column(String(50), default='Google Play')

    # Relationship
    bank = relationship("Bank", back_populates="reviews")

# Create tables


def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created: banks, reviews.")

# Sample insert for banks (run once)


def seed_banks():
    session = Session()
    banks_data = [
        {'bank_name': 'CBE', 'app_name': 'Commercial Bank of Ethiopia Mobile'},
        {'bank_name': 'BOA', 'app_name': 'Bank of Abyssinia Mobile'},
        {'bank_name': 'Dashen', 'app_name': 'Dashen Bank SuperApp'}
    ]
    for data in banks_data:
        if not session.query(Bank).filter_by(bank_name=data['bank_name']).first():
            bank = Bank(**data)
            session.add(bank)
    session.commit()
    session.close()
    print("Banks seeded.")


if __name__ == "__main__":
    create_tables()
    seed_banks()
