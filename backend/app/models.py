from datetime import datetime
from . import db
from flask_sqlalchemy import SQLAlchemy

class ScrapingHistory(db.Model):
    __tablename__ = 'scraping_history'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(50), default='Completed')
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    emails = db.Column(db.Text)
    phones = db.Column(db.Text)
    addresses = db.Column(db.Text)

    def __repr__(self):
        return f'<ScrapingHistory {self.url}>'
