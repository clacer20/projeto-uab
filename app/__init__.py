import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key')

# Use a strictly absolute path for the database to avoid reloader issues
# Assuming the app is in /app
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, '..', 'instance')
os.makedirs(instance_path, exist_ok=True)
db_path = os.path.join(instance_path, 'app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"DEBUG: Database URI is {app.config['SQLALCHEMY_DATABASE_URI']}", file=sys.stderr)

db = SQLAlchemy(app)

# Important: Import models BEFORE create_all to register them
from app import models, routes

with app.app_context():
    print("DEBUG: Running db.create_all()...", file=sys.stderr)
    db.create_all()
    # Double check tables in metadata
    print(f"DEBUG: Registered tables: {list(db.metadata.tables.keys())}", file=sys.stderr)
