#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Media Service
Sèvis pou pwosese medya (audiobook, podcast, PDF, videyo, elatriye)
"""

from pathlib import Path
from datetime import datetime
import uuid
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class MediaService:
    """Sèvis pou pwosese medya"""
    
    def __init__(self):
        """Inisyalize sèvis medya"""
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        print("✅ Media Service initialized")
    
    # ============================================================
    # AUDIOBOOK & PODCAST CREATION
    # ============================================================
    
    async def create_audiobook(self, file_path: Path, voice: str = "creole-native") -> dict:
        """
        Kreye liv odyo konplè soti nan yon dokiman
        
        Args:
            file_path: Chemen fichye dokiman an
            voice: Vwa pou itilize
            
        Returns:
            dict: Enfòmasyon sou fichye yo kreye
        """
        try:
            # Import TTS service
            from app.services.tts_service import text_to_speech_file
            
            # 1. Extract text from document
            print(f"📄 Ekstrè tèks soti nan {file_path.name}...")
            text = await self.extract_text_from_document(str(file_path))
            
            if not text or len(text.strip()) < 10:
                raise ValueError("Dokiman an vid oswa pa gen ase tèks!")
            
            # 2. Generate audio filename
            audio_filename = f"audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            audio_path = self.output_dir / audio_filename
            
            # 3. Convert text to speech
            print(f"🎧 Kreye odyo ak vwa: {voice}...")
            await text_to_speech_file(text, str(audio_path), voice)
            
            # 4. Save text preview
            preview_filename = f"audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}_text.txt"
            preview_path = self.output_dir / preview_filename
            preview_path.write_text(text[:1000] + "..." if len(text) > 1000 else text, encoding='utf-8')
            
            print(f"✅ Audiobook kreye avèk siksè!")
            
            return {
                "audio": f"/output/{audio_filename}",
                "preview": f"/output/{preview_filename}",
                "text_length": len(text),
                "word_count": len(text.split()),
                "voice": voice
            }
            
        except Exception as e:
            print(f"❌ Error creating audiobook: {e}")
            raise
    
    async def create_podcast(self, title: str, content: str, num_speakers: int = 2) -> Path:
        """
        Kreye podcast soti nan kontni
        
        Args:
            title: Tit podcast la
            content: Kontni pou diskite
            num_speakers: Kantite moun kap pale
            
        Returns:
            Path: Chemen fichye podcast la
        """
        try:
            # Import TTS service
            from app.services.tts_service import text_to_speech_file
            
            print(f"🎙️ Kreye podcast: {title}...")
            
            # 1. Generate intro
            intro_text = f"Byenvini nan {title}. "
            
            # 2. Prepare content for podcast format
            if num_speakers > 1:
                # Split content into segments for different speakers
                segments = self._split_for_speakers(content, num_speakers)
            else:
                segments = [{"speaker": 1, "text": content}]
            
            # 3. Generate audio for each segment
            temp_files = []
            voices = ["creole-native", "gtts"]  # Alternate voices for speakers
            
            # Intro
            intro_file = self.output_dir / f"podcast_intro_{uuid.uuid4().hex[:8]}.mp3"
            await text_to_speech_file(intro_text, str(intro_file), "creole-native")
            temp_files.append(intro_file)
            
            # Content segments
            for i, segment in enumerate(segments):
                voice = voices[segment["speaker"] % len(voices)]
                segment_file = self.output_dir / f"podcast_segment_{i}_{uuid.uuid4().hex[:8]}.mp3"
                await text_to_speech_file(segment["text"], str(segment_file), voice)
                temp_files.append(segment_file)
            
            # 4. Combine audio files (simple concatenation)
            output_filename = f"podcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            output_path = self.output_dir / output_filename
            
            # For now, just use the first file (full implementation would use pydub/ffmpeg)
            # TODO: Implement proper audio concatenation
            import shutil
            shutil.copy(temp_files[0], output_path)
            
            # Cleanup temp files
            for temp_file in temp_files:
                try:
                    temp_file.unlink()
                except:
                    pass
            
            print(f"✅ Podcast kreye: {output_filename}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating podcast: {e}")
            raise
    
    async def _extract_pdf_optimized(
        self,
        pdf_path: Path,
        max_pages: int = None,
        show_progress: bool = True,
        chunk_size: int = 50
    ) -> str:
        """
        Ekstrè tèks soti nan PDF ak optimize pou gwo fichye
        
        Args:
            pdf_path: Chemen fichye PDF la
            max_pages: Limit maksimòm paj (None = tout)
            show_progress: Afiche pwogresyon
            chunk_size: Kantite paj pou pwosese an menm tan
            
        Returns:
            str: Tèks ki ekstrè
        """
        try:
            import pypdf
            from tqdm import tqdm
            
            reader = pypdf.PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            # Calculate file size in MB
            file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
            
            # Warning pou gwo fichye
            if total_pages > 1000:
                print(f"\n⚠️  GWO PDF DETEKTE!")
                print(f"   📄 Paj: {total_pages:,}")
                print(f"   💾 Gwosè: {file_size_mb:.2f} MB")
                print(f"   ⏱️  Tan estimé: {total_pages//50}-{total_pages//30} minit")
            
            # Determine pages to process
            if max_pages and max_pages < total_pages:
                pages_to_process = max_pages
                print(f"\n📊 Ap limite ekstraksyon: {pages_to_process}/{total_pages} paj")
            else:
                pages_to_process = total_pages
            
            # Streaming extraction with chunks
            all_text = []
            
            if show_progress and total_pages > 20:
                # Use progress bar for large files
                pbar = tqdm(
                    total=pages_to_process,
                    desc="📄 Ekstrè PDF",
                    unit="paj",
                    ncols=80
                )
            else:
                pbar = None
            
            # Process in chunks
            for start in range(0, pages_to_process, chunk_size):
                end = min(start + chunk_size, pages_to_process)
                
                # Extract chunk
                chunk_text = []
                for i in range(start, end):
                    try:
                        page_text = reader.pages[i].extract_text() or ""
                        chunk_text.append(page_text)
                    except Exception as e:
                        print(f"\n⚠️  Erè paj {i+1}: {str(e)[:50]}")
                        chunk_text.append(f"[Erè paj {i+1}]")
                    
                    if pbar:
                        pbar.update(1)
                
                # Join chunk and add to all text
                all_text.append("\n".join(chunk_text))
                
                # Progress message for manual tracking
                if not pbar and show_progress and end % 100 == 0:
                    print(f"   ✓ {end}/{pages_to_process} paj ekstrè...")
            
            if pbar:
                pbar.close()
            
            # Final text
            text = "\n".join(all_text)
            
            # Add note if limited
            if max_pages and max_pages < total_pages:
                text += f"\n\n📝 NOTE: Sèlman {pages_to_process}/{total_pages} paj ekstrè (pou optimize pèfòmans)"
            
            # Stats
            word_count = len(text.split())
            char_count = len(text)
            
            print(f"\n✅ Ekstraksyon konple!")
            print(f"   📄 Paj pwosese: {pages_to_process}/{total_pages}")
            print(f"   📝 Mo: {word_count:,}")
            print(f"   🔤 Karaktè: {char_count:,}")
            
            return text.strip()
            
        except ImportError:
            # Fallback to PyPDF2 (basic version)
            print("⚠️  pypdf pa disponib, itilize PyPDF2 (pi slow)...")
            import PyPDF2
            
            text_parts = []
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                total = len(reader.pages)
                pages_to_process = min(max_pages or total, total)
                
                for i, page in enumerate(reader.pages[:pages_to_process]):
                    text_parts.append(page.extract_text() or "")
                    if show_progress and i % 50 == 0:
                        print(f"   {i}/{pages_to_process} paj...")
                        
            return "\n".join(text_parts)
            
        except Exception as e:
            print(f"❌ Erè nan ekstraksyon PDF: {e}")
            raise
    
    async def extract_text_from_pdf_streaming(
        self,
        pdf_path: Path,
        chunk_size_pages: int = 100,
        callback = None
    ) -> str:
        """
        Ekstrè PDF an moso (streaming) pou gwo fichye
        Pèmèt pwosesis asenkwon ak callback pou progress
        
        Args:
            pdf_path: Chemen fichye PDF la
            chunk_size_pages: Kantite paj pa chunk
            callback: Fonksyon async pou rele apre chak chunk
                      callback(current_page, total_pages, chunk_text)
            
        Returns:
            str: Tèks konplè
        """
        try:
            import pypdf
            
            reader = pypdf.PdfReader(pdf_path)
            total_pages = len(reader.pages)
            
            print(f"\n🔄 STREAMING PDF EXTRACTION")
            print(f"   📄 Total paj: {total_pages}")
            print(f"   📦 Chunk size: {chunk_size_pages} paj")
            print(f"   💾 Memwa optimize: WI")
            
            all_text = []
            
            for start in range(0, total_pages, chunk_size_pages):
                end = min(start + chunk_size_pages, total_pages)
                
                # Process chunk
                chunk_text = []
                for i in range(start, end):
                    try:
                        page_text = reader.pages[i].extract_text() or ""
                        chunk_text.append(page_text)
                    except Exception as e:
                        print(f"⚠️  Skip paj {i+1}: {str(e)[:40]}")
                        chunk_text.append("")
                
                chunk_result = "\n".join(chunk_text)
                all_text.append(chunk_result)
                
                # Call callback if provided
                if callback:
                    await callback(end, total_pages, chunk_result)
                
                # Progress
                print(f"   ✓ Chunk {start+1}-{end}/{total_pages} done")
            
            final_text = "\n".join(all_text)
            
            print(f"\n✅ Streaming extraction complete!")
            print(f"   📝 Total karaktè: {len(final_text):,}")
            
            return final_text
            
        except Exception as e:
            print(f"❌ Erè streaming: {e}")
            raise
    
    def _split_for_speakers(self, text: str, num_speakers: int) -> list:
        """Split text into segments for multiple speakers"""
        sentences = text.split('. ')
        segment_size = max(1, len(sentences) // num_speakers)
        
        segments = []
        for i in range(0, len(sentences), segment_size):
            segment_sentences = sentences[i:i+segment_size]
            segments.append({
                "speaker": i // segment_size,
                "text": '. '.join(segment_sentences) + '.'
            })
        
        return segments
    
    # ============================================================
    # DOCUMENT PROCESSING
    # ============================================================
    
    async def extract_text_from_document(
        self, 
        file_path: str, 
        max_pages: int = None,
        show_progress: bool = True
    ) -> str:
        """
        Ekstrè tèks soti nan yon dokiman (ak sipò pou gwo fichye)
        Sipòte: PDF, TXT, DOCX, EPUB
        
        Args:
            file_path: Chemen fichye dokiman an
            max_pages: Limit maksimòm paj pou ekstrè (None = tout paj yo)
            show_progress: Afiche pwogresyon pou gwo fichye
            
        Returns:
            str: Tèks ki ekstrè
        """
        try:
            file_path_obj = Path(file_path)
            ext = file_path_obj.suffix.lower()
            
            if ext == '.txt':
                # Simple text file
                text = file_path_obj.read_text(encoding='utf-8', errors='ignore')
                
            elif ext == '.pdf':
                # PDF with optimized processing for large files
                text = await self._extract_pdf_optimized(
                    file_path_obj, 
                    max_pages=max_pages,
                    show_progress=show_progress
                )
                    
            elif ext == '.docx':
                # Word document
                try:
                    from docx import Document as DocxDocument
                    doc = DocxDocument(file_path_obj)
                    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
                except ImportError:
                    raise ImportError("python-docx pa enstale! Run: pip install python-docx")
                    
            elif ext == '.epub':
                # EPUB ebook
                try:
                    import ebooklib
                    from ebooklib import epub
                    from bs4 import BeautifulSoup
                    
                    book = epub.read_epub(file_path_obj)
                    text_parts = []
                    
                    for item in book.get_items():
                        if item.get_type() == ebooklib.ITEM_DOCUMENT:
                            soup = BeautifulSoup(item.get_content(), 'html.parser')
                            text_parts.append(soup.get_text())
                    
                    text = "\n".join(text_parts)
                except ImportError:
                    raise ImportError("ebooklib pa enstale! Run: pip install ebooklib")
                    
            else:
                raise ValueError(f"Format pa sipòte: {ext}. Sipòte: .txt, .pdf, .docx, .epub")
            
            return text.strip()
            
        except Exception as e:
            print(f"❌ Error extracting text from {file_path}: {e}")
            raise
    
    async def html_to_text(self, url: str) -> str:
        """
        Konvèti paj HTML an tèks
        Retire script, style, header, footer, nav, aside
        
        Args:
            url: URL paj wèb la
            
        Returns:
            str: Tèks ki ekstrè
        """
        try:
            import httpx
            from bs4 import BeautifulSoup
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "header", "footer", "nav", "aside"]):
                element.decompose()
            
            # Get text with line breaks
            text = soup.get_text(separator="\n")
            
            # Clean up: remove empty lines and strip whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = "\n".join(lines)
            
            print(f"✅ Extracted {len(text)} characters from {url}")
            return text
            
        except Exception as e:
            print(f"❌ Error converting HTML to text from {url}: {e}")
            raise
    
    # ============================================================
    # AUDIOBOOK & PODCAST
    # ============================================================
    
    async def create_audiobook(self, file_path: Path, voice: str = "creole-native") -> dict:
        """
        Kreye liv odyo soti nan yon dokiman
        
        Args:
            file_path: Chemen fichye dokiman an
            voice: Vwa pou itilize
            
        Returns:
            dict: Enfòmasyon sou fichye yo kreye
        """
        try:
            from traduire_texte import traduire_avec_progress
            from generer_audio_huggingface import generer_audio_creole
            import pypdf
            
            # Extract text
            if file_path.suffix == '.pdf':
                reader = pypdf.PdfReader(file_path)
                text = "\n".join(page.extract_text() for page in reader.pages)
            elif file_path.suffix == '.txt':
                text = file_path.read_text(encoding='utf-8')
            else:
                raise ValueError(f"Format pa sipòte: {file_path.suffix}")
            
            # Translate to Creole
            texte_traduit = traduire_avec_progress(text, langue_cible='ht')
            
            # Create output directory
            nom_base = file_path.stem
            output_base = self.output_dir / f"audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            output_base.mkdir(parents=True, exist_ok=True)
            
            # Save translation
            texte_path = output_base / f"{nom_base}_kreyol.txt"
            texte_path.write_text(texte_traduit, encoding='utf-8')
            
            # Generate audio
            audio_path = output_base / f"{nom_base}_audio.mp3"
            generer_audio_creole(texte_traduit, audio_path)
            
            return {
                "translation": f"/output/{output_base.name}/{texte_path.name}",
                "audio": f"/output/{output_base.name}/{audio_path.name}",
                "text_length": len(texte_traduit)
            }
            
        except Exception as e:
            print(f"❌ Error creating audiobook: {e}")
            raise
    
    async def create_podcast(self, title: str, content: str, num_speakers: int = 2) -> Path:
        """
        Kreye podcast
        
        Args:
            title: Tit podcast la
            content: Kontni pou diskite
            num_speakers: Kantite moun kap pale
            
        Returns:
            Path: Chemen fichye podcast la
        """
        try:
            from podcast_creator import PodcastCreator
            
            # Create podcast
            podcast_creator = PodcastCreator()
            
            # Generate unique filename
            filename = f"podcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.mp3"
            output_path = self.output_dir / filename
            
            # For now, use simple TTS
            # TODO: Implement multi-speaker podcast generation
            from generer_audio_huggingface import generer_audio_creole
            podcast_script = f"{title}. {content}"
            generer_audio_creole(podcast_script, output_path)
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating podcast: {e}")
            raise
    
    # ============================================================
    # PDF TRANSLATION
    # ============================================================
    
    async def translate_pdf(self, pdf_path: Path, target_lang: str = "ht") -> dict:
        """
        Tradwi dokiman PDF
        
        Args:
            pdf_path: Chemen fichye PDF la
            target_lang: Lang sib
            
        Returns:
            dict: Enfòmasyon sou fichye yo kreye
        """
        try:
            from traduire_texte import traduire_avec_progress
            import pypdf
            
            # Extract text from PDF
            reader = pypdf.PdfReader(pdf_path)
            text = "\n".join(page.extract_text() for page in reader.pages)
            
            # Translate
            texte_traduit = traduire_avec_progress(text, langue_cible=target_lang)
            
            # Create output directory
            nom_base = pdf_path.stem
            output_base = self.output_dir / f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            output_base.mkdir(parents=True, exist_ok=True)
            
            # Save translation
            texte_path = output_base / f"{nom_base}_traduit.txt"
            texte_path.write_text(texte_traduit, encoding='utf-8')
            
            return {
                "original": pdf_path.name,
                "translation": f"/output/{output_base.name}/{texte_path.name}",
                "text_length": len(texte_traduit)
            }
            
        except Exception as e:
            print(f"❌ Error translating PDF: {e}")
            raise
    
    # ============================================================
    # VIDEO PROCESSING
    # ============================================================
    
    async def add_voiceover_to_video(self, video_file: str, output_video: str, voice: str = "creole-native") -> Path:
        """
        Ajoute vwadeyò nan videyo
        1. Transkri son aktyèl (optional)
        2. Jenere nouvo audio (TTS)
        3. Melanje ak videyo ak ffmpeg
        
        Args:
            video_file: Chemen fichye videyo orijinal
            output_video: Chemen pou sove videyo ak vwadeyò
            voice: Vwa pou itilize
            
        Returns:
            Path: Chemen videyo ak vwadeyò
        """
        try:
            import shutil
            
            output_path = Path(output_video)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # TODO: Implement full voiceover pipeline
            # For now, copy video as placeholder
            shutil.copy(video_file, output_video)
            
            print(f"⚠️ Video voiceover: Placeholder copy created")
            print(f"   TODO: 1) Extract/transcribe audio")
            print(f"   TODO: 2) Generate TTS with voice: {voice}")
            print(f"   TODO: 3) Mix audio with ffmpeg")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error adding voiceover: {e}")
            raise
    
    async def add_sfx_to_video(self, video_file: str, output_video: str, sfx_files: list = None) -> Path:
        """
        Ajoute efè son ak mizik nan videyo
        Mix audio tracks ak ffmpeg
        
        Args:
            video_file: Chemen fichye videyo orijinal
            output_video: Chemen pou sove videyo ak efè
            sfx_files: Lis fichye efè son (optional)
            
        Returns:
            Path: Chemen videyo ak efè son
        """
        try:
            import shutil
            
            output_path = Path(output_video)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # TODO: Implement SFX mixing with ffmpeg
            # For now, copy video as placeholder
            shutil.copy(video_file, output_video)
            
            print(f"⚠️ SFX addition: Placeholder copy created")
            print(f"   TODO: 1) Load video and audio tracks")
            print(f"   TODO: 2) Add SFX at timestamps: {sfx_files or 'None'}")
            print(f"   TODO: 3) Mix audio with ffmpeg")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error adding SFX: {e}")
            raise
    
    async def generate_captions_from_video(self, video_file: str, srt_path: str, language: str = "ht") -> Path:
        """
        Jenere soutit pou videyo
        1. Ekstrè audio soti nan videyo
        2. Transkri ak STT
        3. Kreye fichye SRT ak timestamps
        
        Args:
            video_file: Chemen fichye videyo
            srt_path: Chemen pou sove fichye SRT
            language: Lang soutit yo (ht=Kreyòl)
            
        Returns:
            Path: Chemen fichye SRT
        """
        try:
            output_path = Path(srt_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # TODO: Implement caption generation pipeline
            # For now, create placeholder SRT
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("1\n")
                f.write("00:00:00,000 --> 00:00:05,000\n")
                f.write("[Caption demo - Transkri ak STT byento]\n\n")
                f.write("2\n")
                f.write("00:00:05,000 --> 00:00:10,000\n")
                f.write("[Itilize STT pou ekstrè tèks soti nan audio]\n")
            
            print(f"⚠️ Caption generation: Placeholder SRT created")
            print(f"   TODO: 1) Extract audio from video (ffmpeg)")
            print(f"   TODO: 2) Transcribe with STT ({language})")
            print(f"   TODO: 3) Generate SRT with proper timestamps")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating captions: {e}")
            raise
    
    async def denoise_audio_in_video(self, video_file: str, output_video: str) -> Path:
        """
        Retire bri background nan odyo videyo a
        Rekòmande: SoX, RNNoise, oswa ffmpeg filters
        
        Args:
            video_file: Chemen fichye videyo orijinal
            output_video: Chemen pou sove videyo netwaye
            
        Returns:
            Path: Chemen videyo netwaye
        """
        try:
            import shutil
            
            output_path = Path(output_video)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # TODO: Implement audio denoising
            # For now, copy video as placeholder
            shutil.copy(video_file, output_video)
            
            print(f"⚠️ Audio denoising: Placeholder copy created")
            print(f"   TODO: 1) Extract audio from video")
            print(f"   TODO: 2) Apply noise reduction (noisereduce/RNNoise)")
            print(f"   TODO: 3) Re-merge clean audio with video")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error denoising audio: {e}")
            raise
    
    async def correct_voiceover(self, video_file: str, output_video: str, voice: str = "creole-native") -> Path:
        """
        Korije erè nan vwadeyò videyo a
        
        Args:
            video_file: Chemen fichye videyo orijinal
            output_video: Chemen pou sove videyo korije
            voice: Vwa pou re-jenere pati yo
            
        Returns:
            Path: Chemen videyo korije
        """
        try:
            # TODO: Implement voiceover correction
            # 1. Transcribe existing voiceover
            # 2. Let user mark errors
            # 3. Re-generate specific segments
            # 4. Splice corrected audio back into video
            print(f"⚠️ Voiceover correction: Feature an devlopman")
            return Path(output_video)
            
        except Exception as e:
            print(f"❌ Error correcting voiceover: {e}")
            raise
    
    async def generate_soundtrack_for_video(self, video_file: str, soundtrack_path: str) -> Path:
        """
        Jenere yon soundtrack ak IA pou videyo
        APIs: Mubert AI, AIVA, Soundraw
        
        Args:
            video_file: Chemen fichye videyo
            soundtrack_path: Chemen pou sove soundtrack la
            
        Returns:
            Path: Chemen fichye soundtrack
        """
        try:
            output_path = Path(soundtrack_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # TODO: Implement AI soundtrack generation
            # Create placeholder text file for now
            placeholder_path = Path(str(output_path) + ".txt")
            with open(placeholder_path, "w", encoding="utf-8") as f:
                f.write("AI Soundtrack Placeholder\n")
                f.write("Video: " + video_file + "\n")
                f.write("\nPotential APIs:\n")
                f.write("- Mubert AI: https://mubert.com/\n")
                f.write("- AIVA: https://www.aiva.ai/\n")
                f.write("- Soundraw: https://soundraw.io/\n")
            
            print(f"⚠️ AI soundtrack: Placeholder created")
            print(f"   TODO: Integrate AI music generation API")
            print(f"   Saved placeholder: {placeholder_path}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating soundtrack: {e}")
            raise


# ============================================================
# STANDALONE FUNCTIONS
# ============================================================

async def extract_text_from_document(file_path: str) -> str:
    """Ekstrè tèks soti nan dokiman"""
    service = MediaService()
    return await service.extract_text_from_document(file_path)

async def html_to_text(url: str) -> str:
    """Konvèti HTML an tèks"""
    service = MediaService()
    return await service.html_to_text(url)

async def add_voiceover_to_video(video_file: str, output_video: str, voice: str = "creole-native") -> Path:
    """Ajoute vwadeyò nan videyo"""
    service = MediaService()
    return await service.add_voiceover_to_video(video_file, output_video, voice)

async def add_sfx_to_video(video_file: str, output_video: str, sfx_files: list = None) -> Path:
    """Ajoute efè son nan videyo"""
    service = MediaService()
    return await service.add_sfx_to_video(video_file, output_video, sfx_files)

async def generate_captions_from_video(video_file: str, srt_path: str, language: str = "ht") -> Path:
    """Jenere soutit pou videyo"""
    service = MediaService()
    return await service.generate_captions_from_video(video_file, srt_path, language)

async def denoise_audio_in_video(video_file: str, output_video: str) -> Path:
    """Retire bri background"""
    service = MediaService()
    return await service.denoise_audio_in_video(video_file, output_video)

async def correct_voiceover(video_file: str, output_video: str, voice: str = "creole-native") -> Path:
    """Korije vwadeyò"""
    service = MediaService()
    return await service.correct_voiceover(video_file, output_video, voice)

async def generate_soundtrack_for_video(video_file: str, soundtrack_path: str) -> Path:
    """Jenere soundtrack ak IA"""
    service = MediaService()
    return await service.generate_soundtrack_for_video(video_file, soundtrack_path)
