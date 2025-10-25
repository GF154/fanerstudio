#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 NLLB Pipeline - PDF → Translation → Audiobook
Entegrasyon NLLB pou Kreyòl IA Studio
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from gtts import gTTS
import PyPDF2
from pathlib import Path
from tqdm import tqdm
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class NLLBPipeline:
    """Pipeline konplè pou PDF → Translation → Audiobook ak NLLB"""
    
    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M"):
        """
        Inisyalize pipeline NLLB
        
        Args:
            model_name: Non model NLLB (default: nllb-200-distilled-600M)
        """
        print(f"📦 Chaje model NLLB: {model_name}...")
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.translator = pipeline("translation", model=self.model, tokenizer=self.tokenizer)
        print("✅ Model NLLB chaje avèk siksè!")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Ekstrè tèks soti nan PDF
        
        Args:
            pdf_path: Chemen fichye PDF
            
        Returns:
            str: Tèks ki ekstrè
        """
        print(f"📄 Ekstrè tèks soti nan: {pdf_path}")
        text = ""
        
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            print(f"📖 Jwenn {total_pages} paj")
            
            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                print(f"   Paj {i}/{total_pages} ekstrè", end="\r")
            
            print(f"\n✅ Ekstraksyon konplete: {len(text)} karaktè")
        
        return text
    
    def translate_to_creole(
        self, 
        text: str, 
        src_lang: str = "fra_Latn",
        tgt_lang: str = "hat_Latn",
        chunk_size: int = 500
    ) -> str:
        """
        Tradwi tèks an Kreyòl Ayisyen ak NLLB
        
        Args:
            text: Tèks pou tradwi
            src_lang: Lang sous (fra_Latn=Franse, eng_Latn=Angle)
            tgt_lang: Lang sib (hat_Latn=Kreyòl Ayisyen)
            chunk_size: Gwosè chak moso pou tradwi
            
        Returns:
            str: Tèks tradwi
        """
        print(f"🌍 Tradiksyon {src_lang} → {tgt_lang}...")
        
        # Split text into chunks
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        translated_chunks = []
        
        print(f"📊 Total chunks: {len(chunks)}")
        
        # Translate each chunk with progress bar
        for chunk in tqdm(chunks, desc="Tradiksyon"):
            try:
                translation = self.translator(
                    chunk, 
                    src_lang=src_lang, 
                    tgt_lang=tgt_lang,
                    max_length=512
                )[0]['translation_text']
                
                translated_chunks.append(translation)
            except Exception as e:
                print(f"\n⚠️ Erè ak chunk: {str(e)[:100]}")
                translated_chunks.append(chunk)  # Keep original if translation fails
        
        result = " ".join(translated_chunks)
        print(f"✅ Tradiksyon konplete: {len(result)} karaktè")
        
        return result
    
    def text_to_audio(
        self, 
        text: str, 
        output_audio: str = "audiobook_kreyol.mp3",
        lang: str = "ht"
    ):
        """
        Kreye audiobook soti nan tèks
        
        Args:
            text: Tèks pou konvèti
            output_audio: Non fichye output
            lang: Lang (ht=Kreyòl Ayisyen)
        """
        print(f"🎧 Kreyasyon odyo an Kreyòl...")
        
        try:
            # Use gTTS for Creole
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_audio)
            
            print(f"✅ Audiobook kreye avèk siksè: {output_audio}")
            
            # Show file size
            file_size = Path(output_audio).stat().st_size
            size_mb = file_size / (1024 * 1024)
            print(f"📊 Gwosè fichye: {size_mb:.2f} MB")
            
        except Exception as e:
            print(f"❌ Erè kreyasyon odyo: {e}")
            
            # Fallback to Kreyòl native TTS
            print("⚠️ Eseye ak Kreyòl native TTS...")
            try:
                from generer_audio_huggingface import generer_audio_creole
                generer_audio_creole(text, Path(output_audio))
                print(f"✅ Audiobook kreye ak Kreyòl native: {output_audio}")
            except Exception as e2:
                print(f"❌ Erè ak fallback: {e2}")
                raise
    
    def process_pdf_to_audiobook(
        self,
        pdf_path: str,
        output_dir: str = "output/nllb",
        src_lang: str = "fra_Latn",
        use_native_tts: bool = False
    ) -> dict:
        """
        Pipeline konplè: PDF → Translation → Audiobook
        
        Args:
            pdf_path: Chemen fichye PDF
            output_dir: Dosye pou sove output yo
            src_lang: Lang sous (fra_Latn oswa eng_Latn)
            use_native_tts: Itilize Kreyòl native TTS olye de gTTS
            
        Returns:
            dict: Info sou fichye yo kreye
        """
        print("\n" + "="*60)
        print("🇭🇹 KREYÒL IA - NLLB PIPELINE")
        print("="*60)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Get base name
        base_name = Path(pdf_path).stem
        
        # Step 1: Extract text
        print("\n📖 STEP 1: Ekstraksyon tèks")
        print("-" * 60)
        text = self.extract_text_from_pdf(pdf_path)
        
        # Save extracted text
        extracted_path = output_path / f"{base_name}_extracted.txt"
        extracted_path.write_text(text, encoding='utf-8')
        print(f"💾 Tèks ekstrè sove: {extracted_path}")
        
        # Step 2: Translate
        print("\n🌍 STEP 2: Tradiksyon")
        print("-" * 60)
        translated_text = self.translate_to_creole(text, src_lang=src_lang)
        
        # Save translated text
        translated_path = output_path / f"{base_name}_kreyol.txt"
        translated_path.write_text(translated_text, encoding='utf-8')
        print(f"💾 Tradiksyon sove: {translated_path}")
        
        # Step 3: Create audiobook
        print("\n🎧 STEP 3: Kreyasyon audiobook")
        print("-" * 60)
        audio_path = output_path / f"{base_name}_audiobook.mp3"
        
        if use_native_tts:
            # Use Kreyòl native TTS
            from generer_audio_huggingface import generer_audio_creole
            generer_audio_creole(translated_text, audio_path)
        else:
            # Use gTTS
            self.text_to_audio(translated_text, str(audio_path))
        
        # Summary
        print("\n" + "="*60)
        print("✅ PWOSESIS KONPLETE!")
        print("="*60)
        print(f"📄 Tèks orijinal: {len(text)} karaktè")
        print(f"🇭🇹 Tèks tradwi: {len(translated_text)} karaktè")
        print(f"📁 Output dosye: {output_path}")
        print("="*60)
        
        return {
            "extracted_text": str(extracted_path),
            "translated_text": str(translated_path),
            "audiobook": str(audio_path),
            "stats": {
                "original_chars": len(text),
                "translated_chars": len(translated_text),
                "output_dir": str(output_path)
            }
        }


# -----------------------------------------------------
# STANDALONE FUNCTION
# -----------------------------------------------------

def pdf_to_kreyol_audiobook(
    pdf_path: str,
    output_dir: str = "output/nllb",
    src_lang: str = "fra_Latn",
    model_name: str = "facebook/nllb-200-distilled-600M",
    use_native_tts: bool = False
) -> dict:
    """
    Fonksyon senp pou konvèti PDF an audiobook Kreyòl
    
    Args:
        pdf_path: Chemen fichye PDF
        output_dir: Dosye output
        src_lang: Lang sous (fra_Latn=Franse, eng_Latn=Angle)
        model_name: Model NLLB pou itilize
        use_native_tts: Itilize Kreyòl native TTS
        
    Returns:
        dict: Info sou fichye yo kreye
    """
    pipeline = NLLBPipeline(model_name=model_name)
    return pipeline.process_pdf_to_audiobook(
        pdf_path=pdf_path,
        output_dir=output_dir,
        src_lang=src_lang,
        use_native_tts=use_native_tts
    )


# -----------------------------------------------------
# MAIN FUNCTION
# -----------------------------------------------------

def main():
    """Fonksyon prensipal pou teste"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python nllb_pipeline.py <pdf_path> [src_lang]")
        print("Example: python nllb_pipeline.py livre.pdf fra_Latn")
        print("\nLang disponib:")
        print("  - fra_Latn (Franse)")
        print("  - eng_Latn (Angle)")
        print("  - spa_Latn (Panyòl)")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    src_lang = sys.argv[2] if len(sys.argv) > 2 else "fra_Latn"
    
    # Process PDF
    result = pdf_to_kreyol_audiobook(
        pdf_path=pdf_path,
        src_lang=src_lang,
        use_native_tts=True  # Use native Creole TTS for better quality
    )
    
    print("\n📊 Rezilta:")
    print(f"   Extracted: {result['extracted_text']}")
    print(f"   Translated: {result['translated_text']}")
    print(f"   Audiobook: {result['audiobook']}")


if __name__ == "__main__":
    main()

