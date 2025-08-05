import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///college_finder.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    
    # AI API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    # Voice AI Services
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
    VAPI_API_KEY = os.environ.get('VAPI_API_KEY')
    RETELL_AI_API_KEY = os.environ.get('RETELL_AI_API_KEY')
    BLAND_AI_API_KEY = os.environ.get('BLAND_AI_API_KEY')
    
    # Database
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/mht_cet_admissions_top20'
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION') or 'us-east-1'
    
    # Workflow Automation
    N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')
    MAKE_WEBHOOK_URL = os.environ.get('MAKE_WEBHOOK_URL')
    
    # External Services
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    
    # Application Settings
    APP_NAME = os.environ.get('APP_NAME') or 'AdmitAI'
    APP_VERSION = os.environ.get('APP_VERSION') or '2.0.0'
    APP_URL = os.environ.get('APP_URL') or 'http://localhost:5000'
    FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://localhost:8000'
    
    @classmethod
    def get_ai_provider(cls):
        """Get the preferred AI provider based on available keys"""
        if cls.OPENAI_API_KEY:
            return 'openai'
        elif cls.GEMINI_API_KEY:
            return 'gemini'
        else:
            return None
    
    @classmethod
    def has_voice_ai(cls):
        """Check if voice AI services are configured"""
        return any([
            cls.ELEVENLABS_API_KEY,
            cls.VAPI_API_KEY,
            cls.RETELL_AI_API_KEY,
            cls.BLAND_AI_API_KEY
        ])
    
    @classmethod
    def has_automation(cls):
        """Check if automation services are configured"""
        return any([cls.N8N_WEBHOOK_URL, cls.MAKE_WEBHOOK_URL])
    
    @classmethod
    def is_aws_configured(cls):
        """Check if AWS is properly configured"""
        return all([cls.AWS_ACCESS_KEY_ID, cls.AWS_SECRET_ACCESS_KEY])

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}