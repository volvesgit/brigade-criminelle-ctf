import sqlite3
import json
import datetime
from typing import Dict, List, Optional, Any
import logging
import os

logger = logging.getLogger(__name__)

class ConversationDB:
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données SQLite"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table des conversations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        flag_found BOOLEAN DEFAULT FALSE,
                        user_ip TEXT,
                        user_agent TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Table des messages
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id TEXT NOT NULL,
                        message_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                    )
                ''')
                
                # Index pour améliorer les performances
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_conversation_timestamp 
                    ON conversations(timestamp DESC)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_messages_conversation 
                    ON messages(conversation_id, timestamp)
                ''')
                
                conn.commit()
                logger.info("Base de données SQLite initialisée avec succès")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    def create_conversation(self, conversation_id: str, user_ip: str = None, user_agent: str = None) -> bool:
        """Crée une nouvelle conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                timestamp = datetime.datetime.now().isoformat()
                
                cursor.execute('''
                    INSERT OR IGNORE INTO conversations 
                    (id, timestamp, flag_found, user_ip, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                ''', (conversation_id, timestamp, False, user_ip, user_agent))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Erreur lors de la création de conversation {conversation_id}: {e}")
            return False
    
    def add_message(self, conversation_id: str, message_type: str, content: str) -> bool:
        """Ajoute un message à une conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                timestamp = datetime.datetime.now().isoformat()
                
                cursor.execute('''
                    INSERT INTO messages 
                    (conversation_id, message_type, content, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (conversation_id, message_type, content, timestamp))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du message à {conversation_id}: {e}")
            return False
    
    def mark_flag_found(self, conversation_id: str) -> bool:
        """Marque qu'un flag a été trouvé dans une conversation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE conversations 
                    SET flag_found = TRUE 
                    WHERE id = ?
                ''', (conversation_id,))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du flag pour {conversation_id}: {e}")
            return False
    
    def get_all_conversations(self) -> List[Dict[str, Any]]:
        """Récupère toutes les conversations avec leurs messages"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Pour avoir des dictionnaires
                cursor = conn.cursor()
                
                # Récupérer les conversations
                cursor.execute('''
                    SELECT * FROM conversations 
                    ORDER BY timestamp DESC
                ''')
                conversations = cursor.fetchall()
                
                result = []
                for conv in conversations:
                    # Récupérer les messages pour cette conversation
                    cursor.execute('''
                        SELECT message_type, content, timestamp 
                        FROM messages 
                        WHERE conversation_id = ? 
                        ORDER BY timestamp ASC
                    ''', (conv['id'],))
                    messages = cursor.fetchall()
                    
                    conversation_data = {
                        "id": conv['id'],
                        "timestamp": conv['timestamp'],
                        "flag_found": bool(conv['flag_found']),
                        "user_info": {
                            "ip": conv['user_ip'] or 'unknown',
                            "user_agent": conv['user_agent'] or 'unknown'
                        },
                        "messages": [
                            {
                                "type": msg['message_type'],
                                "content": msg['content'],
                                "timestamp": msg['timestamp']
                            }
                            for msg in messages
                        ]
                    }
                    result.append(conversation_data)
                
                return result
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des conversations: {e}")
            return []
    
    def get_conversation_stats(self) -> Dict[str, int]:
        """Récupère les statistiques des conversations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total conversations
                cursor.execute('SELECT COUNT(*) FROM conversations')
                total_conversations = cursor.fetchone()[0]
                
                # Flags trouvés
                cursor.execute('SELECT COUNT(*) FROM conversations WHERE flag_found = TRUE')
                flags_found = cursor.fetchone()[0]
                
                # Total messages
                cursor.execute('SELECT COUNT(*) FROM messages')
                total_messages = cursor.fetchone()[0]
                
                return {
                    "total_conversations": total_conversations,
                    "flags_found": flags_found,
                    "total_messages": total_messages
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {"total_conversations": 0, "flags_found": 0, "total_messages": 0}
    
    def clear_all_conversations(self) -> bool:
        """Supprime toutes les conversations (admin uniquement)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM messages')
                cursor.execute('DELETE FROM conversations')
                
                conn.commit()
                logger.info("Toutes les conversations ont été supprimées de la base de données")
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des conversations: {e}")
            return False
    
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Récupère une conversation spécifique par son ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Récupérer la conversation
                cursor.execute('''
                    SELECT * FROM conversations WHERE id = ?
                ''', (conversation_id,))
                conv = cursor.fetchone()
                
                if not conv:
                    return None
                
                # Récupérer les messages
                cursor.execute('''
                    SELECT message_type, content, timestamp 
                    FROM messages 
                    WHERE conversation_id = ? 
                    ORDER BY timestamp ASC
                ''', (conversation_id,))
                messages = cursor.fetchall()
                
                return {
                    "id": conv['id'],
                    "timestamp": conv['timestamp'],
                    "flag_found": bool(conv['flag_found']),
                    "user_info": {
                        "ip": conv['user_ip'] or 'unknown',
                        "user_agent": conv['user_agent'] or 'unknown'
                    },
                    "messages": [
                        {
                            "type": msg['message_type'],
                            "content": msg['content'],
                            "timestamp": msg['timestamp']
                        }
                        for msg in messages
                    ]
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la conversation {conversation_id}: {e}")
            return None

# Instance globale de la base de données
db = ConversationDB()
