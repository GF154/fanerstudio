# 🗄️ SUPABASE - GUIDE SENP AN KREYÒL
# Kijan pou w konekte database ou a

---

## ❓ KISA SUPABASE YE?

Supabase se yon database nan cloud (sou entènèt).
Li pèmèt ou:
- ✅ Kenbe done itilizatè yo
- ✅ Kenbe pwojè yo kreye
- ✅ Kenbe vwa yo kreye
- ✅ Kenbe fichye audio/video

---

## 📝 ETAP PA ETAP (TRE SENP)

### ETAP 1: KREYE KONT SUPABASE (5 minit)

**1.1 Ale sou:**
```
https://supabase.com
```

**1.2 Click "Start your project"**

**1.3 Sign in ak:**
- GitHub (pi rapid) ✅
- Google
- oswa Email

**1.4 Click "New Project"**

---

### ETAP 2: KREYE PROJECT (2 minit)

**2.1 Ranpli enfòmasyon:**

📝 **Project Name**: 
```
faner-studio
```
(oswa nenpòt non ou vle)

🔐 **Database Password**:
```
Kreye yon password solid
Pa egzanp: FanerStudio2024!
```
⚠️ **ENPÒTAN: KOPYE PASSWORD SA A!**

🌍 **Region**:
```
Chwazi: East US (1) [us-east-1]
```
(oswa pi pre kote w ye a)

**2.2 Click "Create new project"**

⏰ **Tann 2-3 minit...**
(Supabase ap prepare database w)

---

### ETAP 3: JWENN 2 BAGAY ENPÒTAN (1 minit)

Lè project la fini setup:

**3.1 Click sou "Settings" (icon gear ⚙️ anba)**

**3.2 Click sou "API"**

**3.3 Kopye 2 bagay sa yo:**

🔗 **1. Project URL** (nan tèt paj la):
```
https://XXXXXXXX.supabase.co
```

🔑 **2. anon public key** (pa service_role):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
(yon long string)
```

⚠️ **KOPYE YO NAN YON NOTPAD!**

---

### ETAP 4: KREYE TABLES NAN DATABASE (2 minit)

**4.1 Nan Supabase dashboard, click sou "SQL Editor"**

**4.2 Click "New Query"**

**4.3 Copy/Paste sa (TOUT BAGAY):**

```sql
-- Kreye tab pou users (itilizatè)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Kreye tab pou projects (pwojè)
CREATE TABLE projects (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    project_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    output_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Kreye tab pou voices (vwa)
CREATE TABLE voices (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    voice_name VARCHAR(255) NOT NULL,
    voice_id VARCHAR(100) UNIQUE NOT NULL,
    quality VARCHAR(50) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Kreye tab pou audios
CREATE TABLE audios (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    project_id BIGINT REFERENCES projects(id),
    filename VARCHAR(255) NOT NULL,
    duration FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**4.4 Click "RUN" anba agoch ✅**

Ou dwe wè: **"Success. No rows returned"**

---

### ETAP 5: METE KEYS YO NAN VERCEL (3 minit)

**5.1 Ale sou:**
```
https://vercel.com/dashboard
```

**5.2 Click sou project "faner-studio"**

**5.3 Click "Settings" (anwo adwat)**

**5.4 Click "Environment Variables" (nan meni agoch)**

**5.5 Add premye key:**
- Click "Add New"
- **Key**: `SUPABASE_URL`
- **Value**: `https://XXXXXXXX.supabase.co` (sa ou te kopye)
- Check ✅ **Production**
- Check ✅ **Preview**  
- Check ✅ **Development**
- Click "Save"

**5.6 Add dezyèm key:**
- Click "Add New" ankò
- **Key**: `SUPABASE_KEY`
- **Value**: `eyJhbGci...` (long anon key ou te kopye)
- Check ✅ **Production**
- Check ✅ **Preview**
- Check ✅ **Development**
- Click "Save"

---

### ETAP 6: REDEPLOY PLATFORM LA (1 minit)

**Nan Vercel Dashboard:**

**6.1 Click "Deployments" (anwo)**

**6.2 Click sou latest deployment**

**6.3 Click "..." (3 dots adwat)**

**6.4 Click "Redeploy"**

**6.5 Click "Redeploy" pou konfime**

⏰ **Tann 1-2 minit...**

---

### ETAP 7: TEST SI L FONKSYONE ✅

**7.1 Ale sou:**
```
https://your-app.vercel.app/health
```

**7.2 Ou dwe wè:**
```json
{
  "status": "healthy",
  "database": "connected"  ← SA DWE DI "connected"!
}
```

---

## ✅ FINI! DATABASE W PARE!

Kounye a platform w gen:
- ✅ Database pou kenbe done
- ✅ User management
- ✅ Project tracking
- ✅ Voice storage

---

## 🆘 SI GEN PWOBLÈM:

### Pwoblèm 1: "database": "disconnected"
**Solisyon:**
- Verifye keys yo nan Vercel correct
- Redeploy ankò

### Pwoblèm 2: SQL pa run
**Solisyon:**
- Efase tout sa ki nan SQL Editor
- Copy/paste script la ankò
- Click RUN

### Pwoblèm 3: Pa ka jwenn Settings
**Solisyon:**
- Check icon ⚙️ anba agoch nan Supabase
- Check si project la fini setup

---

## 📞 BEZWEN ÈD?

Si w bloke, di m:
- "m pa jwenn Settings"
- "SQL pa run"
- "m pa wè API keys"
- "m pa konprann etap X"

M ap ede w! 🚀

---

## 🎯 REZIME RAPID:

1. ✅ Kreye kont Supabase
2. ✅ Kreye project "faner-studio"
3. ✅ Copy URL + anon key
4. ✅ Run SQL script
5. ✅ Add keys nan Vercel
6. ✅ Redeploy
7. ✅ Test /health

**Tout sa se yon fwa sèlman!**
Apre sa, database w ap travay pou tout tan! 💪

