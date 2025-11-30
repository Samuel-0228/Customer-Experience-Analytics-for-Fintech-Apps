import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from database_setup import engine

# Setup
plt.style.use('seaborn-v0_8')  # Clean style
fig_dir = 'reports/figs'
os.makedirs(fig_dir, exist_ok=True)


def plot_sentiment_bar(sent_bank_df):
    """Bar: Avg sentiment by bank."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=sent_bank_df.reset_index(),
                x='bank_name', y='mean', ax=ax)
    ax.set_title('Average Sentiment Score by Bank', fontsize=14)
    ax.set_ylabel('Sentiment Score (-1 to 1)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{fig_dir}/sentiment_by_bank.png',
                dpi=300, bbox_inches='tight')
    plt.show()


def plot_theme_heatmap(theme_sent_df):
    """Heatmap: Sentiment by bank/theme."""
    plt.figure(figsize=(10, 6))
    sns.heatmap(theme_sent_df, annot=True, cmap='RdYlGn', center=0, fmt='.2f')
    plt.title('Sentiment Heatmap by Bank and Theme')
    plt.xlabel('Theme')
    plt.ylabel('Bank')
    plt.tight_layout()
    plt.savefig(f'{fig_dir}/theme_sentiment_heatmap.png',
                dpi=300, bbox_inches='tight')
    plt.show()


def plot_rating_dist(df):
    """Histogram: Rating distribution by bank."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x='rating', hue='bank_name',
                 multiple='dodge', bins=5, ax=ax)
    ax.set_title('Rating Distribution by Bank')
    ax.set_xlabel('Rating (1-5)')
    plt.tight_layout()
    plt.savefig(f'{fig_dir}/rating_distribution.png',
                dpi=300, bbox_inches='tight')
    plt.show()


def wordcloud_themes(df, bank_name):
    """Wordcloud for negative reviews in a theme (e.g., Reliability for BOA)."""
    neg_reviews = df[(df['bank_name'] == bank_name) & (
        df['sentiment_score'] < -0.05) & (df['theme'] == 'Reliability')]
    text = ' '.join(neg_reviews['review_text'].str.lower(
    ).dropna().tolist()[:50])  # Sample for cloud
    if text:
        wc = WordCloud(width=800, height=400,
                       background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(
            f'Word Cloud: Negative Reviews - {bank_name} Reliability Theme')
        plt.savefig(f'{fig_dir}/wordcloud_{bank_name}_reliability.png',
                    dpi=300, bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    df = pd.read_csv('data/insights/full_reviews_db.csv')
    sent_bank = pd.read_csv('data/insights/sentiment_summary.csv')
    theme_sent = pd.read_csv(
        'data/insights/sentiment_summary.csv', index_col=0)  # Adjust if needed

    plot_sentiment_bar(sent_bank)
    plot_theme_heatmap(theme_sent)
    plot_rating_dist(df)
    wordcloud_themes(df, 'BOA')  # Example for pain point
    print("Plots saved to reports/figs/.")
