#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run All Tests
Egzekite Tout Test
"""

import sys
import subprocess
from pathlib import Path


def run_test(test_file):
    """Run a single test file"""
    print(f"\n{'='*70}")
    print(f"🧪 Running: {test_file}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


def main():
    """Run all test files"""
    print("\n" + "="*70)
    print("🧪 RUNNING ALL TESTS")
    print("   Ap egzekite tout tèst yo")
    print("="*70)
    
    test_files = [
        'tests/test_integration.py',
        'tests/test_metadata.py',
        'tests/test_email.py',
        'test_cloud_storage.py',
    ]
    
    results = []
    
    for test_file in test_files:
        test_path = Path(test_file)
        
        if not test_path.exists():
            print(f"\n⚠️  Skipping {test_file} - file not found")
            results.append((test_file, None))
            continue
        
        success = run_test(test_path)
        results.append((test_file, success))
    
    # Summary
    print("\n" + "="*70)
    print("📊 FINAL SUMMARY / REZIME FINAL")
    print("="*70)
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    
    for test_file, result in results:
        if result is True:
            print(f"✅ PASS  - {test_file}")
        elif result is False:
            print(f"❌ FAIL  - {test_file}")
        else:
            print(f"⚠️  SKIP  - {test_file}")
    
    print(f"\n{'='*70}")
    print(f"Total Tests: {len(results)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Skipped: {skipped}")
    print(f"{'='*70}")
    
    if failed == 0 and passed > 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("   Tout tèst yo pase!")
        return 0
    elif failed > 0:
        print(f"\n⚠️  {failed} TEST(S) FAILED")
        print(f"   {failed} tèst echwe")
        return 1
    else:
        print("\n⚠️  NO TESTS RAN")
        print("   Okenn tèst pa egzekite")
        return 2


if __name__ == "__main__":
    sys.exit(main())

