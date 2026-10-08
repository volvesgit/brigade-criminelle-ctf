#!/bin/bash
# Script de vérification post-déploiement Railway

echo "🚨 Brigade Criminelle CTF - Vérification Railway"
echo "================================================"

echo ""
echo "🔍 Vérification des services Railway..."
echo ""

# Demander les URLs Railway
read -p "🌐 Entrez l'URL de votre backend Railway (ex: https://backend-xxx.railway.app): " BACKEND_URL
read -p "🌐 Entrez l'URL de votre frontend Railway (ex: https://frontend-xxx.railway.app): " FRONTEND_URL

echo ""
echo "🧪 Test du backend..."

# Test de l'endpoint de santé
if curl -s -f "$BACKEND_URL/health" > /dev/null; then
    echo "✅ Backend accessible : $BACKEND_URL/health"
else
    echo "❌ Backend non accessible : $BACKEND_URL/health"
    echo "   Vérifiez :"
    echo "   - Le service backend est déployé"
    echo "   - Les variables d'environnement sont configurées"
    echo "   - Les logs Railway pour les erreurs"
fi

echo ""
echo "🧪 Test du frontend..."

# Test de l'accès frontend
if curl -s -f "$FRONTEND_URL" > /dev/null; then
    echo "✅ Frontend accessible : $FRONTEND_URL"
else
    echo "❌ Frontend non accessible : $FRONTEND_URL"
    echo "   Vérifiez :"
    echo "   - Le service frontend est déployé"
    echo "   - La variable REACT_APP_API_URL est configurée"
    echo "   - Les logs Railway pour les erreurs"
fi

echo ""
echo "📋 URLs de votre CTF :"
echo "🎮 Interface principale : $FRONTEND_URL"
echo "🔐 Panel admin : $FRONTEND_URL (cliquez sur 'Admin')"
echo "⚙️ API Backend : $BACKEND_URL"
echo "🏥 Health Check : $BACKEND_URL/health"

echo ""
echo "🎯 Pour tester le CTF :"
echo "1. Ouvrez : $FRONTEND_URL"
echo "2. Cliquez sur 'Démarrer la conversation'"
echo "3. Tentez d'extraire 'Julien Lefevre' de l'inspecteur"
echo "4. Surveillez via le panel admin"

echo ""
echo "📤 Partagez cette URL avec vos collègues :"
echo "   $FRONTEND_URL"

echo ""
echo "✅ Vérification terminée !"
