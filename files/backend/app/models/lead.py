"""
Lead Database Model
Stores all lead information including features for ML scoring
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database.connection import Base
import enum


class LeadStatus(str, enum.Enum):
    """Lead status enumeration"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadSource(str, enum.Enum):
    """Where the lead came from"""
    WEBSITE = "website"
    REFERRAL = "referral"
    LINKEDIN = "linkedin"
    COLD_OUTREACH = "cold_outreach"
    ADVERTISEMENT = "advertisement"
    EVENT = "event"
    OTHER = "other"


class Lead(Base):
    """
    Lead Model - stores all information about sales leads
    This is what our ML model will use for scoring!
    """
    __tablename__ = "leads"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    
    # Company Information (important for scoring!)
    company_name = Column(String(255), nullable=True)
    company_size = Column(String(50), nullable=True)  # "1-10", "11-50", "51-200", etc.
    industry = Column(String(100), nullable=True)
    job_title = Column(String(150), nullable=True)
    department = Column(String(100), nullable=True)
    
    # Lead Source & Context
    source = Column(Enum(LeadSource), default=LeadSource.WEBSITE)
    utm_campaign = Column(String(255), nullable=True)
    utm_source = Column(String(255), nullable=True)
    utm_medium = Column(String(255), nullable=True)
    
    # Engagement Metrics (KEY FEATURES for ML!)
    website_visits = Column(Integer, default=0)
    pages_viewed = Column(Integer, default=0)
    time_on_site = Column(Integer, default=0)  # seconds
    email_opens = Column(Integer, default=0)
    email_clicks = Column(Integer, default=0)
    form_submissions = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    
    # Social Media Engagement
    linkedin_profile = Column(String(255), nullable=True)
    linkedin_connections = Column(Integer, default=0)
    
    # Budget & Timeline (if collected)
    estimated_budget = Column(Float, nullable=True)
    timeline = Column(String(50), nullable=True)  # "immediate", "1-3 months", "3-6 months"
    
    # Lead Status & Scoring
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    lead_score = Column(Float, default=0.0)  # ML model prediction (0-1)
    is_qualified = Column(Boolean, default=False)
    
    # Conversion
    converted = Column(Boolean, default=False)
    conversion_date = Column(DateTime, nullable=True)
    deal_value = Column(Float, nullable=True)
    
    # Notes & History
    notes = Column(Text, nullable=True)
    last_contact_date = Column(DateTime, nullable=True)
    next_follow_up = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Lead {self.first_name} {self.last_name} ({self.email}) - Score: {self.lead_score}>"
    
    @property
    def full_name(self):
        """Get full name of lead"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def engagement_score(self):
        """Calculate total engagement score"""
        return (
            self.website_visits * 2 +
            self.pages_viewed +
            self.email_opens * 3 +
            self.email_clicks * 5 +
            self.form_submissions * 10 +
            self.downloads * 8
        )
