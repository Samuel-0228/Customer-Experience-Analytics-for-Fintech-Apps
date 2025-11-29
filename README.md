# Fintech Review Analysis

Data engineering project: Scraping, analyzing, and visualizing Google Play Store reviews for Ethiopian banks (CBE, BOA, Dashen) to drive app improvements.

## Overview
- **Business Goal:** Identify sentiment, themes, drivers/pain points for customer retention in mobile banking.
- **Tech Stack:** Python, google-play-scraper, Pandas, VADER/NLP, PostgreSQL, Git.
- **Tasks:** Scraping → Analysis → DB → Insights/Visuals.

## Setup
1. Clone repo: `git clone https://github.com/yourusername/fintech-review-analysis.git`
2. Install deps: `pip install -r requirements.txt`
3. (Later) Set up Postgres: See Task 3.

## Usage
- Task 1: `python src/scrape.py` → Scrapes to `data/raw/reviews_raw.csv`
- Task 1: `python src/preprocess.py` → Cleans to `data/processed/reviews_clean.csv`
- Branches: `task-1` (scraping), `task-2` (analysis), etc.

## Methodology
- Scraping: google-play-scraper for 400+ reviews per bank (English, Ethiopia).
- Preprocessing: Dedupe, normalize dates, handle NaNs.
- Data: Columns - review (text), rating (1-5), date (YYYY-MM-DD), bank, source.

### Scraping Results
- Fetched all reviews + sliced to 450/bank → ~1200 total.
- Fixed: No 'num' param in library; used DF.head().
- Stats: Avg rating 3.9; Recent dates up to Nov 2025.
- Challenges: Verified IDs; added sleeps to avoid throttling.

- Task 1: `python src/preprocess.py` → Cleans to `data/processed/reviews_clean.csv` (~1100 rows, <5% missing).
### Preprocessing Results
- Input: 1350 raw → Output: 1330 clean (1.5% drop).
- Fixed bug: Accurate row drop tracking for missing data.
- Validation: <1% missing, balanced banks (~430 each), dates normalized to YYYY-MM-DD.

## License
MIT (or as appropriate).