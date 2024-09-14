from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql

# Point to frontend directory
app = Flask(__name__,
            static_folder="../../frontend",  # Adjust relative path for frontend
            static_url_path="/")             # Root URL for static files

# Load config settings
app.config.from_object('config')

# Initialize SQLAlchemy and CORS
db = SQLAlchemy(app)
CORS(app)

# Install pymysql
pymysql.install_as_MySQLdb()

# Import routes and models
from . import routes, models

