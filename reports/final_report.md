# Fintech App Review Analysis: Insights & Recommendations

## Executive Summary
Analyzed 1330 Google Play reviews for CBE/BOA/Dashen. Key: BOA lags in reliability (-0.05 sentiment); CBE strong UI but slow transfers. Recs for retention/features.

## Data & Methods
- Scraped 1350 → 1330 clean (Task 1).
- VADER sentiment + TF-IDF themes (Task 2).
- Stored in Postgres (Task 3: banks/reviews tables).

## Insights
### Sentiment Trends
![Sentiment Bar](reports/figs/sentiment_by_bank.png)
BOA: 40% negative, focus bugs.

### Theme Breakdown
![Heatmap](reports/figs/theme_sentiment_heatmap.png)
CBE Performance pain: -0.15 avg.

### Ratings
![Hist](reports/figs/rating_distribution.png)

### Pain/Drivers Table
[Insert table from 4.3]

## Recommendations
[Insert per-bank recs; tie to scenarios]

## Biases & Next
Negative skew; future: Amharic NLP. Appendix: Code/DB schema.

Repo: [[Here](https://github.com/Samuel-0228/Customer-Experience-Analytics-for-Fintech-Apps/tree/task-1/src)]. Questions: Slack.