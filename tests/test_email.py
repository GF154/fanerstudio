#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Email Notifications
Test Notifikasyon Email
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.email_notifier import EmailNotifier


def test_configuration():
    """Test email configuration"""
    print("=" * 60)
    print("🧪 TEST 1: Configuration")
    print("=" * 60)
    
    notifier = EmailNotifier()
    
    if notifier.enabled:
        print("✅ Email configured")
        print(f"   Sender: {notifier.sender_email}")
        print(f"   Recipient: {notifier.recipient_email}")
        print(f"   SMTP: {notifier.smtp_server}:{notifier.smtp_port}")
        return True
    else:
        print("❌ Email not configured")
        print("   Set environment variables:")
        print("   - SENDER_EMAIL")
        print("   - SENDER_PASSWORD")
        print("   - RECIPIENT_EMAIL")
        return False


def test_book_notification():
    """Test book completion notification"""
    print("\n" + "=" * 60)
    print("🧪 TEST 2: Book Completion Notification")
    print("=" * 60)
    
    notifier = EmailNotifier()
    
    if not notifier.enabled:
        print("⚠️  Skipping - email not configured")
        return False
    
    test_urls = {
        'text': 'https://example.com/book_text.txt',
        'audio': 'https://example.com/book_audio.mp3',
        'podcast': 'https://example.com/book_podcast.mp3'
    }
    
    success = notifier.notify_book_complete("test_book", test_urls)
    
    if success:
        print("✅ Notification sent successfully")
        return True
    else:
        print("❌ Failed to send notification")
        return False


def test_batch_notification():
    """Test batch completion notification"""
    print("\n" + "=" * 60)
    print("🧪 TEST 3: Batch Completion Notification")
    print("=" * 60)
    
    notifier = EmailNotifier()
    
    if not notifier.enabled:
        print("⚠️  Skipping - email not configured")
        return False
    
    test_results = [
        {
            'name': 'book1',
            'status': 'completed',
            'urls': {
                'text': 'https://example.com/book1_text.txt',
                'audio': 'https://example.com/book1_audio.mp3'
            }
        },
        {
            'name': 'book2',
            'status': 'completed',
            'urls': {
                'text': 'https://example.com/book2_text.txt',
                'audio': 'https://example.com/book2_audio.mp3'
            }
        },
        {
            'name': 'book3',
            'status': 'failed',
            'errors': ['Translation error']
        }
    ]
    
    success = notifier.notify_batch_complete(test_results, duration=120.5)
    
    if success:
        print("✅ Batch notification sent successfully")
        return True
    else:
        print("❌ Failed to send batch notification")
        return False


def test_error_notification():
    """Test error notification"""
    print("\n" + "=" * 60)
    print("🧪 TEST 4: Error Notification")
    print("=" * 60)
    
    notifier = EmailNotifier()
    
    if not notifier.enabled:
        print("⚠️  Skipping - email not configured")
        return False
    
    success = notifier.notify_error("test_book", "This is a test error message")
    
    if success:
        print("✅ Error notification sent successfully")
        return True
    else:
        print("❌ Failed to send error notification")
        return False


def main():
    """Run all email tests"""
    print("\n" + "=" * 60)
    print("📧 EMAIL NOTIFICATION TESTS")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Configuration
    results.append(("Configuration", test_configuration()))
    
    # Test 2: Book notification
    results.append(("Book Notification", test_book_notification()))
    
    # Test 3: Batch notification
    results.append(("Batch Notification", test_batch_notification()))
    
    # Test 4: Error notification
    results.append(("Error Notification", test_error_notification()))
    
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


if __name__ == "__main__":
    main()

