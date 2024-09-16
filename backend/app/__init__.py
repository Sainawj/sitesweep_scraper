from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configurations, e.g., database settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<user>:<password>@<host>/<database>'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints or routes
    from . import routes
    app.register_blueprint(routes.app)  # if using blueprints

    return app


