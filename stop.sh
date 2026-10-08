#!/bin/bash
# Script d'arrêt pour l'application CTF Brigade Criminelle

echo "🛑 Arrêt de l'application Brigade Criminelle..."

# Utiliser docker compose (nouvelle syntaxe) ou docker-compose (ancienne syntaxe)
DOCKER_COMPOSE="docker compose"
if ! docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
fi

$DOCKER_COMPOSE -f docker-compose.prod.yml down

echo "✅ Application arrêtée avec succès"
echo "💾 Les données de la base de données sont conservées"
echo ""
echo "Pour redémarrer l'application, utilisez: ./deploy.sh"
