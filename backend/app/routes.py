from flask import Blueprint, jsonify, request, render_template
from .scraper import scrape_data
from .models import ScrapingHistory
from . import db

# Define a Blueprint for routes
main = Blueprint('main', __name__)

# Serve the homepage
@main.route('/')
def index():
    return render_template('index.html')  # Renders the index.html from frontend

# Serve the history page
@main.route('/history')
def history():
    return render_template('history.html')  # Renders history.html from frontend

# API endpoint to trigger the scraping process
@main.route('/api/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return jsonify({"message": "URL is required"}), 400
    try:
        # Call the scraper function to get the metadata and contact info
        scraped_data = scrape_data(url)

        if "error" in scraped_data:
            return jsonify({"message": "Scraping failed"}), 500

        # Extract metadata from the scraped data
        title = scraped_data.get('title', 'No title found')
        description = scraped_data.get('description', 'No description found')
        emails = ', '.join(scraped_data.get('emails', [])) or "No emails found"
        phones = ', '.join(scraped_data.get('phones', [])) or "No phone numbers found"
        addresses = ', '.join(scraped_data.get('addresses', [])) or "No addresses found"

        # Create a new entry in the database with metadata and contact info
        new_entry = ScrapingHistory(
            url=url, 
            title=title,
            description=description,
            emails=emails,
            phones=phones,
            addresses=addresses,
            data=str(scraped_data),  # Save the full scraped data (if needed) as a string
            status="Completed"
        )
        db.session.add(new_entry)
        db.session.commit()

        # Return the scraped data to the front-end
        return jsonify({
            "message": "Scraping successful!", 
            "data": scraped_data
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# API endpoint to retrieve the scraping history
@main.route('/api/history', methods=['GET'])
def get_history():
    try:
        # Query the latest 10 records from the ScrapingHistory model
        history_records = ScrapingHistory.query.order_by(ScrapingHistory.date.desc()).limit(10).all()
        history_list = [
            {
                "id": record.id,
                "url": record.url,
                "date": record.date,
                "status": record.status
            }
            for record in history_records
        ]
        return jsonify(history_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching history: {str(e)}"}), 500
