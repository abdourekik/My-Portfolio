"""
Grok API Service
Integration with xAI's Grok API for conversational features
"""
import os
from typing import List, Dict, Optional
from openai import OpenAI
from app.config import settings


class GrokService:
    """Service for interacting with Grok API (xAI)"""
    
    def __init__(self):
        """Initialize Grok API client"""
        self.client = OpenAI(
            api_key=settings.GROK_API_KEY,
            base_url=settings.GROK_API_BASE
        )
        self.model = settings.GROK_MODEL
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Send messages to Grok and get response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling Grok API: {e}")
            raise
    
    def generate_email(
        self,
        lead_info: Dict,
        lead_score: float,
        email_type: str = "introduction"
    ) -> Dict[str, str]:
        """Generate personalized email for a lead"""
        
        # Build context about the lead
        first_name = lead_info.get('first_name', '')
        last_name = lead_info.get('last_name', '')
        company = lead_info.get('company_name', 'Unknown')
        title = lead_info.get('job_title', 'Unknown')
        industry = lead_info.get('industry', 'Unknown')
        source = lead_info.get('source', 'Unknown')
        score_pct = lead_score * 100
        
        lead_context = f"""
Lead Information:
- Name: {first_name} {last_name}
- Company: {company}
- Title: {title}
- Industry: {industry}
- Lead Score: {score_pct:.1f}% (AI-predicted conversion probability)
- Source: {source}
"""
        
        # Quality indicator
        quality = "high-value" if lead_score >= 0.7 else "promising" if lead_score >= 0.4 else "potential"
        
        prompt = f"""You are a professional sales expert. Generate a personalized {email_type} email.

{lead_context}

This is a {quality} lead. Write a professional, personalized email that:
1. Is concise (under 150 words)
2. Addresses their specific role and industry
3. Offers clear value proposition
4. Includes a clear call-to-action
5. Is warm but professional

Return ONLY a JSON object with 'subject' and 'body' keys. No other text.
"""
        
        messages = [
            {"role": "system", "content": "You are a professional sales email expert. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.chat_completion(messages, temperature=0.7, max_tokens=500)
            
            # Parse JSON response
            import json
            # Clean response (remove markdown if present)
            clean_response = response.strip()
            if clean_response.startswith('```'):
                clean_response = clean_response.split('```')[1]
                if clean_response.startswith('json'):
                    clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            email_data = json.loads(clean_response)
            return email_data
            
        except Exception as e:
            print(f"Error generating email: {e}")
            # Fallback email
            return {
                "subject": f"Introduction - {company}",
                "body": f"Hi {first_name},\n\nI wanted to reach out regarding opportunities for {company}.\n\nBest regards"
            }
    
    def sales_chat_assistant(
        self,
        conversation_history: List[Dict[str, str]],
        lead_context: Optional[Dict] = None
    ) -> str:
        """Sales chat assistant for helping reps during conversations"""
        
        system_prompt = """You are an expert sales assistant helping sales representatives during conversations.

Your role:
- Provide objection handling strategies
- Suggest next steps in the sales process
- Offer value propositions
- Help with pricing discussions
- Give tactical advice

Be concise, actionable, and professional."""
        
        if lead_context:
            company = lead_context.get('company_name', 'Unknown')
            title = lead_context.get('job_title', 'Unknown')
            industry = lead_context.get('industry', 'Unknown')
            score = lead_context.get('score', 0) * 100
            
            system_prompt += f"""

Current Lead Context:
- Company: {company}
- Title: {title}
- Industry: {industry}
- Score: {score:.0f}%"""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        
        return self.chat_completion(messages, temperature=0.7, max_tokens=300)
    
    def qualify_lead(
        self,
        lead_info: Dict,
        question: str,
        previous_answers: Optional[List[Dict]] = None
    ) -> Dict[str, str]:
        """Generate qualification questions and evaluate answers"""
        
        first_name = lead_info.get('first_name', '')
        last_name = lead_info.get('last_name', '')
        company = lead_info.get('company_name', '')
        title = lead_info.get('job_title', '')
        
        context = f"""
Lead: {first_name} {last_name}
Company: {company}
Title: {title}
"""
        
        if previous_answers:
            context += "\n\nPrevious answers:\n"
            for qa in previous_answers:
                context += f"Q: {qa['question']}\nA: {qa['answer']}\n"
        
        prompt = f"""You are a sales qualification expert.

{context}

Current question: {question}

Based on the lead's answer, provide:
1. Analysis of their response (budget fit, timeline, authority)
2. Recommended next question OR qualification status

Respond in JSON format with: {{"analysis": "...", "next_step": "..."}}"""
        
        messages = [
            {"role": "system", "content": "You are a sales qualification expert. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.chat_completion(messages, temperature=0.6, max_tokens=400)
            import json
            # Clean response
            clean_response = response.strip()
            if clean_response.startswith('```'):
                parts = clean_response.split('```')
                if len(parts) >= 2:
                    clean_response = parts[1]
                    if clean_response.startswith('json'):
                        clean_response = clean_response[4:]
            clean_response = clean_response.strip()
            
            return json.loads(clean_response)
        except:
            return {
                "analysis": "Unable to analyze response",
                "next_step": "Continue with standard qualification"
            }


# Global instance
grok_service = GrokService()
