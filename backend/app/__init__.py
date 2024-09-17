import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='../../frontend', template_folder='../../frontend')
    
    # Load config from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize the login manager
    login_manager.init_app(app)
    
    # Set the login view (redirect users to this endpoint if login is required)
    login_manager.login_view = 'auth.login'  # Make sure 'auth.login' matches the route in your application

    # Import and register the Blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Define the user_loader callback
from .models import User  # Import User model (adjust path if necessary)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Adjust this based on your user model
