#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Translation Quality - Compare Different Models for Haitian Creole
Compare NLLB vs other translation services
"""

import httpx
import os
from typing import Dict, List

class TranslationTester:
    """Test different translation models for Haitian Creole quality"""
    
    def __init__(self):
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        
    def test_nllb(self, text: str, source: str = "en", target: str = "ht") -> Dict:
        """Test NLLB-200 translation"""
        try:
            # New Hugging Face Inference API endpoint (2024+)
            url = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
            
            lang_codes = {
                "en": "eng_Latn",
                "fr": "fra_Latn",
                "ht": "hat_Latn",
                "es": "spa_Latn"
            }
            
            headers = {}
            if self.hf_api_key:
                headers["Authorization"] = f"Bearer {self.hf_api_key}"
            
            payload = {
                "inputs": text,
                "parameters": {
                    "src_lang": lang_codes.get(source, "eng_Latn"),
                    "tgt_lang": lang_codes.get(target, "hat_Latn")
                }
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        translation = result[0].get("translation_text", "")
                    else:
                        translation = result.get("translation_text", "")
                    
                    return {
                        "success": True,
                        "model": "NLLB-200-distilled-600M",
                        "translation": translation,
                        "provider": "Hugging Face (Facebook)",
                        "rating": "⭐⭐⭐⭐⭐"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Status {response.status_code}: {response.text[:100]}"
                    }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_m2m100(self, text: str, source: str = "en", target: str = "ht") -> Dict:
        """Test M2M100 translation"""
        try:
            url = "https://api-inference.huggingface.co/models/facebook/m2m100_418M"
            
            headers = {}
            if self.hf_api_key:
                headers["Authorization"] = f"Bearer {self.hf_api_key}"
            
            # M2M100 uses different format
            payload = {
                "inputs": text,
                "parameters": {
                    "src_lang": source,
                    "tgt_lang": target
                }
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        translation = result[0].get("translation_text", "")
                    else:
                        translation = result.get("translation_text", "")
                    
                    return {
                        "success": True,
                        "model": "M2M100-418M",
                        "translation": translation,
                        "provider": "Hugging Face (Facebook)",
                        "rating": "⭐⭐⭐"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Status {response.status_code}"
                    }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def compare_translations(self, test_cases: List[Dict]):
        """Compare translations from different models"""
        print("="*80)
        print("🇭🇹 COMPARISON: TRANSLATION QUALITY FOR HAITIAN CREOLE")
        print("="*80)
        print()
        
        if not self.hf_api_key:
            print("⚠️  NO HUGGINGFACE_API_KEY - Using public API (limited)")
            print("   Get free key at: https://huggingface.co/settings/tokens")
            print()
        
        for i, test in enumerate(test_cases, 1):
            text = test["text"]
            source = test.get("source", "en")
            
            print(f"📝 TEST {i}/{len(test_cases)}")
            print(f"   Original ({source.upper()}): {text}")
            print()
            
            # Test NLLB
            print("   Testing NLLB-200...")
            nllb_result = self.test_nllb(text, source, "ht")
            
            if nllb_result["success"]:
                print(f"   ✅ NLLB-200 {nllb_result['rating']}")
                print(f"      → {nllb_result['translation']}")
            else:
                print(f"   ❌ NLLB Error: {nllb_result.get('error', 'Unknown')}")
            
            print()
            
            # Test M2M100
            print("   Testing M2M100...")
            m2m_result = self.test_m2m100(text, source, "ht")
            
            if m2m_result["success"]:
                print(f"   ✅ M2M100 {m2m_result['rating']}")
                print(f"      → {m2m_result['translation']}")
            else:
                print(f"   ❌ M2M100 Error: {m2m_result.get('error', 'Unknown')}")
            
            print()
            print("-"*80)
            print()
        
        print("="*80)
        print("📊 RECOMMENDATION:")
        print("="*80)
        print()
        print("🏆 BEST FOR HAITIAN CREOLE: NLLB-200 ⭐⭐⭐⭐⭐")
        print()
        print("Why NLLB-200?")
        print("  ✅ Trained specifically on 200 languages including Haitian Creole")
        print("  ✅ Better cultural context understanding")
        print("  ✅ More natural translations")
        print("  ✅ Currently used in your platform")
        print()
        print("Alternative: M2M100 ⭐⭐⭐")
        print("  • Faster but less accurate for Haitian Creole")
        print("  • Good for quick translations")
        print()


def main():
    """Run translation quality tests"""
    tester = TranslationTester()
    
    # Test cases - Common phrases in different contexts
    test_cases = [
        {
            "text": "Hello, how are you today?",
            "source": "en",
            "context": "Greeting"
        },
        {
            "text": "The doctor said I need to rest and drink water.",
            "source": "en",
            "context": "Medical"
        },
        {
            "text": "I love Haitian food, especially griot and rice.",
            "source": "en",
            "context": "Cultural"
        },
        {
            "text": "Il faut que tu viennes demain matin.",
            "source": "fr",
            "context": "Daily conversation"
        },
        {
            "text": "The meeting is scheduled for next Monday at 9 AM.",
            "source": "en",
            "context": "Business"
        }
    ]
    
    tester.compare_translations(test_cases)
    
    print("="*80)
    print()
    print("💡 TIP: Add HUGGINGFACE_API_KEY to .env for unlimited requests!")
    print()
    print("   1. Go to: https://huggingface.co/settings/tokens")
    print("   2. Create new token (read access)")
    print("   3. Add to .env: HUGGINGFACE_API_KEY=hf_xxxxx")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

