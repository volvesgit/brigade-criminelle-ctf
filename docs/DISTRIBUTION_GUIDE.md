# 🎯 Brigade Criminelle CTF - Guide de Distribution

Ce guide explique comment partager l'application CTF avec des collègues pour qu'ils puissent la tester facilement sans avoir accès au code source.

## 📦 Création du Package de Distribution

### 1. Préparer les fichiers de distribution

Créez un dossier `brigade-criminelle-ctf-dist` contenant uniquement :

```
brigade-criminelle-ctf-dist/
├── .env.example              # Modèle de configuration
├── docker-compose.prod.yml   # Configuration Docker production
├── deploy.bat               # Script de déploiement Windows
├── deploy.sh                # Script de déploiement Linux/macOS
├── stop.bat                 # Script d'arrêt Windows
├── stop.sh                  # Script d'arrêt Linux/macOS
├── README_DISTRIBUTION.md   # Instructions pour l'utilisateur final
└── docker-images/           # Images Docker pré-construites (optionnel)
```

### 2. Script de création du package

Créez ce script pour préparer automatiquement la distribution :

```bash
#!/bin/bash
# create_distribution.sh

DIST_DIR="brigade-criminelle-ctf-dist"

echo "🚨 Création du package de distribution Brigade Criminelle..."

# Nettoyer et créer le répertoire de distribution
rm -rf $DIST_DIR
mkdir -p $DIST_DIR

# Copier les fichiers nécessaires
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
cat > $DIST_DIR/README.md << 'EOF'
# 🚨 Brigade Criminelle - Application CTF

## 🎯 Objectif
Extraire le nom "Julien Lefevre" en conversant avec l'inspecteur de police.

## ⚡ Déploiement rapide

### Windows
1. Double-cliquez sur `deploy.bat`
2. Suivez les instructions à l'écran

### Linux/macOS
1. Ouvrez un terminal dans ce dossier
2. Exécutez : `./deploy.sh`

## 🔑 Configuration des clés API

Vous aurez besoin de :
- **Clé API Google Gemini** : https://makersuite.google.com/app/apikey
- **Clé API OpenAI** : https://platform.openai.com/api-keys

## 🌐 Accès
- **Application** : http://localhost
- **Admin** : Cliquez sur "Admin" (mot de passe par défaut)

## 🆘 Support
En cas de problème, vérifiez :
1. Docker Desktop est installé et en cours d'exécution
2. Les ports 80 et 8000 sont libres
3. Vos clés API sont valides

---
CTF par Hackolyte - Usage éducatif uniquement
EOF

echo "✅ Package de distribution créé dans le dossier: $DIST_DIR"
echo ""
echo "📋 Étapes suivantes :"
echo "1. Testez le déploiement depuis le dossier $DIST_DIR"
echo "2. Créez une archive : tar -czf brigade-criminelle-ctf.tar.gz $DIST_DIR"
echo "3. Partagez l'archive avec vos collègues"
```

### 3. Alternative : Images Docker pré-construites

Pour éviter à vos collègues de compiler les images, vous pouvez les pré-construire :

```bash
# Construire et sauvegarder les images
docker compose -f docker-compose.prod.yml build
docker save -o brigade-criminelle-backend.tar $(docker compose -f docker-compose.prod.yml images -q backend)
docker save -o brigade-criminelle-frontend.tar $(docker compose -f docker-compose.prod.yml images -q frontend)

# Créer un script de chargement des images
cat > load_images.sh << 'EOF'
#!/bin/bash
echo "📦 Chargement des images Docker..."
docker load -i brigade-criminelle-backend.tar
docker load -i brigade-criminelle-frontend.tar
echo "✅ Images chargées avec succès"
EOF

chmod +x load_images.sh
```

## 🌐 Distribution via Docker Hub (Optionnel)

### 1. Publier les images sur Docker Hub

```bash
# Tagger les images
docker tag aiprojectctfagenttalk_backend:latest votre_username/brigade-criminelle-backend:latest
docker tag aiprojectctfagenttalk_frontend:latest votre_username/brigade-criminelle-frontend:latest

# Pousser vers Docker Hub
docker push votre_username/brigade-criminelle-backend:latest
docker push votre_username/brigade-criminelle-frontend:latest
```

### 2. Modifier docker-compose.prod.yml pour utiliser les images publiées

```yaml
version: '3.8'

services:
  backend:
    image: votre_username/brigade-criminelle-backend:latest
    # Supprimer la section 'build'
    ports:
      - "8000:8000"
    # ... reste de la configuration
  
  frontend:
    image: votre_username/brigade-criminelle-frontend:latest
    # Supprimer la section 'build'
    ports:
      - "80:80"
    # ... reste de la configuration
```

## 📧 Instructions pour vos collègues

Envoyez-leur ce message :

---

**Objet : Test Application CTF Brigade Criminelle**

Salut !

J'ai créé une application CTF que j'aimerais que tu testes. C'est un challenge d'ingénierie sociale où tu dois extraire des informations d'un inspecteur de police par conversation.

**Installation :**
1. Assure-toi d'avoir Docker Desktop installé et en cours d'exécution
2. Décompresse l'archive que je t'ai envoyée
3. Double-clique sur `deploy.bat` (Windows) ou lance `./deploy.sh` (Linux/macOS)
4. Configure tes clés API quand demandé :
   - Gemini : https://makersuite.google.com/app/apikey
   - OpenAI : https://platform.openai.com/api-keys

**Objectif CTF :**
Extraire le nom "Julien Lefevre" en conversant avec l'inspecteur.

**Accès :**
- Application : http://localhost
- Panel admin : Clique sur "Admin" en bas de page

N'hésite pas si tu as des questions !

---

## 🔧 Maintenance et mises à jour

### Mise à jour de l'application

Pour mettre à jour l'application chez vos collègues :

1. **Reconstruisez les images** :
   ```bash
   docker compose -f docker-compose.prod.yml build --no-cache
   ```

2. **Créez un nouveau package de distribution**

3. **Envoyez les instructions de mise à jour** :
   ```bash
   # Arrêter l'ancienne version
   docker compose -f docker-compose.prod.yml down
   
   # Supprimer les anciennes images
   docker image prune -f
   
   # Déployer la nouvelle version
   ./deploy.sh
   ```

### Monitoring à distance

Pour aider vos collègues en cas de problème :

```bash
# Script de diagnostic
cat > diagnostic.sh << 'EOF'
#!/bin/bash
echo "🔍 Diagnostic Brigade Criminelle CTF"
echo "=================================="
echo "Docker version:"
docker --version
echo ""
echo "État des conteneurs:"
docker compose -f docker-compose.prod.yml ps
echo ""
echo "Logs récents backend:"
docker compose -f docker-compose.prod.yml logs --tail=20 backend
echo ""
echo "Logs récents frontend:"
docker compose -f docker-compose.prod.yml logs --tail=20 frontend
EOF

chmod +x diagnostic.sh
```

---

Ce guide vous permet de distribuer facilement votre application CTF tout en gardant le code source privé ! 🚀
