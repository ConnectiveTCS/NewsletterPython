"""
Newsletter Application Executable Launcher
This file ensures proper initialization when running as executable
"""
import os
import sys
import tempfile
import shutil

def setup_executable_environment():
    """Setup environment for executable"""
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
        # Create a directory for the database if needed
        app_data_dir = os.path.join(os.path.expanduser("~"), "NewsletterApp")
        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)
        
        # Set environment variables for the executable
        os.environ['FLASK_ENV'] = 'production'
        if not os.environ.get('DATABASE_URL'):
            db_path = os.path.join(app_data_dir, "newsletter.db")
            os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return base_dir

if __name__ == '__main__':
    # Setup environment
    setup_executable_environment()
    
    print("Setting up Newsletter Application...")
    
    # Import the Flask app from app.py
    from app import app
    from models import db, Subscriber, Template, Campaign, EmailLog
    
    # Initialize database using the existing app context
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create sample data for first-time users (only if running as executable)
        if getattr(sys, 'frozen', False):
            # Check if data already exists
            if not Subscriber.query.first() and not Template.query.first():
                try:
                    # Create sample subscribers
                    sample_subscribers = [
                        Subscriber(name="Ahmed Hassan", email="ahmed@example.com", is_active=True),
                        Subscriber(name="Sara Mohamed", email="sara@example.com", is_active=True),
                        Subscriber(name="John Smith", email="john@example.com", is_active=True),
                    ]
                    
                    for subscriber in sample_subscribers:
                        db.session.add(subscriber)
                    
                    # Create sample template
                    sample_template = Template(
                        name="Welcome Template",
                        subject="Welcome to our Newsletter!",
                        content="""
                        <html>
                        <body>
                            <h2>Welcome {{name}}!</h2>
                            <p>Thank you for subscribing to our newsletter.</p>
                            <p>Best regards,<br>The Newsletter Team</p>
                        </body>
                        </html>
                        """
                    )
                    db.session.add(sample_template)
                    
                    db.session.commit()
                    print("Sample data created successfully!")
                except Exception as e:
                    print(f"Note: Could not create sample data: {e}")
                    db.session.rollback()
    
    print("\nStarting Newsletter Application...")
    print("Web interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)