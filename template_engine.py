"""
Template Engine for Newsletter Application
Handles personalization and variable replacement
"""
import re
from datetime import datetime

class TemplateEngine:
    """Enhanced template engine with variables and personalization"""
    
    @staticmethod
    def render_template(content, subscriber, campaign=None, custom_vars=None):
        """
        Render template with dynamic variables
        Supports: {{name}}, {{email}}, {{first_name}}, {{date}}, {{unsubscribe_link}}, etc.
        
        Args:
            content: Template content with {{variable}} placeholders
            subscriber: Subscriber object
            campaign: Campaign object (optional)
            custom_vars: Dictionary of custom variables (optional)
            
        Returns:
            Rendered content with variables replaced
        """
        # Build variables dictionary
        variables = {
            'name': subscriber.name or 'Subscriber',
            'email': subscriber.email,
            'first_name': TemplateEngine._get_first_name(subscriber.name),
            'date': datetime.now().strftime('%B %d, %Y'),
            'year': datetime.now().strftime('%Y'),
            'unsubscribe_link': f'/unsubscribe/{subscriber.id}',
        }
        
        # Add campaign-specific variables
        if campaign:
            variables['campaign_name'] = campaign.name
        
        # Add custom variables
        if custom_vars:
            variables.update(custom_vars)
        
        # Replace variables in template
        rendered_content = content
        for key, value in variables.items():
            # Case-insensitive replacement
            pattern = re.compile(r'\{\{' + re.escape(key) + r'\}\}', re.IGNORECASE)
            rendered_content = pattern.sub(str(value), rendered_content)
        
        return rendered_content
    
    @staticmethod
    def render_subject(subject, subscriber, campaign=None, custom_vars=None):
        """
        Render email subject with variables
        
        Args:
            subject: Subject line with {{variable}} placeholders
            subscriber: Subscriber object
            campaign: Campaign object (optional)
            custom_vars: Dictionary of custom variables (optional)
            
        Returns:
            Rendered subject with variables replaced
        """
        return TemplateEngine.render_template(subject, subscriber, campaign, custom_vars)
    
    @staticmethod
    def _get_first_name(full_name):
        """Extract first name from full name"""
        if not full_name:
            return 'there'
        
        # Handle Arabic names (preserve as-is)
        if TemplateEngine._contains_arabic(full_name):
            return full_name
        
        # For English names, get first part
        name_parts = full_name.strip().split()
        return name_parts[0] if name_parts else 'there'
    
    @staticmethod
    def _contains_arabic(text):
        """Check if text contains Arabic characters"""
        if not text:
            return False
        for char in text:
            if '\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' or '\u08A0' <= char <= '\u08FF':
                return True
        return False
    
    @staticmethod
    def get_available_variables():
        """
        Get list of available template variables
        
        Returns:
            Dictionary of variable names and descriptions
        """
        return {
            'name': 'Full name of the subscriber',
            'first_name': 'First name of the subscriber',
            'email': 'Email address of the subscriber',
            'date': 'Current date (e.g., October 18, 2025)',
            'year': 'Current year',
            'campaign_name': 'Name of the campaign',
            'unsubscribe_link': 'Link to unsubscribe page',
        }
