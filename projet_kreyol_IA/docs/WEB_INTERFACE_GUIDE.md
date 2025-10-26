# 🌐 Web Interface Quick Guide

## **Accessing the Application**

The web interface is now running at: **http://localhost:8501**

If your browser didn't open automatically, click the link above or paste it in your browser.

---

## **📖 How to Use the Web Interface**

### **Main Features:**

1. **📄 Upload & Process Tab**
   - Upload a PDF file
   - Set source and target languages
   - Configure processing options
   - Start translation

2. **📊 Results Tab**
   - View extracted text
   - Download translated text
   - Listen to audiobook
   - Download audio file

3. **ℹ️ About Tab**
   - Project information
   - Features overview
   - Version details

---

## **🎯 Step-by-Step Usage**

### **Step 1: Upload Your PDF**

1. Go to the **📄 Upload & Process** tab
2. Click **"Browse files"** or drag & drop your PDF
3. Supported: Any text-based PDF (not scanned images)

### **Step 2: Configure Settings**

**In the sidebar (⚙️ Settings):**

- **Source Language:** 
  - `Auto-detect` (recommended)
  - Or select: French, English, Spanish, etc.

- **Target Language:**
  - `Haitian Creole` (default)
  - Or choose another language

- **Options:**
  - ☑️ Enable cache (faster for repeated text)
  - ☐ Parallel translation (faster for large docs)
  - ☑️ Generate audiobook

### **Step 3: Process**

1. Click **🚀 Process** button
2. Watch the progress bar:
   - ⏳ Extracting text...
   - ⏳ Translating...
   - ⏳ Generating audio...
3. Wait for completion (2-10 minutes depending on size)

### **Step 4: Get Results**

1. Go to **📊 Results** tab
2. View your translated text
3. Listen to the audiobook
4. Download files:
   - 📥 Download translation (.txt)
   - 📥 Download audiobook (.mp3)

---

## **⚙️ Configuration Options**

### **Sidebar Settings:**

| Setting | Description | Recommended |
|---------|-------------|-------------|
| **Source Language** | Input language | Auto-detect |
| **Target Language** | Output language | Haitian Creole |
| **Enable cache** | Speed up repeats | ✅ ON |
| **Parallel translation** | Faster processing | ✅ ON for large files |
| **Chunk size** | Text segment size | 1000 (default) |
| **Generate audiobook** | Create audio | ✅ ON |

---

## **📊 What Happens During Processing**

### **Phase 1: Text Extraction (30s - 1min)**
- Reads your PDF
- Extracts all text
- Shows character count

### **Phase 2: Translation (2-10min)**
- **First time:** Downloads M2M100 model (~1.5GB, one-time)
- **Subsequent times:** Uses cached model (fast!)
- Translates to Haitian Creole
- Shows progress bar

### **Phase 3: Audio Generation (1-3min)**
- Converts text to speech
- Creates MP3 file
- Shows file size

---

## **💡 Tips for Best Results**

### **PDF Quality:**
✅ **Use text-based PDFs** (not scanned images)
✅ **Clear formatting** (better extraction)
✅ **Reasonable size** (< 50 MB, < 500 pages)

### **Performance:**
✅ **Enable cache** for repeated content
✅ **Use parallel** for documents > 10 pages
✅ **First run is slower** (downloads model)
✅ **Keep browser tab open** during processing

### **Language Detection:**
✅ **Auto-detect works well** for common languages
✅ **Specify manually** if detection is wrong
✅ **Supported:** 100+ languages

---

## **🎨 Interface Features**

### **Top Navigation:**
- **📄 Upload & Process** - Main workflow
- **📊 Results** - View outputs
- **ℹ️ About** - Project info

### **Sidebar (⚙️):**
- **Konfigirasyon / Settings**
- Language selection
- Performance options
- Processing settings

### **Progress Indicators:**
- Progress bars for each step
- Status messages
- Cache hit statistics
- File size information

---

## **📥 Download Options**

After processing completes:

1. **Extracted Text** (.txt)
   - Original text from PDF
   - UTF-8 encoded

2. **Translated Text** (.txt)
   - Haitian Creole translation
   - Ready to edit/use

3. **Audiobook** (.mp3)
   - Full audio narration
   - Haitian Creole speech
   - Standard MP3 format

---

## **🔊 Audio Features**

### **Text-to-Speech Options:**
- **Language:** Haitian Creole (ht)
- **Speed:** Normal (adjustable in settings)
- **Quality:** Google TTS (gTTS)
- **Format:** MP3
- **Max length:** 100,000 characters

### **Playing Audio:**
- ▶️ Play directly in browser
- 📥 Download to your device
- 🎧 Use any MP3 player

---

## **📊 Statistics Displayed**

After processing, you'll see:

- **Original characters:** Text length
- **Translated characters:** Output length
- **Audio size:** File size in MB
- **Cache stats:** Hit rate (if enabled)
- **Processing time:** Total duration

---

## **⚠️ Troubleshooting**

### **Issue: "Model downloading..."**
**Solution:** First run downloads M2M100 (~1.5GB)
- This is normal and only happens once
- Takes 5-10 minutes depending on internet
- Model is cached for future use

### **Issue: "Processing stuck"**
**Solution:** 
- Check console for errors
- Ensure PDF is text-based (not scanned)
- Try a smaller PDF first
- Check internet connection (first run)

### **Issue: "No audio generated"**
**Solution:**
- Check "Generate audiobook" is enabled
- Verify text isn't too long (>100k chars)
- Check FFmpeg is installed

### **Issue: "Translation seems wrong"**
**Solution:**
- Try specifying source language manually
- Check if PDF extracted correctly
- M2M100 model may need context
- Consider editing translation manually

---

## **🎯 Example Workflow**

### **Translating a French Book:**

1. **Prepare PDF:**
   - Have your French PDF ready
   - Check it's not too large (<50MB)

2. **Upload:**
   - Open web interface
   - Upload your PDF
   - Wait for confirmation

3. **Configure:**
   - Source: French (or Auto-detect)
   - Target: Haitian Creole
   - Enable cache: ✅
   - Generate audio: ✅

4. **Process:**
   - Click "Process"
   - Wait for extraction (30s)
   - Wait for translation (2-5 min)
   - Wait for audio (1-2 min)

5. **Review:**
   - Read translation
   - Listen to audio sample
   - Download files

6. **Done!**
   - You have Creole text
   - You have Creole audiobook
   - Files saved locally

---

## **🌟 Advanced Features**

### **Cache System:**
- Speeds up repeated translations
- Stores in `cache/` folder
- View hit rate in stats
- Clear if needed

### **Parallel Processing:**
- Uses multiple CPU cores
- Faster for large documents
- Configure workers (1-8)
- Recommended for 10+ pages

### **Batch Mode:**
(Not in current tab, but available via CLI)
- Process multiple PDFs
- Automated workflow
- See `batch_processor.py`

---

## **📱 Browser Compatibility**

**Recommended browsers:**
- ✅ Chrome/Edge (Best)
- ✅ Firefox (Good)
- ✅ Safari (Good)
- ⚠️ IE (Not supported)

**Requirements:**
- Modern browser (2020+)
- JavaScript enabled
- Cookies enabled
- 2GB+ RAM

---

## **🔐 Privacy & Security**

- **Processing:** All done locally on your computer
- **No cloud upload:** Files stay on your machine
- **Model:** Downloaded from HuggingFace (trusted)
- **Open source:** All code visible

---

## **💾 File Management**

### **Input:**
- Upload via browser
- Temporarily stored
- Deleted after processing

### **Output:**
- Saved in `output/` folder
- Available for download
- Kept until you delete

### **Cache:**
- Stored in `cache/` folder
- Improves performance
- Can be cleared anytime

---

## **🚀 Performance Tips**

### **For Speed:**
1. Enable cache
2. Use parallel processing
3. Process during first setup (model download)
4. Keep browser open

### **For Quality:**
1. Use high-quality PDFs
2. Specify source language
3. Review translations
4. Edit if needed

### **For Large Files:**
1. Enable parallel processing
2. Increase max workers
3. Process in batches
4. Be patient!

---

## **📞 Getting Help**

If you encounter issues:

1. **Check logs:**
   ```
   C:\Users\Fanerlink\OneDrive\Documents\liv odyo\projet_kreyol_IA\logs\
   ```

2. **Run diagnostics:**
   ```powershell
   python check_setup.py
   python test_core_functionality.py
   ```

3. **Check documentation:**
   - `README.md`
   - `INSTALLATION_COMPLETE.md`
   - `QUICKSTART.md`

4. **Console output:**
   - Check terminal for errors
   - Note any error messages

---

## **🎊 Enjoy Your Translation Tool!**

Your web interface is ready to translate documents to Haitian Creole!

**Current URL:** http://localhost:8501

**Quick commands:**
- Stop server: `Ctrl + C` in terminal
- Restart: `streamlit run app.py`
- Check status: Open browser to http://localhost:8501

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen 🇭🇹**

