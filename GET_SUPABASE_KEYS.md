# 🔑 GET YOUR SUPABASE KEYS
# Step-by-Step pou jwenn keys yo

---

## STEP 1: OPEN SUPABASE 🌐

Go to: https://supabase.com/dashboard

---

## STEP 2: SELECT YOUR PROJECT 📁

1. Find project "faner-studio" (oswa non w te bay li)
2. Click sou li

**⚠️ Si w pa gen project:**
- Click "New Project"
- Name: faner-studio
- Password: [kreye yon solid password]
- Region: East US
- Wait 2-3 min pou setup

---

## STEP 3: GET API KEYS 🔑

1. **Click Settings** (icon ⚙️ anba agoch)

2. **Click "API"** (nan left menu)

3. **COPY KEY #1 - Project URL:**
   ```
   Section: "Project URL"
   Format: https://xxxxxxxxxxxxx.supabase.co
   ```
   📋 **COPY SA A!** → Paste nan Notepad

4. **COPY KEY #2 - anon public:**
   ```
   Section: "Project API keys"
   Label: "anon public"
   Format: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M...
   (VERY LONG STRING - 200+ characters)
   ```
   📋 **COPY SA A TOU!** → Paste nan Notepad

   ⚠️ **IMPORTANT:**
   - Use "anon public" key
   - PA use "service_role" key!

---

## STEP 4: PASTE NAN VERCEL 📌

### Now go back to Vercel Environment Variables page

**ADD KEY #1:**
1. Click "Add New"
2. **Name:** `SUPABASE_URL`
3. **Value:** [Paste ton Project URL]
4. **Environments:** Check ALL 3:
   - ✅ Production
   - ✅ Preview
   - ✅ Development
5. Click "Save"

**ADD KEY #2:**
1. Click "Add New" ankò
2. **Name:** `SUPABASE_KEY`
3. **Value:** [Paste ton anon public key]
4. **Environments:** Check ALL 3:
   - ✅ Production
   - ✅ Preview
   - ✅ Development
5. Click "Save"

---

## STEP 5: REDEPLOY 🚀

### Return to PowerShell and run:

```bash
vercel --prod
```

Wait 1-2 minutes...

---

## STEP 6: VERIFY ✅

### Check health again:

Go to: https://your-new-url.vercel.app/health

**Should see:**
```json
{
  "database": "connected"  ← YAY!
}
```

---

## 🆘 HELP NEEDED?

**Where are you stuck?**

Tell me:
- "m pa jwenn Settings" 
- "m pa wè API keys"
- "m kopye keys yo, kounye a?"
- "m add nan Vercel, kounye a?"

**Ki etap ou ye?** 👇

