# 🔍 Deployment Status Checker

Yon script pratik pou tcheke status deplwaman GitHub Actions ak Render an tan reyèl!

---

## 🚀 Quick Start

### **Windows:**
```bash
# Double-click on:
CHECK_DEPLOYMENT.bat

# Or run in PowerShell:
python check_deployment.py
```

### **Mac/Linux:**
```bash
python3 check_deployment.py
```

---

## 📊 Sa Script la Fè

### **1. Quick Status Check** ✅
- Tcheke dènye GitHub Actions workflow
- Verifye si Render service online
- Montre rezime rapid

### **2. Continuous Monitoring** 🔄
- Swiv deplwaman an otomatikman
- Check chak 30 segonn
- Notifye w lè l fini

### **3. Detailed Information** 📊
```
✅ Workflow status
🔀 Branch deployed
📊 Build status
🕐 Timestamps
🌐 Service URLs
💚 Health checks
📦 Version info
```

---

## 🎯 Exemple Output

```
============================================================
           🇭🇹 Faner Studio - Deployment Checker
============================================================

============================================================
              🔍 GitHub Actions Status
============================================================

✅ Workflow:                     🚀 Auto-Deploy to Render
🔀 Branch:                       master
📊 Status:                       completed (success)
🕐 Started:                      2025-11-01T15:30:00Z
🕐 Updated:                      2025-11-01T15:35:00Z
🔗 URL:                          https://github.com/...

============================================================
                ☁️  Render Service Status
============================================================

🔍 Trying: https://kreyol-ia-studio.onrender.com

✅ Service:                      ONLINE
🌐 URL:                          https://kreyol-ia-studio.onrender.com
💚 Health:                       Healthy
📦 Version:                      2.0.0
🏷️ Name:                         Faner Studio
🚀 Deployment:                   GitHub Actions → Render
📊 Environment:                  production
🐍 Python:                       3.11.0

============================================================
                    📊 Summary
============================================================

✅ GitHub Actions:               Completed successfully
✅ Render Service:               Online

Options:
  1. Monitor continuously (check every 30s)
  2. Exit

Choice [1/2]:
```

---

## 🎨 Features

### **Color-Coded Status** 🌈
- 🟢 Green = Success
- 🟡 Yellow = In Progress
- 🔴 Red = Failed
- 🔵 Blue = Links

### **Real-Time Updates** ⚡
- Auto-refresh every 30 seconds
- Shows progress over time
- Timestamps on each check

### **Smart Detection** 🧠
- Tries multiple service URLs
- Handles timeouts gracefully
- Clear error messages

### **User-Friendly** 😊
- Simple interface
- Easy to understand
- Keyboard interrupt support (Ctrl+C)

---

## 📋 Requirements

```bash
# Install dependencies:
pip install requests
```

---

## 🔧 Configuration

### **Custom Service URL**

Edit `check_deployment.py`:

```python
# Line ~85 - Add your Render URL
urls_to_try = [
    "https://your-service.onrender.com",  # Your URL
    "https://kreyol-ia-studio.onrender.com",
    "https://fanerstudio.onrender.com"
]
```

### **Check Interval**

```python
# Line ~180 - Change monitoring interval
monitor_deployment(check_interval=30, max_checks=20)
#                  ↑ seconds      ↑ max attempts
```

---

## 🎯 Use Cases

### **1. After Pushing Code**
```bash
git push
python check_deployment.py
# Monitor until deployment complete
```

### **2. Check Current Status**
```bash
python check_deployment.py
# Choose option 2 for quick check
```

### **3. Debug Failed Deployment**
```bash
python check_deployment.py
# See detailed error info
# Click GitHub Actions link for logs
```

---

## 📚 API Endpoints Checked

| Endpoint | Purpose |
|----------|---------|
| `/health` | Service health status |
| `/api/status` | Detailed system info |
| GitHub Actions API | Workflow status |

---

## 🔍 Troubleshooting

### **"No workflows found"**
- Wait a few seconds after pushing
- Check GitHub Actions manually

### **"Unable to connect"**
- Service might still be deploying
- Wait 2-3 minutes and try again
- Check Render dashboard

### **"Request timed out"**
- Service is starting up
- Try monitoring mode (option 1)

---

## 💡 Tips

1. **Run after pushing** - Start monitoring immediately
2. **Use monitoring mode** - For first deployment
3. **Check GitHub Actions** - For detailed logs
4. **Be patient** - Deployment takes 5-8 minutes

---

## 🆘 Support

- **GitHub Actions**: https://github.com/GF154/fanerstudio/actions
- **Render Dashboard**: https://dashboard.render.com
- **Service Health**: https://your-service.onrender.com/health

---

## 📝 Notes

- Script uses GitHub public API (no token needed)
- Works with any public repository
- Cross-platform (Windows/Mac/Linux)
- No installation required (just Python + requests)

---

## 🎉 Example Workflow

```bash
# 1. Make changes
git add .
git commit -m "Update feature"
git push

# 2. Check deployment
python check_deployment.py

# 3. Choose monitoring
> 1

# 4. Wait for success
✅ DEPLOYMENT SUCCESSFUL!

# 5. Test your service
curl https://your-service.onrender.com/health
```

---

## 🇭🇹 Faner Studio

Made with ❤️ for the Haitian Creole community

**Bon deplwaman!** 🚀

