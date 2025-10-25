#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit GUI Application
Interface grafik pou Pwojè Kreyòl IA
"""

import streamlit as st
import tempfile
from pathlib import Path
import time

from src import Config, PDFExtractor, CreoleTranslator, AudiobookGenerator, setup_logging
from src.custom_voice_manager import CustomVoiceManager


# Page configuration
st.set_page_config(
    page_title="🇭🇹 Pwojè Kreyòl IA",
    page_icon="🇭🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .big-title {
        font-size: 3em;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2em;
    }
    .success-box {
        padding: 1em;
        border-radius: 0.5em;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1em;
        border-radius: 0.5em;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'text' not in st.session_state:
        st.session_state.text = None
    if 'translation' not in st.session_state:
        st.session_state.translation = None
    if 'audio_path' not in st.session_state:
        st.session_state.audio_path = None


def main():
    """Main Streamlit application"""
    
    init_session_state()
    
    # Header
    st.markdown('<h1 class="big-title">🇭🇹 Pwojè Kreyòl IA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Haitian Creole AI Project - PDF Translation & Audiobook Generation</p>', unsafe_allow_html=True)
    
    # Sidebar - Settings
    with st.sidebar:
        st.header("⚙️ Konfigirasyon / Settings")
        
        # Add tabs for settings and custom voices
        tab1, tab2 = st.tabs(["⚙️ Settings", "🎙️ Custom Voices"])
        
        with tab1:
                st.subheader("📝 Lang / Languages")
            source_lang = st.selectbox(
                "Lang sous / Source language",
                options=[("Auto-detect", None), ("French", "fr"), ("English", "en"), 
                        ("Spanish", "es"), ("Portuguese", "pt")],
                format_func=lambda x: x[0],
                index=0
            )[1]
            
            target_lang = st.selectbox(
                "Lang sib / Target language",
                options=[("Haitian Creole", "ht"), ("French", "fr"), ("English", "en")],
                format_func=lambda x: x[0],
                index=0
            )[1]
            
            st.subheader("⚡ Pèfòmans / Performance")
            enable_cache = st.checkbox("💾 Aktive cache / Enable cache", value=True)
            enable_parallel = st.checkbox("⚡ Tradiksyon paralèl / Parallel translation", value=False)
            
            if enable_parallel:
                max_workers = st.slider("Workers", 1, 8, 3)
            else:
                max_workers = 3
            
            st.subheader("🎚️ Opsyon / Options")
            chunk_size = st.slider("Gwosè chunk / Chunk size", 500, 2000, 1000, 100)
            generate_audio = st.checkbox("🔊 Kreye liv odyo / Generate audiobook", value=True)
            
            st.markdown("---")
            st.markdown("**Version:** 3.0")
            st.markdown("**Phase:** 3 - Features")
        
        with tab2:
            st.subheader("🎙️ Vwa Natirèl / Natural Voices")
            st.markdown("Ajoute vwa natirèl an kreyòl / Add natural Creole voices")
            
            # Initialize voice manager
            voice_manager = CustomVoiceManager()
            voices = voice_manager.list_voices(language='ht')
            
            st.markdown(f"**Total vwa / Total voices:** {len(voices)}")
            
            if len(voices) > 0:
                st.markdown("---")
                st.markdown("**Vwa disponib / Available voices:**")
                
                for voice in voices:
                    with st.expander(f"🎤 {voice['voice_name']} - {voice['speaker_name']}"):
                        st.write(f"**ID:** {voice['voice_id']}")
                        st.write(f"**Sèks / Gender:** {voice['gender']}")
                        st.write(f"**Rejyon / Region:** {voice['region']}")
                        st.write(f"**Rating:** {'⭐' * int(voice['rating'])} ({voice['rating']:.1f})")
                        st.write(f"**Itilize / Used:** {voice['times_used']} fwa")
                        st.write(f"**Tèks / Text:**")
                        st.text(voice['text_content'][:200] + "..." if len(voice['text_content']) > 200 else voice['text_content'])
                        
                        # Play audio
                        voice_path = voice_manager.get_voice_path(voice['voice_id'])
                        if voice_path and voice_path.exists():
                            st.audio(str(voice_path))
            else:
                st.info("Pa gen vwa ankò. Itilize `add_custom_voice.py` pou ajoute vwa.\n\nNo voices yet. Use `add_custom_voice.py` to add voices.")
            
            st.markdown("---")
            st.markdown("**Kijan pou ajoute vwa / How to add voices:**")
            st.code("python add_custom_voice.py", language="bash")
            st.markdown("Oswa itilize / Or use:")
            st.code("python -m streamlit run add_custom_voice.py", language="bash")
    
    # Main area
    tab1, tab2, tab3 = st.tabs(["📄 Upload & Process", "📊 Results", "ℹ️ About"])
    
    with tab1:
        st.header("📄 Upload PDF")
        
        uploaded_file = st.file_uploader(
            "Chwazi yon fichye PDF / Choose a PDF file",
            type=['pdf'],
            help="Upload a PDF file to translate and convert to audiobook"
        )
        
        if uploaded_file:
            st.success(f"✅ Fichye chwazi / File selected: {uploaded_file.name}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                process_btn = st.button(
                    "🚀 Trete / Process",
                    use_container_width=True,
                    type="primary"
                )
            
            if process_btn:
                # Create temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = Path(tmp_file.name)
                
                try:
                    # Create configuration
                    config = Config(
                        source_language=source_lang,
                        target_language=target_lang,
                        chunk_size=chunk_size,
                        enable_cache=enable_cache,
                        enable_parallel=enable_parallel,
                        max_workers=max_workers
                    )
                    
                    # Initialize modules
                    extractor = PDFExtractor(config)
                    translator = CreoleTranslator(config)
                    generator = AudiobookGenerator(config)
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Extract
                    status_text.text("⏳ ETAP 1/3: Ekstraksyon tèks / Extracting text...")
                    progress_bar.progress(10)
                    
                    text = extractor.extract(tmp_path, show_progress=False)
                    st.session_state.text = text
                    
                    progress_bar.progress(33)
                    st.success(f"✅ Ekstraksyon konplete / Extraction complete: {len(text)} karaktè")
                    
                    # Step 2: Translate
                    status_text.text("⏳ ETAP 2/3: Tradiksyon / Translation...")
                    progress_bar.progress(40)
                    
                    translation = translator.translate(text, src_lang=source_lang, show_progress=False)
                    st.session_state.translation = translation
                    
                    progress_bar.progress(66)
                    
                    # Show cache stats
                    if enable_cache and translator.cache:
                        stats = translator.cache.get_stats()
                        st.info(f"💾 Cache: {stats['hits']} hits, {stats['misses']} misses ({stats['hit_rate']:.1f}%)")
                    
                    st.success(f"✅ Tradiksyon konplete / Translation complete: {len(translation)} karaktè")
                    
                    # Step 3: Audio (optional)
                    if generate_audio:
                        status_text.text("⏳ ETAP 3/3: Kreyasyon odyo / Generating audio...")
                        progress_bar.progress(70)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as audio_tmp:
                            audio_path = generator.generate(translation, output_path=Path(audio_tmp.name))
                            st.session_state.audio_path = audio_path
                        
                        progress_bar.progress(100)
                        st.success("✅ Liv odyo kreye / Audiobook generated!")
                    else:
                        progress_bar.progress(100)
                    
                    status_text.text("✅ Tout etap yo konplete / All steps complete!")
                    st.session_state.processed = True
                    
                    # Clean up temp PDF
                    tmp_path.unlink()
                    
                    st.balloons()
                    
                    # Navigate to results
                    st.info("👉 Ale nan tab 'Results' pou wè rezilta yo / Go to 'Results' tab to see results")
                    
                except Exception as e:
                    st.error(f"❌ ERÈR / ERROR: {str(e)}")
                    import traceback
                    with st.expander("📋 Detay erè / Error details"):
                        st.code(traceback.format_exc())
    
    with tab2:
        st.header("📊 Rezilta / Results")
        
        if not st.session_state.processed:
            st.info("👈 Tanpri upload epi trete yon PDF dabò / Please upload and process a PDF first")
        else:
            # Text preview
            st.subheader("📄 Tèks Orijinal / Original Text")
            with st.expander("Klike pou wè / Click to view", expanded=False):
                st.text_area(
                    "Extracted Text",
                    st.session_state.text[:1000] + "..." if len(st.session_state.text) > 1000 else st.session_state.text,
                    height=200,
                    label_visibility="collapsed"
                )
                st.download_button(
                    "📥 Telechaje tèks / Download text",
                    st.session_state.text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )
            
            # Translation
            st.subheader("🌍 Tradiksyon Kreyòl / Creole Translation")
            with st.expander("Klike pou wè / Click to view", expanded=True):
                st.text_area(
                    "Translation",
                    st.session_state.translation[:1000] + "..." if len(st.session_state.translation) > 1000 else st.session_state.translation,
                    height=300,
                    label_visibility="collapsed"
                )
                st.download_button(
                    "📥 Telechaje tradiksyon / Download translation",
                    st.session_state.translation,
                    file_name="traduction_creole.txt",
                    mime="text/plain"
                )
            
            # Audio
            if st.session_state.audio_path:
                st.subheader("🔊 Liv Odyo / Audiobook")
                
                # Read audio file
                with open(st.session_state.audio_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                
                st.audio(audio_bytes, format='audio/mp3')
                
                st.download_button(
                    "📥 Telechaje odyo / Download audiobook",
                    audio_bytes,
                    file_name="audiobook_creole.mp3",
                    mime="audio/mp3"
                )
            
            # Statistics
            st.subheader("📈 Estatistik / Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Karaktè orijinal / Original chars", f"{len(st.session_state.text):,}")
            
            with col2:
                st.metric("Karaktè tradui / Translated chars", f"{len(st.session_state.translation):,}")
            
            with col3:
                if st.session_state.audio_path:
                    audio_size = Path(st.session_state.audio_path).stat().st_size / (1024 * 1024)
                    st.metric("Gwosè odyo / Audio size", f"{audio_size:.1f} MB")
    
    with tab3:
        st.header("ℹ️ Sou Pwojè sa a / About This Project")
        
        st.markdown("""
        ### 🎯 Objektif / Objective
        
        **Kreyòl:** Pwojè sa a pèmèt ou tradui dokiman PDF nan Kreyòl Ayisyen epi kreye liv odyo otomatikman.
        
        **English:** This project allows you to translate PDF documents to Haitian Creole and automatically create audiobooks.
        
        ### ✨ Karakteristik / Features
        
        - 📄 **Ekstraksyon PDF** - Ekstrè tèks nan PDF
        - 🧠 **Tradiksyon AI** - Itilize modèl M2M100 Facebook
        - 🌍 **100+ lang** - Sipòte plis pase 100 lang
        - 🔊 **Liv Odyo** - Kreye MP3 otomatikman
        - 💾 **Cache** - Sistèm cache entèlijan
        - ⚡ **Paralèl** - Tradiksyon rapid
        
        ### 🚀 Version
        
        - **Version:** 3.0
        - **Phase:** 3 - Features
        - **Date:** 12 octobre 2025
        
        ### 📚 Documentation
        
        Li dokimantasyon konplè nan fichye README.md
        
        ### ❤️ Open Source
        
        Fèt ak ❤️ pou kominote Kreyòl Ayisyen 🇭🇹
        """)


if __name__ == "__main__":
    main()

