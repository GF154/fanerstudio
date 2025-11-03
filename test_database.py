#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ Test Database Setup
Create test data and verify database functionality
"""

from database import SessionLocal, User, Project, CustomVoice, init_db
from auth import get_password_hash
from datetime import datetime

def test_database():
    """Test database functionality"""
    print("=" * 60)
    print("🗄️  TESTING DATABASE")
    print("=" * 60)
    
    # Initialize database
    print("\n1️⃣  Initializing database...")
    init_db()
    print("✅ Database initialized")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Test 1: Create a test user
        print("\n2️⃣  Creating test user...")
        existing_user = db.query(User).filter(User.username == "testuser").first()
        
        if existing_user:
            print("⚠️  Test user already exists")
            test_user = existing_user
        else:
            test_user = User(
                username="testuser",
                email="test@fanerstudio.com",
                hashed_password=get_password_hash("test123"),
                full_name="Test User",
                is_active=True,
                is_admin=False,
                created_at=datetime.utcnow()
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✅ Test user created: {test_user.username} (ID: {test_user.id})")
        
        # Test 2: Create a test project
        print("\n3️⃣  Creating test project...")
        test_project = Project(
            user_id=test_user.id,
            project_type="audiobook",
            title="Test Audiobook",
            description="A test audiobook project",
            status="pending",
            progress=0.0,
            created_at=datetime.utcnow()
        )
        db.add(test_project)
        db.commit()
        db.refresh(test_project)
        print(f"✅ Test project created: {test_project.title} (ID: {test_project.id})")
        
        # Test 3: Query users
        print("\n4️⃣  Querying all users...")
        users = db.query(User).all()
        print(f"✅ Found {len(users)} user(s)")
        for user in users:
            print(f"   - {user.username} ({user.email})")
        
        # Test 4: Query projects
        print("\n5️⃣  Querying all projects...")
        projects = db.query(Project).all()
        print(f"✅ Found {len(projects)} project(s)")
        for project in projects:
            print(f"   - {project.title} (Type: {project.project_type}, Status: {project.status})")
        
        # Test 5: Query custom voices
        print("\n6️⃣  Querying custom voices...")
        voices = db.query(CustomVoice).all()
        print(f"✅ Found {len(voices)} custom voice(s)")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DATABASE SUMMARY")
        print("=" * 60)
        print(f"Users: {len(users)}")
        print(f"Projects: {len(projects)}")
        print(f"Custom Voices: {len(voices)}")
        print("\n✅ Database is fully functional!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()

def show_database_info():
    """Show database file information"""
    import os
    from pathlib import Path
    
    db_path = Path("data/fanerstudio.db")
    
    if db_path.exists():
        size_bytes = db_path.stat().st_size
        size_kb = size_bytes / 1024
        print(f"\n💾 Database File Info:")
        print(f"   Path: {db_path}")
        print(f"   Size: {size_kb:.2f} KB")
        print(f"   Created: {datetime.fromtimestamp(db_path.stat().st_ctime)}")
    else:
        print("\n❌ Database file not found")

if __name__ == "__main__":
    print("\n🚀 Starting database test...\n")
    success = test_database()
    show_database_info()
    
    if success:
        print("\n🎉 All database tests passed!")
        print("\n💡 Test credentials:")
        print("   Username: testuser")
        print("   Password: test123")
        print("\n📝 You can use these to test authentication endpoints")
    else:
        print("\n❌ Some tests failed")
    
    print()

