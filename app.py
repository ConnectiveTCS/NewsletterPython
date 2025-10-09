"""
Newsletter Application - Main Flask Application
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
# Email handling is done in email_service.py
import threading
import time
# ThreadPoolExecutor removed - using sequential sending to avoid connection issues
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['SMTP_SERVER'] = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
app.config['SMTP_PORT'] = int(os.environ.get('SMTP_PORT', '587'))
app.config['EMAIL_ADDRESS'] = os.environ.get('EMAIL_ADDRESS', '')
app.config['EMAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD', '')

# Initialize database
from models import db, Subscriber, Template, Campaign, EmailLog
db.init_app(app)
migrate = Migrate(app, db)

from email_service import EmailService

# Initialize email service
email_service = EmailService(app.config)

@app.route('/')
def index():
    """Dashboard with overview statistics"""
    total_subscribers = Subscriber.query.count()
    total_templates = Template.query.count()
    total_campaigns = Campaign.query.count()
    recent_campaigns = Campaign.query.order_by(Campaign.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         total_subscribers=total_subscribers,
                         total_templates=total_templates,
                         total_campaigns=total_campaigns,
                         recent_campaigns=recent_campaigns)

@app.route('/subscribers')
def subscribers():
    """Manage subscribers"""
    page = request.args.get('page', 1, type=int)
    subscribers = Subscriber.query.paginate(page=page, per_page=50, error_out=False)
    return render_template('subscribers.html', subscribers=subscribers)

@app.route('/subscribers/add', methods=['GET', 'POST'])
def add_subscriber():
    """Add new subscriber"""
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        name = request.form['name'].strip()
        
        if not email:
            flash('Email is required', 'error')
            return render_template('add_subscriber.html')
        
        # Check if subscriber already exists
        existing = Subscriber.query.filter_by(email=email).first()
        if existing:
            flash('Subscriber already exists', 'error')
            return render_template('add_subscriber.html')
        
        try:
            subscriber = Subscriber(email=email, name=name)
            db.session.add(subscriber)
            db.session.commit()
            flash('Subscriber added successfully', 'success')
            return redirect(url_for('subscribers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding subscriber: {str(e)}', 'error')
    
    return render_template('add_subscriber.html')

@app.route('/subscribers/import', methods=['GET', 'POST'])
def import_subscribers():
    """Bulk import subscribers from CSV"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                import csv
                import io
                
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.reader(stream)
                
                added_count = 0
                duplicate_count = 0
                
                for row in csv_input:
                    if len(row) >= 1:
                        email = row[0].strip().lower()
                        name = row[1].strip() if len(row) > 1 else ''
                        
                        if email and '@' in email:
                            existing = Subscriber.query.filter_by(email=email).first()
                            if not existing:
                                subscriber = Subscriber(email=email, name=name)
                                db.session.add(subscriber)
                                added_count += 1
                            else:
                                duplicate_count += 1
                
                db.session.commit()
                flash(f'Successfully imported {added_count} subscribers. {duplicate_count} duplicates skipped.', 'success')
                
            except Exception as e:
                db.session.rollback()
                flash(f'Error importing subscribers: {str(e)}', 'error')
        else:
            flash('Please upload a CSV file', 'error')
        
        return redirect(url_for('subscribers'))
    
    return render_template('import_subscribers.html')

@app.route('/subscribers/delete/<int:id>')
def delete_subscriber(id):
    """Delete subscriber"""
    subscriber = Subscriber.query.get_or_404(id)
    try:
        db.session.delete(subscriber)
        db.session.commit()
        flash('Subscriber deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting subscriber: {str(e)}', 'error')
    
    return redirect(url_for('subscribers'))

@app.route('/templates')
def templates():
    """Manage email templates"""
    templates = Template.query.order_by(Template.created_at.desc()).all()
    return render_template('templates.html', templates=templates)

@app.route('/templates/add', methods=['GET', 'POST'])
def add_template():
    """Add new template"""
    if request.method == 'POST':
        name = request.form['name'].strip()
        subject = request.form['subject'].strip()
        content = request.form['content']
        
        if not name or not subject or not content:
            flash('All fields are required', 'error')
            return render_template('add_template.html')
        
        try:
            template = Template(name=name, subject=subject, content=content)
            db.session.add(template)
            db.session.commit()
            flash('Template created successfully', 'success')
            return redirect(url_for('templates'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating template: {str(e)}', 'error')
    
    return render_template('add_template.html')

@app.route('/templates/edit/<int:id>', methods=['GET', 'POST'])
def edit_template(id):
    """Edit template"""
    template = Template.query.get_or_404(id)
    
    if request.method == 'POST':
        template.name = request.form['name'].strip()
        template.subject = request.form['subject'].strip()
        template.content = request.form['content']
        template.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Template updated successfully', 'success')
            return redirect(url_for('templates'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating template: {str(e)}', 'error')
    
    return render_template('edit_template.html', template=template)

@app.route('/templates/delete/<int:id>')
def delete_template(id):
    """Delete template"""
    template = Template.query.get_or_404(id)
    try:
        db.session.delete(template)
        db.session.commit()
        flash('Template deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting template: {str(e)}', 'error')
    
    return redirect(url_for('templates'))

@app.route('/campaigns')
def campaigns():
    """View campaigns"""
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/campaigns/create', methods=['GET', 'POST'])
def create_campaign():
    """Create new campaign"""
    if request.method == 'POST':
        name = request.form['name'].strip()
        template_id = request.form['template_id']
        
        if not name or not template_id:
            flash('Campaign name and template are required', 'error')
            templates = Template.query.all()
            return render_template('create_campaign.html', templates=templates)
        
        try:
            campaign = Campaign(name=name, template_id=template_id)
            db.session.add(campaign)
            db.session.commit()
            
            flash('Campaign created successfully', 'success')
            return redirect(url_for('campaign_detail', id=campaign.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating campaign: {str(e)}', 'error')
    
    templates = Template.query.all()
    return render_template('create_campaign.html', templates=templates)

@app.route('/campaigns/<int:id>')
def campaign_detail(id):
    """Campaign detail and sending interface"""
    campaign = Campaign.query.get_or_404(id)
    return render_template('campaign_detail.html', campaign=campaign)

@app.route('/campaigns/<int:id>/send', methods=['POST'])
def send_campaign(id):
    """Send campaign to all subscribers"""
    campaign = Campaign.query.get_or_404(id)
    
    if campaign.status == 'sent':
        flash('Campaign has already been sent', 'error')
        return redirect(url_for('campaign_detail', id=id))
    
    # Start sending in background
    def send_emails():
        with app.app_context():
            try:
                # Refresh campaign object in the new context
                campaign_obj = Campaign.query.get(id)
                campaign_obj.status = 'sending'
                campaign_obj.sent_at = datetime.utcnow()
                db.session.commit()
                
                subscribers = Subscriber.query.filter_by(is_active=True).all()
                template = campaign_obj.template
                
                total_sent = 0
                total_failed = 0
                
                # Send emails sequentially to avoid threading issues
                for subscriber in subscribers:
                    try:
                        # Create a fresh email service for each email to avoid connection issues
                        from email_service import EmailService
                        fresh_email_service = EmailService(app.config)
                        
                        result = fresh_email_service.send_email(
                            subscriber.email,
                            template.subject,
                            template.content,
                            subscriber.name
                        )
                        
                        if result:
                            total_sent += 1
                            # Log successful send
                            log = EmailLog(
                                campaign_id=campaign_obj.id,
                                subscriber_email=subscriber.email,
                                status='sent',
                                sent_at=datetime.utcnow()
                            )
                            logger.info(f"Email sent successfully to {subscriber.email}")
                        else:
                            total_failed += 1
                            # Log failed send
                            log = EmailLog(
                                campaign_id=campaign_obj.id,
                                subscriber_email=subscriber.email,
                                status='failed',
                                error_message='Send failed',
                                sent_at=datetime.utcnow()
                            )
                            logger.warning(f"Failed to send email to {subscriber.email}")
                        
                        db.session.add(log)
                        db.session.commit()  # Commit after each email
                        
                        # Small delay between emails
                        time.sleep(0.5)
                        
                    except Exception as e:
                        total_failed += 1
                        logger.error(f"Error sending to {subscriber.email}: {str(e)}")
                        
                        # Log error
                        log = EmailLog(
                            campaign_id=campaign_obj.id,
                            subscriber_email=subscriber.email,
                            status='failed',
                            error_message=str(e),
                            sent_at=datetime.utcnow()
                        )
                        db.session.add(log)
                        db.session.commit()  # Commit after each email
                
                # Update campaign status
                campaign_obj.status = 'sent'
                campaign_obj.total_sent = total_sent
                campaign_obj.total_failed = total_failed
                db.session.commit()
                
                logger.info(f"Campaign {campaign_obj.name} completed: {total_sent} sent, {total_failed} failed")
                
            except Exception as e:
                with app.app_context():
                    campaign_obj = Campaign.query.get(id)
                    campaign_obj.status = 'failed'
                    db.session.commit()
                logger.error(f"Campaign failed: {str(e)}")
    
    # Start background thread
    thread = threading.Thread(target=send_emails)
    thread.daemon = True
    thread.start()
    
    flash('Campaign sending started in background', 'success')
    return redirect(url_for('campaign_detail', id=id))

@app.route('/campaigns/<int:id>/logs')
def campaign_logs(id):
    """View campaign email logs"""
    campaign = Campaign.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    logs = EmailLog.query.filter_by(campaign_id=id).order_by(EmailLog.sent_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('campaign_logs.html', campaign=campaign, logs=logs)

@app.route('/api/campaign/<int:id>/status')
def campaign_status_api(id):
    """API endpoint to get campaign status"""
    campaign = Campaign.query.get_or_404(id)
    return jsonify({
        'status': campaign.status,
        'total_sent': campaign.total_sent or 0,
        'total_failed': campaign.total_failed or 0
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)