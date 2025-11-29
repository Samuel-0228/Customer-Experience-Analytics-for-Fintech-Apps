import pandas as pd
from datetime import datetime
import os


def preprocess_reviews(raw_path: str, processed_path: str) -> pd.DataFrame:
    """
    Preprocess scraped reviews: Dedupe, handle NaNs, normalize dates, basic text clean.

    Args:
        raw_path: Path to raw CSV
        processed_path: Path to save processed CSV

    Returns:
        Cleaned DataFrame
    """
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw file not found: {raw_path}")

    print("Loading raw data...")
    df = pd.read_csv(raw_path, encoding='utf-8')
    overall_initial_len = len(df)
    print(f"Initial shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    # Step 1: Drop duplicates based on review + date (exact matches)
    print("\nDropping duplicates...")
    df.drop_duplicates(subset=['review', 'date'], inplace=True)
    dedup_len = len(df)
    print(
        f"Dropped {overall_initial_len - dedup_len} duplicates. Shape after dedup: {df.shape}")

    # Step 2: Handle missing data - Drop rows with NaN in core columns (review, rating)
    print("\nHandling missing data...")
    before_drop_len = len(df)
    missing_before = df.isnull().sum()
    core_cols = ['review', 'rating']
    df.dropna(subset=core_cols, inplace=True)
    missing_after = df.isnull().sum()
    dropped_missing = before_drop_len - len(df)
    print(f"Dropped {dropped_missing} rows with missing data in {core_cols}.")
    print(
        f"Missing % overall (after): {df.isnull().sum().sum() / len(df) * 100:.1f}%")

    # Step 3: Normalize dates to YYYY-MM-DD
    print("\nNormalizing dates...")
    # Parse timestamps, NaT on fail
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # To YYYY-MM-DD string
    date_before = len(df)
    df.dropna(subset=['date'], inplace=True)
    print(f"Dropped {date_before - len(df)} rows with invalid dates.")
    print(f"Date range after norm: {df['date'].min()} to {df['date'].max()}")

    # Step 4: Basic text cleaning
    print("\nCleaning text...")
    # Lowercase, remove leading/trailing space
    df['review'] = df['review'].astype(str).str.lower().str.strip()

    # Step 5: Filter short/noisy reviews (e.g., <10 chars)
    print("\nFiltering short reviews...")
    text_before = len(df)
    df = df[df['review'].str.len() > 10]
    print(
        f"Filtered {text_before - len(df)} very short reviews. Final shape: {df.shape}")

    # Ensure required columns exist/order them
    required_cols = ['review', 'rating', 'date', 'bank', 'source']
    for col in required_cols:
        if col not in df.columns:
            df[col] = 'UNKNOWN'
            print(f"Warning: Added missing column '{col}' with 'UNKNOWN'.")

    df = df[required_cols]  # Reorder

    # Save processed
    df.to_csv(processed_path, index=False, encoding='utf-8')
    total_dropped = overall_initial_len - len(df)
    print(f"\n=== Preprocessing Complete ===")
    print(f"Processed data saved to: {processed_path}")
    print(
        f"Total dropped: {total_dropped} ({total_dropped / overall_initial_len * 100:.1f}%)")
    print(f"Final stats:")
    print(df.groupby('bank').size().to_string())
    print(f"Avg rating: {df['rating'].mean():.2f}")

    return df


def main():
    """Main: Run preprocessing on raw file."""
    raw_file = 'data/raw/reviews_raw.csv'
    processed_file = 'data/processed/reviews_clean.csv'

    # Ensure output dir
    os.makedirs('data/processed', exist_ok=True)

    try:
        cleaned_df = preprocess_reviews(raw_file, processed_file)
        print(f"Success! {len(cleaned_df)} clean reviews ready for analysis.")
    except Exception as e:
        print(f"Error in preprocessing: {str(e)}")


if __name__ == "__main__":
    main()
