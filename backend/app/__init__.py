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
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecretkey')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Tell Flask-Login what view to redirect unauthorized users to
    login_manager.login_view = 'main.login'

    # Import and register the Blueprint only after the app is created
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import models here to avoid circular import
    with app.app_context():
        from .models import User

    # Set up the user_loader callback to reload user object from user ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
