@echo off
REM Script de déploiement pour l'application CTF Brigade Criminelle (Windows)
REM Ce script configure et lance l'application en mode production

echo 🚨 Brigade Criminelle - Déploiement de l'application CTF 🚨
echo ==============================================================

REM Vérifier que Docker est installé et en cours d'exécution
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker n'est pas installé ou en cours d'exécution.
    echo Veuillez installer Docker Desktop et le démarrer.
    pause
    exit /b 1
)

echo ✅ Docker est disponible

REM Vérifier la présence du fichier .env
if not exist ".env" (
    echo ⚠️  Fichier .env non trouvé. Création à partir du modèle...
    copy .env.example .env >nul
    echo.
    echo 📝 IMPORTANT: Veuillez éditer le fichier .env avec vos clés API:
    echo    - GEMINI_API_KEY: Votre clé API Google Gemini
    echo    - OPENAI_API_KEY: Votre clé API OpenAI
    echo.
    echo Après avoir configuré vos clés API, relancez ce script.
    pause
    exit /b 1
)

REM Charger les variables d'environnement (simplification pour Windows)
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if "%%a"=="GEMINI_API_KEY" set GEMINI_API_KEY=%%b
    if "%%a"=="OPENAI_API_KEY" set OPENAI_API_KEY=%%b
    if "%%a"=="ADMIN_PASSWORD" set ADMIN_PASSWORD=%%b
)

REM Vérifier que les clés API sont configurées
if "%GEMINI_API_KEY%"=="votre_cle_gemini_ici" (
    echo ❌ GEMINI_API_KEY n'est pas configurée dans le fichier .env
    pause
    exit /b 1
)

if "%OPENAI_API_KEY%"=="votre_cle_openai_ici" (
    echo ❌ OPENAI_API_KEY n'est pas configurée dans le fichier .env
    pause
    exit /b 1
)

echo ✅ Configuration validée

REM Arrêter les conteneurs existants s'ils existent
echo 🔄 Arrêt des conteneurs existants...
docker compose -f docker-compose.prod.yml down --remove-orphans 2>nul

REM Construire et démarrer les services
echo 🏗️  Construction des images Docker...
docker compose -f docker-compose.prod.yml build --no-cache

echo 🚀 Démarrage de l'application...
docker compose -f docker-compose.prod.yml up -d

REM Attendre que les services soient prêts
echo ⏳ Vérification de l'état des services...
timeout /t 10 /nobreak >nul

REM Vérifier l'état des conteneurs
docker compose -f docker-compose.prod.yml ps | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo.
    echo ✅ Application déployée avec succès!
    echo.
    echo 🌐 Accès à l'application:
    echo    Interface principale: http://localhost
    echo    Panel d'administration: http://localhost (cliquez sur 'Admin' en bas^)
    echo.
    echo 🔐 Identifiants admin:
    echo    Mot de passe: %ADMIN_PASSWORD%
    echo.
    echo 📊 Commandes utiles:
    echo    Voir les logs: docker compose -f docker-compose.prod.yml logs -f
    echo    Arrêter l'app: docker compose -f docker-compose.prod.yml down
    echo    Redémarrer: docker compose -f docker-compose.prod.yml restart
    echo.
    echo 🎯 L'objectif CTF: Extraire le nom 'Julien Lefevre' en interrogeant l'inspecteur!
    echo.
    echo Appuyez sur une touche pour ouvrir l'application dans votre navigateur...
    pause >nul
    start http://localhost
) else (
    echo ❌ Erreur lors du démarrage. Vérifiez les logs:
    docker compose -f docker-compose.prod.yml logs
    pause
)
