import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key')

# Ensure the instance folder exists (absolute path)
instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance')
os.makedirs(instance_path, exist_ok=True)

# Use absolute path for SQLite
if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    db_path = os.path.join(instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes, models

# Create tables within app context
with app.app_context():
    db.create_all()
