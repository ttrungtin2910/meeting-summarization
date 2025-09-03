#!/usr/bin/env python3
"""
Test script for API upload functionality
"""

import asyncio
import sys
from pathlib import Path
import requests
import time
import json

# Test configuration
API_BASE = "http://localhost:8000"
TEST_FILE_PATH = "test_audio.mp3"

def create_test_audio_file():
    """Create a small test audio file"""
    # Create a simple MP3-like file for testing
    # This is not a real MP3, but will test the upload mechanism
    test_content = b'\xFF\xFB\x90\x00' + b'A' * 1000  # Fake MP3 header + data
    
    with open(TEST_FILE_PATH, 'wb') as f:
        f.write(test_content)
    
    print(f"✅ Created test audio file: {TEST_FILE_PATH} ({len(test_content)} bytes)")
    return TEST_FILE_PATH

def test_api_health():
    """Test if API is running"""
    try:
        response = requests.get(f"{API_BASE}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and accessible")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def test_sync_upload():
    """Test synchronous upload endpoint"""
    print("\n🔍 Testing synchronous upload (/api/v1/process-audio)...")
    
    if not Path(TEST_FILE_PATH).exists():
        create_test_audio_file()
    
    try:
        with open(TEST_FILE_PATH, 'rb') as f:
            files = {'file': (TEST_FILE_PATH, f, 'audio/mpeg')}
            
            print(f"📤 Uploading {TEST_FILE_PATH}...")
            response = requests.post(
                f"{API_BASE}/api/v1/process-audio",
                files=files,
                timeout=30
            )
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📄 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Synchronous upload successful!")
            print(f"📋 Task ID: {result.get('task_id', 'N/A')}")
            print(f"📝 Summary length: {len(result.get('summary', ''))}")
            return True
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_async_upload():
    """Test asynchronous upload endpoint"""
    print("\n🔍 Testing asynchronous upload (/api/v1/upload-audio)...")
    
    if not Path(TEST_FILE_PATH).exists():
        create_test_audio_file()
    
    try:
        with open(TEST_FILE_PATH, 'rb') as f:
            files = {'file': (TEST_FILE_PATH, f, 'audio/mpeg')}
            
            print(f"📤 Uploading {TEST_FILE_PATH}...")
            response = requests.post(
                f"{API_BASE}/api/v1/upload-audio",
                files=files,
                timeout=30
            )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get('task_id')
            print("✅ Asynchronous upload successful!")
            print(f"📋 Task ID: {task_id}")
            
            # Poll for status
            if task_id:
                return poll_task_status(task_id)
            
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def poll_task_status(task_id, max_polls=10):
    """Poll task status until completion"""
    print(f"\n⏳ Polling task status: {task_id}")
    
    for i in range(max_polls):
        try:
            response = requests.get(f"{API_BASE}/api/v1/tasks/{task_id}/status")
            
            if response.status_code == 200:
                status = response.json()
                current_status = status.get('status', 'unknown')
                progress = status.get('progress', 0)
                
                print(f"📊 Poll {i+1}: Status={current_status}, Progress={progress}%")
                
                if current_status == 'completed':
                    print("✅ Task completed successfully!")
                    return True
                elif current_status == 'failed':
                    print(f"❌ Task failed: {status.get('message', 'Unknown error')}")
                    return False
                
            elif response.status_code == 404:
                print(f"❌ Task not found (404)")
                return False
            else:
                print(f"❌ Status check failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking status: {e}")
        
        if i < max_polls - 1:  # Don't sleep after last iteration
            time.sleep(2)
    
    print("⏰ Polling timeout - task may still be processing")
    return False

def cleanup():
    """Clean up test files"""
    try:
        if Path(TEST_FILE_PATH).exists():
            Path(TEST_FILE_PATH).unlink()
            print(f"🧹 Cleaned up test file: {TEST_FILE_PATH}")
    except Exception as e:
        print(f"⚠️ Could not clean up test file: {e}")

def main():
    """Run all API tests"""
    print("🧪 Meeting Summary API - Upload Test")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API is not running or accessible")
        print("💡 Make sure to run: python main.py")
        return False
    
    tests = [
        ("Async Upload Test", test_async_upload),
        ("Sync Upload Test", test_sync_upload),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed!")
            else:
                print(f"❌ {test_name} failed!")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    cleanup()
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed! Upload functionality is working.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
