#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Start Menu
Meni Enteraktif pou Chwazi Metòd
"""

import os
import sys


def print_header():
    """Print fancy header"""
    print("\n" + "=" * 70)
    print("🇭🇹  PWOJÈ KREYÒL IA / HAITIAN CREOLE AI PROJECT")
    print("=" * 70)
    print("Version 2.0 - Enhanced Edition")
    print()


def print_menu():
    """Print main menu"""
    print("=" * 70)
    print("CHWAZI YON OPSYON / CHOOSE AN OPTION:")
    print("=" * 70)
    print()
    print("1. 🌐 Web Interface (EASIEST!)")
    print("   Launch beautiful web interface")
    print("   Lance entèfas web")
    print()
    print("2. ⚡ Enhanced Single Book")
    print("   Process one book with all features")
    print("   Trete yon liv ak tout fonksyonalite")
    print()
    print("3. 📚 Batch Processing")
    print("   Process multiple books at once")
    print("   Trete plizyè liv an menm tan")
    print()
    print("4. 📖 Simple Cloud Processing")
    print("   Original simple workflow")
    print("   Workflow senp orijinal")
    print()
    print("5. 🧪 Test Cloud Connection")
    print("   Test your GCS connection")
    print("   Teste koneksyon GCS ou")
    print()
    print("6. 📚 View Documentation")
    print("   Open documentation guide")
    print("   Gade gid dokimantasyon")
    print()
    print("7. ⚙️  Setup & Configuration")
    print("   Setup cloud storage and email")
    print("   Konfigire cloud storage ak email")
    print()
    print("0. ❌ Exit / Sòti")
    print()
    print("=" * 70)


def check_env():
    """Check environment setup"""
    bucket = os.getenv("GCS_BUCKET_NAME")
    if not bucket:
        print("\n⚠️  WARNING / AVÈTISMAN:")
        print("GCS_BUCKET_NAME pa defini / not configured")
        print("\nPou konfigire / To configure:")
        print("1. Copy cloud_env_template.txt to .env")
        print("2. Edit .env and set GCS_BUCKET_NAME")
        print("\nOu kapab kontinye men kèk fonksyon pap travay")
        print("You can continue but some functions won't work")
        print()
        input("Press Enter to continue... / Peze Enter pou kontinye...")
    else:
        print(f"\n✅ Bucket configured: {bucket}")


def launch_web():
    """Launch web interface"""
    print("\n" + "=" * 70)
    print("🌐 LAUNCHING WEB INTERFACE / AP LANSE ENTÈFAS WEB")
    print("=" * 70)
    print()
    print("The web app will open in your browser...")
    print("Aplikasyon an ap ouvri nan navigatè ou a...")
    print()
    print("If it doesn't open automatically, go to:")
    print("Si li pa ouvri otomatikman, ale nan:")
    print("http://localhost:8501")
    print()
    
    try:
        import streamlit.web.cli as stcli
        sys.argv = ["streamlit", "run", "web_app.py"]
        sys.exit(stcli.main())
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTry running manually:")
        print("streamlit run web_app.py")


def launch_enhanced():
    """Launch enhanced processor"""
    print("\n" + "=" * 70)
    print("⚡ ENHANCED PROCESSING / PWOSESIS AMELYORE")
    print("=" * 70)
    print()
    
    # Check bucket
    bucket = os.getenv("GCS_BUCKET_NAME")
    if not bucket:
        print("❌ GCS_BUCKET_NAME must be configured first")
        print("Run option 7 to setup")
        input("\nPress Enter to continue...")
        return
    
    print("This will process a single book with all features:")
    print("Sa ap trete yon liv ak tout fonksyonalite:")
    print("  • Metadata tracking")
    print("  • Email notifications")
    print("  • Statistics & reports")
    print("  • Cloud backup")
    print()
    
    # Import and run
    try:
        from process_book_enhanced import main
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to continue...")


def launch_batch():
    """Launch batch processor"""
    print("\n" + "=" * 70)
    print("📚 BATCH PROCESSING / PWOSESIS BATCH")
    print("=" * 70)
    print()
    
    # Check config file
    if not os.path.exists("books_config.json"):
        print("❌ books_config.json not found")
        print("Create this file first with your book list")
        print()
        print("Example:")
        print('''
{
  "books": [
    {
      "name": "book1",
      "input_pdf": "input/book1.pdf",
      "metadata": {"title": "Book 1", "author": "Author"}
    }
  ]
}
        ''')
        input("\nPress Enter to continue...")
        return
    
    # Import and run
    try:
        from run_batch import main
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to continue...")


def launch_simple():
    """Launch simple processor"""
    print("\n" + "=" * 70)
    print("📖 SIMPLE CLOUD PROCESSING")
    print("=" * 70)
    print()
    
    try:
        import main_cloud
        # Run it
        os.system("python main_cloud.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to continue...")


def test_connection():
    """Test cloud connection"""
    print("\n" + "=" * 70)
    print("🧪 TESTING CLOUD CONNECTION / TÈS KONEKSYON")
    print("=" * 70)
    print()
    
    try:
        from test_cloud_storage import test_cloud_storage
        success = test_cloud_storage()
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    input("\nPress Enter to continue...")


def view_docs():
    """Show documentation options"""
    print("\n" + "=" * 70)
    print("📚 DOCUMENTATION / DOKIMANTASYON")
    print("=" * 70)
    print()
    print("Available documentation files:")
    print()
    print("1. QUICK_START_ENHANCED.md - 5-minute quick start")
    print("2. README_ENHANCED_FEATURES.md - Complete feature guide")
    print("3. README_ENHANCED.md - Main enhanced README")
    print("4. CLOUD_STORAGE_GUIDE.md - Cloud storage setup")
    print("5. ENHANCED_FEATURES_COMPLETE.txt - Feature summary")
    print()
    print("Open any of these files in a text editor to read.")
    print("Ouvri nenpòt nan fichye sa yo nan yon editè tèks.")
    print()
    input("Press Enter to continue...")


def setup_config():
    """Setup configuration"""
    print("\n" + "=" * 70)
    print("⚙️  SETUP & CONFIGURATION / KONFIGIRASYON")
    print("=" * 70)
    print()
    
    print("Setup Steps:")
    print()
    print("1. Create .env file:")
    print("   cp cloud_env_template.txt .env")
    print()
    print("2. Edit .env and add:")
    print("   GCS_BUCKET_NAME=your-bucket-name")
    print()
    print("3. Setup GCS authentication:")
    print("   gcloud auth application-default login")
    print()
    print("4. Optional - Email configuration:")
    print("   SENDER_EMAIL=your-email@gmail.com")
    print("   SENDER_PASSWORD=your-app-password")
    print("   RECIPIENT_EMAIL=recipient@email.com")
    print()
    print("5. Test connection:")
    print("   python test_cloud_storage.py")
    print()
    
    choice = input("Run automated setup? (y/n): ").lower()
    
    if choice == 'y':
        # Run setup script
        if sys.platform.startswith('win'):
            os.system("setup_cloud.bat")
        else:
            os.system("bash setup_cloud.sh")
    
    input("\nPress Enter to continue...")


def main():
    """Main interactive menu"""
    
    while True:
        print_header()
        check_env()
        print_menu()
        
        choice = input("Enter your choice / Antre chwa ou (0-7): ").strip()
        
        if choice == "1":
            launch_web()
        elif choice == "2":
            launch_enhanced()
        elif choice == "3":
            launch_batch()
        elif choice == "4":
            launch_simple()
        elif choice == "5":
            test_connection()
        elif choice == "6":
            view_docs()
        elif choice == "7":
            setup_config()
        elif choice == "0":
            print("\n👋 Orevwa! / Goodbye!")
            print("Mèsi pou itilize Pwojè Kreyòl IA!")
            print("Thank you for using the Haitian Creole AI Project!")
            print()
            sys.exit(0)
        else:
            print("\n❌ Invalid choice / Chwa pa valid")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user / Enti pa itilizatè")
        sys.exit(0)

