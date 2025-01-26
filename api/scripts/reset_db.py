import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.core.models import db
from api.app import create_app

def reset_database():
    """Drop all database tables including alembic_version."""
    print("Loading environment...")
    load_dotenv('api/.env.development.local')
    
    print("Creating Flask app...")
    app = create_app()
    
    print("Dropping all tables...")
    with app.app_context():
        # Drop all tables using raw SQL to ensure alembic_version is also dropped
        db.session.execute(text('DROP SCHEMA public CASCADE'))
        db.session.execute(text('CREATE SCHEMA public'))
        db.session.commit()
    
    print("Database reset complete!")

if __name__ == "__main__":
    reset_database() 