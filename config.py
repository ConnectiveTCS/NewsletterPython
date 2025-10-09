"""
Configuration management for Newsletter Application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///newsletter.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', '')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
    USE_TLS = os.environ.get('USE_TLS', 'True').lower() == 'true'
    
    # Application settings
    MAX_BATCH_SIZE = int(os.environ.get('MAX_BATCH_SIZE', '50'))
    EMAIL_DELAY_SECONDS = float(os.environ.get('EMAIL_DELAY_SECONDS', '0.1'))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}