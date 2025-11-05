# 🚀 QUICK SUPABASE SETUP - 5 MINUTES
# Configuration Rapid Database

---

## ✅ CHECKLIST (Check lè w fè yo):

- [ ] Step 1: Supabase project created
- [ ] Step 2: Got URL & Key
- [ ] Step 3: SQL tables created
- [ ] Step 4: Added to Vercel
- [ ] Step 5: Redeployed
- [ ] Step 6: Verified "connected"

---

## STEP 1: GET YOUR KEYS (2 min) 🔑

### Already at: https://supabase.com/dashboard

1. **Find your project** "faner-studio" (oswa kreye si ou pa fè l)

2. **Click Settings** (icon ⚙️ anba agoch)

3. **Click "API"**

4. **COPY 2 BAGAY SA YO:**

📋 **Copy #1 - Project URL:**
```
https://xxxxxxxxxxxxx.supabase.co
```
⚠️ **KOPYE SA A KOUNYE A!** Paste nan Notepad

📋 **Copy #2 - anon public key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFz...
(very long string)
```
⚠️ **KOPYE SA A TOU!** Paste nan Notepad

**⚠️ USE "anon public" KEY, PA "service_role"!**

---

## STEP 2: CREATE TABLES (1 min) 📊

### Still in Supabase:

1. **Click "SQL Editor"** (nan left menu)

2. **Click "New Query"**

3. **Copy/Paste SA (TOUT BAGAY):**

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    project_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    data JSONB,
    status VARCHAR(50) DEFAULT 'pending',
    output_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Voices table
CREATE TABLE IF NOT EXISTS voices (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    voice_name VARCHAR(255) NOT NULL,
    voice_id VARCHAR(100) UNIQUE NOT NULL,
    quality VARCHAR(50) DEFAULT 'medium',
    samples_count INTEGER DEFAULT 0,
    voice_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Audios table
CREATE TABLE IF NOT EXISTS audios (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    project_id BIGINT REFERENCES projects(id),
    filename VARCHAR(255) NOT NULL,
    file_path TEXT,
    duration FLOAT,
    file_size BIGINT,
    format VARCHAR(10) DEFAULT 'mp3',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_voices_user_id ON voices(user_id);
CREATE INDEX IF NOT EXISTS idx_audios_user_id ON audios(user_id);
```

4. **Click "RUN"** (anba agoch) ✅

Ou dwe wè: **"Success. No rows returned"**

---

## STEP 3: ADD TO VERCEL (2 min) ⚙️

### Open new tab:

**Go to:** https://vercel.com/dashboard

1. **Find project "faner-studio"**

2. **Click "Settings"**

3. **Click "Environment Variables"** (left menu)

4. **Add Key #1:**
   - Click "Add New"
   - Name: `SUPABASE_URL`
   - Value: `https://xxxxx.supabase.co` (paste ton URL)
   - Check ✅ Production
   - Check ✅ Preview
   - Check ✅ Development
   - Click "Save"

5. **Add Key #2:**
   - Click "Add New" ankò
   - Name: `SUPABASE_KEY`
   - Value: `eyJhbGci...` (paste ton anon key)
   - Check ✅ Production
   - Check ✅ Preview
   - Check ✅ Development
   - Click "Save"

---

## STEP 4: REDEPLOY (30 sec) 🚀

### Retounen nan PowerShell epi run:

```bash
vercel --prod
```

⏰ Wait 1-2 minutes...

---

## STEP 5: VERIFY (30 sec) ✅

### Check health:

**Go to:** https://your-new-url.vercel.app/health

**You should see:**
```json
{
  "database": "connected"  ← SA DWE DI "connected" KOUNYE A!
}
```

---

## 🆘 IF STUCK:

**Bloke sou ki etap?**
- "m pa jwenn API keys" → M ap ede w
- "SQL pa run" → M ap fikse l
- "Pa ka add nan Vercel" → M ap gide w

**Di m kote w ye kounye a!** 👇

