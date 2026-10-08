#!/bin/bash
# Script de déploiement pour l'application CTF Brigade Criminelle
# Ce script configure et lance l'application en mode production

set -e

echo "🚨 Brigade Criminelle - Déploiement de l'application CTF 🚨"
echo "=============================================================="

# Vérifier que Docker est installé et en cours d'exécution
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker n'est pas en cours d'exécution. Veuillez démarrer Docker."
    exit 1
fi

# Vérifier que Docker Compose est disponible
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose n'est pas disponible. Veuillez installer Docker Compose."
    exit 1
fi

# Utiliser docker compose (nouvelle syntaxe) ou docker-compose (ancienne syntaxe)
DOCKER_COMPOSE="docker compose"
if ! docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
fi

echo "✅ Docker est disponible"

# Vérifier la présence du fichier .env
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env non trouvé. Création à partir du modèle..."
    cp .env.example .env
    echo ""
    echo "📝 IMPORTANT: Veuillez éditer le fichier .env avec vos clés API:"
    echo "   - GEMINI_API_KEY: Votre clé API Google Gemini"
    echo "   - OPENAI_API_KEY: Votre clé API OpenAI"
    echo ""
    echo "Après avoir configuré vos clés API, relancez ce script."
    exit 1
fi

# Vérifier que les clés API sont configurées
source .env
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "votre_cle_gemini_ici" ]; then
    echo "❌ GEMINI_API_KEY n'est pas configurée dans le fichier .env"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "votre_cle_openai_ici" ]; then
    echo "❌ OPENAI_API_KEY n'est pas configurée dans le fichier .env"
    exit 1
fi

echo "✅ Configuration validée"

# Arrêter les conteneurs existants s'ils existent
echo "🔄 Arrêt des conteneurs existants..."
$DOCKER_COMPOSE -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true

# Construire et démarrer les services
echo "🏗️  Construction des images Docker..."
$DOCKER_COMPOSE -f docker-compose.prod.yml build --no-cache

echo "🚀 Démarrage de l'application..."
$DOCKER_COMPOSE -f docker-compose.prod.yml up -d

# Attendre que les services soient prêts
echo "⏳ Vérification de l'état des services..."
sleep 10

# Vérifier l'état des conteneurs
if $DOCKER_COMPOSE -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo ""
    echo "✅ Application déployée avec succès!"
    echo ""
    echo "🌐 Accès à l'application:"
    echo "   Interface principale: http://localhost"
    echo "   Panel d'administration: http://localhost (cliquez sur 'Admin' en bas)"
    echo ""
    echo "🔐 Identifiants admin:"
    echo "   Mot de passe: $ADMIN_PASSWORD"
    echo ""
    echo "📊 Commandes utiles:"
    echo "   Voir les logs: $DOCKER_COMPOSE -f docker-compose.prod.yml logs -f"
    echo "   Arrêter l'app: $DOCKER_COMPOSE -f docker-compose.prod.yml down"
    echo "   Redémarrer: $DOCKER_COMPOSE -f docker-compose.prod.yml restart"
    echo ""
    echo "🎯 L'objectif CTF: Extraire le nom 'Julien Lefevre' en interrogeant l'inspecteur!"
else
    echo "❌ Erreur lors du démarrage. Vérifiez les logs:"
    $DOCKER_COMPOSE -f docker-compose.prod.yml logs
    exit 1
fi
