from datetime import datetime
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class ScrapingHistory(db.Model):
    __tablename__ = 'scraping_history'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(50), default='Completed')
    title = db.Column(db.String(255))  # Added to store page title
    description = db.Column(db.Text)  # Added to store meta description
    emails = db.Column(db.Text)  # Added to store found email addresses
    phones = db.Column(db.Text)  # Added to store found phone numbers
    addresses = db.Column(db.Text)  # Added to store found physical addresses
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to users table
    user = db.relationship('User', backref=db.backref('scraping_histories', lazy=True))  # Relationship to User

    def to_dict(self):
        """
        Converts the ScrapingHistory model data to a dictionary for JSON serialization.
        """
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'emails': self.emails,
            'phones': self.phones,
            'addresses': self.addresses,
            'date': self.date,
            'status': self.status
        }

    def __repr__(self):
        return f'<ScrapingHistory {self.url}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
