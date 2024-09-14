#!/bin/bash

# Exit script on any error
set -e

# Function to run frontend tests
run_frontend_tests() {
  echo "Running Frontend Tests..."

  # Navigate to frontend directory
  cd frontend

  # Install frontend dependencies
  if [ -f "package.json" ]; then
    echo "Installing frontend dependencies..."
    npm install
  else
    echo "No package.json found in frontend directory, skipping frontend dependency installation."
  fi

  # Run frontend tests
  echo "Running frontend tests..."
  npx jest

  # Return to root directory
  cd ..
}

# Function to run backend tests
run_backend_tests() {
  echo "Running Backend Tests..."

  # Navigate to backend directory
  cd backend

  # Set up virtual environment if not already done
  if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
  fi

  # Activate virtual environment
  source venv/bin/activate

  # Install backend dependencies
  if [ -f "requirements.txt" ]; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
  else
    echo "No requirements.txt found in backend directory, skipping backend dependency installation."
  fi

  # Run backend tests
  echo "Running backend tests..."
  pytest

  # Deactivate virtual environment
  deactivate

  # Return to root directory
  cd ..
}

# Main script execution
echo "Starting full project setup and test execution..."

# Check if Python3 and npm are installed
if ! command -v python3 &> /dev/null; then
  echo "Python3 is not installed. Please install Python3 to continue."
  exit 1
fi

if ! command -v npm &> /dev/null; then
  echo "npm is not installed. Please install npm to continue."
  exit 1
fi

# Run frontend tests
run_frontend_tests

# Run backend tests
run_backend_tests

echo "All tests completed successfully!"
