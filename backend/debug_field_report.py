#!/usr/bin/env python3
"""
Script de debug pour tester spécifiquement la génération du rapport de terrain
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_agent import AIAgent

def debug_field_report():
    print("=== DEBUG RAPPORT DE TERRAIN ===")
    
    # Créer une instance d'agent
    agent = AIAgent()
    
    print("État initial de la mission:")
    print(f"  description_provided: {agent.mission_steps['description_provided']}")
    print(f"  coordinates_provided: {agent.mission_steps['coordinates_provided']}")
    print(f"  field_report_given: {agent.mission_steps['field_report_given']}")
    print()
    
    # Test 1: Fournir seulement une description
    print("🔍 Test 1: Description uniquement")
    response1 = agent.generate_response("L'individu mesure environ 1m80, cheveux bruns, yeux verts, corpulence moyenne, âgé d'environ 35 ans")
    print(f"État après description:")
    print(f"  description_provided: {agent.mission_steps['description_provided']}")
    print(f"  coordinates_provided: {agent.mission_steps['coordinates_provided']}")
    print(f"  field_report_given: {agent.mission_steps['field_report_given']}")
    print(f"Réponse: {response1['response'][:100]}...")
    print()
    
    # Test 2: Maintenant ajouter les coordonnées
    print("🗺️ Test 2: Ajout coordonnées GPS")
    response2 = agent.generate_response("Les coordonnées GPS sont 43.2081, 5.4890 - secteur de la Grotte Bleue")
    
    print(f"État après coordonnées:")
    print(f"  description_provided: {agent.mission_steps['description_provided']}")
    print(f"  coordinates_provided: {agent.mission_steps['coordinates_provided']}")
    print(f"  field_report_given: {agent.mission_steps['field_report_given']}")
    print()
    
    print(f"Réponse complète:")
    print(f"Response type: {type(response2)}")
    print(f"Response keys: {response2.keys() if isinstance(response2, dict) else 'Not a dict'}")
    print(f"Content: {response2['response']}")
    print()
    
    # Vérifier si le rapport contient Jules et Grotte Bleue
    if "Jules" in response2['response'] and "Grotte Bleue" in response2['response']:
        print("✅ Rapport de terrain correct généré!")
    else:
        print("❌ Rapport de terrain personnalisé non généré")
        
        # Test direct de la méthode generate_field_report
        print("\n📋 Test direct de generate_field_report:")
        direct_report = agent.generate_field_report()
        print(f"Rapport direct: {direct_report[:200]}...")
        
        if "Jules" in direct_report:
            print("✅ Méthode generate_field_report fonctionne correctement")
        else:
            print("❌ Problème dans generate_field_report")

if __name__ == "__main__":
    debug_field_report()
