# Newsletter Application

A comprehensive web-based newsletter application built with Python Flask that can send emails to thousands of subscribers simultaneously with template management and email audit capabilities.

## Features

### ✅ Core Features
- **Web-based Dashboard** - Clean, responsive web interface
- **Subscriber Management** - Add, import, and manage email subscribers
- **Template System** - Create and manage HTML email templates with personalization
- **Bulk Email Sending** - Send to thousands of emails efficiently with threading
- **Campaign Management** - Create and track email campaigns
- **Email Audit System** - Complete logging and tracking of all sent emails
- **CSV Import** - Import subscribers from CSV files

### ✅ Technical Features
- **SQLite Database** - Lightweight, file-based database
- **Responsive UI** - Bootstrap-based responsive design
- **Error Handling** - Comprehensive error handling and logging
- **Multi-threading** - Efficient bulk email sending with thread pools
- **SMTP Support** - Works with Gmail, Outlook, and other SMTP servers
- **Email Personalization** - Dynamic content with {{name}} placeholders

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings
Copy the example environment file and configure your email settings:
```bash
copy .env.example .env
```

Edit `.env` file with your email configuration:
```
# Email Configuration (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

**For Gmail**: You'll need to use an "App Password" instead of your regular password:
1. Enable 2-factor authentication on your Google account
2. Go to Google Account settings → Security → App passwords
3. Generate an app password for "Mail"
4. Use this app password in the EMAIL_PASSWORD field

### 3. Run the Application
```bash
python run.py
```

The application will:
- Set up the database automatically
- Create sample data for testing
- Start the web server at http://localhost:5000

## Usage Guide

### Dashboard
- Access the main dashboard at http://localhost:5000
- View statistics: total subscribers, templates, campaigns
- Quick access to all main features

### Managing Subscribers
1. **Add Individual Subscribers**: Use the "Add Subscriber" form
2. **Import from CSV**: Upload CSV files with email,name format
3. **View All Subscribers**: Paginated list with search capabilities

### Creating Email Templates
1. Go to Templates → Create Template
2. Design your email with HTML support
3. Use `{{name}}` for personalization in subject and content
4. Preview templates before saving

### Running Email Campaigns
1. Create Campaign → Select template
2. Preview the campaign
3. Click "Send Campaign" to send to all active subscribers
4. Monitor sending progress in real-time
5. View detailed logs and statistics

## Email Configuration Examples

### Gmail Configuration
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Outlook/Hotmail Configuration
```
SMTP_SERVER=smtp.live.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@outlook.com
EMAIL_PASSWORD=your-password
```

### Custom SMTP Server
```
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@yourdomain.com
EMAIL_PASSWORD=your-password
```

## File Structure

```
NewsletterPython/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── email_service.py       # Email sending service
├── config.py              # Configuration management
├── run.py                 # Application startup script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration example
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Dashboard
│   ├── subscribers.html  # Subscriber management
│   ├── templates.html    # Template management
│   ├── campaigns.html    # Campaign management
│   └── ...               # Other templates
└── newsletter.db         # SQLite database (created automatically)
```

## Database Schema

### Subscribers
- Email address (unique)
- Name (optional)
- Active status
- Creation/update timestamps

### Templates
- Template name
- Email subject (supports {{name}} personalization)
- HTML content (supports {{name}} personalization)
- Creation/update timestamps

### Campaigns
- Campaign name
- Associated template
- Status (draft/sending/sent/failed)
- Send statistics
- Creation and sent timestamps

### Email Logs (Audit Trail)
- Campaign reference
- Recipient email
- Send status (sent/failed/bounced)
- Error messages
- Timestamp

## Performance & Scalability

### Email Sending Performance
- **Threading**: Uses ThreadPoolExecutor with 10 concurrent workers
- **Batching**: Processes emails in configurable batches (default: 50)
- **Rate Limiting**: Configurable delay between emails (default: 0.1s)
- **Connection Reuse**: Maintains SMTP connections for efficiency
- **Error Recovery**: Automatic retry logic with exponential backoff

### Recommended Settings for High Volume
```
MAX_BATCH_SIZE=100
EMAIL_DELAY_SECONDS=0.05
```

### Estimated Performance
- **Small lists** (< 1,000): 2-5 minutes
- **Medium lists** (1,000-10,000): 10-30 minutes  
- **Large lists** (10,000+): 1-3 hours

## Troubleshooting

### Common Email Issues

**Authentication Failed**
- Verify email credentials
- For Gmail: Use App Password, not regular password
- Check SMTP server and port settings

**Emails Going to Spam**
- Add proper sender information
- Include unsubscribe links
- Use reputable email provider
- Warm up new email addresses gradually

**Slow Sending**
- Increase MAX_BATCH_SIZE
- Decrease EMAIL_DELAY_SECONDS
- Check SMTP server rate limits

### Application Issues

**Database Errors**
- Ensure write permissions in application directory
- Check disk space
- Restart application to recreate database

**Port Already in Use**
- Change port in run.py: `app.run(port=5001)`
- Or kill existing process using port 5000

## Security Considerations

### Production Deployment
1. **Change Secret Key**: Set a strong SECRET_KEY in production
2. **Environment Variables**: Use environment variables for sensitive data
3. **HTTPS**: Deploy with SSL/TLS encryption
4. **Authentication**: Add user authentication for production use
5. **Rate Limiting**: Implement rate limiting for API endpoints

### Email Security
1. **App Passwords**: Use app-specific passwords for Gmail
2. **Encryption**: Use TLS/SSL for SMTP connections
3. **List Hygiene**: Regularly clean subscriber lists
4. **Compliance**: Follow CAN-SPAM and GDPR regulations

## Development

### Adding New Features
1. **Models**: Add database models in `models.py`
2. **Routes**: Add Flask routes in `app.py`
3. **Templates**: Create HTML templates in `templates/`
4. **Migrations**: Use Flask-Migrate for database changes

### Testing
- Test with small subscriber lists first
- Use test email addresses
- Monitor logs for errors
- Verify email delivery and formatting

## License

This project is open-source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Test with minimal configuration
4. Verify email provider settings