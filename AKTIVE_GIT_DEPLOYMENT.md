# 🔗 Aktive Git Auto-Deployment

## ETAP NAN VERCEL DASHBOARD:

### Option 1: Aktive Git Integration (Rekòmande)

1. **Settings → Git** (paj ki ouvè)
2. Verifye **"Connected to GitHub: GF154/fanerstudio"** ✅
3. Asire w **"Production Branch"** = `master`
4. Check si **"Ignored Build Step"** = OFF (pou li build chak fwa)

### Option 2: Kreye Deploy Hook

1. **Settings → Git** 
2. Scroll anbà pou jwenn **"Deploy Hooks"**
3. Klike **"Create Hook"**
4. Non: `Auto Deploy Master`
5. Branch: `master`
6. Klike **"Create Hook"**
7. Kòpye URL webhook la

### Option 3: Manual Redeploy (Pi Rapid)

1. **Deployments** tab
2. Klike sou dènye **Production** deployment
3. Klike **"..." menu** → **"Redeploy"**
4. Dekoche **"Use existing Build Cache"**
5. Klike **"Redeploy"**

---

## 🎯 APRE SA:

Chak fwa w push sou GitHub:
```bash
git push origin master
```

Vercel ap deploy otomatikman! 🚀

---

## ✅ VERIFYE:

Apre deployment, check:
```
https://your-site.vercel.app/api/audiobook/voices
```

Dwe wè:
```json
{
  "id": "creole-native",
  "name": "🇭🇹 Kreyòl Natif (Male)",
  "default": true
}
```

