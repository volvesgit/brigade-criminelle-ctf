@echo off
REM Script de création du package de distribution Brigade Criminelle CTF (Windows)

set DIST_DIR=brigade-criminelle-ctf-dist

echo 🚨 Création du package de distribution Brigade Criminelle...
echo ============================================================

REM Nettoyer et créer le répertoire de distribution
if exist "%DIST_DIR%" (
    echo 🗑️  Suppression de l'ancien package...
    rmdir /s /q "%DIST_DIR%"
)

mkdir "%DIST_DIR%"

echo 📁 Création du répertoire de distribution...

REM Copier les fichiers nécessaires pour la distribution
echo 📋 Copie des fichiers essentiels...
copy .env.example "%DIST_DIR%\" >nul
copy docker-compose.prod.yml "%DIST_DIR%\" >nul
copy deploy.bat "%DIST_DIR%\" >nul
copy deploy.sh "%DIST_DIR%\" >nul
copy stop.bat "%DIST_DIR%\" >nul
copy stop.sh "%DIST_DIR%\" >nul

REM Créer le README pour la distribution
echo 📝 Création du README de distribution...
(
echo # 🚨 Brigade Criminelle - Application CTF
echo.
echo Application CTF immersive où vous incarnez un enquêteur qui doit extraire des informations d'un inspecteur de police.
echo.
echo ## 🎯 Objectif du Challenge
echo.
echo **Mission :** Extraire le nom "Julien Lefevre" en conversant avec l'inspecteur de la Brigade Criminelle.
echo.
echo L'inspecteur joue un rôle réaliste et ne révélera l'information que si vous savez comment l'approcher correctement.
echo.
echo ## ⚡ Déploiement rapide
echo.
echo ### Windows
echo 1. 🖱️ **Double-cliquez sur `deploy.bat`**
echo 2. 📝 **Suivez les instructions** pour configurer vos clés API
echo 3. 🌐 **L'application s'ouvrira** automatiquement dans votre navigateur
echo.
echo ### Linux/macOS
echo 1. 🔓 **Rendez le script exécutable :** `chmod +x deploy.sh`
echo 2. 🚀 **Lancez le déploiement :** `./deploy.sh`
echo 3. 📝 **Suivez les instructions** pour configurer vos clés API
echo.
echo ## 🔑 Configuration des clés API
echo.
echo ### Google Gemini API ^(pour l'IA^)
echo 1. Allez sur https://makersuite.google.com/app/apikey
echo 2. Créez une nouvelle clé API
echo 3. Copiez la clé ^(format : AIza...^)
echo.
echo ### OpenAI API ^(pour la synthèse vocale^)
echo 1. Allez sur https://platform.openai.com/api-keys
echo 2. Créez une nouvelle clé API
echo 3. Copiez la clé ^(format : sk-...^)
echo.
echo ## 🌐 Accès
echo - **Interface principale :** http://localhost
echo - **Panel admin :** Cliquez sur "Admin" en bas de page
echo - **Mot de passe :** change_me
echo.
echo ## 🆘 Support
echo En cas de problème :
echo 1. Vérifiez que Docker Desktop est installé et en cours d'exécution
echo 2. Vérifiez que les ports 80 et 8000 sont libres
echo 3. Vérifiez vos clés API dans le fichier .env
echo.
echo ---
echo 🚨 **Application CTF fictive à des fins éducatives - Hackolyte** 🚨
) > "%DIST_DIR%\README.md"

REM Créer un fichier de configuration .env pour la distribution
echo ⚙️ Création du fichier de configuration...
(
echo # Configuration Brigade Criminelle CTF
echo # Remplissez ces valeurs avec vos clés API
echo.
echo # Clé API Google Gemini ^(obligatoire^)
echo GEMINI_API_KEY=votre_cle_gemini_ici
echo.
echo # Clé API OpenAI ^(obligatoire^)
echo OPENAI_API_KEY=votre_cle_openai_ici
echo.
echo # Mot de passe admin ^(optionnel^)
echo ADMIN_PASSWORD=change_me
echo.
echo # Configuration base de données ^(optionnel^)
echo DATABASE_PATH=/app/data/conversations.db
) > "%DIST_DIR%\.env"

REM Créer un script de diagnostic pour Windows
echo 🔧 Création du script de diagnostic...
(
echo @echo off
echo echo 🔍 Diagnostic Brigade Criminelle CTF
echo echo ====================================
echo echo.
echo echo 📊 Informations système:
echo echo Docker version:
echo docker --version 2^>nul ^|^| echo ❌ Docker non installé ou non démarré
echo echo.
echo echo Docker Compose version:
echo docker compose version 2^>nul ^|^| echo ❌ Docker Compose non disponible
echo echo.
echo echo 🐳 État des conteneurs:
echo docker compose -f docker-compose.prod.yml ps 2^>nul ^|^| echo ❌ Aucun conteneur en cours d'exécution
echo echo.
echo echo 📋 Configuration:
echo if exist ".env" ^(
echo     echo ✅ Fichier .env présent
echo     findstr "votre_cle_" .env ^>nul ^&^& echo ⚠️  Clés API non configurées ^|^| echo ✅ Clés API configurées
echo ^) else ^(
echo     echo ❌ Fichier .env manquant
echo ^)
echo echo.
echo echo 📊 Logs récents:
echo docker compose -f docker-compose.prod.yml logs --tail=10 2^>nul ^|^| echo ❌ Impossible d'accéder aux logs
echo pause
) > "%DIST_DIR%\diagnostic.bat"

echo.
echo ✅ Package de distribution créé avec succès dans le dossier: %DIST_DIR%
echo.
echo 📋 Contenu du package:
dir "%DIST_DIR%"
echo.
echo 🎯 Étapes suivantes:
echo 1. 🧪 Testez le déploiement depuis le dossier %DIST_DIR%
echo 2. 📦 Créez une archive ZIP du dossier %DIST_DIR%
echo 3. 📤 Partagez l'archive avec vos collègues
echo.
echo 💡 Commandes utiles:
echo    cd %DIST_DIR% ^&^& deploy.bat    # Tester le déploiement
echo.
echo 🚀 Votre package est prêt pour la distribution!
pause
