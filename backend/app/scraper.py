import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    # Fetch the web page content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data from {url}")

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Extract the title and meta description
    title = soup.find('title').get_text()
    description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No description available'

    # Return scraped data as a dictionary
    return {
        "title": title,
        "description": description
    }
