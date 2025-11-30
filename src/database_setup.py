from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date  # Used in insert later

# Connection (MODIFY: Update password/port if needed)
DB_URL = "postgresql://postgres:password@localhost:5432/bank_reviews"
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
    # String for simplicity
    sentiment_label = Column(String(20), default='neutral')
    sentiment_score = Column(Float)  # -1 to 1
    source = Column(String(50), default='Google Play')
    theme = Column(String(50), default='Other')  # From Task 2

    # Relationship
    bank = relationship("Bank", back_populates="reviews")

# Create tables (idempotent)


def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created/verified: banks, reviews.")

# Seed banks (run once)


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
    print("Banks seeded (3 total).")


if __name__ == "__main__":
    create_tables()
    seed_banks()
