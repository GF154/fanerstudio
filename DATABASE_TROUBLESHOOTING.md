# ⚠️ DATABASE DISCONNECTED - TROUBLESHOOTING
# Fikse Pwoblèm Database Connection

---

## 🔍 PWOBLÈM IDANTIFYE:

```json
{
  "database": "disconnected"  ← PA BON!
}
```

**Sa vle di:** Vercel pa ka konekte ak Supabase

---

## 🛠️ SOLISYON RAPID:

### STEP 1: VERIFY VERCEL ENVIRONMENT VARIABLES

Mwen ouvri paj Environment Variables la pou ou.

**Check sa yo:**

1. **SUPABASE_URL exists?**
   - Name: `SUPABASE_URL`
   - Value: `https://xxxxx.supabase.co`
   - ✅ Production checked?

2. **SUPABASE_KEY exists?**
   - Name: `SUPABASE_KEY`
   - Value: `eyJhbGci...` (long string)
   - ✅ Production checked?

---

## 🔧 SI KEYS YO PA LA:

### Option A: KEYS PA ADD ANKÒ

**Add yo kounye a:**

1. Click "Add New"
2. Name: `SUPABASE_URL`
3. Value: [Ton Supabase URL]
4. Check ✅ Production, ✅ Preview, ✅ Development
5. Save

6. Click "Add New" ankò
7. Name: `SUPABASE_KEY`
8. Value: [Ton anon key]
9. Check ✅ Production, ✅ Preview, ✅ Development
10. Save

---

## 🔧 SI KEYS YO EGZISTE:

### Option B: KEYS LA MEN PA LOAD

**Problem:** Deployment avan keys yo

**Solution:**
1. Verify keys are correct
2. Redeploy: `vercel --prod`

---

## 🔧 SI W PA GEN KEYS YO:

### Option C: GET KEYS FROM SUPABASE

1. Go to: https://supabase.com/dashboard
2. Select project
3. Settings → API
4. Copy:
   - Project URL
   - anon public key (NOT service_role!)

---

## 📋 QUICK COMMANDS:

```bash
# After adding/fixing keys, redeploy:
vercel --prod

# Then check health:
# https://your-url.vercel.app/health
```

---

## ✅ VERIFICATION:

**After fixing, you should see:**
```json
{
  "database": "connected"  ← BON!
}
```

---

## 🆘 NEED HELP?

**Tell me where you're at:**
- "m pa gen keys yo" → I'll help you get them
- "m add keys yo" → I'll help redeploy
- "keys yo la men ankò disconnected" → I'll troubleshoot

**Ki pwoblèm ou genyen?** 👇

