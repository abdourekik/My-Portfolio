"""
Groq API Service
Integration with Groq API for conversational features
"""
from typing import List, Dict, Optional
from openai import OpenAI
from app.config import settings


class GroqService:
    """Service for interacting with Groq API"""
    
    def __init__(self):
        """Initialize Groq API client"""
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url=settings.GROQ_API_BASE
        )
        self.model = settings.GROQ_MODEL
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Send messages to Groq and get response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            raise
    
    def generate_email(
        self,
        lead_info: Dict,
        lead_score: float,
        email_type: str = "introduction"
    ) -> Dict[str, str]:
        """Generate personalized email for a lead"""
        
        first_name = lead_info.get('first_name', '')
        last_name = lead_info.get('last_name', '')
        company = lead_info.get('company_name', 'Unknown')
        title = lead_info.get('job_title', 'Unknown')
        industry = lead_info.get('industry', 'Unknown')
        score_pct = lead_score * 100
        
        quality = "high-value" if lead_score >= 0.7 else "promising" if lead_score >= 0.4 else "potential"
        
        prompt = f"""Generate a professional {email_type} sales email for:
- Name: {first_name} {last_name}
- Company: {company}
- Title: {title}
- Industry: {industry}
- Lead Quality: {quality} ({score_pct:.0f}% conversion probability)

Write a concise (under 150 words), personalized email with clear value proposition and call-to-action.

Respond with JSON: {{"subject": "...", "body": "..."}}"""
        
        messages = [
            {"role": "system", "content": "You are a sales email expert. Respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.chat_completion(messages, temperature=0.7, max_tokens=500)
            
            import json
            clean_response = response.strip()
            if '```' in clean_response:
                clean_response = clean_response.split('```')[1]
                if clean_response.startswith('json'):
                    clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            return json.loads(clean_response)
            
        except Exception as e:
            print(f"Error: {e}")
            return {
                "subject": f"Partnership Opportunity - {company}",
                "body": f"Hi {first_name},\n\nI'd love to discuss how we can help {company}.\n\nBest regards"
            }
    
    def sales_chat_assistant(
        self,
        conversation_history: List[Dict[str, str]],
        lead_context: Optional[Dict] = None
    ) -> str:
        """Sales chat assistant"""
        
        system_prompt = """You are an expert sales assistant helping reps during conversations.
Provide: objection handling, next steps, value propositions, pricing help.
Be concise and actionable."""
        
        if lead_context:
            company = lead_context.get('company_name', 'Unknown')
            title = lead_context.get('job_title', 'Unknown')
            system_prompt += f"\n\nCurrent Lead: {title} at {company}"
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        
        return self.chat_completion(messages, temperature=0.7, max_tokens=300)
    
    def qualify_lead(
        self,
        lead_info: Dict,
        question: str,
        previous_answers: Optional[List[Dict]] = None
    ) -> Dict[str, str]:
        """Generate qualification analysis"""
        
        context = f"Lead: {lead_info.get('first_name')} at {lead_info.get('company_name')}"
        
        if previous_answers:
            context += "\nPrevious Q&A:\n"
            for qa in previous_answers:
                context += f"Q: {qa['question']}\nA: {qa['answer']}\n"
        
        prompt = f"""{context}

Current question: {question}

Analyze the response and provide:
1. Analysis (budget fit, timeline, authority)
2. Next step or qualification status

JSON format: {{"analysis": "...", "next_step": "..."}}"""
        
        messages = [
            {"role": "system", "content": "Sales qualification expert. JSON only."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.chat_completion(messages, temperature=0.6, max_tokens=400)
            import json
            clean = response.strip()
            if '```' in clean:
                clean = clean.split('```')[1]
                if clean.startswith('json'):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except:
            return {"analysis": "Unable to analyze", "next_step": "Continue qualification"}


# Global instance
groq_service = GroqService()
