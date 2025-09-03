#!/usr/bin/env python3
"""
Test script for new transcription API endpoints
"""

import requests
import time
from pathlib import Path

# Test configuration
API_BASE = "http://localhost:8000"
TEST_FILE_PATH = "test_small_audio.mp3"

def create_small_test_audio():
    """Create a small test audio file"""
    test_content = b'\xFF\xFB\x90\x00' + b'Test audio for transcription only. ' * 20
    
    with open(TEST_FILE_PATH, 'wb') as f:
        f.write(test_content)
    
    print(f"✅ Created test audio: {TEST_FILE_PATH} ({len(test_content)} bytes)")
    return TEST_FILE_PATH

def test_transcription_endpoint():
    """Test the new transcription-only endpoint"""
    print("🧪 Testing Transcription-Only Endpoint")
    print("=" * 50)
    
    # Create test file
    if not Path(TEST_FILE_PATH).exists():
        create_small_test_audio()
    
    try:
        # Check if API is running
        health_response = requests.get(f"{API_BASE}/docs", timeout=5)
        if health_response.status_code != 200:
            print("❌ API is not running. Start with: python main.py")
            return False
        
        print("✅ API is running")
        
        # Test new transcription endpoint
        print(f"\n📤 Testing transcription endpoint...")
        print(f"URL: {API_BASE}/transcription/transcribe")
        
        with open(TEST_FILE_PATH, 'rb') as f:
            files = {'file': (TEST_FILE_PATH, f, 'audio/mpeg')}
            
            response = requests.post(
                f"{API_BASE}/transcription/transcribe",
                files=files,
                timeout=60
            )
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📄 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transcription endpoint working!")
            print(f"📋 Task ID: {result.get('task_id', 'N/A')}")
            print(f"📝 Transcription length: {len(result.get('transcription', ''))}")
            print(f"🌐 Language: {result.get('transcription_language', 'N/A')}")
            
            task_id = result.get('task_id')
            if task_id:
                # Test summary creation from transcription
                print(f"\n🔄 Testing summary creation...")
                summary_response = requests.post(
                    f"{API_BASE}/transcription/summarize/{task_id}",
                    timeout=30
                )
                
                print(f"📊 Summary response status: {summary_response.status_code}")
                
                if summary_response.status_code == 200:
                    summary_result = summary_response.json()
                    print("✅ Summary creation working!")
                    print(f"📝 Summary length: {len(summary_result.get('summary', ''))}")
                    print(f"🔑 Key points: {len(summary_result.get('key_points', []))}")
                    print(f"✅ Action items: {len(summary_result.get('action_items', []))}")
                    return True
                else:
                    print(f"❌ Summary creation failed: {summary_response.status_code}")
                    print(f"📄 Response: {summary_response.text}")
                    return False
            
        else:
            print(f"❌ Transcription failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_available_endpoints():
    """Test which endpoints are available"""
    print("\n🔍 Testing Available Endpoints")
    print("=" * 50)
    
    endpoints_to_test = [
        "/transcription/transcribe",
        "/api/v1/upload-audio", 
        "/api/v1/process-audio",
        "/docs",
        "/openapi.json"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            url = f"{API_BASE}{endpoint}"
            response = requests.get(url, timeout=5)
            status = "✅" if response.status_code == 200 else "❌" if response.status_code == 404 else "⚠️"
            print(f"{status} {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")

def cleanup():
    """Clean up test files"""
    try:
        if Path(TEST_FILE_PATH).exists():
            Path(TEST_FILE_PATH).unlink()
            print(f"🧹 Cleaned up test file: {TEST_FILE_PATH}")
    except Exception as e:
        print(f"⚠️ Could not clean up test file: {e}")

def main():
    """Run transcription API tests"""
    try:
        # Test available endpoints first
        test_available_endpoints()
        
        # Test transcription workflow
        success = test_transcription_endpoint()
        
        if success:
            print("\n🎉 New transcription workflow test passed!")
            print("✅ Two-step process working: Transcription → Manual Summary")
        else:
            print("\n❌ Transcription workflow test failed!")
        
        return success
        
    finally:
        cleanup()

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
