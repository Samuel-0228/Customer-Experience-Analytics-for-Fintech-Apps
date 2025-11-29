import time
import pandas as pd
from google_play_scraper import reviews_all, Sort
from typing import Dict, List

# Verified app package IDs (from Google Play Store URLs)
APPS: Dict[str, str] = {
    'CBE': 'com.combanketh.mobilebanking',      # Commercial Bank of Ethiopia
    'BOA': 'com.boa.boaMobileBanking',         # Bank of Abyssinia
    'Dashen': 'com.dashen.dashensuperapp'      # Dashen Bank SuperApp
}


def scrape_reviews(bank_name: str, app_id: str, max_reviews: int = 450, lang: str = 'en', country: str = 'ET') -> pd.DataFrame:
    """
    Scrape reviews for a single app using google-play-scraper.

    Args:
        bank_name: Name of the bank (e.g., 'CBE')
        app_id: Google Play package name (e.g., 'com.example.app')
        max_reviews: Max reviews to keep after fetching all (slices DF)
        lang: Language filter (e.g., 'en' for English)
        country: Country filter (e.g., 'ET' for Ethiopia)

    Returns:
        DataFrame with columns: review (content), rating (score 1-5), date (at timestamp), bank, source
    """
    try:
        print(
            f"Fetching all reviews for {bank_name} ({app_id})... (will slice to {max_reviews})")
        result: List[Dict] = reviews_all(
            app_id=app_id,
            sleep_milliseconds=2000,  # 2-sec delay per page (rate limit)
            lang=lang,
            country=country,
            sort=Sort.MOST_RELEVANT,  # Most relevant first
            filter_score_with=None    # All scores (default)
        )

        if not result:
            print(
                f"No reviews found for {app_id}. Check app ID, lang, or country filters.")
            return pd.DataFrame()

        df = pd.DataFrame(result)
        # Select and rename key columns (add more if needed, e.g., 'thumbsUpCount')
        df = df[['content', 'score', 'at', 'userName', 'replyContent']]
        df.rename(columns={
            'content': 'review',
            'score': 'rating',
            'at': 'date'
        }, inplace=True)
        df['bank'] = bank_name
        df['source'] = 'Google Play'

        # Slice to max_reviews (after fetching all)
        df = df.head(max_reviews)

        # Basic early filter: Non-empty reviews, valid ratings
        df = df[df['review'].notna() & (df['rating'].between(1, 5))]

        print(
            f"Successfully scraped and sliced to {len(df)} reviews for {bank_name}.")
        return df

    except Exception as e:
        print(f"Error scraping {app_id} ({bank_name}): {str(e)}")
        # Optional: Log to file for debugging
        with open('scrape_errors.log', 'a') as f:
            f.write(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {bank_name}: {str(e)}\n")
        return pd.DataFrame()


def main():
    """Main function: Scrape all apps and combine into raw CSV."""
    all_reviews: List[pd.DataFrame] = []

    for bank_name, app_id in APPS.items():
        print(f"\n--- Starting scrape for {bank_name} ({app_id}) ---")
        reviews_df = scrape_reviews(bank_name, app_id, max_reviews=450)

        if not reviews_df.empty:
            all_reviews.append(reviews_df)
        else:
            print(f"Skipping {bank_name} due to empty results.")

        # Rate limit: Wait between apps
        time.sleep(5)

    if all_reviews:
        combined_df = pd.concat(all_reviews, ignore_index=True)
        raw_path = 'data/raw/reviews_raw.csv'
        combined_df.to_csv(raw_path, index=False, encoding='utf-8')

        print(f"\n=== Scraping Complete ===")
        print(f"Total reviews collected: {len(combined_df)}")
        print("Breakdown:")
        print(combined_df.groupby('bank').size().to_string())
        print(f"Raw data saved to: {raw_path}")

        # Quick stats
        print(f"Avg rating overall: {combined_df['rating'].mean():.2f}")
        print(
            f"Date range: {pd.to_datetime(combined_df['date']).min().strftime('%Y-%m-%d')} to {pd.to_datetime(combined_df['date']).max().strftime('%Y-%m-%d')}")
    else:
        print("No reviews scraped. Check app IDs, internet, or library version. See scrape_errors.log if created.")


if __name__ == "__main__":
    main()
