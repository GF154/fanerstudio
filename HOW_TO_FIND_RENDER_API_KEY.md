# 🔑 How to Find Your RENDER_API_KEY

**Complete Guide with Screenshots Instructions**

---

## 📍 **LOCATION:**
```
Render Dashboard → Account Settings → API Keys
```

---

## 🎯 **STEP-BY-STEP:**

### **Step 1: Login to Render**
1. Open your browser
2. Go to: **https://dashboard.render.com**
3. Login with your credentials

---

### **Step 2: Navigate to Account Settings**

**Option A: Direct Link**
```
https://dashboard.render.com/u/settings
```

**Option B: Manual Navigation**
1. Click on your **profile icon** (top right corner)
2. Select **"Account Settings"** from dropdown

---

### **Step 3: Go to API Keys Section**

1. In Account Settings, look for left sidebar
2. Click on **"API Keys"** section
3. You'll see the API Keys page

**What you'll see:**
```
API Keys
├─ Create API Key button
├─ List of existing keys (if any)
└─ Key management options
```

---

### **Step 4: Create New API Key**

#### **If you don't have a key yet:**

1. Click **"Create API Key"** button

2. **Fill in details:**
   ```
   Name: Faner Studio Deploy
   Description: For GitHub Actions deployment
   ```

3. Click **"Create"**

4. **IMPORTANT:** Copy the key immediately!
   ```
   Format: rnd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Example: rnd_AbCd1234EfGh5678IjKl9012MnOp
   ```

5. **⚠️ WARNING:** 
   - You can only see the key ONCE
   - Save it in a safe place
   - If you lose it, you'll need to create a new one

---

### **Step 5: Copy Your API Key**

Your API key will look like:
```
rnd_1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S0t
```

**Copy the entire string!**

---

## 🔐 **ADD TO GITHUB SECRETS:**

### **Step 6: Go to GitHub Secrets**

1. Open: **https://github.com/GF154/fanerstudio/settings/secrets/actions**

2. Click **"New repository secret"**

3. Enter:
   ```
   Name:  RENDER_API_KEY
   Value: rnd_[paste your key here]
   ```

4. Click **"Add secret"**

---

## ✅ **VERIFICATION:**

After adding both secrets, you should have:

```
GitHub Secrets:
├─ ✅ RENDER_API_KEY        (rnd_xxxx...)
└─ ✅ RENDER_SERVICE_ID     (tea-d3gfkg8gjchc739npt3g)
```

---

## 🧪 **TEST IT:**

### **Trigger a deployment:**

```bash
# Make a small change
git add .
git commit -m "test: Verify Render secrets configured"
git push origin master
```

### **Check workflow:**
1. Go to: **https://github.com/GF154/fanerstudio/actions**
2. Watch the latest workflow run
3. It should pass the validation step now!

---

## 🎯 **QUICK LINKS:**

| Resource | URL |
|----------|-----|
| **Render Settings** | https://dashboard.render.com/u/settings |
| **API Keys Page** | https://dashboard.render.com/u/settings (then click API Keys) |
| **GitHub Secrets** | https://github.com/GF154/fanerstudio/settings/secrets/actions |
| **GitHub Actions** | https://github.com/GF154/fanerstudio/actions |

---

## ⚠️ **IMPORTANT SECURITY NOTES:**

### **DO:**
- ✅ Store API key in GitHub Secrets only
- ✅ Never commit API key to code
- ✅ Create key with descriptive name
- ✅ Copy key immediately when created
- ✅ Revoke old keys you're not using

### **DON'T:**
- ❌ Share API key publicly
- ❌ Commit to git repository
- ❌ Post in issues or comments
- ❌ Send via email/chat
- ❌ Store in plain text files

---

## 🔄 **IF YOU LOSE YOUR KEY:**

1. Go back to Render API Keys page
2. **Delete the old key**
3. **Create a new key**
4. **Update GitHub Secret** with new value

---

## 💡 **TIPS:**

1. **Name your keys clearly:**
   ```
   ✅ Good: "GitHub Actions - Faner Studio"
   ❌ Bad: "key1"
   ```

2. **Create separate keys** for different purposes:
   - One for GitHub Actions
   - One for local development
   - One for CI/CD tools

3. **Rotate keys regularly** for security

4. **Keep a backup** in a secure password manager

---

## 📞 **NEED HELP?**

If you can't find the API Keys section:

1. **Check your account type:**
   - Free tier has API access ✅
   - Make sure you're logged in

2. **Look for:**
   - Profile icon (top right)
   - Account Settings menu
   - API Keys in sidebar

3. **Still stuck?**
   - Contact Render support
   - Check: https://render.com/docs/api

---

## 🎉 **ONCE CONFIGURED:**

Your workflow will:
```
✅ Validate secrets
✅ Deploy to Render automatically
✅ Run health checks
✅ Report status
```

---

**Good luck! 🚀**

Once you have your API key, add it to GitHub Secrets and you're ready to deploy!

