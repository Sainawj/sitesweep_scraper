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

    # Set the secret key for session management
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '4871b4b9cd4a257721a09f44ecca7866c60479a5bd184ef699249b2e56de32b3')

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize the login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Adjust to your actual login route

    # Import and register the Blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
