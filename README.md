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

## License
MIT (or as appropriate).