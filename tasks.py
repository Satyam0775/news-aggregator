import time
from feed_parser import fetch_news_feed  # Assuming this function fetches parsed news
from models import NewsArticle, db
from app import create_app

# Create the app context for accessing the database
app = create_app()

# This function will handle the process of adding articles to the database
def add_articles_to_db():
    with app.app_context():
        articles = fetch_news_feed()  # Fetches news from RSS feeds (defined in feed_parser.py)
        for article in articles:
            # Check if article already exists by source URL (avoiding duplicates)
            existing_article = NewsArticle.query.filter_by(source_url=article['source_url']).first()
            if not existing_article:
                # Create a new NewsArticle object from parsed article data
                new_article = NewsArticle(
                    title=article['title'],
                    content=article['content'],
                    publication_date=article['publication_date'],
                    source_url=article['source_url'],
                    category=article['category']
                )
                # Add the new article to the database
                db.session.add(new_article)
        # Commit the changes to the database
        db.session.commit()

# This function could be run periodically (or you can use something like Celery for periodic execution)
def run_news_update_task():
    while True:
        print("Fetching and adding news articles to the database...")
        add_articles_to_db()
        print("Sleeping for 1 hour before fetching again...")
        time.sleep(3600)  # Sleep for an hour before checking for new articles again

if __name__ == '__main__':
    run_news_update_task()
