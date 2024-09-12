import pytest
from app.scraper import scrape_data

def test_scrape_data(mocker):
    mocker.patch('requests.get').return_value.status_code = 200
    mocker.patch('requests.get').return_value.content = """
    <html><head><title>Test Page</title></head><body><p>Description</p></body></html>
    """
    data = scrape_data("https://example.com")
    
    assert data['title'] == "Test Page"
    assert "Description" in data['description']
