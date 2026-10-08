@echo off
echo 🧹 NETTOYAGE BASE DE DONNÉES RAILWAY - CTF Agent Vocal
echo ========================================================
echo.

:: Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

:: Vérifier que les dépendances sont installées
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo ❌ psycopg2 non installé. Installation...
    pip install psycopg2-binary
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation de psycopg2
        pause
        exit /b 1
    )
)

:: Vérifier que DATABASE_URL est configurée
if "%DATABASE_URL%"=="" (
    echo ⚠️  DATABASE_URL non configurée
    echo 💡 Configurez votre variable d'environnement DATABASE_URL
    echo    avec l'URL de votre base PostgreSQL Railway
    echo.
    echo Exemple:
    echo set DATABASE_URL=postgresql://username:password@host:port/database
    echo.
    pause
    exit /b 1
)

echo ✅ Prérequis vérifiés
echo 🎯 Base de données: %DATABASE_URL:~0,30%...
echo.

echo Choisissez le type de nettoyage:
echo 1. Nettoyage standard (supprime les données)
echo 2. Reset complet (supprime et recrée les tables)
echo 3. Annuler
echo.

choice /C 123 /M "Votre choix"

if errorlevel 3 goto cancel
if errorlevel 2 goto reset
if errorlevel 1 goto clean

:clean
echo.
echo 🗑️ Nettoyage standard des données...
python clean_railway_db.py
goto end

:reset
echo.
echo 🗑️ Reset complet des tables...
python clean_railway_db.py --reset
goto end

:cancel
echo.
echo ❌ Opération annulée
goto end

:end
echo.
pause
