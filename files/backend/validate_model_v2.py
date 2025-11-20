from app.ml.lead_scorer import LeadScorer
from datetime import datetime

scorer = LeadScorer()
scorer.load_model('app/ml/models/lead_scorer.pkl')

print('\n' + '='*70)
print('🧪 VALIDATION DU NOUVEAU MODÈLE')
print('='*70)

# Test 1: Leads extrêmes
excellent = {
    'email': 'ceo@bigtech.com', 'company_size': '1000+',
    'industry': 'technology', 'job_title': 'CEO',
    'website_visits': 15, 'email_opens': 10, 'email_clicks': 8,
    'estimated_budget': 500000, 'timeline': 'immediate',
    'source': 'referral', 'created_at': datetime.now()
}

mauvais = {
    'email': 'user@gmail.com', 'company_size': '1-10',
    'industry': 'other', 'job_title': 'Stagiaire',
    'website_visits': 1, 'email_opens': 0, 'email_clicks': 0,
    'estimated_budget': None, 'timeline': '6+ months',
    'source': 'cold_outreach', 'created_at': datetime.now()
}

s_excellent = scorer.predict(excellent)
s_mauvais = scorer.predict(mauvais)

print(f'\n✅ Lead Excellent: {s_excellent*100:.1f}%')
print(f'❌ Lead Mauvais:   {s_mauvais*100:.1f}%')
print(f'Différence:        {(s_excellent - s_mauvais)*100:.1f} points')

# Le test le plus important: Excellent > Mauvais
print('\n' + '='*70)
if s_excellent > s_mauvais:
    diff = (s_excellent - s_mauvais) * 100
    print(f'✅ SUCCÈS! Le modèle distingue bien les leads')
    print(f'   Différence de {diff:.1f} points')
    
    if diff > 40:
        print('   🔥 Excellente séparation!')
    elif diff > 20:
        print('   ✅ Bonne séparation')
    else:
        print('   ⚠️ Séparation faible mais correcte')
else:
    print('❌ PROBLÈME: Le mauvais lead score plus haut!')

print('='*70)

# Info du modèle
info = scorer.get_model_info()
model_type = info['model_type']
test_acc = info['metrics'].get('test_accuracy', 0) * 100
roc_auc = info['metrics'].get('roc_auc', 0)

print('\n📊 Info du Modèle:')
print(f'   Type: {model_type}')
print(f'   Précision test: {test_acc:.1f}%')
print(f'   ROC AUC: {roc_auc:.3f}')
print('='*70)
