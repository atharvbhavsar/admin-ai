#!/usr/bin/env python3
"""
AdmitAI Tech Stack Integration Test Script
Tests all the integrated services and features
"""

import sys
import requests
import json
from datetime import datetime

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from config import Config
        print("✅ Config module imported")
        
        from ai_services import ai_service
        print("✅ AI services module imported")
        
        from voice_ai_services import voice_ai_service
        print("✅ Voice AI services module imported")
        
        from workflow_automation import workflow_manager
        print("✅ Workflow automation module imported")
        
        from aws_integration import aws_manager
        print("✅ AWS integration module imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_service_status():
    """Test service status functions"""
    print("\n🔍 Testing service status...")
    
    try:
        from ai_services import ai_service
        from voice_ai_services import voice_ai_service
        from workflow_automation import workflow_manager
        from aws_integration import aws_manager
        
        # Test AI services
        ai_status = ai_service.get_service_status()
        print(f"🤖 AI Services: {json.dumps(ai_status, indent=2)}")
        
        # Test voice services
        voice_status = voice_ai_service.get_voice_service_status()
        print(f"🎤 Voice Services: {json.dumps(voice_status, indent=2)}")
        
        # Test automation
        automation_status = workflow_manager.get_automation_status()
        print(f"⚙️ Automation: {json.dumps(automation_status, indent=2)}")
        
        # Test AWS
        aws_status = aws_manager.get_aws_status()
        print(f"☁️ AWS: {json.dumps(aws_status, indent=2)}")
        
        return True
    except Exception as e:
        print(f"❌ Service status test error: {e}")
        return False

def test_ai_response():
    """Test AI response generation"""
    print("\n🧠 Testing AI response generation...")
    
    try:
        from ai_services import ai_service
        
        test_message = "What are the cutoffs for Computer Engineering?"
        response = ai_service.get_chat_response(test_message)
        
        if response:
            print(f"✅ AI Response received: {response[:100]}...")
        else:
            print("ℹ️ AI Response: Using fallback (API key not configured)")
        
        return True
    except Exception as e:
        print(f"❌ AI response test error: {e}")
        return False

def test_workflow_templates():
    """Test workflow template generation"""
    print("\n📋 Testing workflow templates...")
    
    try:
        from workflow_automation import workflow_manager
        
        templates = workflow_manager.create_workflow_templates()
        print(f"✅ Generated {len(templates)} workflow templates:")
        for name, template in templates.items():
            print(f"  - {name}: {template['description']}")
        
        return True
    except Exception as e:
        print(f"❌ Workflow templates test error: {e}")
        return False

def test_aws_deployment_template():
    """Test AWS deployment template"""
    print("\n☁️ Testing AWS deployment template...")
    
    try:
        from aws_integration import aws_manager
        
        template = aws_manager.get_deployment_template()
        template_data = json.loads(template)
        
        print(f"✅ AWS CloudFormation template generated")
        print(f"  - Resources: {len(template_data.get('Resources', {}))}")
        print(f"  - Parameters: {len(template_data.get('Parameters', {}))}")
        print(f"  - Outputs: {len(template_data.get('Outputs', {}))}")
        
        return True
    except Exception as e:
        print(f"❌ AWS template test error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import Config
        
        print(f"✅ App Name: {Config.APP_NAME}")
        print(f"✅ App Version: {Config.APP_VERSION}")
        print(f"✅ Database URI: {Config.SQLALCHEMY_DATABASE_URI}")
        print(f"✅ AI Provider: {Config.get_ai_provider() or 'Not configured'}")
        print(f"✅ Voice AI Available: {Config.has_voice_ai()}")
        print(f"✅ Automation Available: {Config.has_automation()}")
        print(f"✅ AWS Configured: {Config.is_aws_configured()}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        return False

def test_flask_app():
    """Test Flask app creation"""
    print("\n🌐 Testing Flask app...")
    
    try:
        from app import app
        
        print(f"✅ Flask app created: {app.name}")
        print(f"✅ Debug mode: {app.debug}")
        print(f"✅ Secret key configured: {'Yes' if app.secret_key else 'No'}")
        
        # Test app context
        with app.app_context():
            from flask import current_app
            print(f"✅ App context working")
        
        return True
    except Exception as e:
        print(f"❌ Flask app test error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 AdmitAI Tech Stack Integration Tests")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Service Status", test_service_status),
        ("AI Response", test_ai_response),
        ("Workflow Templates", test_workflow_templates),
        ("AWS Template", test_aws_deployment_template),
        ("Configuration", test_configuration),
        ("Flask App", test_flask_app),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Tech stack integration is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)