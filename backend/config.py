import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://sitesweepuser:sweeperoot@localhost/scraper_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
