#!/usr/bin/env python3
"""
Test script to verify backend API endpoints are working correctly
"""

import requests
import json
import time

# Test the production backend
BASE_URL = "https://backend-production-0c4b.up.railway.app"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Environment: {data.get('environment')}")
            print(f"   AI Agent Status: {data.get('ai_agent', {}).get('status')}")
            print(f"   Database Status: {data.get('database', {}).get('status')}")
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_start_call():
    """Test the start call endpoint"""
    print("\n📞 Testing start call endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/api/start-call", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Start call successful")
            print(f"   Message: {data.get('message')}")
            print(f"   Greeting length: {len(data.get('greeting', ''))}")
            return True
        else:
            print(f"❌ Start call failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Start call error: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with mission steps"""
    print("\n💬 Testing chat endpoint...")
    
    # Test 1: Description
    try:
        payload = {
            "message": "personne grande chauve barbe rasé et matte de peau",
            "session_id": "test_session_123"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=15)
        print(f"Test 1 - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat test 1 successful")
            print(f"   Response length: {len(data.get('response', ''))}")
            print(f"   Flag found: {data.get('flag_found', False)}")
            print(f"   Response preview: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Chat test 1 failed: {response.text}")
            return False
            
        # Wait a bit between requests
        time.sleep(2)
        
        # Test 2: Coordinates
        payload2 = {
            "message": "les coordonnées GPS sont 43.21011503262918, 5.449606424661931",
            "session_id": "test_session_123"
        }
        response2 = requests.post(f"{BASE_URL}/api/chat", json=payload2, timeout=15)
        print(f"Test 2 - Status: {response2.status_code}")
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ Chat test 2 successful")
            print(f"   Response contains 'Jules': {'Jules' in data2.get('response', '')}")
            print(f"   Response contains 'Grotte Bleue': {'Grotte Bleue' in data2.get('response', '')}")
            print(f"   Flag found: {data2.get('flag_found', False)}")
            return True
        else:
            print(f"❌ Chat test 2 failed: {response2.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test error: {e}")
        return False

def main():
    print("=== TESTING PRODUCTION BACKEND ===")
    print(f"🌍 Backend URL: {BASE_URL}")
    print()
    
    # Run all tests
    health_ok = test_health_endpoint()
    start_call_ok = test_start_call()
    chat_ok = test_chat_endpoint()
    
    print("\n=== TEST RESULTS ===")
    print(f"Health Check: {'✅' if health_ok else '❌'}")
    print(f"Start Call: {'✅' if start_call_ok else '❌'}")
    print(f"Chat Flow: {'✅' if chat_ok else '❌'}")
    
    if all([health_ok, start_call_ok, chat_ok]):
        print("\n🎉 All tests passed! Backend is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
