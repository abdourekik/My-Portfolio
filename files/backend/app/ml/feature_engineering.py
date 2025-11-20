"""
Feature Engineering for Lead Scoring Model
Transforms raw lead data into ML features
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime


class LeadFeatureEngineer:
    """
    Engineers features from raw lead data for ML model
    This is crucial for good model performance!
    """
    
    def __init__(self):
        # Company size mapping to numerical values
        self.company_size_map = {
            "1-10": 1,
            "11-50": 2,
            "51-200": 3,
            "201-500": 4,
            "501-1000": 5,
            "1000+": 6,
            None: 0
        }
        
        # Industry scoring (some industries convert better)
        self.industry_scores = {
            "technology": 0.9,
            "finance": 0.85,
            "healthcare": 0.8,
            "manufacturing": 0.75,
            "retail": 0.7,
            "education": 0.65,
            "government": 0.6,
            "other": 0.5
        }
        
        # Lead source quality
        self.source_scores = {
            "referral": 0.95,
            "linkedin": 0.85,
            "website": 0.75,
            "event": 0.7,
            "advertisement": 0.6,
            "cold_outreach": 0.5,
            "other": 0.4
        }
        
        # Timeline urgency
        self.timeline_scores = {
            "immediate": 1.0,
            "1-3 months": 0.8,
            "3-6 months": 0.6,
            "6+ months": 0.3,
            None: 0.5
        }
    
    def extract_email_features(self, email: str) -> Dict[str, float]:
        """
        Extract features from email domain
        Business emails are better quality than generic ones
        """
        if not email:
            return {"email_domain_quality": 0.0, "is_business_email": 0.0}
        
        generic_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"]
        domain = email.split("@")[1].lower() if "@" in email else ""
        
        is_business = 0.0 if domain in generic_domains else 1.0
        domain_quality = 0.3 if domain in generic_domains else 0.9
        
        return {
            "email_domain_quality": domain_quality,
            "is_business_email": is_business
        }
    
    def calculate_engagement_score(self, lead_data: Dict) -> float:
        """
        Calculate overall engagement score from various metrics
        Higher engagement = higher conversion probability
        """
        score = 0.0
        
        # Website engagement (normalized)
        score += min(lead_data.get("website_visits", 0) / 10, 1.0) * 15
        score += min(lead_data.get("pages_viewed", 0) / 20, 1.0) * 10
        score += min(lead_data.get("time_on_site", 0) / 600, 1.0) * 10  # 10 mins max
        
        # Email engagement (very important!)
        score += min(lead_data.get("email_opens", 0) / 5, 1.0) * 20
        score += min(lead_data.get("email_clicks", 0) / 3, 1.0) * 25
        
        # Action-based engagement (highest value)
        score += min(lead_data.get("form_submissions", 0) / 3, 1.0) * 15
        score += min(lead_data.get("downloads", 0) / 2, 1.0) * 5
        
        return min(score, 100) / 100  # Normalize to 0-1
    
    def calculate_recency_score(self, created_at: datetime, last_contact: datetime = None) -> float:
        """
        Recent leads are more valuable
        Leads that haven't been contacted recently need attention
        """
        now = datetime.now()
        days_since_creation = (now - created_at).days if created_at else 365
        
        # Newer leads are better (decay over time)
        recency = 1.0 / (1 + days_since_creation / 30)  # 30-day half-life
        
        return recency
    
    def engineer_features(self, lead_data: Dict) -> Dict[str, float]:
        """
        Main feature engineering function
        Converts raw lead data into ML-ready features
        
        Args:
            lead_data: Dictionary with lead information
            
        Returns:
            Dictionary of engineered features for ML model
        """
        features = {}
        
        # Company features
        features["company_size_score"] = self.company_size_map.get(
            lead_data.get("company_size"), 0
        ) / 6  # Normalize
        
        features["industry_score"] = self.industry_scores.get(
            lead_data.get("industry", "").lower(), 0.5
        )
        
        # Source quality
        features["source_quality"] = self.source_scores.get(
            lead_data.get("source", "other").lower(), 0.5
        )
        
        # Email features
        email_features = self.extract_email_features(lead_data.get("email", ""))
        features.update(email_features)
        
        # Engagement score (MOST IMPORTANT!)
        features["engagement_score"] = self.calculate_engagement_score(lead_data)
        
        # Budget indicator
        budget = lead_data.get("estimated_budget", 0) or 0
        features["has_budget"] = 1.0 if budget > 0 else 0.0
        features["budget_score"] = min(budget / 100000, 1.0) if budget > 0 else 0.5
        
        # Timeline urgency
        features["timeline_score"] = self.timeline_scores.get(
            lead_data.get("timeline"), 0.5
        )
        
        # Job title seniority (decision makers convert better)
        job_title = lead_data.get("job_title", "").lower()
        senior_titles = ["ceo", "cto", "cfo", "vp", "director", "president", "owner", "founder"]
        features["is_decision_maker"] = 1.0 if any(title in job_title for title in senior_titles) else 0.0
        
        # Recency
        created_at = lead_data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        features["recency_score"] = self.calculate_recency_score(created_at)
        
        # LinkedIn presence (professional indicator)
        features["has_linkedin"] = 1.0 if lead_data.get("linkedin_profile") else 0.0
        
        # Form completeness (more complete = more serious)
        total_fields = 15
        filled_fields = sum([
            1 for field in ["first_name", "last_name", "email", "phone", "company_name", 
                          "company_size", "industry", "job_title", "department",
                          "estimated_budget", "timeline", "linkedin_profile"]
            if lead_data.get(field)
        ])
        features["profile_completeness"] = filled_fields / total_fields
        
        return features
    
    def prepare_training_data(self, leads_df: pd.DataFrame) -> tuple:
        """
        Prepare data for model training
        
        Args:
            leads_df: DataFrame with lead data
            
        Returns:
            X (features), y (labels)
        """
        # Engineer features for all leads
        features_list = []
        for _, lead in leads_df.iterrows():
            lead_dict = lead.to_dict()
            features = self.engineer_features(lead_dict)
            features_list.append(features)
        
        X = pd.DataFrame(features_list)
        
        # Target: did the lead convert?
        y = leads_df["converted"].astype(int)
        
        return X, y
    
    def get_feature_names(self) -> List[str]:
        """Get list of all feature names"""
        return [
            "company_size_score",
            "industry_score",
            "source_quality",
            "email_domain_quality",
            "is_business_email",
            "engagement_score",
            "has_budget",
            "budget_score",
            "timeline_score",
            "is_decision_maker",
            "recency_score",
            "has_linkedin",
            "profile_completeness"
        ]
