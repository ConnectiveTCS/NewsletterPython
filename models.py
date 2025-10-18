"""
Database Models for Newsletter Application
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subscriber(db.Model):
    """Subscriber model for email addresses"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=True, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    unsubscribed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    tags = db.relationship('SubscriberTag', secondary='subscriber_tag_associations', backref=db.backref('subscribers', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Subscriber {self.email}>'

class Template(db.Model):
    """Email template model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    campaigns = db.relationship('Campaign', backref='template', lazy=True)
    
    def __repr__(self):
        return f'<Template {self.name}>'

class Campaign(db.Model):
    """Campaign model for email campaigns"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    status = db.Column(db.String(50), default='draft', nullable=False, index=True)  # draft, sending, sent, failed, scheduled
    total_sent = db.Column(db.Integer, default=0)
    total_failed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    sent_at = db.Column(db.DateTime, nullable=True)
    scheduled_at = db.Column(db.DateTime, nullable=True)
    is_scheduled = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False, nullable=False, index=True)
    archived_at = db.Column(db.DateTime, nullable=True)
    
    # Relationship
    email_logs = db.relationship('EmailLog', backref='campaign', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Campaign {self.name}>'

class EmailLog(db.Model):
    """Email log model for audit trail"""
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    subscriber_email = db.Column(db.String(255), nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False)  # sent, failed, bounced
    error_message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships for analytics
    opens = db.relationship('EmailOpen', backref='email_log', lazy=True, cascade='all, delete-orphan')
    clicks = db.relationship('EmailClick', backref='email_log', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<EmailLog {self.subscriber_email} - {self.status}>'

class SubscriberTag(db.Model):
    """Tags for subscriber segmentation"""
    __tablename__ = 'subscriber_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SubscriberTag {self.name}>'

class SubscriberTagAssociation(db.Model):
    """Many-to-many relationship between subscribers and tags"""
    __tablename__ = 'subscriber_tag_associations'
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('subscriber_tags.id'), primary_key=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmailOpen(db.Model):
    """Track email opens"""
    __tablename__ = 'email_opens'
    id = db.Column(db.Integer, primary_key=True)
    email_log_id = db.Column(db.Integer, db.ForeignKey('email_log.id'), nullable=False)
    opened_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<EmailOpen {self.email_log_id}>'

class EmailClick(db.Model):
    """Track email link clicks"""
    __tablename__ = 'email_clicks'
    id = db.Column(db.Integer, primary_key=True)
    email_log_id = db.Column(db.Integer, db.ForeignKey('email_log.id'), nullable=False)
    link_url = db.Column(db.String(500))
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<EmailClick {self.link_url}>'