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
        # Call the scraper function
        scraped_data = scrape_data(url)

        # Store the data in the database
        new_entry = ScrapingHistory(
            url=url,
            data=scraped_data.get('raw_html', ''),
            title=scraped_data.get('title', 'No title'),
            description=scraped_data.get('description', 'No description'),
            emails="; ".join(scraped_data.get('emails', [])),
            phones="; ".join(scraped_data.get('phones', [])),
            addresses="; ".join(scraped_data.get('addresses', []))
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Scraping successful!", "data": scraped_data}), 200
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

