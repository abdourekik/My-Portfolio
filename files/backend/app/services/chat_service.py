"""
Chat Assistant Service - Uses Groq API
"""
from typing import List, Dict, Optional
from datetime import datetime
from app.services.groq_service import groq_service


class ChatAssistantService:
    """Sales chat assistant"""
    
    def __init__(self):
        self.conversation_sessions = {}
    
    def start_session(self, session_id: str, lead_context: Optional[Dict] = None):
        self.conversation_sessions[session_id] = {
            'messages': [],
            'lead_context': lead_context,
            'started_at': datetime.now()
        }
    
    def send_message(self, session_id: str, message: str, role: str = "user") -> str:
        if session_id not in self.conversation_sessions:
            self.start_session(session_id)
        
        session = self.conversation_sessions[session_id]
        
        session['messages'].append({
            'role': role,
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        conversation_history = [
            {'role': msg['role'], 'content': msg['content']}
            for msg in session['messages']
        ]
        
        response = groq_service.sales_chat_assistant(
            conversation_history=conversation_history,
            lead_context=session.get('lead_context')
        )
        
        session['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def handle_objection(self, objection: str, lead_context: Optional[Dict] = None) -> Dict:
        prompt = f"""Objection: "{objection}"

Provide:
1. Professional response
2. 3 tactical tips

JSON: {{"response": "...", "tips": ["...", "...", "..."]}}"""
        
        messages = [
            {"role": "system", "content": "Objection handling expert. JSON only."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = groq_service.chat_completion(messages, temperature=0.6)
            import json
            clean = response.strip()
            if '```' in clean:
                clean = clean.split('```')[1]
                if clean.startswith('json'):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except:
            return {
                "response": "I understand. Could you share more about your concerns?",
                "tips": ["Listen actively", "Provide examples", "Offer trial period"]
            }
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        if session_id in self.conversation_sessions:
            return self.conversation_sessions[session_id]['messages']
        return []
    
    def end_session(self, session_id: str):
        if session_id in self.conversation_sessions:
            del self.conversation_sessions[session_id]


chat_assistant = ChatAssistantService()
