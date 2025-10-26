# 🇭🇹 Kreyòl IA - Creative Platform

<div align="center">

![Kreyòl IA](https://img.shields.io/badge/Kreyòl-IA-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Professional AI-powered content creation platform for Haitian Creole**

[Live Demo](https://kreyol-ia-studio.onrender.com) • [Documentation](./DEPLOYMENT_GUIDE.md) • [Report Bug](../../issues)

</div>

---

## ✨ Features

### 🎧 Audio Tools
- **📚 Audiobook Creation** - Transform documents into native Creole audiobooks
  - ✨ **NEW:** Support for large PDFs (10,000+ pages)
  - ✨ **NEW:** Streaming extraction with progress tracking
  - ✨ **NEW:** Memory optimized (-80% usage)
- **🎙️ Podcast Generation** - Create multi-voice podcasts automatically
- **🗣️ Text to Speech** - Convert any text to natural Creole speech
- **🔗 URL to Audio** - Turn web articles into audiobooks (Coming soon)

### 🎬 Video Tools (Coming Soon)
- **🎥 Video Voiceover** - Add professional Creole narration
- **🎵 SFX & Music** - Enhance with Haitian music styles
- **📝 Auto Captions** - Generate Creole subtitles
- **🔇 Noise Removal** - AI-powered audio cleaning

### 🇭🇹 Kreyòl Tools
- **🌍 Translation** - High-quality AI translation (Google Translate)
- **🚀 NLLB Translation** - Advanced Meta NLLB model for superior Creole translation
- **📄 PDF Translator** - Translate entire documents
- **✨ AI Script Generator** - Generate creative Creole content

---

## 🎨 Screenshots

### Studio Dashboard
<div align="center">
<img src="https://via.placeholder.com/800x400/0a0a0a/ffffff?text=Studio+Dashboard" alt="Studio Dashboard" width="800"/>
</div>

### Text to Speech
<div align="center">
<img src="https://via.placeholder.com/800x400/0a0a0a/ffffff?text=Text+to+Speech" alt="Text to Speech" width="800"/>
</div>

---

## 🚀 Quick Start

### ⚡ ONE-CLICK START (Recommended)

**Simply double-click:**
```
START.bat
```

That's it! The platform will:
- ✅ Start in a single terminal
- ✅ Open browser automatically
- ✅ Handle all setup (Redis, Celery, etc.)
- ✅ Choose features based on what's available

**3 Options:**
1. **Rapid** - Instant start (no Docker needed) ⚡
2. **Complete** - Full power (with Redis + Celery) 🚀
3. **App Only** - Manual control 🎯

### Prerequisites

- Python 3.11+
- pip
- **Optional:**
  - Docker Desktop (for full features)
  - Redis (if not using Docker)
- **RAM:** 
  - 2GB minimum (basic usage)
  - 4GB+ recommended for large PDFs (1000+ pages)
  - 8GB+ for optimal performance with streaming extraction

### Manual Installation (Advanced)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/kreyol-ia.git
cd kreyol-ia

# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py
```

Open your browser at `http://localhost:8000` 🎉

### 📚 Large PDF Processing (NEW v3.2!)

Process **large documents** with optimized performance:

```bash
# Quick test with sample PDF
TEST_GWO_PDF.bat

# View capabilities
# ✅ Up to 10,000+ pages
# ✅ Real-time progress tracking  
# ✅ 80% less memory usage
# ✅ Streaming extraction for huge files
```

**Supported Sizes:**
- **Small PDFs** (< 100 pages): 30s - 2min
- **Medium PDFs** (100-500 pages): 2 - 10min  
- **Large PDFs** (500-2000 pages): 10 - 30min (with streaming)
- **Huge PDFs** (2000+ pages): Supported with page limits

**API Usage:**
```python
# Standard endpoint with limits
POST /api/audiobook
{
  "file": document.pdf,
  "max_pages": 500,
  "show_progress": true
}

# Streaming endpoint for very large files
POST /api/audiobook-streaming
{
  "file": huge_document.pdf,
  "chunk_size_pages": 100
}
```

📖 **Full Guide:** [docs/GWO_PDF_GUIDE.md](./docs/GWO_PDF_GUIDE.md)

---

### 🚀 NLLB Translation (NEW!)

For **superior Creole translation quality**, use the NLLB model:

```bash
# Quick test
TEST_NLLB.bat

# Translate a file
TRADUIRE_NLLB.bat your_file.txt

# Or use Python directly
python traduire_nllb.py data/test_document.txt
```

**Why NLLB?**
- 🎯 Specialized for Haitian Creole
- 📚 Better grammar and idioms
- 🔒 Works offline (after first download)
- 🆓 Free, unlimited usage

See [NLLB_GUIDE.md](./NLLB_GUIDE.md) for full documentation.

---

## 🌐 Deploy to Production

### Deploy on Render (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**See detailed guide**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

### One-Click Deploy

1. Fork this repository
2. Sign up on [Render.com](https://render.com)
3. Connect your GitHub
4. Click "New Web Service"
5. Select this repository
6. Deploy! 🚀

---

## 🏗️ Architecture

```
kreyol-ia/
├── api_final.py              # FastAPI backend
├── app_studio_dark.html      # Modern dark theme UI
├── src/
│   ├── translator.py         # M2M100 translation
│   ├── audio_generator.py    # TTS engine
│   └── pdf_extractor.py      # PDF processing
├── requirements.txt          # Python dependencies
└── render.yaml              # Render config
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Transformers** - Hugging Face AI models
- **M2M100** - Multilingual translation
- **MMS-TTS-HAT** - Native Creole voice synthesis

### Frontend
- **Vanilla JavaScript** - No framework overhead
- **Modern CSS** - Beautiful dark theme
- **Responsive Design** - Works on all devices

### AI Models
- **facebook/m2m100_418M** - Translation
- **facebook/nllb-200-distilled-600M** - Advanced Creole translation (NEW!)
- **facebook/mms-tts-hat** - Haitian Creole TTS
- **gTTS** - Fallback voice

---

## 📊 Performance

- ⚡ **Fast Processing** - Optimized for speed
- 💾 **Low Memory** - Runs on 512MB RAM
- 🌍 **Global CDN** - Fast worldwide access
- 🔒 **Secure** - HTTPS by default

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Hugging Face** - For amazing AI models
- **FastAPI** - For the excellent web framework
- **Haitian Creole Community** - For inspiration and support

---

## 📞 Support

- 📧 Email: support@kreyol-ia.com
- 🐛 Issues: [GitHub Issues](../../issues)
- 💬 Discussions: [GitHub Discussions](../../discussions)

---

## 🎯 Roadmap

- [x] ✅ Text to Speech with native Creole voice
- [x] ✅ PDF to Audiobook conversion
- [x] ✅ Multi-voice podcast generation
- [x] ✅ Modern dark theme UI
- [ ] 🚧 Video voiceover tools
- [ ] 🚧 AI script generation
- [ ] 🚧 Mobile app
- [ ] 🚧 API access for developers

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ for the Haitian Creole community** 🇭🇹

[Website](https://kreyol-ia.com) • [Twitter](https://twitter.com/kreyolia) • [Discord](https://discord.gg/kreyolia)

</div>
