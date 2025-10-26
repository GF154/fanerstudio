# 🚀 QUICK START - VERSION 4.0

## ⚡ **KÒMANSE RAPID (5 MINIT)**

### **1. INSTALL**

```bash
cd projet_kreyol_IA
pip install -r requirements.txt
```

### **2. LANCE**

```bash
python app/main.py
```

### **3. OUVRI**

```
http://localhost:8000
```

**✅ SA A SE TOUT! Platfòm nan ap kouri!**

---

## 🎯 **TESTE NOUVO FEATURES**

### **Login (JWT)**

**Browser:**
1. Ale `http://localhost:8000/docs`
2. Klike "POST /api/auth/login"
3. Try it out
4. Enter:
   - email: `demo@kreyolia.ht`
   - password: `demo123`
5. Execute
6. Copy `access_token`

**cURL:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -F "email=demo@kreyolia.ht" \
  -F "password=demo123"
```

### **Background Audiobook**

**With Token:**
```bash
TOKEN="your-token-here"

curl -X POST http://localhost:8000/api/audiobook/async \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@document.pdf" \
  -F "voice=creole-native"
```

**Response:**
```json
{
  "task_id": "abc-123-def",
  "check_url": "/api/tasks/abc-123-def"
}
```

### **Check Progress**

```bash
curl http://localhost:8000/api/tasks/abc-123-def
```

**Real-time (JavaScript):**
```html
<script>
const ws = new WebSocket('ws://localhost:8000/ws/tasks/abc-123-def');
ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  console.log(`${data.progress}% - ${data.status}`);
};
</script>
```

---

## 🔧 **OPTIONAL: REDIS + CELERY**

**Pou full features (background jobs + cache):**

### **Install Redis:**

**Option 1: Docker (Pi fasil)**
```bash
docker run -d -p 6379:6379 redis:latest
```

**Option 2: Native**
- Windows: Download from https://github.com/microsoftarchive/redis/releases
- Linux: `sudo apt-get install redis-server`
- Mac: `brew install redis`

### **Start Celery Worker:**

```bash
celery -A app.tasks worker --loglevel=info --pool=solo
```

### **Restart Server:**

```bash
python app/main.py
```

**Ou pral wè:**
```
✅ Redis: Connected
✅ Celery: Configured
```

---

## 📝 **DEMO USERS**

| Email | Password | Role |
|-------|----------|------|
| demo@kreyolia.ht | demo123 | User |
| admin@kreyolia.ht | admin123 | Admin |
| test@kreyolia.ht | test123 | Test |

---

## 🎉 **COMPLETE!**

**Sans Redis/Celery:** ✅ Works (limited features)  
**Ak Redis/Celery:** ✅✅ Full power!

**Pwochen Eta:**
- Li `docs/VERSION_4.0_COMPLETE.md` pou detay konplè
- Teste tout nouvo endpoints nan `/docs`
- Kòmanse kreye kontni! 🇭🇹✨

