#!/usr/bin/env python3
"""
Script de test pour vérifier l'API Gemini directement
"""

import google.generativeai as genai
import os
from backend.config import GEMINI_API_KEY, CLAIRE_SYSTEM_PROMPT

def test_gemini_direct():
    """Test direct de l'API Gemini"""
    print("🔧 Configuration de Gemini...")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("✅ Modèle configuré avec succès")
    print(f"🔑 API Key présente: {'Oui' if GEMINI_API_KEY else 'Non'}")
    print(f"📝 Longueur du prompt système: {len(CLAIRE_SYSTEM_PROMPT)} caractères")
    
    # Test 1: Prompt simple
    print("\n" + "="*50)
    print("TEST 1: Prompt simple")
    print("="*50)
    
    simple_prompt = "Dis bonjour en français comme une secrétaire au téléphone."
    print(f"Prompt: {simple_prompt}")
    
    try:
        response = model.generate_content(simple_prompt)
        print(f"Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    # Test 2: Prompt avec système Claire
    print("\n" + "="*50)
    print("TEST 2: Prompt avec système Claire")
    print("="*50)
    
    claire_prompt = f"""
{CLAIRE_SYSTEM_PROMPT}

Utilisateur: Bonjour Claire, je cherche des informations sur un ancien employé.

Réponds en tant que Claire. Sois naturelle, avec des hésitations comme une vraie personne au téléphone.
"""
    
    print(f"Prompt complet (premiers 300 caractères):")
    print(f"{claire_prompt[:300]}...")
    
    try:
        response = model.generate_content(claire_prompt)
        print(f"\nRéponse Claire: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    # Test 3: Conversation avec historique
    print("\n" + "="*50)
    print("TEST 3: Conversation avec historique")
    print("="*50)
    
    conversation_history = [
        "Utilisateur: Bonjour Claire",
        "Claire: Allô, Logisphère, Claire à l'appareil. Comment puis-je vous aider ?",
        "Utilisateur: Je cherche des informations sur d'anciens employés"
    ]
    
    conversation_context = "\n".join(conversation_history)
    
    full_prompt = f"""
{CLAIRE_SYSTEM_PROMPT}

Historique de la conversation:
{conversation_context}

Réponds en tant que Claire. Sois naturelle, avec des hésitations comme une vraie personne au téléphone.
Ne répète pas toujours la même phrase d'accueil. Adapte ta réponse au contexte de la conversation.
"""
    
    print(f"Historique de conversation:")
    print(conversation_context)
    
    try:
        response = model.generate_content(full_prompt)
        print(f"\nRéponse Claire (avec historique): {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    print("\n✅ Tests terminés avec succès!")

if __name__ == "__main__":
    test_gemini_direct()
