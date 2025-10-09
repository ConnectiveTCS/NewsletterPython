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
        self.connection = None
        
    def _get_connection(self):
        """Get SMTP connection with retry logic"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if self.connection is None or not self._test_connection():
                    if self.connection:
                        try:
                            self.connection.quit()
                        except:
                            pass
                    
                    self.connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
                    if self.use_tls:
                        self.connection.starttls()
                    self.connection.login(self.email_address, self.email_password)
                
                return self.connection
                
            except Exception as e:
                retry_count += 1
                logger.error(f"SMTP connection attempt {retry_count} failed: {str(e)}")
                
                if self.connection:
                    try:
                        self.connection.quit()
                    except:
                        pass
                    self.connection = None
                
                if retry_count < max_retries:
                    time.sleep(2 ** retry_count)  # Exponential backoff
                else:
                    raise e
        
        return None
    
    def _test_connection(self):
        """Test if connection is still alive"""
        try:
            status = self.connection.noop()[0]
            return status == 250
        except:
            return False
    
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
            
            # Get connection and send
            connection = self._get_connection()
            if connection:
                connection.send_message(msg)
                logger.debug(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to get SMTP connection for {to_email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            
            # Reset connection on error
            if self.connection:
                try:
                    self.connection.quit()
                except:
                    pass
                self.connection = None
            
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
            # Close connection
            if self.connection:
                try:
                    self.connection.quit()
                except:
                    pass
                self.connection = None
        
        return {
            'sent': sent_count,
            'failed': failed_count,
            'errors': errors
        }
    
    def test_connection(self) -> bool:
        """Test SMTP connection settings"""
        try:
            connection = self._get_connection()
            if connection:
                connection.quit()
                self.connection = None
                return True
            return False
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False