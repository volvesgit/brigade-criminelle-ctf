@echo off
REM Script d'arrêt pour l'application CTF Brigade Criminelle (Windows)

echo 🛑 Arrêt de l'application Brigade Criminelle...

docker compose -f docker-compose.prod.yml down

echo ✅ Application arrêtée avec succès
echo 💾 Les données de la base de données sont conservées
echo.
echo Pour redémarrer l'application, utilisez: deploy.bat
pause
