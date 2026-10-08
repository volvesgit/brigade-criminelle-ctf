import google.generativeai as genai
import openai
import tempfile
import os
import logging
from config import GEMINI_API_KEY, SYSTEM_PROMPT, TTS_PROVIDER, OPENAI_API_KEY, OPENAI_VOICE
import re

# Configuration du logging
logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self):
        # Configuration Gemini avec gestion d'erreur
        self.model = None
        try:
            if GEMINI_API_KEY and GEMINI_API_KEY.strip() and GEMINI_API_KEY != "":
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("✅ Gemini AI configuré avec succès")
            else:
                logger.warning("⚠️ Clé API Gemini manquante - Agent IA en mode dégradé")
        except Exception as e:
            logger.error(f"❌ Erreur configuration Gemini: {e}")
            self.model = None
        
        # Configuration TTS - Support multiple providers
        self.tts_provider = TTS_PROVIDER
        self.tts_client = None
        
        # Historique des conversations
        self.conversation_history = []
        
        # Etapes de la mission
        self.mission_steps = {
            'description_provided': False,
            'coordinates_provided': False,
            'field_report_given': False,
            'hobbies_detected': False
        }
        
        # Pattern pour détecter les hobbies
        self.hobbies_patterns = {
            'fishing': r'(?i)(pêche|pêcher|poisson|canne|ligne|hameçon)',
            'diving': r'(?i)(plongée|plonger|sous-marine|scaphandre|bouteille)',
            'hiking': r'(?i)(randonnée|randonner|marche|lever du soleil|aurore|montagne|sentier)'
        }
          # Patterns pour détecter description et coordonnées
        self.description_patterns = r'(?i)(grand|petit|chauve|barbe|cheveux|yeux|peau|taille|corpulence|âge|ans)'
        self.coordinates_patterns = r'(?i)(\d{1,2}\.\d+,?\s*\d{1,2}\.\d+)|(\d{1,2}°\d+\'.*\d{1,2}°\d+\')|(coordonn|gps|latitude|longitude)'
    
    def reset_conversation(self):
        """Reset conversation history and mission state"""
        self.conversation_history = []
        self.mission_steps = {
            'description_provided': False,
            'coordinates_provided': False,
            'field_report_given': False,
            'hobbies_detected': False
        }
        logger.info("Conversation reset - New mission started")
    
    def get_initial_greeting(self):
        """Message d'accueil initial du brigadier"""
        greeting = """Allô, Brigade de Police de Marseille, Brigadier à l'appareil. 
        
        J'ai reçu votre demande de mission concernant l'individu "Golf". Pour procéder à la reconnaissance sur le terrain, j'ai besoin que vous me fournissiez une description physique détaillée de cet individu ainsi que les coordonnées GPS précises du secteur à surveiller.
        
        Pouvez-vous me transmettre ces informations ?"""
        
        self.conversation_history.append({"role": "assistant", "content": greeting})
        return greeting
    
    def check_golf_hobbies(self, user_message):
        """Vérifie si les trois hobbies sont mentionnés dans le message"""
        detected_hobbies = []
        
        for hobby, pattern in self.hobbies_patterns.items():
            if re.search(pattern, user_message):
                detected_hobbies.append(hobby)
        
        # Vérifier si les 3 hobbies sont présents
        if len(detected_hobbies) >= 3:
            self.mission_steps['hobbies_detected'] = True
            return True, detected_hobbies
        
        return False, detected_hobbies
    
    def detect_hobbies(self, user_message):
        """Alias pour check_golf_hobbies pour compatibilité avec les tests"""
        return self.check_golf_hobbies(user_message)
    
    def check_description_and_coordinates(self, user_message):
        """Vérifie si description et coordonnées sont fournies"""
        has_description = False
        has_coordinates = False
        
        # Patterns pour description physique
        description_patterns = [
            r'(?i)(taille|cheveux|yeux|cicatrice|tatouage|corpulence|âge|barbe)',
            r'(?i)(grand|petit|brun|blond|mince|corpulent|jeune|vieux)',
            r'(?i)(mètre|cm|ans|année)'
        ]
        
        # Pattern pour coordonnées GPS
        coord_pattern = r'(?i)(\d{2}\.\d+,?\s*\d{1,2}\.\d+)|coordonnées|gps|latitude|longitude'
        
        for pattern in description_patterns:
            if re.search(pattern, user_message):
                has_description = True
                break
        
        if re.search(coord_pattern, user_message):
            has_coordinates = True
        if has_description:
            self.mission_steps['description_provided'] = True
        if has_coordinates:
            self.mission_steps['coordinates_provided'] = True
        
        return has_description, has_coordinates
    def generate_field_report(self):
        """Génère le rapport de terrain mentionnant Jules et ses hobbies"""
        report = """Très bien, j'ai les informations nécessaires. Je me rends immédiatement sur zone pour la reconnaissance.
        
        *Quelques minutes plus tard*
        
        Brigadier en rapport : Je suis positionné aux coordonnées indiquées, secteur de la Grotte Bleue. J'ai effectué la reconnaissance de l'individu "Golf" selon votre description.
        
        Observation terrain : Confirme la présence de l'individu "Golf", conforme à votre description. Il est en compagnie d'un associé prénommé Jules, la quarantaine, qui semble faire partie de la même organisation. D'après ce que j'ai pu observer discrètement, cet associé Jules a des activités régulières dans le secteur. Il pratique apparemment la pêche en mer depuis les rochers, fait de la plongée sous-marine dans les calanques, et d'après les habitants locaux, il aime faire des randonnées solitaires pour admirer le lever du soleil depuis les hauteurs.
        
        Dois-je poursuivre la surveillance ou avez-vous des instructions particulières concernant cet associé Jules ?"""
        self.mission_steps['field_report_given'] = True
        return report
    
    def detect_description(self, text):
        """Détecte si une description physique a été fournie"""
        return bool(re.search(self.description_patterns, text))
    def detect_coordinates(self, text):
        """Détecte si des coordonnées GPS ont été fournies"""
        return bool(re.search(self.coordinates_patterns, text))

    def update_mission_steps(self, user_input):
        """Met à jour les étapes de la mission basé sur l'input utilisateur"""
        if not self.mission_steps['description_provided'] and self.detect_description(user_input):
            self.mission_steps['description_provided'] = True
            logger.info("✅ Description physique détectée")
            
        if not self.mission_steps['coordinates_provided'] and self.detect_coordinates(user_input):
            self.mission_steps['coordinates_provided'] = True
            logger.info("✅ Coordonnées GPS détectées")

    def generate_victory_message(self):
        """Message de succès quand le joueur trouve le flag"""
        return """Excellent travail, enquêteur ! Vous avez parfaitement identifié les passions de l'associé : pêche, plongée, et randonnées au lever du soleil.
        
        MISSION VALIDÉE - FLAG TROUVÉ ! 
        L'identité de l'associé est confirmée : Jules Lefèvre.
        
        *Le Brigadier range ses affaires*
        *Fin de communication avec le central*
        *Coupure de la ligne radio - Mission terminée*
        
        Transmission interrompue."""
    
    def generate_response(self, user_message):
        """Génère une réponse contextuelle selon l'état de la mission"""
        try:
            # Mettre à jour les étapes de la mission d'abord
            self.update_mission_steps(user_message)
            
            # Ajouter le message utilisateur à l'historique
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Vérifier si le flag a été détecté
            hobbies_found, detected_hobbies = self.check_golf_hobbies(user_message)
            if hobbies_found and self.mission_steps['field_report_given']:
                response = self.generate_victory_message()
                self.conversation_history.append({"role": "assistant", "content": response})
                return {
                    'response': response,
                    'flag_found': True,
                    'mission_complete': True
                }
            
            # Si description et coordonnées fournies mais pas encore de rapport de terrain
            if (self.mission_steps['description_provided'] and 
                self.mission_steps['coordinates_provided'] and 
                not self.mission_steps['field_report_given']):
                response = self.generate_field_report()
                self.conversation_history.append({"role": "assistant", "content": response})
                return {
                    'response': response,
                    'flag_found': False,
                    'mission_complete': False
                }
              # Si description et coordonnées pas encore fournies, laisser Gemini répondre naturellement
            if not self.mission_steps['description_provided'] or not self.mission_steps['coordinates_provided']:
                missing = []
                if not self.mission_steps['description_provided']:
                    missing.append("description physique détaillée")
                if not self.mission_steps['coordinates_provided']: 
                    missing.append("coordonnées GPS")
                
                # Ajouter le contexte des informations manquantes pour Gemini
                missing_context = f"\n\nContexte mission: Il me manque encore {', '.join(missing)} pour procéder à la reconnaissance de l'individu 'Golf'."
              # Réponse générale avec Gemini ou fallback
            if self.model:
                try:
                    # Construire le contexte complet
                    full_context = SYSTEM_PROMPT + "\n\nHistorique de conversation:\n"
                    for msg in self.conversation_history[-10:]:  # Garder les 10 derniers messages
                        role = "Enquêteur Hackosint" if msg["role"] == "user" else "Brigadier"
                        full_context += f"{role}: {msg['content']}\n"
                    
                    # Ajouter le contexte des informations manquantes si applicable
                    if not self.mission_steps['description_provided'] or not self.mission_steps['coordinates_provided']:
                        missing = []
                        if not self.mission_steps['description_provided']:
                            missing.append("description physique détaillée")
                        if not self.mission_steps['coordinates_provided']: 
                            missing.append("coordonnées GPS")
                        full_context += f"\n\nContexte mission: Il me manque encore {', '.join(missing)} pour procéder à la reconnaissance de l'individu 'Golf'."
                    
                    full_context += f"\n\nEnquêteur Hackosint: {user_message}\nBrigadier:"
                    
                    gemini_response = self.model.generate_content(full_context)
                    response = gemini_response.text.strip()
                    
                    self.conversation_history.append({"role": "assistant", "content": response})
                    return {
                        'response': response,
                        'flag_found': False,
                        'mission_complete': False
                    }
                    
                except Exception as e:
                    logger.error(f"Erreur Gemini: {e}")
                    return self._fallback_response(user_message)
            else:
                return self._fallback_response(user_message)
                
        except Exception as e:
            logger.error(f"Erreur génération réponse: {e}")
            return {
                'response': "Désolé, problème technique momentané. Pouvez-vous répéter ?",
                'flag_found': False,
                'mission_complete': False
            }
    
    def _fallback_response(self, user_message):
        """Réponse de secours si Gemini n'est pas disponible"""
        fallback_responses = [
            "Brigadier en écoute, pouvez-vous préciser votre demande ?",
            "Bien reçu. Avez-vous d'autres éléments à me communiquer ?",
            "Entendu. Que souhaitez-vous que je vérifie sur le terrain ?",
            "Message reçu. Des instructions particulières ?"
        ]        
        import random
        response = random.choice(fallback_responses)
        self.conversation_history.append({"role": "assistant", "content": response})
        return {
            'response': response,
            'flag_found': False,
            'mission_complete': False
        }
    
    def text_to_speech(self, text):
        """Conversion texte vers audio avec gestion d'erreur"""
        try:
            if not text or text.strip() == "":
                logger.warning("Texte vide pour TTS")
                return None
            
            # Nettoyer le texte pour TTS - Plus agressif pour éviter les coupures
            clean_text = re.sub(r'[*_#`]', '', text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            
            # Remplacer les caractères problématiques
            clean_text = clean_text.replace('**', '')
            clean_text = clean_text.replace('*', '')
            clean_text = clean_text.replace('…', '...')
            clean_text = clean_text.replace('«', '"')
            clean_text = clean_text.replace('»', '"')
            
            # Diviser en segments plus courts pour éviter les coupures
            if len(clean_text) > 400:
                # Trouver une coupure naturelle
                sentences = clean_text.split('.')
                truncated = []
                current_length = 0
                
                for sentence in sentences:
                    if current_length + len(sentence) < 400:
                        truncated.append(sentence)
                        current_length += len(sentence)
                    else:
                        break
                
                clean_text = '. '.join(truncated)
                if not clean_text.endswith('.'):
                    clean_text += '.'
            
            logger.info(f"TTS text length: {len(clean_text)} chars")
            logger.info(f"TTS text preview: {clean_text[:100]}...")
            
            if self.tts_provider == "openai":
                if not OPENAI_API_KEY or OPENAI_API_KEY.strip() == "":
                    logger.warning("⚠️ Clé API OpenAI manquante pour TTS")
                    return None
                
                # Configuration OpenAI
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                
                # Générer l'audio avec OpenAI TTS
                response = client.audio.speech.create(
                    model="tts-1",
                    voice=OPENAI_VOICE,  # onyx pour voix masculine française
                    input=clean_text
                )
                
                # Sauvegarder dans un fichier temporaire
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    response.stream_to_file(tmp_file.name)
                    logger.info(f"TTS OpenAI généré: {tmp_file.name}")
                    return tmp_file.name
            else:
                logger.warning(f"Provider TTS non supporté: {self.tts_provider}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur TTS: {e}")
            return None
