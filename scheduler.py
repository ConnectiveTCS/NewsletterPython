"""
Campaign Scheduler for Newsletter Application
Handles scheduled and recurring campaigns
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CampaignScheduler:
    """Schedule campaigns for future sending"""
    
    def __init__(self, app):
        self.app = app
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Campaign scheduler started")
    
    def schedule_campaign(self, campaign_id, send_time):
        """
        Schedule a campaign to be sent at specific time
        
        Args:
            campaign_id: ID of the campaign to send
            send_time: datetime when to send the campaign
        """
        try:
            job_id = f'campaign_{campaign_id}'
            
            # Remove existing job if any
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
            
            # Schedule new job
            self.scheduler.add_job(
                func=self._send_scheduled_campaign,
                trigger='date',
                run_date=send_time,
                args=[campaign_id],
                id=job_id,
                name=f'Send Campaign {campaign_id}'
            )
            
            logger.info(f"Campaign {campaign_id} scheduled for {send_time}")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling campaign {campaign_id}: {str(e)}")
            return False
    
    def cancel_scheduled_campaign(self, campaign_id):
        """
        Cancel a scheduled campaign
        
        Args:
            campaign_id: ID of the campaign to cancel
        """
        try:
            job_id = f'campaign_{campaign_id}'
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
                logger.info(f"Cancelled scheduled campaign {campaign_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error cancelling campaign {campaign_id}: {str(e)}")
            return False
    
    def _send_scheduled_campaign(self, campaign_id):
        """
        Send scheduled campaign (internal method)
        
        Args:
            campaign_id: ID of the campaign to send
        """
        with self.app.app_context():
            try:
                from models import Campaign, db
                
                campaign = Campaign.query.get(campaign_id)
                if not campaign:
                    logger.error(f"Campaign {campaign_id} not found")
                    return
                
                # Update status
                campaign.status = 'sending'
                campaign.is_scheduled = False
                db.session.commit()
                
                # Trigger the actual sending (this will be handled by the main send_campaign function)
                logger.info(f"Scheduled campaign {campaign_id} is now ready to send")
                
                # Import here to avoid circular imports
                from app import send_campaign_emails
                send_campaign_emails(campaign_id)
                
            except Exception as e:
                logger.error(f"Error sending scheduled campaign {campaign_id}: {str(e)}")
    
    def get_scheduled_jobs(self):
        """
        Get list of all scheduled jobs
        
        Returns:
            List of scheduled job information
        """
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time,
            })
        return jobs
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Campaign scheduler stopped")
