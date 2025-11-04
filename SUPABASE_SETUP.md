# 🗄️ SUPABASE DATABASE SETUP

Ann konfigiwe Supabase pou Faner Studio!

## 📋 STEP 1: Kreye Kont Supabase

1. Ale sou https://supabase.com
2. Klike **"Start your project"**
3. Kreye yon nouvo kont oswa login
4. Klike **"New Project"**

---

## 🏗️ STEP 2: Kreye Database Tables

Kòpye SQL code sa yo e execute yo nan Supabase SQL Editor:

### 1️⃣ **Users Table**
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for faster lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### 2️⃣ **Projects Table**
```sql
CREATE TABLE projects (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    project_type VARCHAR(50) NOT NULL, -- 'audiobook', 'podcast', 'video', 'custom_voice'
    title VARCHAR(255) NOT NULL,
    data JSONB, -- Store project configuration
    status VARCHAR(50) DEFAULT 'processing', -- 'processing', 'completed', 'failed'
    output_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_type ON projects(project_type);
CREATE INDEX idx_projects_created ON projects(created_at DESC);
```

### 3️⃣ **Voices Table**
```sql
CREATE TABLE voices (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    voice_name VARCHAR(100) NOT NULL,
    quality VARCHAR(50) NOT NULL, -- 'basic', 'medium', 'premium'
    samples_count INTEGER DEFAULT 0,
    voice_data JSONB, -- Store voice configuration
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index
CREATE INDEX idx_voices_user_id ON voices(user_id);
CREATE INDEX idx_voices_active ON voices(is_active);
```

### 4️⃣ **Audios Table**
```sql
CREATE TABLE audios (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    project_id BIGINT REFERENCES projects(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    file_type VARCHAR(50) NOT NULL, -- 'audiobook', 'podcast', 'voiceover', etc.
    duration VARCHAR(20),
    size_mb FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index
CREATE INDEX idx_audios_user_id ON audios(user_id);
CREATE INDEX idx_audios_project_id ON audios(project_id);
```

---

## 🔑 STEP 3: Jwenn Credentials yo

1. Nan Supabase dashboard, klike sou **Settings** (⚙️)
2. Klike **API**
3. Kòpye:
   - **Project URL** (sa se `SUPABASE_URL`)
   - **anon/public key** (sa se `SUPABASE_KEY`)

---

## 🌐 STEP 4: Ajoute Environment Variables sou Vercel

1. Ale sou Vercel dashboard
2. Chwazi pwojè **faner-studio**
3. Klike **Settings** → **Environment Variables**
4. Ajoute 2 variables sa yo:

```
SUPABASE_URL = your-project-url
SUPABASE_KEY = your-anon-key
```

5. Klike **Save**
6. Redeploy pwojè a

---

## ✅ STEP 5: Teste Connection

Apre deploy, visite:
```
https://your-vercel-url.vercel.app/health
```

Ou dwe wè:
```json
{
  "status": "healthy",
  "database": "connected",
  ...
}
```

---

## 📊 STEP 6: Enable Row Level Security (Optional men rekòmande)

Pou sekirite, ajoute RLS policies:

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE voices ENABLE ROW LEVEL SECURITY;
ALTER TABLE audios ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can view own projects" ON projects
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can view own voices" ON voices
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can view own audios" ON audios
    FOR ALL USING (auth.uid()::text = user_id::text);
```

---

## 🎉 FINISH!

Database ou a konfigiwe! Kounye a Faner Studio ka:
- ✅ Sove tout pwojè yo
- ✅ Jere itilizatè yo
- ✅ Stock custom voices
- ✅ Track audio files

---

## 🆘 TROUBLESHOOTING

### Connection Error?
- Verifye `SUPABASE_URL` ak `SUPABASE_KEY` yo kòrèk
- Asire w tables yo kreye nan Supabase
- Redeploy sou Vercel apre chanje env variables

### Tables pa egziste?
- Execute SQL scripts yo nan Supabase SQL Editor
- Refresh page la

---

**Bon travay! Database ou a pare! 🚀**

