from app import app

def test_config():
    assert app.config['TESTING'] is False  # Default setting
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql://username:password@localhost/scraper_db'
