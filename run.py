#!/usr/bin/env python3
"""
Newsletter Application Startup Script
"""
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, migrate, upgrade
from config import config

def create_app(config_name=None):
    """Create Flask application"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    from models import db
    db.init_app(app)
    
    migrate = Migrate(app, db)
    
    return app

def setup_database():
    """Initialize database and create tables"""
    app = create_app()
    with app.app_context():
        from models import db, Subscriber, Template, Campaign, EmailLog
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Create sample data for development
        if app.config['FLASK_ENV'] == 'development':
            create_sample_data(db)

def create_sample_data(db):
    """Create sample data for development"""
    from models import Subscriber, Template
    
    # Check if data already exists
    if Subscriber.query.first() or Template.query.first():
        print("Sample data already exists, skipping...")
        return
    
    # Create sample subscribers
    sample_subscribers = [
        {'email': 'john@example.com', 'name': 'John Doe'},
        {'email': 'jane@example.com', 'name': 'Jane Smith'},
        {'email': 'bob@example.com', 'name': 'Bob Johnson'},
        {'email': 'alice@example.com', 'name': 'Alice Brown'},
        {'email': 'charlie@example.com', 'name': 'Charlie Wilson'},
    ]
    
    for sub_data in sample_subscribers:
        subscriber = Subscriber(**sub_data)
        db.session.add(subscriber)
    
    # Create sample template
    sample_template = Template(
        name='Welcome Email',
        subject='Welcome to Our Newsletter, {{name}}!',
        content='''<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f8f9fa; }
        .footer { padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Our Newsletter!</h1>
        </div>
        <div class="content">
            <h2>Hello {{name}}!</h2>
            <p>Thank you for subscribing to our newsletter. We're excited to have you on board!</p>
            <p>You'll receive regular updates about:</p>
            <ul>
                <li>Latest news and updates</li>
                <li>Special offers and promotions</li>
                <li>Industry insights and tips</li>
            </ul>
            <p>Stay tuned for great content!</p>
        </div>
        <div class="footer">
            <p>You received this email because you subscribed to our newsletter.</p>
            <p>If you no longer wish to receive these emails, please unsubscribe.</p>
        </div>
    </div>
</body>
</html>'''
    )
    
    db.session.add(sample_template)
    
    try:
        db.session.commit()
        print("Sample data created successfully!")
        print("Sample subscribers: 5 subscribers added")
        print("Sample template: 'Welcome Email' template created")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")

def main():
    """Main startup function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init-db':
            setup_database()
            return
        elif command == 'run':
            # Run the application
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
            return
    
    # Default: setup database and run
    print("Setting up Newsletter Application...")
    setup_database()
    
    print("\nStarting Newsletter Application...")
    print("Web interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()