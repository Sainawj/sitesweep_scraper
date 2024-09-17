from backend.app import create_app

# Create the Flask app instance using the factory function
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode, so any changes to the code automatically reload
    app.run(debug=True)
