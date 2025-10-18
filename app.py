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
# ThreadPoolExecutor removed - using sequential sending to avoid connection issues
import logging
import unicodedata
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def format_name(name):
    """
    Format names properly:
    - Arabic names: keep as-is (preserve original formatting)
    - English names: Title Case (First Letter Capital, rest lowercase)
    - Handle special cases like hyphenated names, apostrophes, etc.
    """
    if not name or not name.strip():
        return ""
    
    name = name.strip()
    
    # Check if name contains Arabic characters
    def contains_arabic(text):
        for char in text:
            if '\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' or '\u08A0' <= char <= '\u08FF':
                return True
        return False
    
    # If name contains Arabic characters, preserve original formatting
    if contains_arabic(name):
        return name
    
    # For non-Arabic names, apply proper title casing
    # Handle special cases for names
    formatted_name = []
    
    # Split by spaces to handle multiple names
    name_parts = name.split()
    
    for part in name_parts:
        if not part:
            continue
            
        # Handle hyphenated names (e.g., "Al-Rashid")
        if '-' in part:
            hyphen_parts = part.split('-')
            formatted_hyphen = []
            for hyp_part in hyphen_parts:
                if hyp_part:
                    # Special handling for prefixes like "Al", "De", "Van", etc.
                    if hyp_part.lower() in ['al', 'de', 'van', 'von', 'da', 'del', 'della', 'di']:
                        formatted_hyphen.append(hyp_part.title())
                    else:
                        formatted_hyphen.append(hyp_part.capitalize())
            formatted_name.append('-'.join(formatted_hyphen))
        
        # Handle names with apostrophes (e.g., "O'Connor")
        elif "'" in part:
            apos_parts = part.split("'")
            formatted_apos = []
            for i, apos_part in enumerate(apos_parts):
                if apos_part:
                    formatted_apos.append(apos_part.capitalize())
                else:
                    formatted_apos.append(apos_part)
            formatted_name.append("'".join(formatted_apos))
        
        # Handle regular names
        else:
            # Special handling for prefixes and Celtic names
            if part.lower() in ['al', 'de', 'van', 'von', 'da', 'del', 'della', 'di']:
                formatted_name.append(part.title())
            # Handle Celtic names like McPherson, MacDonald, O'Brien
            elif part.lower().startswith('mc') and len(part) > 2:
                formatted_name.append('Mc' + part[2:].capitalize())
            elif part.lower().startswith('mac') and len(part) > 3:
                formatted_name.append('Mac' + part[3:].capitalize())
            else:
                formatted_name.append(part.capitalize())
    
    return ' '.join(formatted_name)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
# Use the database URL from environment if set (for executable), otherwise use default
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///newsletter.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['SMTP_SERVER'] = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
app.config['SMTP_PORT'] = int(os.environ.get('SMTP_PORT', '587'))
app.config['EMAIL_ADDRESS'] = os.environ.get('EMAIL_ADDRESS', '')
app.config['EMAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD', '')

# Initialize database
from models import db, Subscriber, Template, Campaign, EmailLog, SubscriberTag, EmailOpen, EmailClick
db.init_app(app)
migrate = Migrate(app, db)

from email_service import EmailService
from template_engine import TemplateEngine
from scheduler import CampaignScheduler

# Initialize services
email_service = EmailService(app.config)
template_engine = TemplateEngine()
campaign_scheduler = CampaignScheduler(app)

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
    search = request.args.get('search', '').strip()
    
    # Build query with search if provided
    query = Subscriber.query
    if search:
        # Search in both email and name fields (case-insensitive)
        search_filter = f"%{search.lower()}%"
        query = query.filter(
            db.or_(
                db.func.lower(Subscriber.email).like(search_filter),
                db.func.lower(Subscriber.name).like(search_filter)
            )
        )
    
    subscribers = query.paginate(page=page, per_page=50, error_out=False)
    return render_template('subscribers.html', subscribers=subscribers, search=search)

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
                import re
                
                # Read the file content with better encoding handling
                content = file.stream.read()
                
                # Try different encodings
                encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
                decoded_content = None
                
                for encoding in encodings_to_try:
                    try:
                        decoded_content = content.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if decoded_content is None:
                    flash('Unable to decode CSV file. Please ensure it\'s saved in UTF-8 format.', 'error')
                    return redirect(request.url)
                
                stream = io.StringIO(decoded_content, newline=None)
                
                # Detect delimiter (tab, semicolon, or comma)
                sample_line = decoded_content.split('\n')[0] if '\n' in decoded_content else decoded_content
                
                # Check for tab delimiter first (most specific)
                if '\t' in sample_line:
                    delimiter = '\t'
                # Then check for semicolon vs comma
                elif ';' in sample_line and sample_line.count(';') > sample_line.count(','):
                    delimiter = ';'
                else:
                    delimiter = ','
                
                csv_input = csv.reader(stream, delimiter=delimiter)
                
                added_count = 0
                duplicate_count = 0
                error_count = 0
                invalid_emails = []  # For debugging
                
                # Track processed rows
                row_number = 0
                
                for row in csv_input:
                    row_number += 1
                    
                    # Skip empty rows
                    if not row or (len(row) == 1 and not row[0].strip()):
                        continue
                    
                    # Check if this looks like a header row
                    if row_number == 1:
                        row_str = ','.join(row).lower()
                        if 'email' in row_str or 'e-mail' in row_str:
                            continue  # Skip header row
                    
                    if len(row) >= 1:
                        email = row[0].strip()
                        name = row[1].strip() if len(row) > 1 else ''
                        
                        # Clean up email - remove any quotes or extra spaces
                        email = email.replace('"', '').replace("'", "").strip().lower()
                        
                        # Clean and format name properly
                        name = format_name(name)
                        
                        # Validate email using helper function
                        if is_valid_email(email):
                            existing = Subscriber.query.filter_by(email=email).first()
                            if not existing:
                                subscriber = Subscriber(email=email, name=name)
                                db.session.add(subscriber)
                                added_count += 1
                            else:
                                duplicate_count += 1
                        else:
                            error_count += 1
                            # Keep track of first few invalid emails for debugging
                            if len(invalid_emails) < 5:
                                invalid_emails.append(f"Row {row_number}: '{email}'")
                
                db.session.commit()
                
                # Create detailed success message
                message_parts = [f'Successfully imported {added_count} subscribers']
                if duplicate_count > 0:
                    message_parts.append(f'{duplicate_count} duplicates skipped')
                if error_count > 0:
                    message_parts.append(f'{error_count} invalid entries skipped')
                
                message = '. '.join(message_parts) + '.'
                
                flash(message, 'success')
                
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

@app.route('/subscribers/bulk-delete', methods=['POST'])
def bulk_delete_subscribers():
    """Bulk delete subscribers"""
    subscriber_ids = request.form.getlist('subscriber_ids')
    
    if not subscriber_ids:
        flash('No subscribers selected for deletion', 'error')
        return redirect(url_for('subscribers'))
    
    try:
        # Convert string IDs to integers and validate
        ids_to_delete = []
        for id_str in subscriber_ids:
            try:
                ids_to_delete.append(int(id_str))
            except ValueError:
                flash(f'Invalid subscriber ID: {id_str}', 'error')
                return redirect(url_for('subscribers'))
        
        # Delete subscribers
        deleted_count = 0
        for subscriber_id in ids_to_delete:
            subscriber = Subscriber.query.get(subscriber_id)
            if subscriber:
                db.session.delete(subscriber)
                deleted_count += 1
        
        db.session.commit()
        
        if deleted_count > 0:
            message = f'Successfully deleted {deleted_count} subscriber{"s" if deleted_count != 1 else ""}'
            flash(message, 'success')
        else:
            flash('No subscribers were deleted', 'warning')
            
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error in bulk delete: {str(e)}')
        flash(f'Error deleting subscribers: {str(e)}', 'error')
    
    return redirect(url_for('subscribers'))

@app.route('/subscribers/update-status/<int:id>', methods=['POST'])
def update_subscriber_status(id):
    """Update subscriber status (toggle active/inactive)"""
    subscriber = Subscriber.query.get_or_404(id)
    
    try:
        # Toggle the status
        subscriber.is_active = not subscriber.is_active
        subscriber.updated_at = datetime.utcnow()
        db.session.commit()
        
        status_text = "active" if subscriber.is_active else "inactive"
        
        # Return JSON response for AJAX calls
        return jsonify({
            'success': True,
            'message': f'Subscriber status updated to {status_text}',
            'is_active': subscriber.is_active,
            'status_text': status_text
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating subscriber status: {str(e)}')
        
        # Return JSON error response
        return jsonify({
            'success': False,
            'message': f'Error updating subscriber status: {str(e)}'
        }), 500

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
    thread = threading.Thread(target=send_campaign_emails, args=(id,))
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

# ===== NEW FEATURES =====

@app.route('/unsubscribe/<int:subscriber_id>')
def unsubscribe_page(subscriber_id):
    """Show unsubscribe confirmation page"""
    subscriber = Subscriber.query.get_or_404(subscriber_id)
    return render_template('unsubscribe.html', subscriber=subscriber)

@app.route('/unsubscribe/<int:subscriber_id>/confirm', methods=['POST'])
def unsubscribe_confirm(subscriber_id):
    """Process unsubscribe request"""
    subscriber = Subscriber.query.get_or_404(subscriber_id)
    try:
        subscriber.is_active = False
        subscriber.unsubscribed_at = datetime.utcnow()
        db.session.commit()
        flash('You have been unsubscribed successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error processing unsubscribe: {str(e)}', 'error')
    
    return render_template('unsubscribed.html')

@app.route('/subscribers/export')
def export_subscribers():
    """Export all subscribers to CSV"""
    import csv
    from flask import Response
    from io import StringIO
    
    subscribers = Subscriber.query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Email', 'Name', 'Status', 'Created At', 'Unsubscribed At'])
    
    for sub in subscribers:
        writer.writerow([
            sub.email,
            sub.name or '',
            'Active' if sub.is_active else 'Inactive',
            sub.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            sub.unsubscribed_at.strftime('%Y-%m-%d %H:%M:%S') if sub.unsubscribed_at else ''
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=subscribers_export.csv'}
    )

@app.route('/api/template-variables')
def template_variables_api():
    """API endpoint to get available template variables"""
    variables = template_engine.get_available_variables()
    return jsonify(variables)

@app.route('/campaigns/schedule/<int:id>', methods=['POST'])
def schedule_campaign(id):
    """Schedule a campaign for future sending"""
    campaign = Campaign.query.get_or_404(id)
    
    scheduled_datetime = request.form.get('scheduled_datetime')
    if not scheduled_datetime:
        flash('Please select a date and time', 'error')
        return redirect(url_for('campaign_detail', id=id))
    
    try:
        # Parse the datetime
        send_time = datetime.strptime(scheduled_datetime, '%Y-%m-%dT%H:%M')
        
        # Check if time is in the future
        if send_time <= datetime.now():
            flash('Scheduled time must be in the future', 'error')
            return redirect(url_for('campaign_detail', id=id))
        
        # Update campaign
        campaign.scheduled_at = send_time
        campaign.is_scheduled = True
        campaign.status = 'scheduled'
        db.session.commit()
        
        # Schedule with scheduler
        campaign_scheduler.schedule_campaign(id, send_time)
        
        flash(f'Campaign scheduled for {send_time.strftime("%Y-%m-%d %H:%M")}', 'success')
    except ValueError:
        flash('Invalid date/time format', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error scheduling campaign: {str(e)}', 'error')
    
    return redirect(url_for('campaign_detail', id=id))

@app.route('/campaigns/cancel-schedule/<int:id>', methods=['POST'])
def cancel_schedule_campaign(id):
    """Cancel a scheduled campaign"""
    campaign = Campaign.query.get_or_404(id)
    
    try:
        # Cancel scheduler job
        campaign_scheduler.cancel_scheduled_campaign(id)
        
        # Update campaign
        campaign.scheduled_at = None
        campaign.is_scheduled = False
        campaign.status = 'draft'
        db.session.commit()
        
        flash('Campaign schedule cancelled', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error cancelling schedule: {str(e)}', 'error')
    
    return redirect(url_for('campaign_detail', id=id))

# Helper function to send campaign emails (extracted for scheduler use)
def send_campaign_emails(campaign_id):
    """Send campaign emails (can be called by scheduler or manual trigger)"""
    with app.app_context():
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return
        
        campaign.status = 'sending'
        db.session.commit()
        
        template = Template.query.get(campaign.template_id)
        active_subscribers = Subscriber.query.filter_by(is_active=True).all()
        
        total_sent = 0
        total_failed = 0
        
        for subscriber in active_subscribers:
            try:
                # Render template with personalization
                personalized_content = template_engine.render_template(
                    template.content,
                    subscriber,
                    campaign
                )
                personalized_subject = template_engine.render_subject(
                    template.subject,
                    subscriber,
                    campaign
                )
                
                # Send email
                success = email_service.send_email(
                    subscriber.email,
                    personalized_subject,
                    personalized_content,
                    subscriber.name
                )
                
                # Log result
                if success:
                    total_sent += 1
                    log = EmailLog(
                        campaign_id=campaign.id,
                        subscriber_email=subscriber.email,
                        status='sent',
                        sent_at=datetime.utcnow()
                    )
                else:
                    total_failed += 1
                    log = EmailLog(
                        campaign_id=campaign.id,
                        subscriber_email=subscriber.email,
                        status='failed',
                        error_message='Send failed',
                        sent_at=datetime.utcnow()
                    )
                
                db.session.add(log)
                db.session.commit()
                
            except Exception as e:
                total_failed += 1
                logger.error(f"Error sending to {subscriber.email}: {str(e)}")
                
                log = EmailLog(
                    campaign_id=campaign.id,
                    subscriber_email=subscriber.email,
                    status='failed',
                    error_message=str(e),
                    sent_at=datetime.utcnow()
                )
                db.session.add(log)
                db.session.commit()
        
        # Update campaign final status
        campaign.status = 'sent'
        campaign.sent_at = datetime.utcnow()
        campaign.total_sent = total_sent
        campaign.total_failed = total_failed
        db.session.commit()
        
        logger.info(f"Campaign {campaign.id} completed: {total_sent} sent, {total_failed} failed")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)