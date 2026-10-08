import requests
import json
import os

# Test de l'API admin
BASE_URL = "http://localhost:8000"
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

def test_admin_api():
    print("🔧 Test de l'API d'administration...")
    
    # Test d'authentification
    print("\n1. Test d'authentification admin...")
    auth_response = requests.post(f"{BASE_URL}/api/admin/auth", 
                                 json={"password": ADMIN_PASSWORD})
    
    if auth_response.status_code == 200:
        print("✅ Authentification réussie")
        token = auth_response.json()["token"]
    else:
        print("❌ Échec de l'authentification")
        return
    
    # Test de récupération des conversations
    print("\n2. Test de récupération des conversations...")
    headers = {"Authorization": f"Bearer {token}"}
    
    conv_response = requests.get(f"{BASE_URL}/api/admin/conversations", 
                                headers=headers)
    
    if conv_response.status_code == 200:
        data = conv_response.json()
        print(f"✅ Conversations récupérées: {data['total']} conversations")
        print(f"   - Flags trouvés: {data['flags_found']}")
        print(f"   - Messages total: {data.get('total_messages', 'N/A')}")
        
        if data['conversations']:
            print(f"   - Première conversation: {data['conversations'][0]['id'][:8]}...")
            print(f"   - Messages dans la première: {len(data['conversations'][0]['messages'])}")
    else:
        print(f"❌ Erreur récupération conversations: {conv_response.status_code}")
        print(f"   Réponse: {conv_response.text}")
    
    # Test des statistiques
    print("\n3. Test des statistiques...")
    stats_response = requests.get(f"{BASE_URL}/api/admin/stats", 
                                 headers=headers)
    
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"✅ Statistiques récupérées:")
        print(f"   - Total conversations: {stats['total_conversations']}")
        print(f"   - Flags trouvés: {stats['flags_found']}")
        print(f"   - Total messages: {stats['total_messages']}")
    else:
        print(f"❌ Erreur récupération statistiques: {stats_response.status_code}")

if __name__ == "__main__":
    try:
        test_admin_api()
        print("\n🎉 Tests de l'API admin terminés !")
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Vérifiez que le backend tourne sur le port 8000.")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
