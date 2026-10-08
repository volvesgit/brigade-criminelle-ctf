# 🚀 Configuration Railway - Instructions Détaillées

## 🔧 Configuration du Backend

### 1. Créer le service Backend
- **Root Directory**: `/backend`
- Railway détectera automatiquement le `railway.toml`

### 2. Variables d'environnement Backend
Ajoutez ces variables dans Railway > Backend Service > Variables :

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ADMIN_PASSWORD=change_me
```

### 3. Ajouter PostgreSQL
- Dans votre projet Railway, cliquez sur "+ New"
- Sélectionnez "Database" > "PostgreSQL"
- Railway créera automatiquement `DATABASE_URL`

## 🌐 Configuration du Frontend

### 1. Créer le service Frontend
- **Root Directory**: `/frontend`
- Railway détectera automatiquement le `railway.toml`

### 2. Variables d'environnement Frontend
⚠️ **IMPORTANT** : Attendez que le backend soit déployé pour récupérer son URL

```env
REACT_APP_API_URL=https://[BACKEND-URL-FROM-RAILWAY]
CI=false
```

## 📋 Checklist de déploiement

### ✅ Backend
- [ ] Service backend créé avec root directory `/backend`
- [ ] Variables d'environnement configurées
- [ ] Base PostgreSQL ajoutée
- [ ] Déploiement réussi (vert)
- [ ] Test de l'endpoint : `https://[backend-url]/health`

### ✅ Frontend  
- [ ] Service frontend créé avec root directory `/frontend`
- [ ] Variable `REACT_APP_API_URL` configurée avec l'URL backend
- [ ] Déploiement réussi (vert)
- [ ] Test de l'interface web

## 🔑 Obtenir vos clés API

### Google Gemini API (obligatoire)
1. Allez sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key"
4. Copiez la clé (format: `AIza...`)

### OpenAI API (pour TTS français)
1. Allez sur [OpenAI Platform](https://platform.openai.com/api-keys)
2. Connectez-vous à votre compte OpenAI
3. Cliquez sur "Create new secret key"
4. Copiez la clé (format: `sk-...`)
5. ⚠️ Assurez-vous d'avoir des crédits sur votre compte

## 🧪 Tests après déploiement

### 1. Test Backend
```bash
curl https://[your-backend-url]/health
# Devrait retourner: {"status": "healthy"}
```

### 2. Test Frontend
- Ouvrez l'URL frontend dans votre navigateur
- Interface Brigade Criminelle devrait s'afficher
- Testez le bouton "Démarrer la conversation"

### 3. Test CTF complet
- Cliquez sur le micro ou tapez du texte
- L'inspecteur devrait répondre en français
- Tentez d'extraire "Julien Lefevre"

### 4. Test Panel Admin
- Cliquez sur "Admin" en bas de page
- Entrez le mot de passe configuré
- Vérifiez le monitoring temps réel

## 🔧 Troubleshooting

### Backend ne démarre pas
```bash
# Vérifiez les logs Railway
# Causes possibles :
# - GEMINI_API_KEY manquant
# - Erreur de connexion PostgreSQL
# - Dépendances Python manquantes
```

### Frontend ne se connecte pas
```bash
# Vérifiez :
# - REACT_APP_API_URL pointe vers le bon backend
# - Le backend répond sur /health
# - CORS configuré correctement
```

### TTS ne fonctionne pas
```bash
# Vérifiez :
# - OPENAI_API_KEY valide
# - Crédits OpenAI disponibles
# - Connexion réseau stable
```

## 🎯 URLs de production

Une fois déployé, vous aurez :

- **API Backend** : `https://[project-name]-backend-[hash].railway.app`
- **Interface Web** : `https://[project-name]-frontend-[hash].railway.app`

## 🔄 Mises à jour

Pour déployer des modifications :

```bash
# Local changes
git add .
git commit -m "Update: description of changes"
git push origin main

# Railway déploiera automatiquement
```

## 📊 Monitoring

- **Railway Dashboard** : Logs en temps réel, métriques CPU/RAM
- **Admin Panel CTF** : Conversations, statistiques joueurs
- **Health Check** : `/health` endpoint pour surveillance

---

🚨 **Votre CTF sera accessible via l'URL frontend Railway !** 🚨
