import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.core.models import db
from api.app import create_app

def reset_database():
    """Drop and recreate all database tables."""
    print("Loading environment...")
    load_dotenv('.env.development.local')
    
    print("Creating Flask app...")
    app = create_app()
    
    print("Resetting database...")
    with app.app_context():
        db.drop_all()
        db.create_all()
    
    print("Database reset complete!")

if __name__ == "__main__":
    reset_database() 