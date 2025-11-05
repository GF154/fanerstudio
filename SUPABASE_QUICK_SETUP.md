# 🗄️ SUPABASE CONFIGURATION GUIDE
# Guide Konfigirasyon Supabase

## STEP 1: KREYE SUPABASE PROJECT 🚀

### 1.1 Ale sou Supabase
```
https://supabase.com
```

### 1.2 Sign in / Create account
- Use Google, GitHub, oswa email

### 1.3 Create New Project
- Click "New Project"
- Project name: **faner-studio** (oswa non ou vle)
- Database Password: **[Bay yon strong password]** ⚠️ KENBE L!
- Region: Chwazi pi pre ou (ex: East US, Europe West)
- Click "Create new project"
- ⏰ Wait 2-3 minutes pou setup

---

## STEP 2: GET API KEYS 🔑

### 2.1 Ale nan Settings → API
```
Project Dashboard → Settings (gear icon) → API
```

### 2.2 Copy sa yo:
1. **Project URL**
   ```
   https://xxxxxxxxxxxxx.supabase.co
   ```

2. **anon/public key** (NOT service_role!)
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

⚠️ **IMPORTANT**: Use `anon` key, PA `service_role` key!

---

## STEP 3: SETUP DATABASE TABLES 📊

### 3.1 Ale nan SQL Editor
```
Project Dashboard → SQL Editor
```

### 3.2 Run sa (copy tout bagay):

```sql
-- ============================================================
-- FANER STUDIO DATABASE SCHEMA
-- ============================================================

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. PROJECTS TABLE
CREATE TABLE IF NOT EXISTS projects (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    project_type VARCHAR(50) NOT NULL, -- 'audiobook', 'podcast', 'video'
    title VARCHAR(255) NOT NULL,
    data JSONB,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    output_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. VOICES TABLE
CREATE TABLE IF NOT EXISTS voices (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    voice_name VARCHAR(255) NOT NULL,
    voice_id VARCHAR(100) UNIQUE NOT NULL,
    quality VARCHAR(50) DEFAULT 'medium', -- 'basic', 'medium', 'premium'
    samples_count INTEGER DEFAULT 0,
    voice_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. AUDIOS TABLE
CREATE TABLE IF NOT EXISTS audios (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    project_id BIGINT REFERENCES projects(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT,
    duration FLOAT,
    file_size BIGINT,
    format VARCHAR(10) DEFAULT 'mp3',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_voices_user_id ON voices(user_id);
CREATE INDEX idx_audios_user_id ON audios(user_id);
CREATE INDEX idx_audios_project_id ON audios(project_id);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE voices ENABLE ROW LEVEL SECURITY;
ALTER TABLE audios ENABLE ROW LEVEL SECURITY;

-- Create policies (users can only see their own data)
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can view own projects" ON projects
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can view own voices" ON voices
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can view own audios" ON audios
    FOR ALL USING (auth.uid()::text = user_id::text);
```

### 3.3 Click "Run" ✅

---

## STEP 4: CONFIGURE VERCEL ENVIRONMENT VARIABLES 🔧

### 4.1 Ale sou Vercel Dashboard
```
https://vercel.com/dashboard
```

### 4.2 Chwazi project "faner-studio"

### 4.3 Ale nan Settings → Environment Variables

### 4.4 Add sa yo:

**Variable 1:**
- Name: `SUPABASE_URL`
- Value: `https://xxxxxxxxxxxxx.supabase.co` (from Step 2)
- Environments: ✅ Production, ✅ Preview, ✅ Development

**Variable 2:**
- Name: `SUPABASE_KEY`
- Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (anon key from Step 2)
- Environments: ✅ Production, ✅ Preview, ✅ Development

### 4.5 Click "Save" ✅

---

## STEP 5: REDEPLOY SOU VERCEL 🚀

### 5.1 Run sa nan terminal:
```bash
vercel --prod
```

Oswa:

### 5.2 Nan Vercel Dashboard:
- Deployments → Latest deployment → ... menu → Redeploy

---

## STEP 6: TEST DATABASE CONNECTION 🧪

### 6.1 Check Health Endpoint
```
https://your-app.vercel.app/health
```

Should show:
```json
{
  "status": "healthy",
  "database": "connected",
  ...
}
```

### 6.2 Test API
```
https://your-app.vercel.app/api/test
```

---

## QUICK SETUP COMMANDS 🚀

```bash
# 1. Make sure .env exists locally (for development)
echo "SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co" > .env
echo "SUPABASE_KEY=your-anon-key-here" >> .env

# 2. Redeploy to Vercel
vercel --prod

# 3. Test health
curl https://your-app.vercel.app/health

# 4. Check logs
vercel logs
```

---

## TROUBLESHOOTING 🔧

### Problem: "Database not connected"
**Solution**:
1. Check environment variables nan Vercel
2. Verify Supabase URL ak Key
3. Redeploy after adding variables

### Problem: "Row Level Security" errors
**Solution**:
1. Disable RLS for testing:
   ```sql
   ALTER TABLE users DISABLE ROW LEVEL SECURITY;
   ALTER TABLE projects DISABLE ROW LEVEL SECURITY;
   ```
2. Or create test user with proper auth

### Problem: Can't connect from Vercel
**Solution**:
1. Check Supabase project is not paused
2. Verify API keys are correct
3. Check Vercel logs: `vercel logs`

---

## VERIFICATION CHECKLIST ✅

- [ ] Supabase project created
- [ ] SQL schema executed
- [ ] Tables visible in Supabase dashboard
- [ ] API keys copied
- [ ] Environment variables added to Vercel
- [ ] Redeployed to Vercel
- [ ] `/health` shows "connected"
- [ ] Can create/read data

---

## NEXT STEPS 🎯

1. **Test User Creation**:
   ```bash
   curl -X POST https://your-app.vercel.app/api/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
   ```

2. **Test Project Creation**:
   - Use audiobook/podcast/video features
   - Check if data saved in Supabase

3. **Monitor Database**:
   - Supabase Dashboard → Table Editor
   - See data in real-time

---

## 🎉 FÉLICITASYON!

Database w pare! Kounye a ou gen:
- ✅ User management
- ✅ Project tracking
- ✅ Voice storage
- ✅ Audio metadata
- ✅ Real-time sync

**Platform w 100% functional! 🚀**

