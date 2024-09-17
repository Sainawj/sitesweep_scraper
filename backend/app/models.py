from datetime import datetime
from . import db
from flask_login import UserMixin

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

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'
