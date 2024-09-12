import pytest
from app import app, db
from app.models import ScrapingHistory

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data  # Replace with text present in your index.html

def test_scrape_route(client, mocker):
    mock_scraper = mocker.patch('app.scraper.scrape_data')
    mock_scraper.return_value = {'title': 'Test Title', 'description': 'Test Description'}

    response = client.post('/api/scrape', data={'url': 'https://example.com'})
    assert response.status_code == 200
    assert b'Scraping successful' in response.data

def test_history_route(client):
    history = ScrapingHistory(url="https://example.com", data="{'title': 'Test'}")
    db.session.add(history)
    db.session.commit()

    response = client.get('/api/history')
    assert response.status_code == 200
    assert b'https://example.com' in response.data
