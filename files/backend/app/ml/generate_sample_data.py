"""
Sample Lead Data Generator
Creates realistic training data for the ML model
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_sample_leads(n_samples: int = 500) -> pd.DataFrame:
    """
    Generate sample lead data for training
    Mix of converted and non-converted leads
    
    Args:
        n_samples: Number of leads to generate
        
    Returns:
        DataFrame with sample lead data
    """
    np.random.seed(42)
    random.seed(42)
    
    leads = []
    
    # Sample data pools
    first_names = ["Ahmed", "Sarah", "Mohamed", "Fatima", "Karim", "Leila", "Youssef", "Amira",
                   "John", "Emma", "Michael", "Sophie", "David", "Lisa", "James", "Maria"]
    
    last_names = ["Ben Ali", "Trabelsi", "Mansour", "Saidi", "Cherif", "Hamdi", "Lakhal",
                  "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Martinez"]
    
    companies = ["TechCorp", "InnovateSoft", "DataSystems", "CloudWorks", "FinanceHub",
                "RetailPro", "HealthCare Plus", "EduTech", "ManufactureX", "StartupLab"]
    
    industries = ["technology", "finance", "healthcare", "manufacturing", "retail", 
                 "education", "government", "other"]
    
    job_titles = ["CEO", "CTO", "VP Sales", "Director", "Manager", "Engineer", 
                 "Analyst", "Consultant", "Coordinator", "Specialist"]
    
    sources = ["website", "referral", "linkedin", "cold_outreach", "advertisement", "event"]
    
    company_sizes = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"]
    
    timelines = ["immediate", "1-3 months", "3-6 months", "6+ months"]
    
    for i in range(n_samples):
        # Basic info
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        company = random.choice(companies) + f" {random.randint(1, 100)}"
        industry = random.choice(industries)
        job_title = random.choice(job_titles)
        source = random.choice(sources)
        company_size = random.choice(company_sizes)
        timeline = random.choice(timelines)
        
        # Email (business email more likely for senior positions)
        is_senior = job_title in ["CEO", "CTO", "VP Sales", "Director"]
        if is_senior and random.random() > 0.3:
            email = f"{first_name.lower()}.{last_name.lower()}@{company.lower().replace(' ', '')}.com"
        else:
            domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", 
                                   company.lower().replace(' ', '') + ".com"])
            email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
        
        # Engagement metrics (correlated with quality indicators)
        base_quality = (
            0.5 +  # base
            (0.3 if is_senior else 0) +
            (0.2 if source in ["referral", "linkedin"] else 0) +
            (0.2 if industry in ["technology", "finance"] else 0) +
            (0.1 if "@gmail" not in email and "@yahoo" not in email else -0.1)
        )
        base_quality = max(0.1, min(1.0, base_quality))
        
        # Add randomness
        quality_factor = base_quality * random.uniform(0.7, 1.3)
        
        website_visits = int(np.random.poisson(quality_factor * 5))
        pages_viewed = int(np.random.poisson(quality_factor * 10))
        time_on_site = int(np.random.poisson(quality_factor * 300))
        email_opens = int(np.random.poisson(quality_factor * 3))
        email_clicks = int(np.random.poisson(quality_factor * 2))
        form_submissions = int(np.random.poisson(quality_factor * 1))
        downloads = int(np.random.poisson(quality_factor * 1))
        
        # Budget (higher for senior roles and larger companies)
        if is_senior and company_size in ["501-1000", "1000+"]:
            estimated_budget = random.randint(50000, 500000) if random.random() > 0.3 else None
        elif is_senior:
            estimated_budget = random.randint(10000, 100000) if random.random() > 0.4 else None
        else:
            estimated_budget = random.randint(5000, 50000) if random.random() > 0.6 else None
        
        # LinkedIn (more likely for professionals)
        has_linkedin = random.random() < (0.9 if is_senior else 0.5)
        linkedin_profile = f"linkedin.com/in/{first_name.lower()}-{last_name.lower()}" if has_linkedin else None
        
        # Created date (within last 90 days)
        created_at = datetime.now() - timedelta(days=random.randint(0, 90))
        
        # Conversion probability based on quality factors
        conversion_probability = (
            base_quality * 0.4 +
            min(website_visits / 10, 1) * 0.1 +
            min(email_opens / 5, 1) * 0.15 +
            min(email_clicks / 3, 1) * 0.2 +
            (0.1 if estimated_budget else 0) +
            (0.05 if timeline == "immediate" else 0)
        )
        
        # Add noise and decide conversion
        conversion_probability = max(0, min(1, conversion_probability + random.uniform(-0.2, 0.2)))
        converted = random.random() < conversion_probability
        
        # Deal value for converted leads
        deal_value = None
        conversion_date = None
        if converted:
            base_deal = estimated_budget if estimated_budget else 20000
            deal_value = base_deal * random.uniform(0.5, 1.5)
            conversion_date = created_at + timedelta(days=random.randint(7, 60))
        
        lead = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': f"+216 {random.randint(20, 99)} {random.randint(100, 999)} {random.randint(100, 999)}",
            'company_name': company,
            'company_size': company_size,
            'industry': industry,
            'job_title': job_title,
            'department': random.choice(["Sales", "Marketing", "IT", "Operations", "Finance"]),
            'source': source,
            'website_visits': website_visits,
            'pages_viewed': pages_viewed,
            'time_on_site': time_on_site,
            'email_opens': email_opens,
            'email_clicks': email_clicks,
            'form_submissions': form_submissions,
            'downloads': downloads,
            'linkedin_profile': linkedin_profile,
            'estimated_budget': estimated_budget,
            'timeline': timeline,
            'status': 'won' if converted else random.choice(['new', 'contacted', 'qualified']),
            'converted': converted,
            'deal_value': deal_value,
            'conversion_date': conversion_date,
            'created_at': created_at,
            'notes': f"Lead from {source}. {job_title} at {company}."
        }
        
        leads.append(lead)
    
    df = pd.DataFrame(leads)
    
    print(f"✅ Generated {n_samples} sample leads")
    print(f"   Converted: {df['converted'].sum()} ({df['converted'].mean()*100:.1f}%)")
    print(f"   Sources: {df['source'].value_counts().to_dict()}")
    
    return df


if __name__ == "__main__":
    # Generate and save sample data
    df = generate_sample_leads(500)
    df.to_csv("../../data/raw/sample_leads.csv", index=False)
    print("\n✅ Saved to: data/raw/sample_leads.csv")
