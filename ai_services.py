import requests
import json
import logging
from typing import Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class AIServiceManager:
    """Manages AI services including OpenAI, Gemini, and voice AI"""
    
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
        self.gemini_api_key = Config.GEMINI_API_KEY
        self.elevenlabs_api_key = Config.ELEVENLABS_API_KEY
        self.preferred_provider = Config.get_ai_provider()
        
        # API URLs
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech"
    
    def get_chat_response(self, prompt: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Get AI chat response using the best available provider"""
        
        if self.preferred_provider == 'openai':
            return self._call_openai(prompt, context)
        elif self.preferred_provider == 'gemini':
            return self._call_gemini(prompt, context)
        else:
            return self._get_fallback_response(prompt)
    
    def _call_openai(self, prompt: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Call OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            messages = [
                {
                    "role": "system",
                    "content": """You are AdmitAI, a comprehensive college admission assistant for MHT-CET, JEE Main, and BITSAT exams. 
                    
                    Provide detailed, helpful responses about:
                    1. College admissions and cutoff trends
                    2. Exam preparation strategies
                    3. Course recommendations based on scores
                    4. Fee structure and scholarship information
                    5. Placement statistics and career guidance
                    6. Hostel facilities and campus life
                    7. Application procedures and deadlines
                    
                    Focus on Maharashtra colleges for MHT-CET, but also cover national colleges for JEE Main and BITSAT.
                    Include specific cutoff data, fee breakdowns, and placement information when relevant.
                    Keep responses informative but concise."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(self.openai_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return None
    
    def _call_gemini(self, prompt: str, context: Dict[str, Any] = None) -> Optional[str]:
        """Call Gemini API"""
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            enhanced_prompt = f"""You are AdmitAI, a comprehensive college admission assistant for MHT-CET, JEE Main, and BITSAT exams.
            
            User Question: "{prompt}"
            
            Provide detailed, helpful responses about:
            1. College admissions and cutoff trends
            2. Exam preparation strategies
            3. Course recommendations based on scores
            4. Fee structure and scholarship information
            5. Placement statistics and career guidance
            6. Hostel facilities and campus life
            7. Application procedures and deadlines
            
            Focus on Maharashtra colleges for MHT-CET, but also cover national colleges for JEE Main and BITSAT.
            Include specific cutoff data, fee breakdowns, and placement information when relevant.
            Keep responses informative but concise. Current year: 2025"""
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": enhanced_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048
                }
            }
            
            response = requests.post(
                f"{self.gemini_url}?key={self.gemini_api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    logger.error(f"Unexpected Gemini API response structure: {result}")
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                
            return None
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return None
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Provide fallback response when no AI service is available"""
        fallback_responses = {
            "cutoff": "For current cutoff information, please check the college details page. Generally, top colleges like COEP require 95+ percentile, while good colleges require 85+ percentile.",
            "fees": "Fee structure varies by college and category. Government colleges typically charge ₹1-2L per year, while private colleges charge ₹2-5L per year. Reserved categories get fee concessions.",
            "placement": "Top colleges like COEP, VJTI have excellent placements with packages ranging from 10-50 LPA. Private colleges also have good placement records with major IT companies.",
            "hostel": "Most colleges provide hostel facilities. Boys and girls hostels are separate with fees ranging from ₹40K-80K per year including mess charges.",
            "default": "I'm currently unable to process your request due to AI service configuration. Please check the college listings for detailed information or contact the college directly."
        }
        
        prompt_lower = prompt.lower()
        for key, response in fallback_responses.items():
            if key in prompt_lower:
                return response
        
        return fallback_responses["default"]
    
    def generate_voice_response(self, text: str, voice_id: str = "default") -> Optional[bytes]:
        """Generate voice response using ElevenLabs"""
        if not self.elevenlabs_api_key:
            return None
        
        try:
            headers = {
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
                'xi-api-key': self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(
                f"{self.elevenlabs_url}/{voice_id}",
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"ElevenLabs API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling ElevenLabs API: {e}")
            return None
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all AI services"""
        return {
            "openai_available": bool(self.openai_api_key),
            "gemini_available": bool(self.gemini_api_key),
            "elevenlabs_available": bool(self.elevenlabs_api_key),
            "preferred_provider": self.preferred_provider,
            "voice_ai_available": Config.has_voice_ai(),
            "automation_available": Config.has_automation()
        }

# Global instance
ai_service = AIServiceManager()