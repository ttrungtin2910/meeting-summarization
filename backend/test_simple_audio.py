#!/usr/bin/env python3
"""
Test simple audio với file giả để kiểm tra persistent storage logic
"""

import asyncio
import os
import tempfile
import uuid
from pathlib import Path

# Import các modules từ backend
import sys
sys.path.append('src')

from meeting_summary.infrastructure.storage.file_storage import FileStorage
from meeting_summary.infrastructure.storage.temp_file_handler import TempFileHandler

async def test_persistent_logic():
    """Test logic persistent storage trực tiếp"""
    print("🧪 Testing Persistent Storage Logic")
    print("=" * 50)
    
    try:
        # Tạo file storage instance
        file_storage = FileStorage()
        
        # Tạo fake audio content
        fake_audio_content = b'\xFF\xFB\x90\x00' + b'Fake audio for testing' * 100
        task_id = uuid.uuid4()
        filename = "test_audio.mp3"
        
        print(f"📁 Creating test content: {len(fake_audio_content)} bytes")
        print(f"🆔 Task ID: {task_id}")
        print(f"📄 Filename: {filename}")
        
        # Test save content
        print("\n1️⃣ Testing save_file_content...")
        temp_path = await file_storage.save_file_content(fake_audio_content, task_id, filename)
        print(f"✅ Temp file created: {temp_path}")
        
        # Verify temp file exists
        if os.path.exists(temp_path):
            temp_size = os.path.getsize(temp_path)
            print(f"✅ Temp file verified: {temp_size} bytes")
        else:
            print(f"❌ Temp file not found: {temp_path}")
            return False
        
        # Test move to persistent
        print("\n2️⃣ Testing move_to_persistent_storage...")
        persistent_path = await file_storage.move_to_persistent_storage(temp_path, task_id, filename)
        print(f"✅ Persistent file created: {persistent_path}")
        
        # Verify persistent file exists
        if os.path.exists(persistent_path):
            persistent_size = os.path.getsize(persistent_path)
            print(f"✅ Persistent file verified: {persistent_size} bytes")
            
            # Check directory contents
            persistent_dir = Path("processed_audio_files")
            if persistent_dir.exists():
                files = list(persistent_dir.glob("*"))
                print(f"\n📁 Persistent storage contents: {len(files)} files")
                for file in files:
                    file_size = os.path.getsize(file)
                    print(f"   - {file.name} ({file_size:,} bytes)")
                
                return True
            else:
                print("❌ Persistent directory not found")
                return False
        else:
            print(f"❌ Persistent file not found: {persistent_path}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

async def main():
    """Run the simple test"""
    try:
        success = await test_persistent_logic()
        
        if success:
            print("\n🎉 Persistent storage logic test passed!")
            print("✅ Files are being saved correctly for inspection.")
        else:
            print("\n❌ Persistent storage logic test failed!")
        
        return success
        
    except Exception as e:
        print(f"❌ Main test failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
