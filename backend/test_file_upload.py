#!/usr/bin/env python3
"""
Test script for file upload functionality
"""

import sys
from pathlib import Path
import asyncio
import tempfile
import uuid

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

async def test_file_storage():
    """Test file storage functionality"""
    print("🔧 Testing file storage...")
    
    try:
        from meeting_summary.infrastructure.storage.file_storage import FileStorage
        from fastapi import UploadFile
        import io
        
        # Create a mock UploadFile
        test_content = b"This is a test audio file content"
        test_file = UploadFile(
            filename="test_audio.mp3",
            file=io.BytesIO(test_content)
        )
        
        # Test file storage
        storage = FileStorage()
        task_id = uuid.uuid4()
        
        print(f"📁 Testing file save for task {task_id}")
        file_path = await storage.save_file(test_file, task_id)
        print(f"✅ File saved to: {file_path}")
        
        # Check if file exists and has correct content
        with open(file_path, 'rb') as f:
            saved_content = f.read()
        
        if saved_content == test_content:
            print("✅ File content matches original")
        else:
            print("❌ File content mismatch")
            return False
            
        # Cleanup
        await storage.cleanup_file(file_path)
        print("✅ File cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ File storage test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_audio_service():
    """Test audio processing service creation"""
    print("\n🎵 Testing audio processing service...")
    
    try:
        from meeting_summary.application.services.audio_processing_service import AudioProcessingService
        from meeting_summary.infrastructure.openai_client.openai_service import OpenAIService
        from meeting_summary.infrastructure.storage.file_storage import FileStorage
        
        # Create services
        openai_service = OpenAIService()
        file_storage = FileStorage()
        audio_service = AudioProcessingService(openai_service, file_storage)
        
        print("✅ Audio processing service created successfully")
        print(f"📊 Current tasks in memory: {len(audio_service.tasks)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🧪 Meeting Summary - File Upload Test")
    print("=" * 50)
    
    tests = [
        ("File Storage Test", test_file_storage),
        ("Audio Service Test", test_audio_service),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if await test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! File upload should work correctly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
