# 🚔 CTF Brigade Criminelle - Documentation Admin

## 📋 Résumé des Améliorations

### ✅ Modifications Effectuées

#### 1. **Interface Utilisateur Améliorée**
- **Titre de page** : Changé de "React App" à "Brigade Criminelle - Enquête Prioritaire"
- **Disclaimer ajouté** : Footer avec mention "Cette enquête est fictive - Réalisée dans le cadre du CTF organisé par Hackolyte"
- **Design policier** : Interface avec thème investigation criminelle (bleu foncé, or, badges)

#### 2. **Correction de l'Accent TTS**
- **Configuration** : Retour à OpenAI TTS avec voix "nova" pour meilleur accent français
- **Alternative** : Google TTS configuré mais nécessite credentials (voix fr-FR-Neural2-C disponible)

#### 3. **Panel d'Administration Sécurisé**
- **Accès** : Bouton 🔒 discret en haut à droite de l'interface principale
- **Authentification** : Mot de passe sécurisé `change_me`
- **Surveillance complète** : Toutes les conversations en temps réel

---

## 🔐 Panel d'Administration

### Accès
1. Cliquer sur l'icône 🔒 en haut à droite
2. Entrer le mot de passe : `change_me`
3. Accès immédiat au panel de surveillance

### Fonctionnalités

#### **📊 Tableau de Bord**
- **Statistiques en temps réel** :
  - Total des conversations
  - Nombre de flags trouvés
  - Total des messages échangés

#### **💬 Surveillance des Conversations**
- **Liste complète** : Toutes les sessions avec horodatage
- **Indicateurs visuels** : 🏁 pour les flags trouvés
- **Détails techniques** : IP et User-Agent des utilisateurs

#### **🔍 Analyse Détaillée**
- **Messages complets** : Conversation entière utilisateur ↔ IA
- **Timeline** : Horodatage précis de chaque message
- **Statut CTF** : Indication claire si le flag a été extrait

#### **🛡️ Sécurité**
- **Authentification robuste** : Mot de passe complexe
- **Session management** : Déconnexion sécurisée
- **Accès restreint** : Interface dédiée personnel autorisé

---

## 🎯 Utilisation CTF

### Pour les Organisateurs
```
Mot de passe admin : change_me
```

### Surveillance en Temps Réel
1. **Accéder au panel** via l'icône 🔒
2. **Observer les tentatives** des participants
3. **Identifier les flags trouvés** (indicateur 🏁)
4. **Analyser les stratégies** des joueurs

### Informations Collectées
- **Conversations complètes** : Échanges utilisateur/IA
- **Métadonnées techniques** : IP, User-Agent
- **Progression CTF** : Statut de découverte du flag
- **Timing** : Durée des sessions et vitesse de résolution

---

## 🛠️ Configuration Technique

### Backend (Port 8000)
- **Endpoints admin** : `/api/admin/*`
- **Authentification** : Bearer token
- **Base de données** : En mémoire (conversations_db)
- **Logging** : Événements CTF tracés

### Frontend (Port 3000)
- **Routage simple** : Vue principale ↔ Admin
- **Composants** : AdminPanel.tsx + AdminPanel.css
- **Sécurité** : Authentification côté client + serveur

### APIs Disponibles
```
GET  /api/admin/conversations  - Liste toutes les conversations
POST /api/admin/auth          - Authentification admin
DELETE /api/admin/conversations - Vide les conversations (admin)
```

---

## 🎮 Expérience Participant

### Interface Principale
- **Design immersif** : Thème police criminelle authentique
- **Personnage IA** : Inspecteur Claire Dubois, Brigade Criminelle
- **Mission** : Identifier le suspect "Serpent" en fournissant 4 détails précis

### Interactions Réalistes
- **Roleplay avancé** : "Je note...", "D'accord, j'inscris..."
- **Validation immersive** : Récapitulatif professionnel complet
- **Accent français** : TTS OpenAI voix "nova" optimisée

### Objectif CTF
Extraire le flag **"Julien Lefevre"** en fournissant :
- Cheveux : noirs et blancs (poivre et sel)
- Cicatrice sous l'œil gauche  
- Tatouage serpent sur le cou
- Âge : entre 30 et 40 ans

---

## 📱 Responsive & Accessibility

- **Design adaptatif** : Mobile, tablette, desktop
- **Contraste élevé** : Lisibilité optimale
- **Navigation intuitive** : UX police investigation
- **Performance** : Chargement rapide, animations fluides

---

*Cette application CTF combine ingénierie sociale, roleplay immersif et surveillance administrative pour une expérience complète de capture du flag.*
