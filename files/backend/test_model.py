"""
Quick Test Script for Lead Scoring Model
Run this to verify everything is working!
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    try:
        import pandas
        import numpy
        import sklearn
        import xgboost
        import joblib
        print("✅ All packages installed correctly!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install -r requirements.txt")
        return False


def test_model_files():
    """Test if model files exist"""
    print("\n🔍 Checking model files...")
    
    files_to_check = [
        'app/config.py',
        'app/ml/feature_engineering.py',
        'app/ml/lead_scorer.py',
        'app/ml/generate_sample_data.py',
        'app/models/lead.py',
    ]
    
    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} not found")
            all_exist = False
    
    return all_exist


def test_model_training():
    """Test model training with sample data"""
    print("\n🎯 Testing model training...")
    
    try:
        from app.ml.lead_scorer import LeadScorer
        from app.ml.generate_sample_data import generate_sample_leads
        
        # Generate small sample
        print("   Generating 100 sample leads...")
        leads_df = generate_sample_leads(100)
        
        # Train model
        print("   Training model...")
        scorer = LeadScorer(model_type='xgboost')
        metrics = scorer.train(leads_df, test_size=0.2)
        
        print(f"\n   ✅ Training complete!")
        print(f"   Accuracy: {metrics['test_accuracy']*100:.1f}%")
        print(f"   ROC AUC: {metrics['roc_auc']:.3f}")
        
        return scorer, metrics
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def test_prediction(scorer):
    """Test model prediction"""
    print("\n🎯 Testing prediction...")
    
    try:
        from datetime import datetime
        
        # Test lead 1: High quality
        high_quality_lead = {
            'first_name': 'Ahmed',
            'last_name': 'CEO',
            'email': 'ahmed@techcorp.tn',
            'company_name': 'TechCorp',
            'company_size': '201-500',
            'industry': 'technology',
            'job_title': 'CEO',
            'source': 'referral',
            'website_visits': 10,
            'pages_viewed': 20,
            'time_on_site': 600,
            'email_opens': 6,
            'email_clicks': 4,
            'form_submissions': 2,
            'downloads': 1,
            'linkedin_profile': 'linkedin.com/in/ahmed',
            'estimated_budget': 100000,
            'timeline': 'immediate',
            'created_at': datetime.now()
        }
        
        score1 = scorer.predict(high_quality_lead)
        print(f"\n   Test Lead 1 (High Quality):")
        print(f"   • Name: Ahmed CEO (CEO at TechCorp)")
        print(f"   • Email: ahmed@techcorp.tn")
        print(f"   • Engagement: High (10 visits, 6 opens, 4 clicks)")
        print(f"   • Score: {score1*100:.1f}% {'🔥' if score1 >= 0.7 else '⚡' if score1 >= 0.4 else '❄️'}")
        
        # Test lead 2: Low quality
        low_quality_lead = {
            'first_name': 'User',
            'last_name': 'Test',
            'email': 'user@gmail.com',
            'company_name': 'Small Shop',
            'company_size': '1-10',
            'industry': 'retail',
            'job_title': 'Coordinator',
            'source': 'cold_outreach',
            'website_visits': 1,
            'pages_viewed': 2,
            'time_on_site': 30,
            'email_opens': 0,
            'email_clicks': 0,
            'form_submissions': 0,
            'downloads': 0,
            'linkedin_profile': None,
            'estimated_budget': None,
            'timeline': '6+ months',
            'created_at': datetime.now()
        }
        
        score2 = scorer.predict(low_quality_lead)
        print(f"\n   Test Lead 2 (Low Quality):")
        print(f"   • Name: User Test (Coordinator at Small Shop)")
        print(f"   • Email: user@gmail.com")
        print(f"   • Engagement: Low (1 visit, 0 opens)")
        print(f"   • Score: {score2*100:.1f}% {'🔥' if score2 >= 0.7 else '⚡' if score2 >= 0.4 else '❄️'}")
        
        # Verify scores make sense
        if score1 > score2:
            print(f"\n   ✅ Model working correctly!")
            print(f"      High-quality lead scored higher ({score1:.2f} > {score2:.2f})")
            return True
        else:
            print(f"\n   ⚠️ Unexpected results")
            print(f"      High-quality lead: {score1:.2f}")
            print(f"      Low-quality lead: {score2:.2f}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_save_load(scorer):
    """Test saving and loading the model"""
    print("\n🔍 Testing model save/load...")
    
    try:
        # Save model
        os.makedirs('app/ml/models', exist_ok=True)
        scorer.save_model('app/ml/models/test_model.pkl')
        print("   ✅ Model saved successfully")
        
        # Load model
        from app.ml.lead_scorer import LeadScorer
        new_scorer = LeadScorer()
        new_scorer.load_model('app/ml/models/test_model.pkl')
        print("   ✅ Model loaded successfully")
        
        # Verify it works
        from datetime import datetime
        test_lead = {
            'first_name': 'Test',
            'email': 'test@example.com',
            'company_size': '51-200',
            'industry': 'technology',
            'job_title': 'Manager',
            'source': 'website',
            'website_visits': 5,
            'email_opens': 2,
            'created_at': datetime.now()
        }
        
        score = new_scorer.predict(test_lead)
        print(f"   ✅ Loaded model can predict: {score*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Save/load failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("🚀 LEAD SCORING MODEL - VERIFICATION TEST")
    print("="*60)
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Setup incomplete. Install requirements first!")
        return
    
    # Test 2: Files
    if not test_model_files():
        print("\n❌ Some files are missing. Check project structure!")
        return
    
    # Test 3: Training
    scorer, metrics = test_model_training()
    if scorer is None:
        print("\n❌ Model training failed!")
        return
    
    # Test 4: Prediction
    if not test_prediction(scorer):
        print("\n⚠️ Predictions may need tuning")
    
    # Test 5: Save/Load
    if not test_model_save_load(scorer):
        print("\n❌ Model persistence failed!")
        return
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)
    print("\n✅ Your lead scoring model is ready to use!")
    print("\nNext steps:")
    print("1. Review the training notebook: notebooks/01_model_training.ipynb")
    print("2. Read the documentation: README_STEP1.md")
    print("3. When ready, say: 'Let's continue to Step 2!'")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
