# 🔧 ADD USERNAME COLUMN TO USERS TABLE
# SQL to fix database schema

---

## 📋 COPY AND RUN THIS SQL:

```sql
-- Add username column to users table
ALTER TABLE users 
ADD COLUMN username varchar;

-- Make it unique (no duplicates)
ALTER TABLE users 
ADD CONSTRAINT users_username_unique UNIQUE (username);

-- Add index for faster lookups
CREATE INDEX idx_users_username ON users(username);
```

---

## ✅ WHAT THIS DOES:

1. Adds `username` column (varchar)
2. Makes it unique (no duplicate usernames)
3. Adds index for fast searches

---

## 📋 STEPS:

1. **Copy** the SQL above
2. **Paste** in Supabase SQL Editor
3. **Click "RUN"**
4. **Wait** for "Success"
5. **Di m "success"**

---

**Copy SQL la epi run li kounye a!** 🚀

