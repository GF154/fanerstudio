# 🔧 GUIDE: Fix Render Service - Step by Step

**Problem Detected:** Render service is using OLD CODE  
**Solution:** Update service configuration and redeploy  
**Time Required:** 5-10 minutes

---

## 🎯 **WHAT YOU'LL FIX:**

```
Current State:
❌ Only 3/10 endpoints working
❌ No admin dashboard
❌ No new API features

After Fix:
✅ All 10 endpoints working
✅ Admin dashboard live
✅ All features active
```

---

## 📋 **STEP-BY-STEP INSTRUCTIONS:**

### **STEP 1: Open Render Dashboard** 🌐

1. Open your browser
2. Go to: **https://dashboard.render.com**
3. Login if prompted
4. You should see your services list

**Screenshot location:** You'll see "fanerstudio-1" in the list

---

### **STEP 2: Select Your Service** 🎯

1. Click on: **`fanerstudio-1`**
2. You'll see the service overview page
3. Look for tabs at the top: Overview, Logs, **Settings**, etc.

**Current status:** Service shows "Live" but with old code

---

### **STEP 3: Go to Settings** ⚙️

1. Click the **"Settings"** tab (in left sidebar OR top menu)
2. Scroll down to find these sections:
   - Build & Deploy
   - General

---

### **STEP 4: Update Build & Deploy** 🏗️

#### **A. Find "Build & Deploy" section**

Scroll to: **Build & Deploy** section

#### **B. Update Build Command:**

**Current (wrong):** 
```
(might be empty or different)
```

**Change to (correct):**
```
pip install --upgrade pip && pip install -r requirements.txt
```

**How to change:**
1. Click the "Edit" button next to "Build Command"
2. Clear the field
3. Copy and paste the command above
4. Click "Save"

#### **C. Update Start Command:**

**Current (wrong):**
```
(might be gunicorn or something else)
```

**Change to (correct):**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**How to change:**
1. Click the "Edit" button next to "Start Command"
2. Clear the field
3. Copy and paste the command above
4. Click "Save"

---

### **STEP 5: Check General Settings** 🔍

#### **A. Scroll to "General" section**

#### **B. Verify Branch:**

**Should be:** `master`

**If it says "main":**
1. Click "Edit" next to Branch
2. Change to: `master`
3. Click "Save"

#### **C. Verify Auto-Deploy:**

**Should be:** ✅ Enabled (Yes)

**If it's disabled:**
1. Toggle the switch to enable
2. Save changes

#### **D. Verify Root Directory:**

**Should be:** (empty/blank)

**If something is there:**
1. Clear it
2. Save

---

### **STEP 6: Manual Deploy** 🚀

Now trigger a fresh deployment:

1. **Go back to the top of the page**
2. Look for **"Manual Deploy"** button (usually top right)
3. Click **"Manual Deploy"**
4. Select: **"Deploy latest commit"**
5. Click **"Yes, deploy"** or confirm

**What happens next:**
```
⏰ 0-1 min:  "Build in progress..."
⏰ 1-3 min:  Installing dependencies
⏰ 3-4 min:  Building application
⏰ 4-5 min:  Deploying...
✅ 5 min:    "Your service is live!"
```

---

### **STEP 7: Monitor Deployment** 👀

#### **A. Watch the Logs:**

1. Click **"Logs"** tab
2. You'll see real-time output
3. Look for these messages:

**Good signs:**
```
==> Building...
==> Cloning repository...
==> Installing dependencies...
==> Running: pip install -r requirements.txt
==> Build completed successfully
==> Starting service...
==> Your service is live!
```

**Bad signs (if you see these, check your settings again):**
```
❌ Error: Command not found
❌ Error: No such file requirements.txt
❌ Build failed
```

#### **B. Wait for "Live" status:**

Top of page should show:
```
🟢 Live
```

---

### **STEP 8: Verify Deployment** ✅

After deployment finishes (5 minutes):

#### **Option A: Run verification script**

In your terminal:
```bash
python verify_deployment.py
```

**Expected result:**
```
✅ fanerstudio-1: ACTIVE (10/10 endpoints)
```

#### **Option B: Test manually**

Open these URLs in browser:

1. **Main platform:**
   ```
   https://fanerstudio-1.onrender.com
   ```
   Should show: Beautiful interface

2. **Admin dashboard:**
   ```
   https://fanerstudio-1.onrender.com/admin
   ```
   Should show: Admin login page

3. **API docs:**
   ```
   https://fanerstudio-1.onrender.com/docs
   ```
   Should show: 28 endpoints documented

4. **API status:**
   ```
   https://fanerstudio-1.onrender.com/api/status
   ```
   Should return: JSON with system info

---

## 🎉 **SUCCESS CHECKLIST:**

After completing all steps, verify:

```
✅ Build Command updated
✅ Start Command updated
✅ Branch set to "master"
✅ Auto-Deploy enabled
✅ Manual deploy triggered
✅ Deployment completed (5 min)
✅ Service shows "Live"
✅ 10/10 endpoints working
✅ Admin dashboard accessible
```

---

## 🐛 **TROUBLESHOOTING:**

### **Problem: Build fails**

**Solution:**
- Check Build Command is EXACTLY:
  ```
  pip install --upgrade pip && pip install -r requirements.txt
  ```
- Check Branch is set to `master`

### **Problem: Service starts but 404 errors**

**Solution:**
- Check Start Command is EXACTLY:
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
- Make sure Root Directory is EMPTY

### **Problem: "No such file requirements.txt"**

**Solution:**
- Branch is wrong (should be `master` not `main`)
- Root Directory should be empty

### **Problem: Deployment takes too long (>10 min)**

**Solution:**
- Check Logs for errors
- Try canceling and redeploying
- Check your internet connection

---

## 📞 **NEED HELP?**

If you get stuck:

1. **Check Logs tab** - Shows exactly what's happening
2. **Take a screenshot** - Of the error message
3. **Run verification script** - Shows what's wrong
4. **Ask me** - I can help troubleshoot!

---

## ✅ **WHEN YOU'RE DONE:**

Run this to confirm everything works:

```bash
python verify_deployment.py
```

Should show:
```
✅ fanerstudio-1: ACTIVE (10/10 endpoints)
📊 DIAGNOSIS: EVERYTHING LOOKS GOOD!
```

---

## 🎯 **VISUAL CHECKLIST:**

Print this and check off as you go:

```
☐ Step 1: Opened Render Dashboard
☐ Step 2: Selected fanerstudio-1
☐ Step 3: Went to Settings
☐ Step 4: Updated Build Command
☐ Step 5: Updated Start Command
☐ Step 6: Verified Branch = master
☐ Step 7: Enabled Auto-Deploy
☐ Step 8: Clicked Manual Deploy
☐ Step 9: Waited 5 minutes
☐ Step 10: Verified with script
☐ Step 11: ALL TESTS PASS! 🎉
```

---

**Good luck! You got this!** 💪

If you follow these steps exactly, your platform will be fully deployed in ~10 minutes.

---

**Created:** 2025-11-03  
**Platform:** Faner Studio  
**Service:** fanerstudio-1.onrender.com

