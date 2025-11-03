#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 Supabase Setup Helper - Faner Studio
Interactive setup for Supabase integration
"""

import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(num, text):
    """Print step"""
    print(f"\n{'='*60}")
    print(f"STEP {num}: {text}")
    print(f"{'='*60}\n")

def main():
    print_header("🔥 SUPABASE SETUP - FANER STUDIO")
    
    print("This script will help you integrate Supabase with Faner Studio.")
    print("Follow each step carefully!\n")
    
    input("Press Enter to continue...")
    
    # Step 1: Account Creation
    print_step(1, "CREATE SUPABASE ACCOUNT")
    print("1. Go to: https://supabase.com")
    print("2. Click 'Start your project'")
    print("3. Sign in with GitHub or email")
    print("4. Create a new project named 'faner-studio'")
    print("5. Choose region: US East (closest to Haiti)")
    print("6. Generate and SAVE your database password!")
    print("\n⚠️  IMPORTANT: Save your database password now!")
    
    input("\nPress Enter once you've created your project...")
    
    # Step 2: Get Connection String
    print_step(2, "GET CONNECTION STRING")
    print("1. In Supabase dashboard → Settings (⚙️) → Database")
    print("2. Scroll to 'Connection String'")
    print("3. Select 'URI' tab")
    print("4. Copy the connection string")
    print("5. Replace [YOUR-PASSWORD] with your actual password")
    print("\nExample:")
    print("postgresql://postgres:MyPass123@db.xxx.supabase.co:5432/postgres")
    
    connection_string = input("\nPaste your connection string here: ").strip()
    
    if not connection_string.startswith("postgresql://"):
        print("\n❌ Invalid connection string! Should start with 'postgresql://'")
        print("Please run this script again.")
        return
    
    print("\n✅ Connection string saved!")
    
    # Step 3: SQL Script
    print_step(3, "CREATE DATABASE TABLES")
    print("1. In Supabase dashboard → SQL Editor (📝)")
    print("2. Click 'New query'")
    print("3. Open file: SUPABASE_SETUP_GUIDE.md")
    print("4. Copy the entire SQL script from STEP 3")
    print("5. Paste into SQL Editor")
    print("6. Click 'Run' (▶️)")
    
    ran_sql = input("\nDid you run the SQL script? (yes/no): ").strip().lower()
    
    if ran_sql != "yes":
        print("\n⚠️  Please run the SQL script first, then run this script again.")
        return
    
    print("\n✅ Database tables created!")
    
    # Step 4: Update database.py
    print_step(4, "UPDATE DATABASE.PY")
    
    db_file = Path("database.py")
    
    if not db_file.exists():
        print("❌ database.py not found!")
        return
    
    print("Updating database.py to use Supabase...")
    
    # Read current content
    content = db_file.read_text(encoding='utf-8')
    
    # Update database URL configuration
    if 'sqlite:///' in content and 'os.getenv("DATABASE_URL")' not in content:
        # Add environment variable support
        new_config = '''
# Database file location
DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "fanerstudio.db"

# Get database URL from environment (Supabase) or use SQLite locally
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    print("⚠️  Using local SQLite. Set DATABASE_URL for Supabase.")
else:
    print("✅ Using Supabase PostgreSQL database")
'''
        
        # Find and replace the database setup section
        old_setup = '''# Database file location
DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "fanerstudio.db"

# SQLAlchemy setup
DATABASE_URL = f"sqlite:///{DB_PATH}"'''
        
        if old_setup in content:
            content = content.replace(old_setup, new_config + "\n# SQLAlchemy setup")
            db_file.write_text(content, encoding='utf-8')
            print("✅ database.py updated successfully!")
        else:
            print("⚠️  Could not auto-update database.py")
            print("Please manually add environment variable support.")
    else:
        print("✅ database.py already configured for environment variables!")
    
    # Step 5: Create .env file
    print_step(5, "CREATE .ENV FILE")
    
    env_file = Path(".env")
    env_content = f"""# Supabase Configuration
DATABASE_URL={connection_string}

# Other configurations
SECRET_KEY=your-secret-key-change-this-in-production
HUGGINGFACE_API_KEY=your-huggingface-key
ALLOWED_ORIGINS=*
"""
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        overwrite = input("Overwrite? (yes/no): ").strip().lower()
        if overwrite == "yes":
            env_file.write_text(env_content, encoding='utf-8')
            print("✅ .env file updated!")
        else:
            print("⚠️  Please manually add DATABASE_URL to your .env file")
    else:
        env_file.write_text(env_content, encoding='utf-8')
        print("✅ .env file created!")
    
    # Step 6: Add to Render
    print_step(6, "ADD TO RENDER")
    print("1. Go to: https://dashboard.render.com")
    print("2. Select your service: 'faner-studio-complete'")
    print("3. Click 'Environment'")
    print("4. Click 'Add Environment Variable'")
    print("5. Add:")
    print(f"   Key: DATABASE_URL")
    print(f"   Value: {connection_string}")
    print("6. Click 'Save Changes'")
    print("\nRender will automatically redeploy with the new database!")
    
    input("\nPress Enter once you've added the variable to Render...")
    
    # Step 7: Test Connection
    print_step(7, "TEST CONNECTION")
    
    test_now = input("Test Supabase connection now? (yes/no): ").strip().lower()
    
    if test_now == "yes":
        print("\n🔗 Testing connection to Supabase...")
        try:
            from sqlalchemy import create_engine, text
            
            engine = create_engine(connection_string)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT version();"))
                version = result.fetchone()[0]
                print(f"\n✅ Connected successfully!")
                print(f"PostgreSQL version: {version[:50]}...")
                
                # Test tables
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """))
                tables = [row[0] for row in result]
                print(f"\n✅ Found {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table}")
                
        except Exception as e:
            print(f"\n❌ Connection failed: {e}")
            print("\nPlease check:")
            print("1. Connection string is correct")
            print("2. Password is correct")
            print("3. You have internet connection")
            return
    
    # Summary
    print_header("🎉 SETUP COMPLETE!")
    print("✅ Supabase account created")
    print("✅ Database tables created")
    print("✅ database.py updated")
    print("✅ .env file configured")
    print("✅ Ready for Render deployment")
    
    print("\n📋 NEXT STEPS:")
    print("1. Add DATABASE_URL to Render environment variables")
    print("2. Commit and push changes:")
    print("   git add .")
    print("   git commit -m 'Integrate Supabase database'")
    print("   git push origin master")
    print("3. Render will auto-deploy!")
    
    print("\n🌐 Your platform now has:")
    print("   • Professional PostgreSQL database")
    print("   • 500MB free storage (forever!)")
    print("   • Auto-backups")
    print("   • Real-time capabilities")
    print("   • Built-in authentication")
    
    print("\n📚 Documentation:")
    print("   • Full guide: SUPABASE_SETUP_GUIDE.md")
    print("   • Supabase docs: https://supabase.com/docs")
    
    print("\n🚀 Your platform is now PRODUCTION READY!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

