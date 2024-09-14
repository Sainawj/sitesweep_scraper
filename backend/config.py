import os

# Flask configuration
SECRET_KEY = os.getenv('SECRET_KEY', '4871b4b9cd4a257721a09f44ecca7866c60479a5bd184ef699249b2e56de32b3')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# MySQL database configuration
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sitesweepuser:sweeperoot@localhost/scraping_db'

