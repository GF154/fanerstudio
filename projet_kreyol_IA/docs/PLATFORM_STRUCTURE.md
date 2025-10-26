# 🏗️ Kreyòl IA - Platform Structure

> **Documentation sou estrikti platfòm nan**

## 📊 Current Structure (Recommended ✅)

```
projet_kreyol_IA/
├── app_studio_dark.html         # 🎨 Single-page app (RECOMMENDED)
├── app_kreyol.html              # 🇭🇹 100% Kreyòl version
├── app/                         # 🐍 Backend API
│   ├── main.py
│   ├── api.py
│   ├── workflows.py
│   ├── nllb_pipeline.py
│   └── services/
│       ├── tts_service.py
│       ├── stt_service.py
│       └── media_service.py
└── pages/                       # 📄 (Optional) Multi-page structure
    ├── audiobook.html
    ├── podcast.html
    └── ...
```

---

## 🎯 Two Approaches

### Approach 1: Single-Page Application (SPA) ✅ CURRENT

**Files:**
- `app_studio_dark.html` - Main interface (dark theme)
- `app_kreyol.html` - 100% Kreyòl version

**Advantages:**
- ✅ Faster (no page reloads)
- ✅ Better UX (smooth transitions)
- ✅ Modern approach
- ✅ Already implemented
- ✅ All features in one place

**How it works:**
- All content in one file
- JavaScript switches between sections
- API calls to backend

---

### Approach 2: Multi-Page Application (MPA)

**Structure:**
```
/creative-platform
├── index.html              # Home page
├── style.css               # Shared styles
├── script.js               # Shared JavaScript
├── pages/
│   ├── audiobook.html      # Audiobook creator
│   ├── podcast.html        # Podcast generator
│   ├── url_to_audio.html   # URL to audio
│   ├── script_generator.html # AI script gen
│   ├── video_voiceover.html  # Add voiceover
│   ├── add_music.html      # Add SFX/music
│   ├── fix_voice.html      # Fix voiceover
│   ├── captions.html       # Generate captions
│   ├── soundtrack.html     # AI soundtrack
│   └── noise_remove.html   # Remove noise
└── assets/
    └── icons/              # Icons
```

**Advantages:**
- ✅ Easier to maintain (separate files)
- ✅ Better for SEO
- ✅ Clearer organization

**Disadvantages:**
- ❌ Page reloads
- ❌ More files to manage
- ❌ Need to duplicate navigation

---

## 🔄 Migration Options

### Option 1: Keep SPA (Recommended)

**Current status:** ✅ Working perfectly
- Modern dark UI
- All features accessible
- Fast and responsive
- Already localized in Creole

**Action:** Keep using `app_studio_dark.html` or `app_kreyol.html`

---

### Option 2: Create MPA

If you want multi-page structure, I can:

1. **Extract sections** from `app_studio_dark.html`
2. **Create individual pages** for each feature
3. **Add navigation** between pages
4. **Share styles** with CSS file

---

## 💡 Recommendation

### For Your Use Case:

**KEEP THE SINGLE-PAGE APP** (`app_studio_dark.html`)

**Why?**
- ✅ Already built and working
- ✅ Modern UX with smooth transitions
- ✅ All features already implemented
- ✅ Dark theme looks professional
- ✅ Backend API already supports it

**What you have:**
- Beautiful dark UI
- Card-based navigation
- Modal dialogs for each feature
- Smooth animations
- Professional look

---

## 🎨 Current Features in app_studio_dark.html

### Audio Section:
- 📚 New audiobook
- 🎙️ Create podcast
- 🔗 URL to audio
- ✨ AI Script Generator

### Video Section:
- 🎥 New video voiceover
- 🎵 Add SFX and music
- 📝 Add captions
- 🔇 Remove background noise
- 🔧 Fix voiceover mistakes
- 🎼 AI Soundtrack Generator

### Navigation:
- 🏠 Home
- 🎤 Voices
- 🗣️ Text to Speech
- 🎭 Voice Changer
- 🔊 Sound Effects
- 🎯 Voice Isolator

---

## 🔧 If You Want Multi-Page

I can create a multi-page version, but you'll need to decide:

### Questions:

1. **Do you want to keep the current SPA or switch to MPA?**
2. **Do you want both versions available?**
3. **Which pages are most important to split out?**

### If switching to MPA, I will:

1. ✅ Create `index.html` (home page)
2. ✅ Create individual pages in `pages/`
3. ✅ Extract shared CSS to `style.css`
4. ✅ Extract shared JS to `script.js`
5. ✅ Add navigation component
6. ✅ Link all pages together
7. ✅ Update API endpoints if needed

---

## 📝 What Would You Like?

### Option A: Keep Current SPA ✅
- Continue using `app_studio_dark.html`
- No changes needed
- Everything works

### Option B: Create MPA Structure
- I'll build the multi-page version
- Extract each feature to its own page
- Add navigation between pages

### Option C: Hybrid
- Keep SPA as main interface
- Create separate pages for complex features
- Best of both worlds

---

## 🚀 Next Steps

Let me know which option you prefer:

1. **Keep SPA** - No changes, already perfect
2. **Create MPA** - I'll build the full multi-page structure
3. **Hybrid** - Combine both approaches

**Current recommendation:** Keep the SPA (app_studio_dark.html) because:
- It's already built
- Modern and professional
- Works perfectly
- All features accessible

---

**What do you prefer?** 🤔

