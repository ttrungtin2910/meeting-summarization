#!/usr/bin/env python3
"""
Test với real audio file để kiểm tra persistent storage
"""

import os
import requests
import time
from pathlib import Path

# Test configuration
API_BASE = "http://localhost:8000"

def find_real_audio_file():
    """Tìm file audio thật trong hệ thống"""
    # Tìm trong các thư mục common
    search_paths = [
        ".",
        "..",
        "../../",
        Path.home() / "Downloads",
        Path.home() / "Music",
        Path.home() / "Documents",
    ]
    
    audio_extensions = ['.mp3', '.wav', '.m4a', '.mp4', '.webm', '.flac']
    
    for search_path in search_paths:
        try:
            path = Path(search_path)
            if path.exists():
                for ext in audio_extensions:
                    audio_files = list(path.glob(f"*{ext}"))
                    if audio_files:
                        # Lấy file nhỏ nhất để test nhanh
                        smallest_file = min(audio_files, key=lambda x: x.stat().st_size if x.exists() else float('inf'))
                        if smallest_file.stat().st_size > 0 and smallest_file.stat().st_size < 50 * 1024 * 1024:  # < 50MB
                            return str(smallest_file)
        except Exception as e:
            continue
    
    return None

def test_with_real_audio():
    """Test persistent storage với real audio file"""
    print("🧪 Testing Persistent Storage with Real Audio")
    print("=" * 50)
    
    # Tìm real audio file
    audio_file = find_real_audio_file()
    
    if not audio_file:
        print("❌ No suitable audio file found in common locations")
        print("💡 Please place a small audio file (.mp3, .wav, etc.) in current directory")
        return False
    
    print(f"📁 Found audio file: {audio_file}")
    file_size = os.path.getsize(audio_file)
    print(f"📊 File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    
    if file_size > 25 * 1024 * 1024:  # 25MB limit
        print("⚠️ File too large (>25MB), but proceeding anyway...")
    
    try:
        # Check API health
        response = requests.get(f"{API_BASE}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ API not running. Start with: python main.py")
            return False
        
        print("✅ API is running")
        
        # Upload using async endpoint (better for larger files)
        print(f"\n📤 Uploading to async endpoint...")
        
        with open(audio_file, 'rb') as f:
            files = {'file': (Path(audio_file).name, f, 'audio/mpeg')}
            
            upload_response = requests.post(
                f"{API_BASE}/api/v1/upload-audio",
                files=files,
                timeout=30
            )
        
        print(f"📊 Upload response: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            task_id = upload_result.get('task_id')
            print(f"✅ Upload successful! Task ID: {task_id}")
            
            # Poll for completion
            print("\n⏳ Waiting for processing to complete...")
            
            for i in range(30):  # Wait up to 5 minutes
                try:
                    status_response = requests.get(f"{API_BASE}/api/v1/tasks/{task_id}/status", timeout=5)
                    
                    if status_response.status_code == 200:
                        status = status_response.json()
                        current_status = status.get('status', 'unknown')
                        progress = status.get('progress', 0)
                        
                        print(f"📊 Status: {current_status} ({progress}%)")
                        
                        if current_status == 'completed':
                            print("✅ Processing completed!")
                            
                            # Check persistent storage
                            persistent_dir = Path("processed_audio_files")
                            if persistent_dir.exists():
                                files = list(persistent_dir.glob("*"))
                                print(f"\n📁 Files in persistent storage: {len(files)}")
                                
                                for file in files:
                                    if str(task_id) in file.name:
                                        file_size = os.path.getsize(file)
                                        print(f"🎵 Found saved audio: {file.name} ({file_size:,} bytes)")
                                        print(f"📂 Full path: {file.absolute()}")
                                        return True
                                
                                print("⚠️ Task completed but no matching file found in persistent storage")
                                # List all files for debugging
                                for file in files:
                                    print(f"   - {file.name}")
                                return False
                            else:
                                print("❌ Persistent storage directory not found")
                                return False
                                
                        elif current_status == 'failed':
                            error_msg = status.get('message', 'Unknown error')
                            print(f"❌ Processing failed: {error_msg}")
                            return False
                        
                    elif status_response.status_code == 404:
                        print(f"❌ Task not found (404) - may have been cleaned up")
                        return False
                    else:
                        print(f"⚠️ Status check failed: {status_response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Error checking status: {e}")
                
                if i < 29:  # Don't sleep on last iteration
                    time.sleep(10)  # Wait 10 seconds between checks
            
            print("⏰ Timeout waiting for completion")
            return False
            
        else:
            print(f"❌ Upload failed: {upload_response.status_code}")
            print(f"Response: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run the real audio test"""
    try:
        success = test_with_real_audio()
        
        if success:
            print("\n🎉 Persistent storage test with real audio passed!")
            print("📁 Audio file saved for inspection.")
        else:
            print("\n❌ Persistent storage test failed!")
        
        return success
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
