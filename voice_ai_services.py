import requests
import json
import logging
from typing import Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class VoiceAIManager:
    """Manages voice AI services including Vapi, Retell AI, and Bland AI"""
    
    def __init__(self):
        self.vapi_api_key = Config.VAPI_API_KEY
        self.retell_api_key = Config.RETELL_AI_API_KEY
        self.bland_api_key = Config.BLAND_AI_API_KEY
        
        # API URLs
        self.vapi_url = "https://api.vapi.ai/call"
        self.retell_url = "https://api.retellai.com/v2"
        self.bland_url = "https://api.bland.ai/v1"
    
    def create_voice_assistant(self, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a voice assistant with the best available provider"""
        
        if self.vapi_api_key:
            return self._create_vapi_assistant(config)
        elif self.retell_api_key:
            return self._create_retell_assistant(config)
        elif self.bland_api_key:
            return self._create_bland_assistant(config)
        else:
            return None
    
    def _create_vapi_assistant(self, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create assistant using Vapi"""
        try:
            headers = {
                'Authorization': f'Bearer {self.vapi_api_key}',
                'Content-Type': 'application/json'
            }
            
            assistant_config = {
                "name": "AdmitAI Voice Assistant",
                "firstMessage": "Hello! I'm AdmitAI, your college admission assistant. How can I help you today?",
                "systemMessage": """You are AdmitAI, a helpful college admission assistant specializing in Indian engineering colleges, particularly for MHT-CET, JEE Main, and BITSAT exams.

                Key areas you help with:
                1. College recommendations based on scores and preferences
                2. Cutoff trends and admission probability
                3. Fee structure and scholarship information
                4. Placement statistics and career guidance
                5. Exam preparation strategies
                6. Hostel facilities and campus life
                7. Application procedures and deadlines

                Always be encouraging, provide specific data when possible, and ask clarifying questions to give better recommendations.""",
                "model": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7,
                    "maxTokens": 500
                },
                "voice": {
                    "provider": "11labs",
                    "voiceId": "default"
                },
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-2",
                    "language": "en-IN"
                }
            }
            
            # Override with custom config
            assistant_config.update(config)
            
            response = requests.post(
                f"{self.vapi_url}/assistant",
                headers=headers,
                json=assistant_config,
                timeout=30
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                logger.error(f"Vapi API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating Vapi assistant: {e}")
            return None
    
    def _create_retell_assistant(self, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create assistant using Retell AI"""
        try:
            headers = {
                'Authorization': f'Bearer {self.retell_api_key}',
                'Content-Type': 'application/json'
            }
            
            assistant_config = {
                "agent_name": "AdmitAI Assistant",
                "voice_id": "default",
                "language": "en",
                "response_engine": {
                    "type": "openai_gpt",
                    "llm_id": "gpt-3.5-turbo"
                },
                "llm_websocket_url": None,
                "begin_message": "Hello! I'm AdmitAI, your college admission assistant. How can I help you today?",
                "general_prompt": """You are AdmitAI, a helpful college admission assistant specializing in Indian engineering colleges.
                
                Help users with:
                - College recommendations based on their scores
                - Cutoff trends and admission chances
                - Fee structures and scholarships
                - Placement statistics
                - Exam preparation guidance
                
                Be encouraging and provide specific, actionable advice.""",
                "general_tools": [],
                "states": [
                    {
                        "name": "default",
                        "edges": []
                    }
                ]
            }
            
            assistant_config.update(config)
            
            response = requests.post(
                f"{self.retell_url}/create-agent",
                headers=headers,
                json=assistant_config,
                timeout=30
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                logger.error(f"Retell AI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating Retell AI assistant: {e}")
            return None
    
    def _create_bland_assistant(self, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create assistant using Bland AI"""
        try:
            headers = {
                'Authorization': f'Bearer {self.bland_api_key}',
                'Content-Type': 'application/json'
            }
            
            assistant_config = {
                "name": "AdmitAI Phone Assistant",
                "prompt": """You are AdmitAI, a helpful college admission assistant for Indian engineering students.
                
                Your expertise includes:
                - MHT-CET, JEE Main, and BITSAT exam guidance
                - College recommendations based on scores and preferences
                - Cutoff trends and admission probability calculations
                - Fee structures and scholarship opportunities
                - Placement statistics and career guidance
                - Exam preparation strategies
                
                Always be encouraging, ask relevant questions to understand the student's needs, and provide specific, actionable advice.""",
                "voice": "default",
                "language": "en",
                "max_duration": 10,
                "answered_by_enabled": True,
                "wait_for_greeting": True,
                "record": True
            }
            
            assistant_config.update(config)
            
            response = requests.post(
                f"{self.bland_url}/calls",
                headers=headers,
                json=assistant_config,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Bland AI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating Bland AI assistant: {e}")
            return None
    
    def start_voice_call(self, phone_number: str, assistant_id: str = None) -> Optional[Dict[str, Any]]:
        """Start a voice call using the available provider"""
        
        if self.bland_api_key:
            return self._start_bland_call(phone_number, assistant_id)
        elif self.vapi_api_key:
            return self._start_vapi_call(phone_number, assistant_id)
        else:
            return None
    
    def _start_bland_call(self, phone_number: str, assistant_id: str = None) -> Optional[Dict[str, Any]]:
        """Start a call using Bland AI"""
        try:
            headers = {
                'Authorization': f'Bearer {self.bland_api_key}',
                'Content-Type': 'application/json'
            }
            
            call_data = {
                "phone_number": phone_number,
                "task": "Provide college admission guidance and answer questions about engineering colleges, cutoffs, and exam preparation.",
                "voice": "default",
                "language": "en",
                "max_duration": 10,
                "answered_by_enabled": True,
                "wait_for_greeting": True,
                "record": True
            }
            
            if assistant_id:
                call_data["assistant_id"] = assistant_id
            
            response = requests.post(
                f"{self.bland_url}/calls",
                headers=headers,
                json=call_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Bland AI call error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error starting Bland AI call: {e}")
            return None
    
    def _start_vapi_call(self, phone_number: str, assistant_id: str = None) -> Optional[Dict[str, Any]]:
        """Start a call using Vapi"""
        try:
            headers = {
                'Authorization': f'Bearer {self.vapi_api_key}',
                'Content-Type': 'application/json'
            }
            
            call_data = {
                "phoneNumberId": phone_number,
                "assistantId": assistant_id or "default"
            }
            
            response = requests.post(
                f"{self.vapi_url}",
                headers=headers,
                json=call_data,
                timeout=30
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                logger.error(f"Vapi call error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error starting Vapi call: {e}")
            return None
    
    def get_voice_service_status(self) -> Dict[str, Any]:
        """Get status of all voice AI services"""
        return {
            "vapi_available": bool(self.vapi_api_key),
            "retell_available": bool(self.retell_api_key),
            "bland_available": bool(self.bland_api_key),
            "voice_calls_enabled": any([self.vapi_api_key, self.bland_api_key]),
            "voice_assistant_enabled": any([self.vapi_api_key, self.retell_api_key, self.bland_api_key])
        }

# Global instance
voice_ai_service = VoiceAIManager()