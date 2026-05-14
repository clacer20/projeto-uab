import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key')

# Configure the database to use the Flask instance folder
db_path = os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models to ensure they are registered with SQLAlchemy metadata
from app import models, routes

# Ensure the instance folder and tables exist
with app.app_context():
    # Use an absolute path for the instance folder to avoid ambiguity
    instance_path = app.instance_path
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)
    
    # Force registration check and creation
    db.create_all()
