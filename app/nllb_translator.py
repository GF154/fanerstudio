"""
NLLB Translation Service via Hugging Face REST API
Lightweight - no huggingface-hub needed!
Ultra-compatible with Render free tier
"""
import os
import httpx
from typing import Optional

class NLLBTranslator:
    """NLLB translator using Hugging Face REST API (ultra-lightweight!)"""
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")  # Optional but recommended
        self.api_url = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
        
        # Language codes for NLLB
        self.lang_codes = {
            "en": "eng_Latn",
            "fr": "fra_Latn",
            "es": "spa_Latn",
            "ht": "hat_Latn",  # Haitian Creole
            "creole": "hat_Latn",
            "kreyol": "hat_Latn"
        }
    
    def translate(
        self, 
        text: str, 
        source_lang: str = "auto",
        target_lang: str = "ht"
    ) -> dict:
        """
        Translate text using NLLB via Hugging Face REST API
        
        Args:
            text: Text to translate
            source_lang: Source language code (en, fr, es, auto)
            target_lang: Target language code (ht for Haitian Creole)
            
        Returns:
            dict with translated_text and metadata
        """
        try:
            # Convert language codes to NLLB format
            if source_lang == "auto":
                # Default to French if auto-detect
                source_lang = "fr"
            
            src_code = self.lang_codes.get(source_lang.lower(), "fra_Latn")
            tgt_code = self.lang_codes.get(target_lang.lower(), "hat_Latn")
            
            # Prepare headers
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            # Make request to Hugging Face Inference API
            payload = {
                "inputs": text,
                "parameters": {
                    "src_lang": src_code,
                    "tgt_lang": tgt_code
                }
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(self.api_url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Handle different response formats
                    if isinstance(result, list) and len(result) > 0:
                        translated = result[0].get("translation_text", text)
                    else:
                        translated = result.get("translation_text", text)
                    
                    return {
                        "success": True,
                        "translated_text": translated,
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "model": "NLLB-200-distilled-600M",
                        "method": "Hugging Face REST API"
                    }
                else:
                    raise Exception(f"API returned status {response.status_code}: {response.text}")
            
        except Exception as e:
            # Fallback to deep-translator if NLLB API fails
            from deep_translator import GoogleTranslator
            
            try:
                translator = GoogleTranslator(source='auto', target='ht')
                translated = translator.translate(text)
                
                return {
                    "success": True,
                    "translated_text": translated,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "model": "Google Translate",
                    "method": "Fallback",
                    "note": f"NLLB API failed: {str(e)}"
                }
            except Exception as fallback_error:
                return {
                    "success": False,
                    "error": str(fallback_error),
                    "translated_text": text,
                    "note": "Both NLLB and Google Translate failed"
                }
    
    async def translate_async(
        self,
        text: str,
        source_lang: str = "auto",
        target_lang: str = "ht"
    ) -> dict:
        """Async version of translate"""
        return self.translate(text, source_lang, target_lang)


# Convenience function
def translate_to_creole(text: str, source_lang: str = "auto") -> str:
    """
    Quick translation to Haitian Creole
    
    Args:
        text: Text to translate
        source_lang: Source language (auto, en, fr, es)
        
    Returns:
        Translated text in Haitian Creole
    """
    translator = NLLBTranslator()
    result = translator.translate(text, source_lang, "ht")
    
    if result["success"]:
        return result["translated_text"]
    else:
        return text  # Return original if translation fails


# Example usage
if __name__ == "__main__":
    translator = NLLBTranslator()
    
    # Test translations
    tests = [
        ("Hello, how are you?", "en"),
        ("Bonjour, comment allez-vous?", "fr"),
        ("Good morning", "en")
    ]
    
    for text, lang in tests:
        result = translator.translate(text, lang, "ht")
        print(f"\n{lang.upper()} → HT:")
        print(f"  Input:  {text}")
        print(f"  Output: {result['translated_text']}")
        print(f"  Method: {result.get('method', 'Unknown')}")

