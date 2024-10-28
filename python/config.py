# python/config.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Get the absolute path of the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
           template_folder=os.path.join(BASE_DIR, 'templates'),  # Set template folder path
           static_folder=os.path.join(BASE_DIR, 'static'))      # Set static folder path

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/StatutoryDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)