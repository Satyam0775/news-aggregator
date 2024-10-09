import feedparser
from models import NewsArticle, db

# List of RSS feeds to fetch from
feeds = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics'
]

# Function to fetch and return news from RSS feeds
def fetch_news_feed():
    articles = []
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            article = {
                'title': entry.title,
                'content': entry.summary,
                'publication_date': entry.published,
                'source_url': entry.link,
                'category': 'Others'  # You can categorize based on the feed or content
            }
            articles.append(article)
    return articles

# Function to fetch and store news articles in the database
def fetch_and_store_news():
    articles = fetch_news_feed()
    for article in articles:
        # Check if the article already exists
        if not NewsArticle.query.filter_by(source_url=article['source_url']).first():
            # Create a new NewsArticle object
            new_article = NewsArticle(
                title=article['title'],
                content=article['content'],
                publication_date=article['publication_date'],
                source_url=article['source_url'],
                category=article['category']
            )
            # Add the new article to the session
            db.session.add(new_article)
    # Commit the changes to the database
    db.session.commit()
