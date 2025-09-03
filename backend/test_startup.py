#!/usr/bin/env python3
"""
Test script to check if FastAPI app can start without errors
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

def test_imports():
    """Test if all imports work correctly"""
    print("🔍 Testing imports...")
    
    try:
        from meeting_summary.config import api_config, openai_config
        print("✅ Config imports successful")
        
        from meeting_summary.api.router import router
        print("✅ Router import successful")
        
        from meeting_summary.api.dependencies.service_dependencies import get_audio_processing_service
        print("✅ Service dependencies import successful")
        
        from meeting_summary.api.schemas.audio_processing import AudioUploadResponse
        print("✅ Schema imports successful")
        
        from meeting_summary.domain.models.audio_task import AudioTask
        print("✅ Domain models import successful")
        
        from meeting_summary.infrastructure.openai_client.openai_service import OpenAIService
        print("✅ OpenAI service import successful")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_fastapi_app():
    """Test if FastAPI app can be created without errors"""
    print("\n🚀 Testing FastAPI app creation...")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from meeting_summary.api.router import router
        from meeting_summary.config import api_config
        
        app = FastAPI(
            title="Meeting Summary API",
            description="AI-powered meeting summary from audio files using OpenAI Speech-to-Text",
            version="1.0.0"
        )
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=api_config.allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        app.include_router(router)
        
        print("✅ FastAPI app created successfully!")
        print(f"📋 Routes registered: {len(app.routes)}")
        
        # Print available routes
        print("\n📍 Available routes:")
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                methods = ', '.join(route.methods) if route.methods else 'N/A'
                print(f"  {methods}: {route.path}")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI app creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependency_injection():
    """Test dependency injection"""
    print("\n🔧 Testing dependency injection...")
    
    try:
        from meeting_summary.api.dependencies.service_dependencies import (
            get_audio_processing_service,
            get_openai_service,
            get_file_storage
        )
        
        # Test service creation
        openai_service = get_openai_service()
        print("✅ OpenAI service created")
        
        file_storage = get_file_storage()
        print("✅ File storage created")
        
        audio_service = get_audio_processing_service()
        print("✅ Audio processing service created")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependency injection error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Meeting Summary Backend - Startup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("FastAPI App Test", test_fastapi_app),
        ("Dependency Injection Test", test_dependency_injection),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to start.")
        print("\n🚀 You can now run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
