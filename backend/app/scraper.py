import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    try:
        # Make a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the desired data (customize based on your target site structure)
        data = soup.find('body').get_text()  # Simplified example
        
        # Return the scraped data
        return data
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Error scraping data: {str(e)}")

