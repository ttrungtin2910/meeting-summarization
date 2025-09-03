#!/usr/bin/env python3
"""
Test script for persistent audio file storage
"""

import asyncio
import os
import requests
import time
from pathlib import Path

# Test configuration
API_BASE = "http://localhost:8000"
TEST_FILE_PATH = "test_audio_small.mp3"

def create_small_test_audio():
    """Create a very small test audio file"""
    # Create a minimal MP3-like file for testing
    test_content = b'\xFF\xFB\x90\x00' + b'Test audio content for persistent storage check. ' * 50
    
    with open(TEST_FILE_PATH, 'wb') as f:
        f.write(test_content)
    
    print(f"✅ Created small test audio: {TEST_FILE_PATH} ({len(test_content)} bytes)")
    return TEST_FILE_PATH

def test_persistent_storage():
    """Test that audio files are saved to persistent storage"""
    print("🧪 Testing Persistent Audio Storage")
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
        
        # Upload file using sync endpoint
        print(f"\n📤 Uploading {TEST_FILE_PATH} to sync endpoint...")
        
        with open(TEST_FILE_PATH, 'rb') as f:
            files = {'file': (TEST_FILE_PATH, f, 'audio/mpeg')}
            
            response = requests.post(
                f"{API_BASE}/api/v1/process-audio",
                files=files,
                timeout=60  # Longer timeout for OpenAI processing
            )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload and processing successful!")
            print(f"📋 Task ID: {result.get('task_id', 'N/A')}")
            print(f"📝 Summary length: {len(result.get('summary', ''))}")
            
            # Check for persistent file path
            audio_file_path = result.get('audio_file_path')
            if audio_file_path:
                print(f"🎵 Audio file saved at: {audio_file_path}")
                
                # Verify file exists
                if os.path.exists(audio_file_path):
                    file_size = os.path.getsize(audio_file_path)
                    print(f"✅ Persistent file verified: {file_size} bytes")
                    
                    # Show directory contents
                    persistent_dir = Path("processed_audio_files")
                    if persistent_dir.exists():
                        files = list(persistent_dir.glob("*"))
                        print(f"📁 Files in persistent storage: {len(files)}")
                        for file in files:
                            print(f"   - {file.name} ({os.path.getsize(file)} bytes)")
                    
                    return True
                else:
                    print(f"❌ Persistent file not found: {audio_file_path}")
                    return False
            else:
                print("❌ No audio_file_path in response")
                return False
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
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
    """Run persistent storage test"""
    try:
        success = test_persistent_storage()
        
        if success:
            print("\n🎉 Persistent storage test passed!")
            print("📁 Audio files are now saved for inspection.")
        else:
            print("\n❌ Persistent storage test failed!")
        
        return success
        
    finally:
        cleanup()

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
