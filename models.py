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
    name = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
    status = db.Column(db.String(50), default='draft', nullable=False)  # draft, sending, sent, failed
    total_sent = db.Column(db.Integer, default=0)
    total_failed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    
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
    
    def __repr__(self):
        return f'<EmailLog {self.subscriber_email} - {self.status}>'