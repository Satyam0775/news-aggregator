from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLAlchemy connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Saty%402677sa@localhost:5432/news_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define the NewsArticle model (matches your existing model)
class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    publication_date = db.Column(db.DateTime)
    source_url = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String, nullable=False)

@app.route('/')
def index():
    # Query all articles to display on the home page
    articles = NewsArticle.query.all()
    return render_template('index.html', articles=articles)

@app.route('/category/<category>')
def filter_by_category(category):
    # Filter articles by category
    articles = NewsArticle.query.filter_by(category=category).all()
    return render_template('index.html', articles=articles)

# Temporary route to fix URLs missing http:// or https://
@app.route('/fix_urls')
def fix_urls():
    # Fetch all articles with incorrect URLs (missing http:// or https://)
    incorrect_urls = NewsArticle.query.filter(~NewsArticle.source_url.startswith(('http://', 'https://'))).all()

    for article in incorrect_urls:
        article.source_url = f"http://{article.source_url}"  # Prepend http:// if missing
        db.session.add(article)
    
    # Commit the changes to the database
    db.session.commit()

    return f"Fixed {len(incorrect_urls)} URLs"

# Temporary route to fix example.com placeholder URLs
@app.route('/fix_example_urls')
def fix_example_urls():
    # Fetch all articles with example.com in their URLs
    articles_with_example_urls = NewsArticle.query.filter(NewsArticle.source_url.like('%example.com%')).all()

    for article in articles_with_example_urls:
        # Update placeholder URLs with real URLs (replace these with actual URLs)
        if article.source_url == 'https://example.com/sample-article-1':
            article.source_url = 'https://www.cnn.com/real-news-article-1'
        elif article.source_url == 'https://example.com/sample-article-2':
            article.source_url = 'https://www.bbc.com/real-news-article-2'
        elif article.source_url == 'https://example.com/sample-article-3':
            article.source_url = 'https://www.nytimes.com/real-news-article-3'

        # Add the updated article to the session
        db.session.add(article)

    # Commit the changes to the database
    db.session.commit()

    return f"Updated {len(articles_with_example_urls)} placeholder URLs!"

# Temporary route to fix double prefix 'http://https://'
@app.route('/fix_double_prefix')
def fix_double_prefix():
    # Fetch all articles with 'http://https://' in their URLs
    articles_with_double_prefix = NewsArticle.query.filter(NewsArticle.source_url.like('http://https://%')).all()

    for article in articles_with_double_prefix:
        # Replace 'http://https://' with 'https://'
        article.source_url = article.source_url.replace('http://https://', 'https://')
        db.session.add(article)

    # Commit the changes to the database
    db.session.commit()

    return f"Fixed {len(articles_with_double_prefix)} URLs!"

if __name__ == '__main__':
    app.run(debug=True)
