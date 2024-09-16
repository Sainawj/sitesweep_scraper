from bs4 import BeautifulSoup
import requests
import re

def scrape_data(url):
    try:
        # Fetch the page content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Extract Metadata
        page_title = soup.title.string if soup.title else "No title found"
        meta_description = ""
        meta_tag = soup.find("meta", {"name": "description"})
        if meta_tag:
            meta_description = meta_tag.get("content", "No description found")

        # 2. Extract Contact Information
        # Emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', response.text)

        # Phone Numbers (basic regex for common formats)
        phones = re.findall(r'\+?\d[\d -]{8,}\d', response.text)

        # Addresses (simplified, based on common address keywords)
        addresses = []
        address_keywords = ["P. O. Box", "P.O. Box","P.O Box", "PO Box", "Street", "St.", "Avenue", "Ave.", "Road", "Rd.", "Boulevard", "Blvd.", "Drive", "Dr.", "Lane", "Ln.", "Way", "Plaza"]
        for keyword in address_keywords:
            addresses += soup.find_all(text=re.compile(rf'\b{keyword}\b'))

        return {
            "title": page_title,
            "description": meta_description,
            "emails": emails,
            "phones": phones,
            "addresses": addresses
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {"error": str(e)}
