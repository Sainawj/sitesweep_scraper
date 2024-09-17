import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='../../frontend', template_folder='../../frontend')
    
    # Load config from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecretkey')

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register the Blueprint only after the app is created
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import models here to avoid circular import
    with app.app_context():
        from .models import User

    return app
