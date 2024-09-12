from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ScrapingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Completed")

    def save(self):
        db.session.add(self)
        db.session.commit()
