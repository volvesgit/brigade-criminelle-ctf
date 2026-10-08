#!/usr/bin/env python3
"""
Test pour vérifier que les réponses sont naturelles et variées
"""

import requests
import json

def test_natural_responses():
    """Test des réponses naturelles et variées"""
    url = 'https://backend-production-0c4b.up.railway.app/api/chat'
    session_id = 'test_session_123'

    messages = [
        'Bonjour',
        'non', 
        'je vais donner',
        'non pas maintenant',
        'attendez'
    ]

    print("=== TEST DES RÉPONSES NATURELLES ===\n")
    
    for i, msg in enumerate(messages):
        print(f'🔹 Message {i+1}: "{msg}"')
        try:
            response = requests.post(url, json={'message': msg, 'session_id': session_id})
            if response.status_code == 200:
                data = response.json()
                print(f'✅ Réponse: {data["response"][:150]}...\n')
            else:
                print(f'❌ Erreur: {response.status_code}\n')
        except Exception as e:
            print(f'❌ Exception: {e}\n')

if __name__ == "__main__":
    test_natural_responses()
