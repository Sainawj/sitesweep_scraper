from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from .scraper import scrape_data
from flask_login import login_required, current_user, login_user, logout_user
from .models import ScrapingHistory, User
from . import db
from .forms import LoginForm
from werkzeug.security import check_password_hash

# Define a Blueprint for routes
main = Blueprint('main', __name__)

# Serve the homepage
@main.route('/')
def index():
    return render_template('index.html')  # Renders the index.html from frontend

# Serve the history page (Requires login)
@main.route('/history')
@login_required
def history():
    return render_template('history.html')  # Renders history.html from frontend

# API endpoint to trigger the scraping process (Requires login)
@main.route('/api/scrape', methods=['POST'])
@login_required
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
            "data": {
                "title": title,
                "description": description,
                "emails": scraped_data.get('emails', []),
                "phones": scraped_data.get('phones', []),
                "addresses": scraped_data.get('addresses', [])
            }
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred"}), 500

# API endpoint to fetch scraping history (Requires login)
@main.route('/api/history', methods=['GET'])
@login_required
def get_history():
    try:
        # Fetch scraping history from the database
        history_records = ScrapingHistory.query.order_by(ScrapingHistory.date.desc()).all()
        history_list = [{
            "id": record.id,
            "url": record.url,
            "date": record.date,
            "status": record.status
        } for record in history_records]

        return jsonify(history_list)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred"}), 500

# API endpoint to fetch scraped data by ID (Requires login)
@main.route('/api/scraped_data/<int:id>', methods=['GET'])
@login_required
def get_scraped_data(id):
    try:
        # Fetch the scraped data by ID from the database
        record = ScrapingHistory.query.get(id)
        if not record:
            return jsonify({"message": "Record not found"}), 404

        return jsonify({
            "title": record.title,
            "description": record.description,
            "emails": record.emails.split(', ') if record.emails else [],
            "phones": record.phones.split(', ') if record.phones else [],
            "addresses": record.addresses.split(', ') if record.addresses else []
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred"}), 500

# Route for login
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Fetch user by email
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

# Route for logout (Requires login)
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

