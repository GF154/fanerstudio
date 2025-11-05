#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Test Supabase Connection
Quick test to verify Supabase credentials
"""

import os
from supabase import create_client

# Get credentials
SUPABASE_URL = "https://cxxbakzhlnuhkfgoaslv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4eGJha3pobG51aGtmZ29hc2x2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMzkxOTQsImV4cCI6MjA3NzkxNTE5NH0.0iIoT5aVReYImBtsqZdKdbSNhM8XVv7MQbI5_6AbdhY"

print(f"📍 URL: {SUPABASE_URL}")
print(f"🔑 KEY: {SUPABASE_KEY[:20]}...")

try:
    print("\n🔄 Creating Supabase client...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client created!")
    
    print("\n🔄 Testing connection (listing tables)...")
    # Try to query a simple table or check connection
    result = supabase.table("users").select("*", count="exact").limit(0).execute()
    print(f"✅ Connection successful!")
    print(f"📊 Users table exists (count check passed)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"❌ Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

