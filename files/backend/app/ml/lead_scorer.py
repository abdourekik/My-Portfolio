"""
Lead Scoring Machine Learning Model
THIS IS YOUR TRAINED AI MODEL - NOT AN EXTERNAL API!

Train your own model to predict lead conversion probability
"""
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score, precision_recall_curve
from xgboost import XGBClassifier
import os
from datetime import datetime
from typing import Dict, List, Tuple
from app.ml.feature_engineering import LeadFeatureEngineer
from app.config import settings


class LeadScorer:
    """
    Lead Scoring ML Model
    Predicts probability of lead conversion (0-1)
    
    YOU TRAIN THIS MODEL - it's YOUR AI!
    """
    
    def __init__(self, model_type: str = "xgboost"):
        """
        Initialize the lead scorer
        
        Args:
            model_type: "random_forest", "gradient_boosting", or "xgboost"
        """
        self.model_type = model_type
        self.model = None
        self.feature_engineer = LeadFeatureEngineer()
        self.is_trained = False
        self.training_date = None
        self.feature_importance = None
        self.model_metrics = {}
        
        # Initialize model based on type
        if model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                class_weight='balanced'
            )
        elif model_type == "gradient_boosting":
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        else:  # xgboost (recommended!)
            self.model = XGBClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                min_child_weight=1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                scale_pos_weight=1
            )
    
    def train(self, leads_df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """
        Train the lead scoring model
        
        THIS IS WHERE YOU TRAIN YOUR OWN AI MODEL!
        
        Args:
            leads_df: DataFrame with historical lead data
            test_size: Fraction of data to use for testing
            
        Returns:
            Dictionary with training metrics
        """
        print(f"\n{'='*60}")
        print(f"🎯 TRAINING YOUR LEAD SCORING MODEL")
        print(f"{'='*60}\n")
        
        # Prepare training data
        print("📊 Engineering features from lead data...")
        X, y = self.feature_engineer.prepare_training_data(leads_df)
        
        print(f"✓ Features engineered: {X.shape[1]} features")
        print(f"✓ Training samples: {len(X)}")
        print(f"✓ Positive samples (converted): {y.sum()} ({y.mean()*100:.1f}%)")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"\n🔄 Training {self.model_type} model...")
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        print("\n📈 Evaluating model performance...")
        
        # Training score
        train_score = self.model.score(X_train, y_train)
        print(f"✓ Training Accuracy: {train_score*100:.2f}%")
        
        # Test score
        test_score = self.model.score(X_test, y_test)
        print(f"✓ Test Accuracy: {test_score*100:.2f}%")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # ROC AUC (important metric for imbalanced data)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        print(f"✓ ROC AUC Score: {roc_auc:.3f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        print(f"✓ Cross-validation Score: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\n📊 Top 5 Most Important Features:")
            for idx, row in self.feature_importance.head().iterrows():
                print(f"   {row['feature']:30s} {row['importance']:.3f}")
        
        # Store metrics
        self.model_metrics = {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'roc_auc': roc_auc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'positive_rate': y.mean()
        }
        
        # Mark as trained
        self.is_trained = True
        self.training_date = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"✅ MODEL TRAINING COMPLETE!")
        print(f"{'='*60}\n")
        
        return self.model_metrics
    
    def predict(self, lead_data: Dict) -> float:
        """
        Predict conversion probability for a single lead
        
        Args:
            lead_data: Dictionary with lead information
            
        Returns:
            Probability of conversion (0-1)
        """
        if not self.is_trained:
            raise ValueError("Model not trained! Call train() first.")
        
        # Engineer features
        features = self.feature_engineer.engineer_features(lead_data)
        
        # Convert to DataFrame with correct column order
        feature_names = self.feature_engineer.get_feature_names()
        X = pd.DataFrame([features])[feature_names]
        
        # Predict probability
        probability = self.model.predict_proba(X)[0, 1]
        
        return float(probability)
    
    def predict_batch(self, leads_list: List[Dict]) -> List[float]:
        """
        Predict conversion probability for multiple leads
        
        Args:
            leads_list: List of lead dictionaries
            
        Returns:
            List of probabilities
        """
        if not self.is_trained:
            raise ValueError("Model not trained! Call train() first.")
        
        # Engineer features for all leads
        features_list = [
            self.feature_engineer.engineer_features(lead)
            for lead in leads_list
        ]
        
        # Convert to DataFrame
        feature_names = self.feature_engineer.get_feature_names()
        X = pd.DataFrame(features_list)[feature_names]
        
        # Predict
        probabilities = self.model.predict_proba(X)[:, 1]
        
        return probabilities.tolist()
    
    def get_lead_insights(self, lead_data: Dict) -> Dict:
        """
        Get detailed insights about why a lead got its score
        
        Args:
            lead_data: Dictionary with lead information
            
        Returns:
            Dictionary with score and feature contributions
        """
        # Get prediction
        score = self.predict(lead_data)
        
        # Get features
        features = self.feature_engineer.engineer_features(lead_data)
        
        # Combine with importance
        insights = {
            'lead_score': score,
            'is_high_quality': score >= settings.LEAD_SCORE_THRESHOLD,
            'features': features
        }
        
        if self.feature_importance is not None:
            # Show which features contributed most
            feature_contributions = []
            for _, row in self.feature_importance.head(5).iterrows():
                feature_name = row['feature']
                if feature_name in features:
                    feature_contributions.append({
                        'feature': feature_name,
                        'value': features[feature_name],
                        'importance': row['importance']
                    })
            insights['top_contributors'] = feature_contributions
        
        return insights
    
    def save_model(self, filepath: str = None):
        """
        Save trained model to disk
        
        Args:
            filepath: Path to save model (default: MODEL_PATH/lead_scorer.pkl)
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model!")
        
        if filepath is None:
            filepath = os.path.join(settings.MODEL_PATH, "lead_scorer.pkl")
        
        # Save model and metadata
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'training_date': self.training_date,
            'feature_importance': self.feature_importance,
            'metrics': self.model_metrics,
            'feature_engineer': self.feature_engineer
        }
        
        joblib.dump(model_data, filepath)
        print(f"✅ Model saved to: {filepath}")
    
    def load_model(self, filepath: str = None):
        """
        Load trained model from disk
        
        Args:
            filepath: Path to model file (default: MODEL_PATH/lead_scorer.pkl)
        """
        if filepath is None:
            filepath = os.path.join(settings.MODEL_PATH, "lead_scorer.pkl")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        # Load model data
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.training_date = model_data['training_date']
        self.feature_importance = model_data.get('feature_importance')
        self.model_metrics = model_data.get('metrics', {})
        self.feature_engineer = model_data.get('feature_engineer', LeadFeatureEngineer())
        self.is_trained = True
        
        print(f"✅ Model loaded from: {filepath}")
        print(f"   Trained on: {self.training_date}")
        print(f"   Test accuracy: {self.model_metrics.get('test_accuracy', 'N/A')}")
    
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        return {
            'is_trained': self.is_trained,
            'model_type': self.model_type,
            'training_date': self.training_date.isoformat() if self.training_date else None,
            'metrics': self.model_metrics,
            'feature_count': len(self.feature_engineer.get_feature_names())
        }
