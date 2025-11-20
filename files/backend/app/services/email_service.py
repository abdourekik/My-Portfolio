"""
Email Service - Uses Groq API
"""
from typing import Dict, List
from datetime import datetime
from app.services.groq_service import groq_service
from app.ml.lead_scorer import LeadScorer


class EmailService:
    """Email generation service"""
    
    def __init__(self):
        self.scorer = LeadScorer()
        try:
            self.scorer.load_model('app/ml/models/lead_scorer.pkl')
        except:
            print("Warning: ML model not loaded")
    
    def generate_personalized_email(self, lead_info: Dict, email_type: str = "introduction") -> Dict:
        """Generate personalized email"""
        try:
            lead_score = self.scorer.predict(lead_info)
        except:
            lead_score = 0.5
        
        email_data = groq_service.generate_email(
            lead_info=lead_info,
            lead_score=lead_score,
            email_type=email_type
        )
        
        email_data['generated_at'] = datetime.now().isoformat()
        email_data['lead_score'] = lead_score
        email_data['email_type'] = email_type
        
        return email_data
    
    def generate_batch_emails(self, leads: List[Dict], email_type: str = "introduction") -> List[Dict]:
        """Generate emails for multiple leads"""
        emails = []
        for lead in leads:
            try:
                email = self.generate_personalized_email(lead, email_type)
                email['lead_email'] = lead.get('email')
                emails.append(email)
            except Exception as e:
                print(f"Error: {e}")
        return emails


email_service = EmailService()
