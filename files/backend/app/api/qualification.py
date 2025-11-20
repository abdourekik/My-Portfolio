"""
Lead Qualification API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from app.services.grok_service import grok_service

router = APIRouter(prefix=\"/api/qualify\", tags=[\"Lead Qualification\"])


class QualificationQuestion(BaseModel):
    \"\"\"Qualification question\"\"\"
    question: str
    lead_info: Dict
    previous_answers: Optional[List[Dict]] = None


class QualificationResponse(BaseModel):
    \"\"\"Qualification response\"\"\"
    analysis: str
    next_step: str
    timestamp: str


@router.post(\"/question\", response_model=QualificationResponse)
async def ask_qualification_question(request: QualificationQuestion):
    \"\"\"
    Analyze lead response and suggest next qualification step
    \"\"\"
    try:
        result = grok_service.qualify_lead(
            lead_info=request.lead_info,
            question=request.question,
            previous_answers=request.previous_answers
        )
        
        return QualificationResponse(
            analysis=result.get('analysis', 'Analysis unavailable'),
            next_step=result.get('next_step', 'Continue qualification'),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f\"Error in qualification: {str(e)}\")


@router.post(\"/evaluate-fit\")
async def evaluate_lead_fit(lead_info: Dict, answers: List[Dict]):
    \"\"\"
    Evaluate overall lead fit based on qualification answers
    \"\"\"
    try:
        # Build context
        context = f\"\"\"
Lead: {lead_info.get('first_name')} {lead_info.get('last_name')}
Company: {lead_info.get('company_name')}
Title: {lead_info.get('job_title')}

Qualification Answers:
\"\"\"
        for qa in answers:
            context += f\"Q: {qa.get('question', 'N/A')}\nA: {qa.get('answer', 'N/A')}\n\n\"
        
        prompt = f\"\"\"{context}

Based on these qualification answers, evaluate:
1. Budget fit (1-10)
2. Authority (decision maker?) (1-10)
3. Need (how urgent?) (1-10)
4. Timeline fit (1-10)
5. Overall qualification score (1-10)
6. Recommendation (qualified/not qualified/needs more info)

Respond in JSON: {{
    \"budget_fit\": X,
    \"authority\": X,
    \"need\": X,
    \"timeline_fit\": X,
    \"overall_score\": X,
    \"recommendation\": \"...\",
    \"reasoning\": \"...\"
}}\"\"\"
        
        messages = [
            {\"role\": \"system\", \"content\": \"You are a sales qualification expert. Respond with valid JSON only.\"},
            {\"role\": \"user\", \"content\": prompt}
        ]
        
        response = grok_service.chat_completion(messages, temperature=0.5)
        
        import json
        clean_response = response.strip()
        if clean_response.startswith('`'):
            clean_response = clean_response.split('`')[1]
            if clean_response.startswith('json'):
                clean_response = clean_response[4:]
        
        evaluation = json.loads(clean_response.strip())
        evaluation['timestamp'] = datetime.now().isoformat()
        evaluation['lead_info'] = lead_info
        
        return evaluation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f\"Error evaluating fit: {str(e)}\")
