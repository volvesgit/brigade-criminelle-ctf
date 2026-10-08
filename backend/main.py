# Railway deployment fix - June 7, 2025
import os
import secrets
import sys
from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from ai_agent import AIAgent
from config import MAX_REQUESTS_PER_MINUTE, MAX_MESSAGE_LENGTH
from database_railway import db  # Import de notre base de données hybride SQLite/PostgreSQL
import asyncio
from typing import Optional, List, Dict
import datetime
import uuid
import json

# Configuration des logs pour Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Logs de démarrage pour Railway
logger.info("🚀 Starting Brigade Criminelle CTF Backend...")
logger.info(f"🌍 Environment: {'Railway' if os.getenv('RAILWAY_ENVIRONMENT') else 'Local'}")
logger.info(f"🔌 Port: {os.getenv('PORT', '8000')}")
logger.info(f"🗄️ Database URL: {'***configured***' if os.getenv('DATABASE_URL') else 'SQLite (local)'}")

# Configuration FastAPI
app = FastAPI(
    title="CTF Agent Vocal",
    description="Challenge CTF avec agent vocal IA",
    version="1.0.0"
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS - Configuration pour Railway et développement local
allowed_origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000", 
    "http://localhost:3001", 
    "http://127.0.0.1:3001"
]

# Ajouter les domaines Railway si on est en production
if os.getenv('RAILWAY_ENVIRONMENT'):
    allowed_origins.extend([
        "https://frontend-production-59e6.up.railway.app",
        "https://backend-production-0c4b.up.railway.app"
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialisation de l'agent IA avec gestion d'erreur robuste
ai_agent = None
try:
    logger.info("🤖 Tentative d'initialisation de l'agent IA...")
    ai_agent = AIAgent()
    logger.info("✅ Agent IA initialisé avec succès")
except Exception as e:
    logger.error(f"❌ Erreur lors de l'initialisation de l'agent IA: {e}")
    logger.info("🔄 L'application démarrera sans l'agent IA (mode dégradé)")
    logger.info("ℹ️  Vérifiez vos clés API GEMINI_API_KEY et OPENAI_API_KEY")

# Mot de passe admin - le panneau admin est désactivé si la variable n'est pas définie
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
if not ADMIN_PASSWORD:
    logger.warning("ADMIN_PASSWORD non défini : le panneau admin est désactivé")


def is_valid_admin_password(candidate: str) -> bool:
    return bool(ADMIN_PASSWORD) and secrets.compare_digest(candidate, ADMIN_PASSWORD)

# Modèles Pydantic
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    audio_base64: Optional[str] = None
    flag_found: bool = False

# Modèles Pydantic pour l'admin
class AdminAuth(BaseModel):
    password: str

# Routes API
@app.get("/")
async def root():
    return {"message": "CTF Agent Vocal API", "status": "running", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/ping")
async def ping():
    """Simple ping endpoint for basic connectivity test"""
    return {"ping": "pong", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    """Health check endpoint with detailed diagnostics"""
    try:        # Test database connection
        db_status = "unknown"
        try:
            # Simple test to see if database is accessible
            conversations = db.get_all_conversations()
            db_status = "connected"
            logger.info("✅ Database connection successful")
        except Exception as e:
            db_status = f"error: {str(e)}"
            logger.error(f"❌ Database connection failed: {e}")
        
        # Test AI agent
        ai_status = "unknown"
        try:
            if ai_agent is not None:
                ai_status = "ready"
                logger.info("✅ AI Agent is available")
            else:
                ai_status = "not_initialized"
                logger.warning("⚠️ AI Agent not initialized")
        except Exception as e:
            ai_status = f"error: {str(e)}"
            logger.error(f"❌ AI Agent check failed: {e}")
        
        # Pour Railway, on considère le service healthy même si l'AI agent n'est pas prêt
        # tant que la base de données fonctionne
        status_code = 200
        overall_status = "healthy"
        
        # Log des variables d'environnement importantes (sans révéler les secrets)
        env_info = {
            "GEMINI_API_KEY": "SET" if os.getenv("GEMINI_API_KEY") else "MISSING",
            "OPENAI_API_KEY": "SET" if os.getenv("OPENAI_API_KEY") else "MISSING", 
            "DATABASE_URL": "SET" if os.getenv("DATABASE_URL") else "MISSING",
            "PORT": os.getenv("PORT", "8000"),
            "RAILWAY_ENVIRONMENT": os.getenv("RAILWAY_ENVIRONMENT", "local")
        }
        
        response = {
            "status": overall_status,
            "timestamp": datetime.datetime.now().isoformat(),
            "environment": os.getenv("RAILWAY_ENVIRONMENT", "local"),
            "port": os.getenv("PORT", "8000"),
            "database": {
                "status": db_status,
                "type": "PostgreSQL" if os.getenv("DATABASE_URL") else "SQLite"
            },
            "ai_agent": {
                "status": ai_status
            },
            "env_check": env_info,
            "version": "1.0.0"
        }
        
        logger.info(f"Health check result: {response}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        # Même en cas d'erreur, on retourne 200 pour Railway
        return {
            "status": "partial",
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }

@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit(f"{MAX_REQUESTS_PER_MINUTE}/minute")
async def chat_with_agent(
    chat_message: ChatMessage,
    request: Request
):
    """Endpoint pour converser avec le Brigadier Rosetti"""
    try:
        # Vérifier que l'agent IA est disponible
        if ai_agent is None:
            raise HTTPException(
                status_code=503,
                detail="Service temporairement indisponible. L'agent IA n'est pas initialisé."
            )
        # Validation de la longueur du message
        if len(chat_message.message) > MAX_MESSAGE_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Message trop long. Maximum {MAX_MESSAGE_LENGTH} caractères."
            )
        
        # Vérification que le message n'est pas vide
        if not chat_message.message.strip():
            raise HTTPException(
                status_code=400,
                detail="Le message ne peut pas être vide."
            )
        
        # Générer un session_id si pas fourni
        session_id = chat_message.session_id or str(uuid.uuid4())
        
        logger.info(f"Message reçu (session {session_id}): {chat_message.message[:100]}...")
          # Enregistrer le message utilisateur
        log_conversation_message(session_id, "user", chat_message.message, request)
        
        # Générer la réponse du Brigadier
        response_data = ai_agent.generate_response(chat_message.message)
        response_text = response_data['response']
        flag_found = response_data['flag_found']
        
        # Générer l'audio pour la réponse
        audio_file = ai_agent.text_to_speech(response_text)
        audio_base64 = None
        
        if audio_file:
            try:
                import base64
                with open(audio_file, 'rb') as f:
                    audio_base64 = base64.b64encode(f.read()).decode('utf-8')
                # Nettoyer le fichier temporaire
                os.unlink(audio_file)
            except Exception as e:
                logger.warning(f"Erreur lors de l'encodage audio: {e}")
          # Enregistrer la réponse de l'IA
        log_conversation_message(session_id, "ai", response_text, request)
        
        # Marquer le flag si trouvé
        if flag_found:
            db.mark_flag_found(session_id)
          # Log si le flag a été trouvé
        if flag_found:
            logger.info("🎉 FLAG TROUVÉ ! Les trois hobbies ont été identifiés.")
        
        return ChatResponse(
            response=response_text,
            audio_base64=audio_base64,
            flag_found=flag_found
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la génération de réponse: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne du serveur. Veuillez réessayer."
        )

@app.post("/api/start-call")
@limiter.limit("10/minute")
async def start_call(request: Request):
    """Démarre un nouvel appel avec le Brigadier"""
    try:
        # Vérifier que l'agent IA est disponible
        if ai_agent is None:
            raise HTTPException(
                status_code=503,
                detail="Service temporairement indisponible. L'agent IA n'est pas initialisé."
            )
        
        ai_agent.reset_conversation()
        greeting_text = ai_agent.get_initial_greeting()
        
        # Générer l'audio pour le message d'accueil
        audio_file = ai_agent.text_to_speech(greeting_text)
        audio_base64 = None
        
        if audio_file:
            try:
                import base64
                with open(audio_file, 'rb') as f:
                    audio_base64 = base64.b64encode(f.read()).decode('utf-8')
                # Nettoyer le fichier temporaire
                os.unlink(audio_file)
            except Exception as e:
                logger.warning(f"Erreur lors de l'encodage audio: {e}")
        
        logger.info("Nouvel appel démarré - mission Hackosint initialisée")
        
        return {
            "message": "Appel démarré",
            "greeting": greeting_text,
            "audio_base64": audio_base64
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'appel: {e}")
        raise HTTPException(
            status_code=500,
            detail="Impossible de démarrer l'appel"
        )

@app.post("/api/end-call")
@limiter.limit("10/minute")
async def end_call(request: Request):
    """Termine l'appel et remet à zéro"""
    try:
        # Vérifier que l'agent IA est disponible
        if ai_agent is None:
            raise HTTPException(
                status_code=503,
                detail="Service temporairement indisponible. L'agent IA n'est pas initialisé."
            )
        ai_agent.reset_conversation()
        logger.info("Appel terminé")
        
        return {"message": "Appel terminé"}
        
    except Exception as e:
        logger.error(f"Erreur lors de la fin de l'appel: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la fin de l'appel"
        )

@app.get("/api/status")
async def get_status():
    """Retourne le statut de la conversation"""
    if ai_agent is None:
        return {
            "status": "agent_unavailable",
            "flag_found": False,
            "conversation_length": 0,
            "conversation_history": []
        }
    return {
        "flag_found": ai_agent.flag_found,
        "conversation_length": len(ai_agent.conversation_history),
        "conversation_history": ai_agent.conversation_history[-5:]  # Les 5 derniers messages pour debug
    }

# Fonctions d'aide pour l'administration
def verify_admin_auth(authorization: str = Header(None)) -> bool:
    """Vérifie l'authentification admin"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header manquant")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Format d'authorization invalide")
    
    token = authorization.replace("Bearer ", "")
    if not is_valid_admin_password(token):
        raise HTTPException(status_code=401, detail="Token d'accès invalide")
    
    return True

def log_conversation_message(session_id: str, message_type: str, content: str, request: Request):
    """Enregistre un message dans la base de données SQLite"""
    try:
        # Créer la conversation si elle n'existe pas
        user_ip = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
        user_agent = request.headers.get("user-agent", "unknown")
        
        db.create_conversation(session_id, user_ip, user_agent)
        
        # Ajouter le message
        db.add_message(session_id, message_type, content)
            
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement du message: {e}")

# Routes d'administration
@app.get("/api/admin/conversations")
async def get_conversations(
    request: Request,
    _: bool = Depends(verify_admin_auth)
):
    """Récupère toutes les conversations pour l'administration"""
    try:
        conversations_list = db.get_all_conversations()
        stats = db.get_conversation_stats()
        
        return {
            "conversations": conversations_list,
            "total": stats["total_conversations"],
            "flags_found": stats["flags_found"],
            "total_messages": stats["total_messages"]
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des conversations: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.post("/api/admin/auth")
async def admin_login(auth: AdminAuth):
    """Endpoint de connexion admin"""
    if is_valid_admin_password(auth.password):
        return {"authenticated": True, "token": ADMIN_PASSWORD}
    else:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

@app.delete("/api/admin/conversations")
async def clear_conversations(
    request: Request,
    _: bool = Depends(verify_admin_auth)
):
    """Vide toutes les conversations (admin uniquement)"""
    try:
        success = db.clear_all_conversations()
        if success:
            logger.info("Toutes les conversations ont été supprimées par l'admin")
            return {"message": "Conversations supprimées", "count": 0}
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de la suppression")
    except Exception as e:
        logger.error(f"Erreur lors de la suppression des conversations: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/api/admin/stats")
async def get_admin_stats(
    request: Request,
    _: bool = Depends(verify_admin_auth)
):
    """Récupère les statistiques pour le dashboard admin"""
    try:
        stats = db.get_conversation_stats()
        return stats
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/debug")
async def debug_endpoint():
    """Endpoint de debug simple pour diagnostiquer les problèmes Railway"""
    import os
    return {
        "status": "ok",
        "timestamp": datetime.datetime.now().isoformat(),
        "environment_vars": {
            "GEMINI_API_KEY": "SET" if os.getenv("GEMINI_API_KEY") else "MISSING",
            "OPENAI_API_KEY": "SET" if os.getenv("OPENAI_API_KEY") else "MISSING",
            "DATABASE_URL": "SET" if os.getenv("DATABASE_URL") else "MISSING",
            "PORT": os.getenv("PORT", "8000"),
            "RAILWAY_ENVIRONMENT": os.getenv("RAILWAY_ENVIRONMENT", "not_set")
        },
        "python_version": sys.version,
        "working_directory": os.getcwd()
    }

@app.post("/api/chat-fallback")
async def chat_fallback(chat_message: ChatMessage):
    """Endpoint de fallback quand l'agent IA n'est pas disponible"""
    return ChatResponse(
        response="Service temporairement indisponible. L'agent IA est en cours d'initialisation. Veuillez réessayer dans quelques instants.",
        audio_base64=None,
        flag_found=False
    )

# FastAPI application instance - ready for WSGI deployment
app = app
