# 🔐 DISABLE ROW LEVEL SECURITY (RLS)
# For testing/development - Enable policies later for production

---

## ⚠️ PROBLEM:

```
Status: 401
"new row violates row-level security policy for table \"projects\""
```

**Supabase RLS** anpeche inserts/updates san authentication!

---

## ✅ SOLUTION - Run SQL nan Supabase:

### OPSYON 1: Disable RLS (Quick - Pou Testing)

```sql
-- Disable RLS on all tables
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE projects DISABLE ROW LEVEL SECURITY;
ALTER TABLE voices DISABLE ROW LEVEL SECURITY;
ALTER TABLE audios DISABLE ROW LEVEL SECURITY;
```

### OPSYON 2: Enable Public Access (Better - Keep RLS active)

```sql
-- Create policies to allow all operations (for now)

-- Users table
CREATE POLICY "Enable all access for users" ON users
FOR ALL USING (true) WITH CHECK (true);

-- Projects table  
CREATE POLICY "Enable all access for projects" ON projects
FOR ALL USING (true) WITH CHECK (true);

-- Voices table
CREATE POLICY "Enable all access for voices" ON voices
FOR ALL USING (true) WITH CHECK (true);

-- Audios table
CREATE POLICY "Enable all access for audios" ON audios
FOR ALL USING (true) WITH CHECK (true);
```

---

## 📋 KISA POU W FÈ:

1. **Go to Supabase Dashboard** → SQL Editor
2. **Copy ak paste** youn nan 2 SQL scripts yo
3. **Click "Run"**
4. **Di m "m fè l"**

---

## 🎯 RECOMMENDATION:

**Use OPSYON 2** (policies) - Pi bon pou production pi devan!

**OPSYON 1** (disable RLS) - Pi rapid pou testing, men mwens secure.

---

**Ki opsyon w prefere?** 🔧

