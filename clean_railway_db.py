#!/usr/bin/env python3
"""
Script pour nettoyer la base de données PostgreSQL sur Railway.
Supprime toutes les conversations et messages pour remettre la DB à zéro.
"""

import os
import sys
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_database():
    """Nettoie complètement la base de données"""
    
    # Vérifier que la DATABASE_URL est configurée
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
        logger.error("❌ DATABASE_URL PostgreSQL non configurée")
        logger.info("💡 Configurez d'abord votre DATABASE_URL Railway")
        return False
    
    try:
        import psycopg2
        logger.info("📦 psycopg2 disponible")
    except ImportError:
        logger.error("❌ psycopg2 non installé. Installez-le avec: pip install psycopg2-binary")
        return False
    
    try:
        # Connexion à la base de données
        logger.info("🔌 Connexion à la base de données PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Afficher les statistiques avant nettoyage
        logger.info("📊 Statistiques avant nettoyage:")
        
        cursor.execute("SELECT COUNT(*) FROM conversations")
        conv_count = cursor.fetchone()[0]
        logger.info(f"   - Conversations: {conv_count}")
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        msg_count = cursor.fetchone()[0]
        logger.info(f"   - Messages: {msg_count}")
        
        if conv_count == 0 and msg_count == 0:
            logger.info("✅ La base de données est déjà vierge!")
            return True
        
        # Demander confirmation
        print(f"\n⚠️  ATTENTION: Vous allez supprimer {conv_count} conversations et {msg_count} messages!")
        print("Cette action est IRRÉVERSIBLE!")
        confirm = input("Tapez 'OUI' pour confirmer: ")
        
        if confirm != "OUI":
            logger.info("❌ Nettoyage annulé par l'utilisateur")
            return False
        
        # Supprimer tous les messages
        logger.info("🗑️ Suppression des messages...")
        cursor.execute("DELETE FROM messages")
        deleted_messages = cursor.rowcount
        logger.info(f"   - {deleted_messages} messages supprimés")
        
        # Supprimer toutes les conversations
        logger.info("🗑️ Suppression des conversations...")
        cursor.execute("DELETE FROM conversations")
        deleted_conversations = cursor.rowcount
        logger.info(f"   - {deleted_conversations} conversations supprimées")
        
        # Réinitialiser les séquences auto-increment
        logger.info("🔄 Réinitialisation des séquences...")
        cursor.execute("ALTER SEQUENCE messages_id_seq RESTART WITH 1")
        
        # Commit des changements
        conn.commit()
        
        # Vérifier que tout est vide
        cursor.execute("SELECT COUNT(*) FROM conversations")
        conv_count_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        msg_count_after = cursor.fetchone()[0]
        
        logger.info("📊 Statistiques après nettoyage:")
        logger.info(f"   - Conversations: {conv_count_after}")
        logger.info(f"   - Messages: {msg_count_after}")
        
        if conv_count_after == 0 and msg_count_after == 0:
            logger.info("🎉 Base de données nettoyée avec succès!")
            logger.info("✅ La base est maintenant vierge et prête pour demain")
            return True
        else:
            logger.error("❌ Erreur: La base n'est pas complètement vide")
            return False
            
    except psycopg2.Error as e:
        logger.error(f"❌ Erreur PostgreSQL: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Erreur inattendue: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()
            logger.info("🔌 Connexion fermée")

def reset_tables():
    """Alternative: Supprime et recrée les tables complètement"""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
        logger.error("❌ DATABASE_URL PostgreSQL non configurée")
        return False
    
    try:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("⚠️  RESET COMPLET: Suppression et recréation des tables!")
        confirm = input("Tapez 'RESET' pour confirmer: ")
        
        if confirm != "RESET":
            logger.info("❌ Reset annulé")
            return False
        
        # Supprimer les tables
        logger.info("🗑️ Suppression des tables...")
        cursor.execute("DROP TABLE IF EXISTS messages CASCADE")
        cursor.execute("DROP TABLE IF EXISTS conversations CASCADE")
        
        # Recréer les tables
        logger.info("🏗️ Recréation des tables...")
        
        # Table conversations
        cursor.execute('''
            CREATE TABLE conversations (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                flag_found BOOLEAN DEFAULT FALSE,
                user_ip TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table messages
        cursor.execute('''
            CREATE TABLE messages (
                id SERIAL PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        # Index
        cursor.execute('''
            CREATE INDEX idx_conversation_timestamp 
            ON conversations(timestamp DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX idx_messages_conversation 
            ON messages(conversation_id, timestamp)
        ''')
        
        conn.commit()
        logger.info("🎉 Tables recréées avec succès!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du reset: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🧹 NETTOYAGE BASE DE DONNÉES RAILWAY")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("Mode RESET complet (suppression/recréation tables)")
        success = reset_tables()
    else:
        print("Mode nettoyage standard (suppression données)")
        print("Pour reset complet: python clean_railway_db.py --reset")
        success = clean_database()
    
    if success:
        print("\n✅ Opération terminée avec succès!")
        print("🚀 La base de données est prête pour demain!")
    else:
        print("\n❌ Erreur lors de l'opération")
        sys.exit(1)
