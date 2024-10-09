from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    publication_date = db.Column(db.String)
    source_url = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String, nullable=False)
