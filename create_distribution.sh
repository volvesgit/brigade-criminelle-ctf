#!/bin/bash
# Script de création du package de distribution Brigade Criminelle CTF

DIST_DIR="brigade-criminelle-ctf-dist"

echo "🚨 Création du package de distribution Brigade Criminelle..."
echo "============================================================"

# Nettoyer et créer le répertoire de distribution
if [ -d "$DIST_DIR" ]; then
    echo "🗑️  Suppression de l'ancien package..."
    rm -rf $DIST_DIR
fi

mkdir -p $DIST_DIR

echo "📁 Création du répertoire de distribution..."

# Copier les fichiers nécessaires pour la distribution
echo "📋 Copie des fichiers essentiels..."
cp .env.example $DIST_DIR/
cp docker-compose.prod.yml $DIST_DIR/
cp deploy.bat $DIST_DIR/
cp deploy.sh $DIST_DIR/
cp stop.bat $DIST_DIR/
cp stop.sh $DIST_DIR/

# Rendre les scripts exécutables
chmod +x $DIST_DIR/deploy.sh
chmod +x $DIST_DIR/stop.sh

# Créer le README pour la distribution
echo "📝 Création du README de distribution..."
cat > $DIST_DIR/README.md << 'EOF'
# 🚨 Brigade Criminelle - Application CTF

Application CTF immersive où vous incarnez un enquêteur qui doit extraire des informations d'un inspecteur de police.

## 🎯 Objectif du Challenge

**Mission :** Extraire le nom "Julien Lefevre" en conversant avec l'inspecteur de la Brigade Criminelle.

L'inspecteur joue un rôle réaliste et ne révélera l'information que si vous savez comment l'approcher correctement.

## ⚡ Déploiement rapide

### Prérequis
- **Docker Desktop** installé et en cours d'exécution
- **Clés API** (configuration guidée au premier lancement)

### Instructions

#### Windows
1. 🖱️ **Double-cliquez sur `deploy.bat`**
2. 📝 **Suivez les instructions** pour configurer vos clés API
3. 🌐 **L'application s'ouvrira** automatiquement dans votre navigateur

#### Linux/macOS
1. 🔓 **Rendez le script exécutable :** `chmod +x deploy.sh`
2. 🚀 **Lancez le déploiement :** `./deploy.sh`
3. 📝 **Suivez les instructions** pour configurer vos clés API

## 🔑 Configuration des clés API

Vous aurez besoin de ces clés API gratuites :

### Google Gemini API (pour l'IA)
1. Allez sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key"
4. Copiez la clé (format : `AIza...`)

### OpenAI API (pour la synthèse vocale)
1. Allez sur [OpenAI Platform](https://platform.openai.com/api-keys)
2. Connectez-vous à votre compte OpenAI
3. Cliquez sur "Create new secret key"
4. Copiez la clé (format : `sk-...`)
5. ⚠️ Assurez-vous d'avoir des crédits sur votre compte

## 🌐 Accès à l'application

Une fois déployée :
- **Interface principale :** http://localhost
- **Panel d'administration :** Cliquez sur "Admin" en bas de page
- **Mot de passe admin :** `change_me`

## 🎮 Comment jouer

1. 🗣️ **Démarrez une conversation** avec l'inspecteur
2. 🎭 **Adoptez un rôle crédible** (journaliste, collègue, etc.)
3. 🔍 **Posez des questions** pour obtenir des informations
4. 🏆 **Extrayez le flag** "Julien Lefevre"

## 🛠️ Gestion de l'application

### Arrêter l'application
- **Windows :** Double-cliquez sur `stop.bat`
- **Linux/macOS :** `./stop.sh`

### Redémarrer
- Relancez le script de déploiement

### Voir les logs
```bash
docker compose -f docker-compose.prod.yml logs -f
```

## 🆘 Dépannage

### L'application ne démarre pas
1. ✅ **Vérifiez Docker :** `docker --version`
2. 🔌 **Vérifiez les ports :** 80 et 8000 doivent être libres
3. 🔑 **Vérifiez les clés API** dans le fichier `.env`

### Problèmes de synthèse vocale
1. 💳 **Vérifiez vos crédits OpenAI**
2. 🔑 **Vérifiez votre clé API OpenAI**
3. 📊 **Consultez les logs :** `docker compose -f docker-compose.prod.yml logs backend`

### Erreurs courantes

**"Port already in use" :**
```bash
docker compose -f docker-compose.prod.yml down
./deploy.sh
```

**"Permission denied" (Linux/macOS) :**
```bash
chmod +x deploy.sh stop.sh
```

## 📊 Fonctionnalités

- 🎤 **Interface vocale et textuelle**
- 🇫🇷 **Synthèse vocale française naturelle**
- 🕵️ **IA inspecteur réaliste avec personnalité**
- 📱 **Interface responsive moderne**
- 📈 **Panel admin avec monitoring temps réel**
- 💾 **Sauvegarde persistante des conversations**

## 📞 Support

En cas de problème persistant :

1. **Consultez les logs :**
   ```bash
   docker compose -f docker-compose.prod.yml logs
   ```

2. **Redéploiement propre :**
   ```bash
   docker compose -f docker-compose.prod.yml down -v
   ./deploy.sh
   ```

3. **Vérifiez la configuration :**
   - Fichier `.env` présent et correct
   - Clés API valides
   - Docker en cours d'exécution

---

🚨 **Application CTF fictive à des fins éducatives - Hackolyte** 🚨
EOF

# Créer un fichier de configuration .env vide pour la distribution
echo "⚙️ Création du fichier de configuration..."
cat > $DIST_DIR/.env << 'EOF'
# Configuration Brigade Criminelle CTF
# Remplissez ces valeurs avec vos clés API

# Clé API Google Gemini (obligatoire)
GEMINI_API_KEY=votre_cle_gemini_ici

# Clé API OpenAI (obligatoire)
OPENAI_API_KEY=votre_cle_openai_ici

# Mot de passe admin (optionnel, par défaut : change_me)
ADMIN_PASSWORD=change_me

# Configuration base de données (optionnel)
DATABASE_PATH=/app/data/conversations.db
EOF

# Créer un script de diagnostic
echo "🔧 Création du script de diagnostic..."
cat > $DIST_DIR/diagnostic.sh << 'EOF'
#!/bin/bash
echo "🔍 Diagnostic Brigade Criminelle CTF"
echo "===================================="
echo ""
echo "📊 Informations système:"
echo "Docker version:"
docker --version 2>/dev/null || echo "❌ Docker non installé ou non démarré"
echo ""
echo "Docker Compose version:"
docker compose version 2>/dev/null || docker-compose --version 2>/dev/null || echo "❌ Docker Compose non disponible"
echo ""
echo "🐳 État des conteneurs:"
docker compose -f docker-compose.prod.yml ps 2>/dev/null || echo "❌ Aucun conteneur en cours d'exécution"
echo ""
echo "📱 Test de connectivité:"
curl -s http://localhost >/dev/null && echo "✅ Frontend accessible" || echo "❌ Frontend non accessible"
curl -s http://localhost:8000/health >/dev/null && echo "✅ Backend accessible" || echo "❌ Backend non accessible"
echo ""
echo "📋 Configuration:"
if [ -f ".env" ]; then
    echo "✅ Fichier .env présent"
    if grep -q "votre_cle_" .env; then
        echo "⚠️  Clés API non configurées dans .env"
    else
        echo "✅ Clés API configurées"
    fi
else
    echo "❌ Fichier .env manquant"
fi
echo ""
echo "📊 Logs récents (backend):"
docker compose -f docker-compose.prod.yml logs --tail=10 backend 2>/dev/null || echo "❌ Impossible d'accéder aux logs backend"
echo ""
echo "📊 Logs récents (frontend):"
docker compose -f docker-compose.prod.yml logs --tail=10 frontend 2>/dev/null || echo "❌ Impossible d'accéder aux logs frontend"
EOF

chmod +x $DIST_DIR/diagnostic.sh

# Créer un script de diagnostic pour Windows
cat > $DIST_DIR/diagnostic.bat << 'EOF'
@echo off
echo 🔍 Diagnostic Brigade Criminelle CTF
echo ====================================
echo.
echo 📊 Informations système:
echo Docker version:
docker --version 2>nul || echo ❌ Docker non installé ou non démarré
echo.
echo Docker Compose version:
docker compose version 2>nul || echo ❌ Docker Compose non disponible
echo.
echo 🐳 État des conteneurs:
docker compose -f docker-compose.prod.yml ps 2>nul || echo ❌ Aucun conteneur en cours d'exécution
echo.
echo 📋 Configuration:
if exist ".env" (
    echo ✅ Fichier .env présent
    findstr "votre_cle_" .env >nul && echo ⚠️  Clés API non configurées dans .env || echo ✅ Clés API configurées
) else (
    echo ❌ Fichier .env manquant
)
echo.
echo 📊 Logs récents:
docker compose -f docker-compose.prod.yml logs --tail=10 2>nul || echo ❌ Impossible d'accéder aux logs
pause
EOF

echo ""
echo "✅ Package de distribution créé avec succès dans le dossier: $DIST_DIR"
echo ""
echo "📋 Contenu du package:"
ls -la $DIST_DIR/
echo ""
echo "🎯 Étapes suivantes:"
echo "1. 🧪 Testez le déploiement depuis le dossier $DIST_DIR"
echo "2. 📦 Créez une archive: tar -czf brigade-criminelle-ctf.tar.gz $DIST_DIR"
echo "3. 📤 Partagez l'archive avec vos collègues"
echo ""
echo "💡 Commandes utiles:"
echo "   cd $DIST_DIR && ./deploy.sh    # Tester le déploiement"
echo "   tar -czf brigade-criminelle-ctf.tar.gz $DIST_DIR  # Créer l'archive"
echo ""
echo "🚀 Votre package est prêt pour la distribution!"
