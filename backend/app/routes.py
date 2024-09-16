from flask import render_template, jsonify, request
from . import app, db
from .scraper import scrape_data
from .models import ScrapingHistory

# Serve the homepage
@app.route('/')
def home():
    # Using send_static_file to serve static HTML from the frontend directory
    return app.send_static_file('index.html')

# Serve the history page
@app.route('/history')
def history():
    # Using send_static_file to serve static HTML from the frontend directory
    return app.send_static_file('history.html')

# API endpoint to trigger the scraping process
@app.route('/api/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return jsonify({"message": "URL is required"}), 400
    try:
        # Call the scraper function to get the metadata and contact info
        scraped_data = scrape_data(url)

        # Extract metadata from the scraped data
        title = scraped_data.get('title', '')
        description = scraped_data.get('description', '')
        emails = ', '.join(scraped_data.get('emails', []))
        phones = ', '.join(scraped_data.get('phones', []))
        addresses = ', '.join(scraped_data.get('addresses', []))

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
        app.logger.error(f"Scraping error: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

# API endpoint to retrieve the scraping history
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        # Query all records from the ScrapingHistory model
        history_records = ScrapingHistory.query.all()
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
        # Log the error for debugging
        app.logger.error(f"History fetching error: {str(e)}")
        return jsonify({"message": f"Error fetching history: {str(e)}"}), 500

