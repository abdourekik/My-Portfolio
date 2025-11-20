"""
FastAPI Main Application
AI Sales & Lead Qualification Assistant
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime
from app.config import settings
from app.ml.lead_scorer import LeadScorer
from app.services.groq_service import groq_service
from app.services.email_service import email_service
from app.services.chat_service import chat_assistant

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Sales & Lead Qualification Platform with ML scoring, email generation, and chat assistant"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
allow_origins=settings.allowed_origins_list,    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML model
scorer = LeadScorer()
try:
    scorer.load_model('app/ml/models/lead_scorer.pkl')
    print("✅ ML Model loaded successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not load ML model: {e}")


# Pydantic Models
class LeadInput(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    company_name: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    job_title: Optional[str] = None
    source: Optional[str] = "website"
    website_visits: int = 0
    pages_viewed: int = 0
    email_opens: int = 0
    email_clicks: int = 0
    form_submissions: int = 0
    estimated_budget: Optional[float] = None
    timeline: Optional[str] = None
    linkedin_profile: Optional[str] = None


class LeadScoreResponse(BaseModel):
    lead_score: float
    score_percentage: float
    quality_level: str
    recommendation: str
    insights: Dict


class EmailGenerationRequest(BaseModel):
    lead: LeadInput
    email_type: str = "introduction"


class EmailResponse(BaseModel):
    subject: str
    body: str
    lead_score: float
    email_type: str
    generated_at: str


class ChatMessage(BaseModel):
    session_id: str
    message: str
    lead_context: Optional[Dict] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str


class ObjectionHandlingRequest(BaseModel):
    objection: str
    lead_context: Optional[Dict] = None


# API ENDPOINTS
@app.get("/")
async def root():
    return {
        "message": "🚀 AI Sales Assistant API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "docs": "/docs",
            "lead_scoring": "/api/leads/score",
            "email_generation": "/api/emails/generate",
            "chat_assistant": "/api/chat/message",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ml_model_loaded": scorer.is_trained,
        "grok_api_configured": bool(settings.GROQ_API_KEY)
    }


@app.post("/api/leads/score", response_model=LeadScoreResponse)
async def score_lead(lead: LeadInput):
    try:
        lead_dict = lead.dict()
        lead_dict['created_at'] = datetime.now()
        
        score = scorer.predict(lead_dict)
        insights = scorer.get_lead_insights(lead_dict)
        
        if score >= 0.7:
            quality = "HIGH"
            recommendation = "Contact immediately! High conversion probability."
        elif score >= 0.4:
            quality = "MEDIUM"
            recommendation = "Follow up within 24-48 hours."
        else:
            quality = "LOW"
            recommendation = "Add to long-term nurture sequence."
        
        return LeadScoreResponse(
            lead_score=score,
            score_percentage=score * 100,
            quality_level=quality,
            recommendation=recommendation,
            insights=insights
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring lead: {str(e)}")


@app.post("/api/leads/score-batch")
async def score_leads_batch(leads: List[LeadInput]):
    try:
        results = []
        for lead in leads:
            lead_dict = lead.dict()
            lead_dict['created_at'] = datetime.now()
            score = scorer.predict(lead_dict)
            
            results.append({
                "email": lead.email,
                "name": f"{lead.first_name} {lead.last_name or ''}".strip(),
                "score": score,
                "score_percentage": score * 100,
                "quality": "HIGH" if score >= 0.7 else "MEDIUM" if score >= 0.4 else "LOW"
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            "total_leads": len(results),
            "high_quality": len([r for r in results if r['score'] >= 0.7]),
            "medium_quality": len([r for r in results if 0.4 <= r['score'] < 0.7]),
            "low_quality": len([r for r in results if r['score'] < 0.4]),
            "leads": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch scoring: {str(e)}")


@app.post("/api/emails/generate", response_model=EmailResponse)
async def generate_email(request: EmailGenerationRequest):
    try:
        if not settings.GROQ_API_KEY:
            raise HTTPException(
                status_code=503,
                detail="Grok API key not configured. Set GROK_API_KEY in .env file."
            )
        
        lead_dict = request.lead.dict()
        lead_dict['created_at'] = datetime.now()
        
        email_data = email_service.generate_personalized_email(
            lead_info=lead_dict,
            email_type=request.email_type
        )
        
        return EmailResponse(**email_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")


@app.post("/api/emails/generate-batch")
async def generate_batch_emails(leads: List[LeadInput], email_type: str = "introduction"):
    try:
        if not settings.GROQ_API_KEY:
            raise HTTPException(status_code=503, detail="Grok API key not configured")
        
        leads_dict = [lead.dict() for lead in leads]
        emails = email_service.generate_batch_emails(leads_dict, email_type)
        
        return {
            "total_generated": len(emails),
            "email_type": email_type,
            "emails": emails
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating batch emails: {str(e)}")


@app.post("/api/chat/message", response_model=ChatResponse)
async def chat_message(chat: ChatMessage):
    try:
        if not settings.GROQ_API_KEY:
            raise HTTPException(status_code=503, detail="Grok API key not configured")
        
        response = chat_assistant.send_message(
            session_id=chat.session_id,
            message=chat.message
        )
        
        return ChatResponse(
            response=response,
            session_id=chat.session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


@app.post("/api/chat/objection")
async def handle_objection(request: ObjectionHandlingRequest):
    try:
        if not settings.GROQ_API_KEY:
            raise HTTPException(status_code=503, detail="Grok API key not configured")
        
        strategy = chat_assistant.handle_objection(
            objection=request.objection,
            lead_context=request.lead_context
        )
        
        return {
            "objection": request.objection,
            "strategy": strategy,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error handling objection: {str(e)}")


@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    history = chat_assistant.get_session_history(session_id)
    return {
        "session_id": session_id,
        "message_count": len(history),
        "messages": history
    }


@app.delete("/api/chat/session/{session_id}")
async def end_chat_session(session_id: str):
    chat_assistant.end_session(session_id)
    return {"message": f"Session {session_id} ended"}


@app.get("/api/analytics/model-info")
async def get_model_info():
    try:
        info = scorer.get_model_info()
        return {
            "model_info": info,
            "status": "operational" if scorer.is_trained else "not_loaded"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    print("")
    print("="*60)
    print("🚀 AI Sales Assistant API Starting...")
    print("="*60)
    print(f"App Name: {settings.APP_NAME}")
    print(f"Version: {settings.APP_VERSION}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"ML Model Loaded: {scorer.is_trained}")
    print(f"Grok API Configured: {bool(settings.GROQ_API_KEY)}")
    print("="*60)
    print("📚 API Documentation: http://localhost:8000/docs")
    print("="*60)
    print("")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

