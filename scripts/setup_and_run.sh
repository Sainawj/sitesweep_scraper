#!/bin/bash

# Exit script on any error
set -e

# MySQL database credentials
DB_NAME="weescraper_db"
DB_USER="sitesweepuser"
DB_PASSWORD="sweeproot"

# Function to install and set up MySQL database
setup_mysql_db() {
    echo "Setting up MySQL database..."

    # Check if MySQL is installed
    if ! command -v mysql &> /dev/null; then
        echo "MySQL is not installed. Please install MySQL and re-run the script."
        exit 1
    fi

    # Log in to MySQL as root and create the database, user, and grant privileges
    echo "Creating database and user..."
    mysql -u root -p <<MYSQL_SCRIPT
    CREATE DATABASE IF NOT EXISTS $DB_NAME;
    CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
    GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
    FLUSH PRIVILEGES;
MYSQL_SCRIPT

    echo "Database and user setup completed successfully."
}

# Function to set up backend (Flask) environment
setup_backend() {
    echo "Setting up backend (Flask)..."

    # Navigate to the backend directory
    cd backend

    # Set up a virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate the virtual environment
    source venv/bin/activate

    # Install backend dependencies
    echo "Installing backend dependencies..."
    pip install -r requirements.txt

    # Set up environment variables in .env file
    echo "Configuring environment variables..."
    if [ ! -f ".env" ]; then
        cat <<EOL > .env
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=3306
EOL
    fi

    echo "Backend setup completed."

    # Return to the root directory
    cd ..
}

# Function to install frontend dependencies
setup_frontend() {
    echo "Setting up frontend (static HTML/JS)..."

    # Navigate to frontend directory
    cd frontend

    # Install frontend dependencies if package.json exists (in case frontend is using npm)
    if [ -f "package.json" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi

    echo "Frontend setup completed."

    # Return to the root directory
    cd ..
}

# Function to start Flask app
start_flask() {
    echo "Starting Flask server..."

    # Navigate to backend directory
    cd backend

    # Activate virtual environment
    source venv/bin/activate

    # Start Flask app with host 0.0.0.0
    flask run --host=0.0.0.0

    # Return to root directory
    cd ..
}

# Main script execution
echo "Starting full environment setup..."

# Check for Python3, MySQL, and npm
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm to continue."
    exit 1
fi

# Set up MySQL database
setup_mysql_db

# Set up backend (Flask) environment
setup_backend

# Set up frontend (Static/JS)
setup_frontend

# Start Flask server
start_flask

echo "Setup and Flask startup completed successfully!"
