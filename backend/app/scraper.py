from bs4 import BeautifulSoup
import requests
import re

def scrape_data(url):
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
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

        # Phone Numbers (improved regex and context-based extraction)
        phone_keywords = ["Tel:", "Phone:", "Contact:", "Mobile:", "Cell:"]
        phone_numbers = set()  # Use a set to avoid duplicates

        # Regex pattern to capture phone numbers
        phone_pattern = re.compile(r'\+?\d[\d\s\-\(\)\/]{8,}\d')

        # Search in visible text
        for keyword in phone_keywords:
            # Find all text that contains the keyword
            found_texts = soup.find_all(text=re.compile(rf'\b{keyword}\b', re.IGNORECASE))
            for text in found_texts:
                # Extract potential phone numbers
                potential_numbers = phone_pattern.findall(text)
                for number in potential_numbers:
                    # Clean up the numbers to remove extra spaces or symbols
                    cleaned_number = re.sub(r'\D', '', number)
                    if len(cleaned_number) >= 10:  # Ensure it's a valid phone number length
                        phone_numbers.add(number.strip())

        # Additional check in all text for phone patterns
        all_text = soup.get_text()
        additional_numbers = phone_pattern.findall(all_text)
        for number in additional_numbers:
            cleaned_number = re.sub(r'\D', '', number)
            if len(cleaned_number) >= 10:  # Ensure it's a valid phone number length
                phone_numbers.add(number.strip())

        # Addresses (simplified, based on common address keywords)
        addresses = []
        address_keywords = ["P. O. Box", "P.O. Box", "Street", "St.", "Avenue", "Ave.", "Road", "Rd.", "Boulevard", "Blvd.", "Drive", "Floor", "Lane", "Ln.", "Way", "Plaza"]
        for keyword in address_keywords:
            found_addresses = soup.find_all(text=re.compile(rf'\b{keyword}\b'))
            addresses += [addr.strip() for addr in found_addresses]

        return {
            "title": page_title,
            "description": meta_description,
            "emails": emails,
            "phones": list(phone_numbers),
            "addresses": addresses
        }

    except requests.RequestException as e:
        return {"error": f"Network error: {e}"}
    except Exception as e:
        return {"error": f"Error scraping {url}: {e}"}
