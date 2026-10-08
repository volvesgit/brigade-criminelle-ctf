# 🧹 Guide de Nettoyage Base de Données Railway

## Vue d'ensemble
Scripts pour nettoyer votre base de données PostgreSQL Railway avant un événement CTF.

## Prérequis

1. **Variable d'environnement DATABASE_URL configurée**
   ```bash
   # Windows
   set DATABASE_URL=postgresql://username:password@host:port/database
   
   # Ou via .env
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

2. **Dépendances Python**
   ```bash
   pip install psycopg2-binary
   ```

## Méthodes de Nettoyage

### Option 1: Script Automatique (Recommandé)
```bash
# Windows
clean_railway_db.bat

# Linux/Mac
python clean_railway_db.py
```

### Option 2: Nettoyage Standard
Supprime toutes les données mais garde la structure des tables :
```bash
python clean_railway_db.py
```

### Option 3: Reset Complet
Supprime et recrée complètement les tables :
```bash
python clean_railway_db.py --reset
```

## Ce qui est nettoyé

- ✅ **Toutes les conversations** (`conversations` table)
- ✅ **Tous les messages** (`messages` table)  
- ✅ **Réinitialisation des compteurs** (sequences)
- ✅ **Préservation de la structure** (sauf en mode --reset)

## Sécurité

- 🔒 **Confirmation obligatoire** avant suppression
- 📊 **Statistiques avant/après** pour vérification
- 🔄 **Opération transactionnelle** (rollback en cas d'erreur)
- 📝 **Logs détaillés** de toutes les opérations

## Récupération de l'URL Railway

1. Allez sur [railway.app](https://railway.app)
2. Sélectionnez votre projet CTF
3. Onglet **"Variables"**
4. Copiez la valeur `DATABASE_URL`

## Exemple d'utilisation

```bash
# 1. Configurer l'URL
set DATABASE_URL=postgresql://postgres:abcd1234@monrail.railway.app:5432/railway

# 2. Lancer le nettoyage
python clean_railway_db.py

# 3. Confirmer
# Tapez 'OUI' pour confirmer

# 4. Vérifier
# ✅ Base de données nettoyée avec succès!
```

## Dépannage

### Erreur "psycopg2 non installé"
```bash
pip install psycopg2-binary
```

### Erreur "DATABASE_URL non configurée"
Vérifiez votre variable d'environnement ou fichier .env

### Erreur de connexion
- Vérifiez que l'URL est correcte
- Vérifiez que Railway est accessible
- Vérifiez vos credentials

## Timing Recommandé

- 🕐 **24h avant l'événement** : Test du script
- 🕘 **2h avant l'événement** : Nettoyage final
- 🕘 **Juste avant ouverture** : Vérification que la DB est vide

---

⚠️ **IMPORTANT** : Cette opération est **IRRÉVERSIBLE**. Assurez-vous d'avoir une sauvegarde si nécessaire.
