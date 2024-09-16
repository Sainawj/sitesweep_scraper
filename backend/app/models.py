from datetime import datetime
from . import db

class ScrapingHistory(db.Model):
    __tablename__ = 'scraping_history'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(50), default='Completed')
    
    # New columns for metadata and contact information
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    emails = db.Column(db.Text)
    phones = db.Column(db.Text)
    addresses = db.Column(db.Text)

    def __repr__(self):
        return f'<ScrapingHistory {self.url}>'
