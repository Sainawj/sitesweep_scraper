from flask import Flask, render_template, jsonify, request
from .scraper import scrape_data  # Assuming you have a scraping function
from .models import ScrapingHistory  # Your database models

app = Flask(__name__)

# Route to serve the home page
@app.route('/')
def home():
    return app.send_static_file('index.html')

# Route to serve the scraping history page
@app.route('/history')
def history():
    return app.send_static_file('history.html')

# API route for handling data scraping requests
@app.route('/api/scrape', methods=['POST'])
def scrape():
    # Get form data from the request
    url = request.form.get('url')
    
    if not url:
        return jsonify({"message": "URL is required"}), 400

    try:
        # Call your scraper function to fetch data from the given URL
        scraped_data = scrape_data(url)
        
        # Store scraped data in the database (e.g., in a `ScrapingHistory` table)
        new_entry = ScrapingHistory(url=url, data=scraped_data)
        new_entry.save()

        return jsonify({"message": "Scraping successful!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# API route to fetch scraping history from the database
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        # Fetch all scraping history records from the database
        history_records = ScrapingHistory.query.all()
        history_list = [{"id": record.id, "url": record.url, "date": record.date, "status": record.status} for record in history_records]

        return jsonify(history_list), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching history: {str(e)}"}), 500
