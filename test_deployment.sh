#!/bin/bash
# Script de test de déploiement rapide

echo "🧪 Test de déploiement Brigade Criminelle CTF"
echo "============================================="

# Vérifier Docker
echo "🔍 Vérification de Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker n'est pas en cours d'exécution"
    exit 1
fi

echo "✅ Docker OK"

# Vérifier Docker Compose
echo "🔍 Vérification de Docker Compose..."
DOCKER_COMPOSE="docker compose"
if ! docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose non disponible"
        exit 1
    fi
fi

echo "✅ Docker Compose OK ($DOCKER_COMPOSE)"

# Vérifier les fichiers nécessaires
echo "🔍 Vérification des fichiers..."
required_files=("docker-compose.prod.yml" "deploy.sh" ".env.example")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Fichier manquant: $file"
        exit 1
    fi
done

echo "✅ Tous les fichiers requis sont présents"

# Test de construction des images (sans démarrage)
echo "🏗️  Test de construction des images..."
if $DOCKER_COMPOSE -f docker-compose.prod.yml build --quiet; then
    echo "✅ Images construites avec succès"
else
    echo "❌ Erreur lors de la construction des images"
    exit 1
fi

# Nettoyage
echo "🧹 Nettoyage..."
$DOCKER_COMPOSE -f docker-compose.prod.yml down --remove-orphans &> /dev/null

echo ""
echo "🎉 Test de déploiement réussi !"
echo ""
echo "✅ Votre application est prête pour la distribution"
echo "📦 Vous pouvez créer le package avec : ./create_distribution.sh"
echo "🚀 Vos collègues pourront déployer avec : ./deploy.sh"
