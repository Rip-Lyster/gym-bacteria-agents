from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv('.env.development.local')

database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

engine = create_engine(database_url)

with engine.connect() as conn:
    # Check current schema
    result = conn.execute(text("SELECT current_schema();"))
    current_schema = result.scalar()
    print(f"Current schema: {current_schema}")
    
    # List all schemas
    result = conn.execute(text("SELECT schema_name FROM information_schema.schemata;"))
    print("\nAvailable schemas:")
    for row in result:
        print(row[0])
        
    # List all tables in current schema
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = current_schema();
    """))
    print("\nTables in current schema:")
    for row in result:
        print(row[0]) 