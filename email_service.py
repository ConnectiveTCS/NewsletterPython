"""
Email Service for Newsletter Application
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails"""
    
    def __init__(self, config):
        self.smtp_server = config.get('SMTP_SERVER')
        self.smtp_port = config.get('SMTP_PORT')
        self.email_address = config.get('EMAIL_ADDRESS')
        self.email_password = config.get('EMAIL_PASSWORD')
        self.use_tls = config.get('USE_TLS', True)  # Default to True for backward compatibility
        
    def _get_fresh_connection(self):
        """Get a fresh SMTP connection for each email"""
        try:
            connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
            connection.set_debuglevel(0)  # Disable debug output
            
            if self.use_tls:
                connection.starttls()
            
            connection.login(self.email_address, self.email_password)
            return connection
            
        except Exception as e:
            logger.error(f"SMTP connection failed: {str(e)}")
            raise e
    

    
    def send_email(self, to_email: str, subject: str, content: str, recipient_name: str = None) -> bool:
        """
        Send individual email
        
        Args:
            to_email: recipient email address
            subject: email subject
            content: email content (HTML supported)
            recipient_name: recipient name for personalization
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Personalize content
            personalized_content = content
            if recipient_name:
                personalized_content = content.replace('{{name}}', recipient_name)
                personalized_subject = subject.replace('{{name}}', recipient_name)
            else:
                personalized_subject = subject
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = personalized_subject
            msg['From'] = self.email_address
            msg['To'] = to_email
            
            # Add HTML content
            html_part = MIMEText(personalized_content, 'html')
            msg.attach(html_part)
            
            # Get fresh connection and send
            connection = None
            try:
                connection = self._get_fresh_connection()
                connection.send_message(msg)
                logger.debug(f"Email sent successfully to {to_email}")
                return True
                
            except Exception as e:
                logger.error(f"Error sending email to {to_email}: {str(e)}")
                return False
                
            finally:
                # Always close the connection
                if connection:
                    try:
                        connection.quit()
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"Error preparing email for {to_email}: {str(e)}")
            return False
    
    def send_bulk_emails(self, recipients: list, subject: str, content: str, batch_size: int = 50) -> dict:
        """
        Send bulk emails with batching
        
        Args:
            recipients: list of (email, name) tuples
            subject: email subject
            content: email content
            batch_size: number of emails per batch
            
        Returns:
            dict: {'sent': count, 'failed': count, 'errors': [error_messages]}
        """
        sent_count = 0
        failed_count = 0
        errors = []
        
        try:
            # Process in batches
            for i in range(0, len(recipients), batch_size):
                batch = recipients[i:i + batch_size]
                logger.info(f"Processing batch {i//batch_size + 1}, emails {i+1} to {min(i+batch_size, len(recipients))}")
                
                for email, name in batch:
                    try:
                        if self.send_email(email, subject, content, name):
                            sent_count += 1
                        else:
                            failed_count += 1
                            errors.append(f"Failed to send to {email}")
                            
                        # Small delay to avoid overwhelming SMTP server
                        time.sleep(0.1)
                        
                    except Exception as e:
                        failed_count += 1
                        error_msg = f"Error sending to {email}: {str(e)}"
                        errors.append(error_msg)
                        logger.error(error_msg)
                
                # Pause between batches
                if i + batch_size < len(recipients):
                    time.sleep(1)
                    
        except Exception as e:
            error_msg = f"Bulk email sending failed: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)
        
        finally:
            # No persistent connection to close in this implementation
            pass
        
        return {
            'sent': sent_count,
            'failed': failed_count,
            'errors': errors
        }
    
    def test_connection(self) -> bool:
        """Test SMTP connection settings"""
        try:
            connection = self._get_fresh_connection()
            if connection:
                connection.quit()
                return True
            return False
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False