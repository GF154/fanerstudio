# 🔥 SUPABASE SETUP GUIDE - Faner Studio

Complete guide to integrate Supabase with Faner Studio

---

## 📋 **STEP 1: CREATE SUPABASE ACCOUNT**

### 1.1 Sign Up
1. Go to: https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub (recommended) or email
4. Verify your email if needed

### 1.2 Create New Project
1. Click "New Project"
2. Fill in:
   - **Name**: `faner-studio`
   - **Database Password**: (generate strong password - SAVE IT!)
   - **Region**: Choose closest to you (US East for Haiti)
   - **Pricing Plan**: Free (500MB, forever!)
3. Click "Create new project"
4. Wait 2-3 minutes for setup

---

## 📋 **STEP 2: GET DATABASE CONNECTION**

### 2.1 Find Connection String
1. In Supabase dashboard, go to: **Settings** (⚙️ icon)
2. Click **Database**
3. Scroll to **Connection String**
4. Select **URI** tab
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres
   ```
6. Replace `[YOUR-PASSWORD]` with your actual database password

### 2.2 Example Connection String
```
postgresql://postgres:MySecurePass123@db.pqrstuvwxyz.supabase.co:5432/postgres
```

**⚠️ SAVE THIS! You'll need it!**

---

## 📋 **STEP 3: CREATE DATABASE TABLES**

### 3.1 Open SQL Editor
1. In Supabase dashboard, click **SQL Editor** (📝 icon)
2. Click "New query"
3. Paste this SQL:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    project_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    progress FLOAT DEFAULT 0.0,
    voice_id VARCHAR(100),
    input_file VARCHAR(500),
    output_files TEXT,
    settings TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Custom Voices table
CREATE TABLE custom_voices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    voice_id VARCHAR(100) UNIQUE NOT NULL,
    voice_name VARCHAR(200) NOT NULL,
    speaker_name VARCHAR(200),
    language VARCHAR(10) DEFAULT 'ht',
    gender VARCHAR(20) DEFAULT 'unknown',
    age_range VARCHAR(20) DEFAULT 'adult',
    region VARCHAR(100) DEFAULT 'Haiti',
    audio_file VARCHAR(500) NOT NULL,
    audio_format VARCHAR(10) NOT NULL,
    duration_seconds FLOAT DEFAULT 0.0,
    file_size_mb FLOAT DEFAULT 0.0,
    text_content TEXT,
    notes TEXT,
    times_used INTEGER DEFAULT 0,
    rating FLOAT DEFAULT 0.0,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- API Keys table
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    key_name VARCHAR(100) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used TIMESTAMP,
    expires_at TIMESTAMP
);

-- Activity Logs table
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    endpoint VARCHAR(200),
    status_code INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_data TEXT,
    response_data TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_custom_voices_user_id ON custom_voices(user_id);
CREATE INDEX idx_custom_voices_voice_id ON custom_voices(voice_id);
CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created_at ON activity_logs(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE custom_voices ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- RLS Policies for projects table
CREATE POLICY "Users can view own projects" ON projects
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own projects" ON projects
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own projects" ON projects
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own projects" ON projects
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- RLS Policies for custom_voices table
CREATE POLICY "Users can view own voices" ON custom_voices
    FOR SELECT USING (auth.uid()::text = user_id::text OR is_public = TRUE);

CREATE POLICY "Users can insert own voices" ON custom_voices
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own voices" ON custom_voices
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own voices" ON custom_voices
    FOR DELETE USING (auth.uid()::text = user_id::text);
```

4. Click **Run** (▶️ button)
5. You should see "Success. No rows returned"

---

## 📋 **STEP 4: UPDATE LOCAL CODE**

### 4.1 Install Supabase Client
```bash
pip install supabase psycopg2-binary
```

### 4.2 Update database.py

Replace the DATABASE_URL line:

```python
# OLD (SQLite):
DATABASE_URL = f"sqlite:///{DB_PATH}"

# NEW (Supabase):
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"
)
```

Full example:
```python
import os
from sqlalchemy import create_engine

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback to SQLite for local development
    from pathlib import Path
    DB_DIR = Path("data")
    DB_DIR.mkdir(exist_ok=True)
    DB_PATH = DB_DIR / "fanerstudio.db"
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    print("⚠️  Using local SQLite database")
else:
    print("✅ Using Supabase PostgreSQL database")

engine = create_engine(DATABASE_URL)
# ... rest of code
```

---

## 📋 **STEP 5: ADD TO RENDER**

### 5.1 Add Environment Variable
1. Go to: https://dashboard.render.com
2. Select your service: `faner-studio-complete`
3. Click **Environment**
4. Click **Add Environment Variable**
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres`
6. Click **Save Changes**

### 5.2 Trigger Redeploy
1. Render will auto-deploy with new env var
2. Or manually: Click **Manual Deploy** → **Deploy latest commit**

---

## 📋 **STEP 6: TEST CONNECTION**

### 6.1 Create Test Script

```python
# test_supabase.py
import os
from sqlalchemy import create_engine, text

# Your Supabase connection string
DATABASE_URL = "postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"

try:
    print("🔗 Connecting to Supabase...")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Connected! PostgreSQL version: {version}")
        
        # Test tables
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]
        print(f"✅ Found {len(tables)} tables: {', '.join(tables)}")
        
except Exception as e:
    print(f"❌ Error: {e}")
```

Run:
```bash
python test_supabase.py
```

---

## 📋 **STEP 7: ENABLE STORAGE (FOR AUDIO FILES)**

### 7.1 Create Storage Bucket
1. In Supabase dashboard, click **Storage** (🗄️ icon)
2. Click **Create a new bucket**
3. Name: `audio-files`
4. Make it **Public** ✅
5. Click **Create bucket**

### 7.2 Create Policies
1. Click on `audio-files` bucket
2. Click **Policies**
3. Add policy:
   - **Policy name**: "Allow authenticated uploads"
   - **Policy definition**: 
   ```sql
   CREATE POLICY "Allow authenticated uploads"
   ON storage.objects FOR INSERT
   WITH CHECK (bucket_id = 'audio-files' AND auth.role() = 'authenticated');
   ```

### 7.3 Update Code to Use Storage

```python
from supabase import create_client

supabase_url = "https://xxx.supabase.co"
supabase_key = "your-anon-key"
supabase = create_client(supabase_url, supabase_key)

# Upload audio file
with open("voice.mp3", "rb") as f:
    supabase.storage.from_("audio-files").upload(
        f"voices/{voice_id}.mp3",
        f
    )

# Get public URL
url = supabase.storage.from_("audio-files").get_public_url(
    f"voices/{voice_id}.mp3"
)
```

---

## 📋 **STEP 8: OPTIONAL - ENABLE AUTH**

### 8.1 Enable Email Auth
1. Dashboard → **Authentication** → **Providers**
2. Enable **Email** provider
3. Configure email templates (optional)

### 8.2 Use Supabase Auth (Instead of JWT)

```python
from supabase import create_client

supabase = create_client(supabase_url, supabase_key)

# Sign up
user = supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "password123"
})

# Sign in
session = supabase.auth.sign_in_with_password({
    "email": "user@example.com",
    "password": "password123"
})

# Get current user
user = supabase.auth.get_user()
```

---

## ✅ **VERIFICATION CHECKLIST**

```
□ Supabase account created
□ Project created
□ Database password saved
□ Connection string copied
□ Tables created (SQL ran successfully)
□ database.py updated
□ DATABASE_URL added to Render
□ Connection tested
□ Storage bucket created (optional)
□ Auth enabled (optional)
```

---

## 🎉 **YOU'RE DONE!**

Your Faner Studio now has:
- ✅ Professional PostgreSQL database
- ✅ 500MB free storage
- ✅ Auto-backups
- ✅ Real-time capabilities
- ✅ Built-in authentication
- ✅ File storage for audio

---

## 🆘 **TROUBLESHOOTING**

### Problem: Connection refused
**Solution**: Check if DATABASE_URL is correct and includes password

### Problem: Tables not found
**Solution**: Make sure you ran the SQL script in Supabase SQL Editor

### Problem: Authentication errors
**Solution**: Check Row Level Security policies are correct

### Problem: Slow queries
**Solution**: Add indexes (already included in SQL script)

---

## 📞 **SUPPORT**

- Supabase Docs: https://supabase.com/docs
- Supabase Discord: https://discord.supabase.com
- GitHub Issues: Ask me for help!

---

**Bon travay! Your database is now PRODUCTION READY! 🚀**

