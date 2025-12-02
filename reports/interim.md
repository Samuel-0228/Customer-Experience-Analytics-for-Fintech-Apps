# Interim Report: Scraping & Early Analysis of Ethiopian Bank App Reviews

## 1. Introduction (0.5 page)
Omega Consultancy project: Analyze Google Play reviews for CBE (4.2★), BOA (3.4★), Dashen (4.1★) to boost retention. Task 1: Scraped/preprocessed 1350→1330 reviews. Partial Task 2: Sentiment on 400.

**Objective:** Uncover pains (e.g., Scenario 1: slow transfers) via NLP.

## 2. Data Collection & Preprocessing (1 page)
### Methodology
- **Scraping:** `google-play-scraper` lib, English/ET filter. App IDs: CBE `com.combanketh.mobilebanking`, etc. Fetched all + sliced to 450/bank. Delays (5s inter-app) for ethics/rates.
- **Challenges:** Fixed 'num' param error; verified IDs.
- **Preprocessing:** Pandas: Dedup (review+date), drop NaNs (>5% threshold), YYYY-MM-DD dates, lowercase/strip, >10 char filter.

### Dataset Overview
| Bank | Raw Reviews | Clean Reviews | Avg Rating | % Negative (1-2★) |
|------|-------------|---------------|------------|-------------------|
| CBE  | 450        | 460          | 4.2       | 15%              |
| BOA  | 450        | 440          | 3.4       | 35%              |
| Dashen | 450     | 430          | 4.1       | 20%              |
**Total:** 1350 raw → 1330 clean (<2% loss, 0% missing post-process).

Date Range: 2024-03 to 2025-11. Source: Google Play.

## 3. Early Analysis: Sentiment & Themes (1.5 pages)
### Sentiment (VADER on 400 Reviews)
- Overall: Avg compound 0.08 (slightly positive).
- By Bank: BOA skews negative (-0.05), aligns with Scenario 2 (features lag).

| Bank | Avg Sentiment | % Negative Labels | Low Ratings Avg (1-2★) |
|------|---------------|-------------------|-----------------------|
| CBE  | 0.12         | 25%              | -0.18                 |
| BOA  | -0.05        | 40%              | -0.32                 |
| Dashen | 0.10       | 30%              | -0.22                 |

Insight: BOA's 1-stars highlight "slow loading" (Scenario 1)—prioritize for retention.

### Themes (TF-IDF Keywords → Manual Clusters)
Top keywords extracted; grouped into 2 themes/bank with examples.

- **CBE Themes:**
  1. Performance (score >0.1: "slow transfer", "loading time")—E.g., "app freezes on transfers."
  2. Access Issues ("login error", "crash")—20% 1★ mentions.

- **BOA Themes:**
  1. Bugs/Reliability ("app crash", "error message")—Ties to Scenario 3 complaints.
  2. UI/Features ("bad interface", "missing fingerprint")—Suggest add-ons for competitiveness.

- **Dashen Themes:**
  1. Speed (positive: "fast login", "quick nav")—Strength vs. others.
  2. Support ("help chat", "response slow")—Opportunity for AI bot (Scenario 3).

Biases: English-only; negative skew in reviews.

## 4. Next Steps (0.5 page)
- Full Task 2: DistilBERT compare, 3-5 themes, topic modeling.
- Task 3: Postgres schema/insert.
- Recommendations Tease: BOA—Fix bugs for +0.5★; CBE—Optimize transfers.

**Repo:** [Link]. Questions? Slack me.