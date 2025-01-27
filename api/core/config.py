from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from typing import Dict, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the absolute path to the .env file
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env.development.local'
logger.debug(f"Looking for .env file at: {env_path}")
load_dotenv(env_path)

db = SQLAlchemy()

class Config:
    """Base configuration."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    logger.debug(f"Environment DATABASE_URL: {os.getenv('DATABASE_URL')}")
    
    if not SQLALCHEMY_DATABASE_URI:
        logger.warning("No DATABASE_URL found in environment, falling back to SQLite")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    elif SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    logger.debug(f"Final Database URL: {SQLALCHEMY_DATABASE_URI}")
    
    # Security
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DEVELOPMENT = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # In production, these must be set via environment variables
    def __init__(self):
        if not os.getenv('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable is required in production")
        if not os.getenv('DATABASE_URL'):
            raise ValueError("DATABASE_URL environment variable is required in production")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False

config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration class based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    return config[env] 