#!/bin/bash

# Script de lancement rapide pour l'application CTF Agent Vocal
# Usage: ./start.sh

echo "🎯 Démarrage de l'application CTF Agent Vocal..."

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour vérifier si un port est libre
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 1
    else
        return 0
    fi
}

# Vérification des prérequis
echo -e "${BLUE}Vérification des prérequis...${NC}"

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js n'est pas installé${NC}"
    exit 1
fi

# Vérifier npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm n'est pas installé${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prérequis vérifiés${NC}"

# Vérification des ports
echo -e "${BLUE}Vérification des ports...${NC}"

if ! check_port 8000; then
    echo -e "${YELLOW}⚠️  Le port 8000 est déjà utilisé${NC}"
    read -p "Voulez-vous continuer ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if ! check_port 3000; then
    echo -e "${YELLOW}⚠️  Le port 3000 est déjà utilisé${NC}"
    read -p "Voulez-vous continuer ? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Installation des dépendances backend
echo -e "${BLUE}Installation des dépendances backend...${NC}"
cd backend
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Création de l'environnement virtuel...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances Python${NC}"
    exit 1
fi

cd ..

# Installation des dépendances frontend
echo -e "${BLUE}Installation des dépendances frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erreur lors de l'installation des dépendances npm${NC}"
        exit 1
    fi
fi

cd ..

# Démarrage du backend
echo -e "${BLUE}Démarrage du backend...${NC}"
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Attendre que le backend soit prêt
echo -e "${YELLOW}Attente du démarrage du backend...${NC}"
sleep 5

# Vérifier si le backend fonctionne
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend démarré avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors du démarrage du backend${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Démarrage du frontend
echo -e "${BLUE}Démarrage du frontend...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Attendre un peu pour le frontend
sleep 3

echo -e "${GREEN}🎉 Application démarrée avec succès !${NC}"
echo -e "${BLUE}📱 Frontend : http://localhost:3000${NC}"
echo -e "${BLUE}🔗 Backend API : http://localhost:8000${NC}"
echo -e "${BLUE}📚 Documentation API : http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}🎯 Objectif : Découvrir le flag 'Julien Lefevre' en parlant avec Claire${NC}"
echo ""
echo -e "${RED}Pour arrêter l'application, appuyez sur Ctrl+C${NC}"

# Fonction de nettoyage lors de l'arrêt
cleanup() {
    echo -e "\n${YELLOW}Arrêt de l'application...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Application arrêtée${NC}"
    exit 0
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre indéfiniment
while true; do
    sleep 1
done
