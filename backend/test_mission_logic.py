#!/usr/bin/env python3
"""
Script de test pour vérifier les corrections de l'AI Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_agent import AIAgent

def test_mission_steps():
    """Test des étapes de mission"""
    agent = AIAgent()
    
    print("=== TEST DE LA LOGIQUE DE MISSION ===\n")
    
    # Test 1: Description physique
    print("🔍 Test 1: Description physique")
    response1 = agent.generate_response("personne grande chauve barbe rasé et matte de peau")
    print(f"Description détectée: {agent.mission_steps['description_provided']}")
    print(f"Réponse: {response1['response'][:100]}...\n")
    
    # Test 2: Coordonnées GPS
    print("🗺️ Test 2: Coordonnées GPS")
    response2 = agent.generate_response("les cordonne gps sont : 43.21011503262918, 5.449606424661931")
    print(f"Coordonnées détectées: {agent.mission_steps['coordinates_provided']}")
    print(f"Rapport de terrain: {agent.mission_steps['field_report_given']}")
    print(f"Réponse: {response2['response'][:100]}...\n")
    
    # Test 3: État final de la mission
    print("📊 État final de la mission:")
    for step, completed in agent.mission_steps.items():
        status = "✅" if completed else "❌"
        print(f"  {status} {step}: {completed}")
    
    print(f"\n🎯 Mission prête pour la phase hobbies: {agent.mission_steps['field_report_given']}")
    
    # Test 4: Détection des hobbies
    print("\n🎣 Test 4: Détection des hobbies")
    hobbies_text = "il aime la pêche, la plongée et les randonnées au lever du soleil"
    hobbies_found, detected = agent.detect_hobbies(hobbies_text)
    print(f"Hobbies détectés: {detected}")
    print(f"Flag trouvé: {hobbies_found}")
    
    if hobbies_found:
        response3 = agent.generate_response(hobbies_text)
        print(f"Flag found dans réponse: {response3['flag_found']}")

if __name__ == "__main__":
    test_mission_steps()
