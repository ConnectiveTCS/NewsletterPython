#!/usr/bin/env python3
"""
Simple SMTP test script to verify email configuration
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config

def test_smtp_connection():
    """Test SMTP connection with current configuration"""
    config = Config()
    
    print(f"Testing SMTP connection to {config.SMTP_SERVER}:{config.SMTP_PORT}")
    print(f"Username: {config.EMAIL_ADDRESS}")
    print(f"Use TLS: {config.USE_TLS}")
    
    try:
        # Create connection
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.set_debuglevel(1)  # Enable debug output
        
        print("Connected to SMTP server")
        
        if config.USE_TLS:
            print("Starting TLS...")
            server.starttls()
        
        print("Logging in...")
        server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
        
        print("Login successful!")
        
        # Test sending a simple email
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL_ADDRESS
        msg['To'] = config.EMAIL_ADDRESS  # Send to self for testing
        msg['Subject'] = "SMTP Test Email"
        
        body = "This is a test email from the newsletter application."
        msg.attach(MIMEText(body, 'plain'))
        
        print("Sending test email...")
        server.send_message(msg)
        print("Test email sent successfully!")
        
        server.quit()
        return True
        
    except Exception as e:
        print(f"SMTP test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_smtp_connection()
    if success:
        print("\n✅ SMTP configuration is working correctly!")
    else:
        print("\n❌ SMTP configuration has issues. Please check your settings.")