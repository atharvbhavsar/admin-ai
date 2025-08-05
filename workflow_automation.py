import requests
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class WorkflowManager:
    """Manages workflow automation using n8n and Make.com"""
    
    def __init__(self):
        self.n8n_webhook_url = Config.N8N_WEBHOOK_URL
        self.make_webhook_url = Config.MAKE_WEBHOOK_URL
    
    def trigger_workflow(self, workflow_type: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Trigger a workflow using the available automation platform"""
        
        if self.n8n_webhook_url:
            return self._trigger_n8n_workflow(workflow_type, data)
        elif self.make_webhook_url:
            return self._trigger_make_workflow(workflow_type, data)
        else:
            return None
    
    def _trigger_n8n_workflow(self, workflow_type: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Trigger n8n workflow"""
        try:
            payload = {
                "workflow_type": workflow_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            
            response = requests.post(
                self.n8n_webhook_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return response.json() if response.content else {"status": "success"}
            else:
                logger.error(f"n8n workflow error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error triggering n8n workflow: {e}")
            return None
    
    def _trigger_make_workflow(self, workflow_type: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Trigger Make.com workflow"""
        try:
            payload = {
                "workflow_type": workflow_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            
            response = requests.post(
                self.make_webhook_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return response.json() if response.content else {"status": "success"}
            else:
                logger.error(f"Make.com workflow error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error triggering Make.com workflow: {e}")
            return None
    
    def send_admission_notification(self, user_data: Dict[str, Any], college_data: Dict[str, Any]) -> bool:
        """Send admission notification through workflow automation"""
        
        workflow_data = {
            "notification_type": "admission_update",
            "user": {
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "phone": user_data.get("phone"),
                "category": user_data.get("category")
            },
            "college": {
                "name": college_data.get("name"),
                "cutoff": college_data.get("cutoff"),
                "status": college_data.get("admission_status", "eligible")
            },
            "message": f"New admission update for {college_data.get('name')}"
        }
        
        result = self.trigger_workflow("admission_notification", workflow_data)
        return result is not None
    
    def send_deadline_reminder(self, user_data: Dict[str, Any], deadline_data: Dict[str, Any]) -> bool:
        """Send deadline reminder through workflow automation"""
        
        workflow_data = {
            "notification_type": "deadline_reminder",
            "user": {
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "phone": user_data.get("phone")
            },
            "deadline": {
                "exam_name": deadline_data.get("exam_name"),
                "event": deadline_data.get("event"),
                "date": deadline_data.get("date"),
                "priority": deadline_data.get("priority", "medium")
            },
            "message": f"Reminder: {deadline_data.get('event')} deadline approaching"
        }
        
        result = self.trigger_workflow("deadline_reminder", workflow_data)
        return result is not None
    
    def sync_college_data(self, college_updates: List[Dict[str, Any]]) -> bool:
        """Sync college data updates through workflow automation"""
        
        workflow_data = {
            "sync_type": "college_data_update",
            "updates": college_updates,
            "total_updates": len(college_updates),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = self.trigger_workflow("data_sync", workflow_data)
        return result is not None
    
    def track_user_interaction(self, user_data: Dict[str, Any], interaction_data: Dict[str, Any]) -> bool:
        """Track user interactions for analytics"""
        
        workflow_data = {
            "analytics_type": "user_interaction",
            "user": {
                "id": user_data.get("id"),
                "category": user_data.get("category"),
                "location": user_data.get("city")
            },
            "interaction": {
                "type": interaction_data.get("type"),
                "page": interaction_data.get("page"),
                "action": interaction_data.get("action"),
                "data": interaction_data.get("data")
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = self.trigger_workflow("analytics_tracking", workflow_data)
        return result is not None
    
    def generate_ai_recommendation_report(self, user_data: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> bool:
        """Generate and send AI recommendation report"""
        
        workflow_data = {
            "report_type": "ai_recommendations",
            "user": {
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "percentile": user_data.get("percentile"),
                "category": user_data.get("category"),
                "preferences": user_data.get("preferences", [])
            },
            "recommendations": recommendations,
            "generation_timestamp": datetime.utcnow().isoformat()
        }
        
        result = self.trigger_workflow("recommendation_report", workflow_data)
        return result is not None
    
    def schedule_follow_up(self, user_data: Dict[str, Any], follow_up_type: str, schedule_date: str) -> bool:
        """Schedule follow-up communications"""
        
        workflow_data = {
            "schedule_type": "follow_up",
            "user": {
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "phone": user_data.get("phone")
            },
            "follow_up": {
                "type": follow_up_type,
                "scheduled_date": schedule_date,
                "priority": "medium"
            },
            "creation_timestamp": datetime.utcnow().isoformat()
        }
        
        result = self.trigger_workflow("schedule_follow_up", workflow_data)
        return result is not None
    
    def create_workflow_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create workflow templates for common automation tasks"""
        
        templates = {
            "admission_notification": {
                "name": "College Admission Notification",
                "description": "Notify users about college admission updates",
                "triggers": ["admission_status_change", "cutoff_update"],
                "actions": [
                    "send_email",
                    "send_sms",
                    "update_user_dashboard",
                    "log_notification"
                ],
                "conditions": [
                    "user_preferences.notifications_enabled",
                    "admission_status != 'no_change'"
                ]
            },
            "deadline_reminder": {
                "name": "Exam Deadline Reminder",
                "description": "Send reminders for important exam deadlines",
                "triggers": ["scheduled_time", "deadline_approaching"],
                "actions": [
                    "send_email_reminder",
                    "send_push_notification",
                    "update_calendar"
                ],
                "conditions": [
                    "days_until_deadline <= 7",
                    "user_preferences.reminders_enabled"
                ]
            },
            "data_sync": {
                "name": "College Data Synchronization",
                "description": "Sync college data across multiple systems",
                "triggers": ["data_update", "scheduled_sync"],
                "actions": [
                    "validate_data",
                    "update_database",
                    "refresh_cache",
                    "notify_admin"
                ],
                "conditions": [
                    "data_validation_passed",
                    "sync_window_open"
                ]
            },
            "analytics_tracking": {
                "name": "User Analytics Tracking",
                "description": "Track user interactions for analytics",
                "triggers": ["user_interaction", "page_view"],
                "actions": [
                    "log_interaction",
                    "update_user_profile",
                    "generate_insights"
                ],
                "conditions": [
                    "user_consent_given",
                    "interaction_valid"
                ]
            },
            "recommendation_report": {
                "name": "AI Recommendation Report",
                "description": "Generate and send personalized recommendation reports",
                "triggers": ["recommendation_generated", "weekly_schedule"],
                "actions": [
                    "generate_pdf_report",
                    "send_email_report",
                    "update_user_dashboard",
                    "schedule_follow_up"
                ],
                "conditions": [
                    "recommendations_available",
                    "user_preferences.reports_enabled"
                ]
            }
        }
        
        return templates
    
    def get_automation_status(self) -> Dict[str, Any]:
        """Get status of automation services"""
        return {
            "n8n_available": bool(self.n8n_webhook_url),
            "make_available": bool(self.make_webhook_url),
            "automation_enabled": bool(self.n8n_webhook_url or self.make_webhook_url),
            "workflow_templates": list(self.create_workflow_templates().keys())
        }

# Global instance
workflow_manager = WorkflowManager()