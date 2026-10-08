# Fichier de configuration pour le déploiement Vercel
from fastapi import FastAPI
from main import app

# Pour Vercel, nous devons exposer l'app comme une fonction
def handler(event, context):
    return app

# Export pour Vercel
vercel_app = app
