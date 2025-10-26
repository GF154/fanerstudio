#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for cloud storage functionality
"""

import os
from pathlib import Path
from utils.cloud_storage import upload_to_gcs, download_from_gcs

def test_cloud_storage():
    """Test basic cloud storage operations"""
    
    # Check environment variable
    bucket = os.getenv("GCS_BUCKET_NAME")
    
    if not bucket:
        print("❌ GCS_BUCKET_NAME pa defini / not defined")
        print("   Defini l ak / Set it with:")
        print("   export GCS_BUCKET_NAME=your-bucket-name")
        return False
    
    print(f"✅ Bucket configured: {bucket}")
    
    # Create test file
    test_file = "test_upload.txt"
    test_content = "Tèst Google Cloud Storage\nThis is a test file for GCS"
    
    try:
        # Write test file
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        print(f"✅ Test file created: {test_file}")
        
        # Upload to GCS
        print(f"\n📤 Uploading to GCS...")
        upload_to_gcs(test_file, f"test/{test_file}", bucket)
        
        # Download from GCS
        download_file = "test_download.txt"
        print(f"\n📥 Downloading from GCS...")
        download_from_gcs(f"test/{test_file}", download_file, bucket)
        
        # Verify content
        with open(download_file, "r", encoding="utf-8") as f:
            downloaded_content = f.read()
        
        if downloaded_content == test_content:
            print(f"✅ Content verified - Upload/Download successful!")
            
            # Cleanup
            Path(test_file).unlink()
            Path(download_file).unlink()
            print(f"\n🧹 Cleaned up test files")
            
            return True
        else:
            print(f"❌ Content mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        # Cleanup on error
        for file in [test_file, "test_download.txt"]:
            if Path(file).exists():
                Path(file).unlink()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TÈS CLOUD STORAGE / CLOUD STORAGE TEST")
    print("=" * 60)
    print()
    
    success = test_cloud_storage()
    
    print()
    print("=" * 60)
    if success:
        print("🎉 Tout tèst pase / All tests passed!")
    else:
        print("❌ Tèst echwe / Tests failed")
    print("=" * 60)

