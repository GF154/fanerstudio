#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit Web App - Entèfas web pou pwojè Kreyòl IA
Web interface for Haitian Creole AI Project
"""

import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime
from utils.cloud_storage import upload_to_gcs, download_from_gcs
from utils.text_extraction import extract_text_from_pdf
from utils.translate import translate_text
from utils.audio_gen import generate_audio
from utils.podcast_mix import mix_voices


# Page configuration
st.set_page_config(
    page_title="Pwojè Kreyòl IA",
    page_icon="🇭🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #002D62 0%, #D21034 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def check_bucket_config():
    """Check if bucket is configured"""
    bucket = os.getenv("GCS_BUCKET_NAME")
    if not bucket:
        st.error("❌ GCS_BUCKET_NAME pa defini / not configured")
        st.info("Defini l nan fichye .env / Set it in .env file")
        st.stop()
    return bucket


def save_uploaded_file(uploaded_file, directory="input"):
    """Save uploaded file"""
    Path(directory).mkdir(exist_ok=True)
    file_path = Path(directory) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def main():
    """Main app function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🇭🇹 Pwojè Kreyòl IA</h1>
        <h3>Haitian Creole AI Project</h3>
        <p>Tradui ak kreye liv odyo an kreyòl / Translate and create Creole audiobooks</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Konfigirasyon / Settings")
    
    # Check bucket
    bucket = check_bucket_config()
    st.sidebar.success(f"✅ Bucket: {bucket}")
    
    # Mode selection
    mode = st.sidebar.radio(
        "Mòd / Mode:",
        ["📤 Upload & Process", "📚 Batch Processing", "📊 View Results"]
    )
    
    # Main content
    if mode == "📤 Upload & Process":
        show_upload_mode(bucket)
    elif mode == "📚 Batch Processing":
        show_batch_mode(bucket)
    else:
        show_results_mode()


def show_upload_mode(bucket):
    """Upload and process single book"""
    st.header("📤 Upload ak Trete / Upload & Process")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File uploader
        uploaded_file = st.file_uploader(
            "📄 Chwazi yon PDF / Choose a PDF",
            type=['pdf'],
            help="Upload yon fichye PDF pou tradui / Upload a PDF file to translate"
        )
        
        if uploaded_file:
            st.success(f"✅ Fichye chwazi / File selected: {uploaded_file.name}")
            
            # Book metadata
            st.subheader("📝 Enfòmasyon liv / Book information")
            
            book_name = st.text_input(
                "Non liv / Book name:",
                value=Path(uploaded_file.name).stem
            )
            
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                author = st.text_input("Otè / Author:", "Unknown")
                title = st.text_input("Tit / Title:", book_name)
            
            with col_meta2:
                language = st.selectbox("Lang orijinal / Source language:", ["fr", "en", "es"])
                year = st.number_input("Ane / Year:", min_value=1900, max_value=2100, value=2024)
            
            # Process button
            if st.button("🚀 Kòmanse Pwosesis / Start Processing", type="primary"):
                process_single_book(
                    uploaded_file, book_name, bucket,
                    metadata={'author': author, 'title': title, 'language': language, 'year': year}
                )
    
    with col2:
        st.info("""
        **Etap yo / Steps:**
        
        1. 📥 Upload PDF
        2. 📄 Ekstrè tèks
        3. 🌍 Tradui an kreyòl
        4. 🎧 Kreye audiobook
        5. 🎙️ Kreye podcast
        6. ☁️ Upload nan cloud
        """)


def process_single_book(uploaded_file, book_name, bucket, metadata):
    """Process a single book"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Save uploaded file
        status_text.text("📥 Sov fichye / Saving file...")
        progress_bar.progress(10)
        
        file_path = save_uploaded_file(uploaded_file)
        
        # Upload to GCS
        status_text.text("☁️ Upload nan cloud / Uploading to cloud...")
        progress_bar.progress(20)
        
        remote_pdf = f"input/{book_name}.pdf"
        upload_to_gcs(str(file_path), remote_pdf, bucket, make_public=False)
        
        # Extract text
        status_text.text("📄 Ekstrè tèks / Extracting text...")
        progress_bar.progress(30)
        
        text = extract_text_from_pdf(str(file_path))
        st.info(f"✅ {len(text)} karaktè ekstré / characters extracted")
        
        # Translate
        status_text.text("🌍 Tradiksyon / Translating...")
        progress_bar.progress(50)
        
        translated = translate_text(text, "ht")
        
        # Save translation
        output_dir = Path(f"output/{book_name}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        txt_path = output_dir / f"{book_name}_kreyol.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(translated)
        
        # Upload translation
        status_text.text("☁️ Upload tradiksyon / Uploading translation...")
        progress_bar.progress(60)
        
        remote_txt = f"output/{book_name}/{book_name}_kreyol.txt"
        url_txt = upload_to_gcs(str(txt_path), remote_txt, bucket)
        
        # Generate audio
        status_text.text("🎧 Kreye audiobook / Creating audiobook...")
        progress_bar.progress(75)
        
        audio_path = output_dir / f"{book_name}_audio.mp3"
        generate_audio(translated, str(audio_path), language="ht")
        
        # Upload audio
        status_text.text("☁️ Upload audiobook / Uploading audiobook...")
        progress_bar.progress(85)
        
        remote_audio = f"output/{book_name}/{book_name}_audio.mp3"
        url_audio = upload_to_gcs(str(audio_path), remote_audio, bucket)
        
        # Create podcast
        status_text.text("🎙️ Kreye podcast / Creating podcast...")
        progress_bar.progress(90)
        
        podcast_path = output_dir / f"{book_name}_podcast.mp3"
        mix_voices([str(audio_path)], str(podcast_path))
        
        # Upload podcast
        status_text.text("☁️ Upload podcast / Uploading podcast...")
        progress_bar.progress(95)
        
        remote_podcast = f"output/{book_name}/{book_name}_podcast.mp3"
        url_podcast = upload_to_gcs(str(podcast_path), remote_podcast, bucket)
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Konple! / Complete!")
        
        # Show results
        st.success("🎉 Pwosesis fini avèk siksè! / Processing completed successfully!")
        
        st.markdown("### 🔗 Lyen Piblik / Public Links")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **📘 Tèks Tradui / Translated Text**
            
            [{url_txt}]({url_txt})
            """)
        
        with col2:
            st.markdown(f"""
            **🔊 Audiobook**
            
            [{url_audio}]({url_audio})
            """)
        
        with col3:
            st.markdown(f"""
            **🎙️ Podcast**
            
            [{url_podcast}]({url_podcast})
            """)
        
        # Save result
        result = {
            'book_name': book_name,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata,
            'urls': {
                'text': url_txt,
                'audio': url_audio,
                'podcast': url_podcast
            }
        }
        
        results_dir = Path("output/web_results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        result_file = results_dir / f"{book_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
    except Exception as e:
        st.error(f"❌ Erè / Error: {e}")
        progress_bar.progress(0)


def show_batch_mode(bucket):
    """Batch processing mode"""
    st.header("📚 Batch Processing")
    
    st.info("""
    **Batch mode pèmèt ou trete plizyè liv an menm tan**
    
    Batch mode allows you to process multiple books at once
    """)
    
    # Upload multiple files
    uploaded_files = st.file_uploader(
        "📄 Chwazi plizyè PDF / Choose multiple PDFs",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} fichye chwazi / files selected")
        
        # Show files
        st.subheader("📋 Fichye yo / Files:")
        for i, file in enumerate(uploaded_files, 1):
            st.write(f"{i}. {file.name}")
        
        if st.button("🚀 Kòmanse Batch / Start Batch", type="primary"):
            st.warning("⚠️ Fonksyonalite sa a ap vini / This feature is coming soon")
            st.info("Itilize run_batch.py pou batch processing / Use run_batch.py for batch processing")


def show_results_mode():
    """View previous results"""
    st.header("📊 Rezilta Anvan / Previous Results")
    
    results_dir = Path("output/web_results")
    
    if not results_dir.exists() or not list(results_dir.glob("*.json")):
        st.info("📭 Pa gen rezilta ankò / No results yet")
        return
    
    # Load all results
    results = []
    for result_file in sorted(results_dir.glob("*.json"), reverse=True):
        with open(result_file, 'r', encoding='utf-8') as f:
            results.append(json.load(f))
    
    st.success(f"✅ {len(results)} rezilta jwenn / results found")
    
    # Display results
    for result in results:
        with st.expander(f"📚 {result['book_name']} - {result['timestamp'][:10]}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Metadata:**")
                metadata = result.get('metadata', {})
                st.write(f"- Otè / Author: {metadata.get('author', 'N/A')}")
                st.write(f"- Tit / Title: {metadata.get('title', 'N/A')}")
                st.write(f"- Lang / Language: {metadata.get('language', 'N/A')}")
            
            with col2:
                st.write("**Lyen / Links:**")
                urls = result.get('urls', {})
                if urls.get('text'):
                    st.markdown(f"[📘 Text]({urls['text']})")
                if urls.get('audio'):
                    st.markdown(f"[🔊 Audio]({urls['audio']})")
                if urls.get('podcast'):
                    st.markdown(f"[🎙️ Podcast]({urls['podcast']})")


if __name__ == "__main__":
    main()

