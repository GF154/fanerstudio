#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Metadata Manager
Test Jesyon Metadone
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.metadata_manager import MetadataManager


def test_create_metadata():
    """Test metadata creation"""
    print("=" * 60)
    print("🧪 TEST 1: Create Metadata")
    print("=" * 60)
    
    manager = MetadataManager()
    
    metadata = manager.create_metadata(
        book_name="test_book",
        title="Test Book Title",
        author="Test Author",
        year=2024,
        genre="Test Genre"
    )
    
    # Verify required fields
    assert metadata['book_name'] == "test_book"
    assert metadata['title'] == "Test Book Title"
    assert metadata['author'] == "Test Author"
    assert 'created_at' in metadata
    assert 'version' in metadata
    
    print("✅ Metadata created successfully")
    print(f"   Book: {metadata['book_name']}")
    print(f"   Title: {metadata['title']}")
    print(f"   Author: {metadata['author']}")
    
    return True


def test_save_load_metadata():
    """Test saving and loading metadata"""
    print("\n" + "=" * 60)
    print("🧪 TEST 2: Save & Load Metadata")
    print("=" * 60)
    
    manager = MetadataManager()
    
    # Create and save
    metadata = manager.create_metadata(
        book_name="test_save_load",
        title="Test Save Load",
        author="Test Author"
    )
    
    manager.save_metadata(metadata, "test_save_load")
    print("✅ Metadata saved")
    
    # Load
    loaded = manager.load_metadata("test_save_load")
    
    if loaded:
        assert loaded['book_name'] == "test_save_load"
        assert loaded['title'] == "Test Save Load"
        print("✅ Metadata loaded successfully")
        return True
    else:
        print("❌ Failed to load metadata")
        return False


def test_add_processing_step():
    """Test adding processing steps"""
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Add Processing Steps")
    print("=" * 60)
    
    manager = MetadataManager()
    
    # Create metadata
    metadata = manager.create_metadata(
        book_name="test_steps",
        title="Test Steps",
        author="Test Author"
    )
    manager.save_metadata(metadata, "test_steps")
    
    # Add steps
    manager.add_processing_step("test_steps", "extraction", "completed")
    manager.add_processing_step("test_steps", "translation", "completed")
    manager.add_processing_step("test_steps", "audio", "completed")
    
    # Load and verify
    updated = manager.load_metadata("test_steps")
    
    if updated:
        steps = updated['processing']['steps_completed']
        assert len(steps) == 3
        assert steps[0]['name'] == "extraction"
        assert steps[1]['name'] == "translation"
        assert steps[2]['name'] == "audio"
        print(f"✅ Added {len(steps)} processing steps")
        return True
    else:
        print("❌ Failed to add steps")
        return False


def test_add_file_metadata():
    """Test adding file metadata"""
    print("\n" + "=" * 60)
    print("🧪 TEST 4: Add File Metadata")
    print("=" * 60)
    
    manager = MetadataManager()
    
    # Create metadata
    metadata = manager.create_metadata(
        book_name="test_files",
        title="Test Files",
        author="Test Author"
    )
    manager.save_metadata(metadata, "test_files")
    
    # Add files
    manager.add_file_metadata(
        "test_files",
        "text",
        "output/test_files/text.txt",
        file_url="https://example.com/text.txt",
        file_size=1024
    )
    
    manager.add_file_metadata(
        "test_files",
        "audio",
        "output/test_files/audio.mp3",
        file_url="https://example.com/audio.mp3",
        file_size=5242880
    )
    
    # Load and verify
    updated = manager.load_metadata("test_files")
    
    if updated:
        files = updated['files']
        assert 'text' in files
        assert 'audio' in files
        assert files['text']['url'] == "https://example.com/text.txt"
        assert files['audio']['size_mb'] == 5.0
        print(f"✅ Added {len(files)} file entries")
        return True
    else:
        print("❌ Failed to add files")
        return False


def test_statistics():
    """Test adding statistics"""
    print("\n" + "=" * 60)
    print("🧪 TEST 5: Add Statistics")
    print("=" * 60)
    
    manager = MetadataManager()
    
    # Create metadata
    metadata = manager.create_metadata(
        book_name="test_stats",
        title="Test Stats",
        author="Test Author"
    )
    manager.save_metadata(metadata, "test_stats")
    
    # Add statistics
    manager.add_statistics("test_stats", {
        'original_characters': 50000,
        'translated_characters': 52000,
        'original_words': 10000,
        'translated_words': 10500,
        'duration_seconds': 300,
        'duration_minutes': 5.0
    })
    
    # Load and verify
    updated = manager.load_metadata("test_stats")
    
    if updated:
        stats = updated['statistics']
        assert stats['original_characters'] == 50000
        assert stats['duration_minutes'] == 5.0
        print(f"✅ Added {len(stats)} statistics")
        return True
    else:
        print("❌ Failed to add statistics")
        return False


def test_report_generation():
    """Test report generation"""
    print("\n" + "=" * 60)
    print("🧪 TEST 6: Generate Report")
    print("=" * 60)
    
    manager = MetadataManager()
    
    # Create complete metadata
    metadata = manager.create_metadata(
        book_name="test_report",
        title="Test Report Book",
        author="Test Author"
    )
    manager.save_metadata(metadata, "test_report")
    
    # Add data
    manager.add_processing_step("test_report", "extraction", "completed")
    manager.add_processing_step("test_report", "translation", "completed")
    
    manager.add_file_metadata(
        "test_report",
        "text",
        "output/test_report/text.txt",
        file_url="https://example.com/text.txt",
        file_size=1024
    )
    
    manager.add_statistics("test_report", {
        'characters': 50000,
        'duration': 300
    })
    
    # Generate report
    report = manager.generate_metadata_report("test_report")
    
    if report and len(report) > 100:
        print("✅ Report generated successfully")
        print(f"   Length: {len(report)} characters")
        print("\n" + report[:500] + "...")
        return True
    else:
        print("❌ Failed to generate report")
        return False


def test_search():
    """Test search functionality"""
    print("\n" + "=" * 60)
    print("🧪 TEST 7: Search Metadata")
    print("=" * 60)
    
    manager = MetadataManager()
    
    # Create multiple metadata entries
    for i in range(3):
        metadata = manager.create_metadata(
            book_name=f"search_book_{i}",
            title=f"Search Book {i}",
            author="Test Author" if i < 2 else "Other Author"
        )
        manager.save_metadata(metadata, f"search_book_{i}")
    
    # Search by author
    results = manager.search_metadata(author="Test Author")
    
    if len(results) >= 2:
        print(f"✅ Search found {len(results)} results")
        return True
    else:
        print(f"❌ Search failed: found {len(results)} results, expected >= 2")
        return False


def main():
    """Run all metadata tests"""
    print("\n" + "=" * 60)
    print("📋 METADATA MANAGER TESTS")
    print("=" * 60)
    print()
    
    results = []
    
    try:
        results.append(("Create Metadata", test_create_metadata()))
        results.append(("Save & Load", test_save_load_metadata()))
        results.append(("Processing Steps", test_add_processing_step()))
        results.append(("File Metadata", test_add_file_metadata()))
        results.append(("Statistics", test_statistics()))
        results.append(("Report Generation", test_report_generation()))
        results.append(("Search", test_search()))
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("=" * 60)
    
    # Cleanup test files
    print("\n🧹 Cleaning up test files...")
    from pathlib import Path
    test_files = Path("output/metadata").glob("test_*.json")
    for f in test_files:
        f.unlink()
    print("✅ Cleanup complete")


if __name__ == "__main__":
    main()

