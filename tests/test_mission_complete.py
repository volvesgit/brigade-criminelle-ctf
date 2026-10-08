#!/usr/bin/env python3
"""
Test complet de la mission pour voir l'affichage MISSION VALIDÉE
"""

import requests
import json

def test_complete_mission():
    """Test du flow complet jusqu'au flag"""
      # URL du backend en production
    backend_url = "https://backend-production-0c4b.up.railway.app"
    
    print("=== TEST MISSION COMPLÈTE ===\n")
    
    # 1. Démarrer l'appel
    print("📞 1. Démarrage de l'appel...")
    start_response = requests.post(f"{backend_url}/api/start-call")
    if start_response.status_code == 200:
        session_id = start_response.json().get('session_id')
        print(f"✅ Session créée: {session_id}\n")
    else:
        print("❌ Erreur démarrage appel")
        return
    
    # 2. Envoyer la description
    print("🔍 2. Envoi de la description physique...")
    desc_response = requests.post(f"{backend_url}/api/chat", json={
        "message": "Golf est une personne grande, chauve, avec une barbe rasée et la peau mate",
        "session_id": session_id
    })
    print(f"Réponse: {desc_response.json()['response'][:100]}...\n")
    
    # 3. Envoyer les coordonnées
    print("🗺️ 3. Envoi des coordonnées GPS...")
    coord_response = requests.post(f"{backend_url}/api/chat", json={
        "message": "Les coordonnées GPS sont : 43.21011503262918, 5.449606424661931",
        "session_id": session_id
    })
    print(f"Réponse: {coord_response.json()['response'][:100]}...\n")
    
    # 4. Envoyer les hobbies pour obtenir le flag
    print("🎣 4. Envoi des hobbies pour déclencher MISSION VALIDÉE...")
    hobbies_response = requests.post(f"{backend_url}/api/chat", json={
        "message": "Alors Jules aime la pêche, la plongée et les randonnées au lever du soleil",
        "session_id": session_id
    })
    
    result = hobbies_response.json()
    print(f"Flag trouvé: {result['flag_found']}")
    print(f"Réponse complète:")
    print("=" * 50)
    print(result['response'])
    print("=" * 50)
    
    if result['flag_found']:
        print("\n🎉 SUCCESS! MISSION VALIDÉE est affiché!")
    else:
        print("\n❌ Le flag n'a pas été détecté...")

if __name__ == "__main__":
    test_complete_mission()
