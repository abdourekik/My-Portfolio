from app.ml.lead_scorer import LeadScorer
from datetime import datetime

scorer = LeadScorer()
scorer.load_model('app/ml/models/test_model.pkl')

print('\n' + '='*70)
print('🧪 VALIDATION COMPLÈTE DU MODÈLE ML')
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

# Validation
tests_passed = 0
total_tests = 4

if s_excellent > 0.7:
    print('\n✅ Test 1: Lead excellent > 70%')
    tests_passed += 1
else:
    print('\n❌ Test 1: Lead excellent devrait être > 70%')

if s_mauvais < 0.4:
    print('✅ Test 2: Lead mauvais < 40%')
    tests_passed += 1
else:
    print('❌ Test 2: Lead mauvais devrait être < 40%')

if s_excellent > s_mauvais:
    print('✅ Test 3: Excellent > Mauvais')
    tests_passed += 1
else:
    print('❌ Test 3: Excellent devrait être > Mauvais')

if (s_excellent - s_mauvais) > 0.4:
    print('✅ Test 4: Différence > 40 points')
    tests_passed += 1
else:
    print('❌ Test 4: Différence devrait être > 40 points')

print('\n' + '='*70)
print(f'RÉSULTAT: {tests_passed}/{total_tests} tests passés')

if tests_passed == total_tests:
    print('🎉 PARFAIT! Votre modèle fonctionne correctement!')
elif tests_passed >= 3:
    print('✅ BON! Votre modèle fonctionne bien')
elif tests_passed >= 2:
    print('⚠️ ACCEPTABLE! Quelques ajustements nécessaires')
else:
    print('❌ PROBLÈME! Le modèle doit être réentraîné')

print('='*70)
