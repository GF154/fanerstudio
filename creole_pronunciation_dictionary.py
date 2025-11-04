#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Haitian Creole Pronunciation Dictionary
Diksyonè pwononsyasyon Kreyòl Ayisyen

Maps Creole words to phonetic equivalents for better TTS pronunciation
"""

from typing import Dict, List, Optional
import json
from pathlib import Path
import re


class CreolePronunciationDictionary:
    """
    Comprehensive Creole pronunciation dictionary
    Diksyonè pwononsyasyon konplè pou Kreyòl
    """
    
    def __init__(self):
        self.dictionary = self._load_base_dictionary()
        self.common_patterns = self._load_common_patterns()
        self.nasalized_vowels = self._load_nasalized_vowels()
    
    def _load_base_dictionary(self) -> Dict[str, str]:
        """Load base pronunciation dictionary"""
        return {
            # ============================================================
            # COMMON GREETINGS / SALITASYON KOMEN
            # ============================================================
            "bonjou": "bon-ZHOO",
            "bonswa": "bon-SWAH",
            "bonnwit": "bon-NWEE",
            "kòman ou ye": "koh-MAN oo YEH",
            "mwen byen": "mwen bee-YEN",
            "mèsi": "meh-SEE",
            "tanpri": "tan-PREE",
            "padon": "pah-DON",
            "orevwa": "oh-reh-VWAH",
            
            # ============================================================
            # PRONOUNS / PWONON
            # ============================================================
            "mwen": "mwen",  # nasalized
            "ou": "oo",
            "li": "lee",
            "nou": "noo",
            "yo": "yoh",
            
            # ============================================================
            # COMMON VERBS / VÈB KOMEN
            # ============================================================
            "ale": "ah-LEH",
            "vini": "vee-NEE",
            "manje": "man-ZHEH",
            "bwè": "BWEH",
            "dòmi": "doh-MEE",
            "travay": "trah-VAY",
            "pale": "pah-LEH",
            "tande": "tan-DEH",
            "gade": "gah-DEH",
            "konnen": "koh-NEN",
            "renmen": "ren-MEN",
            "fè": "FEH",
            "di": "DEE",
            "pran": "PRAN",
            "bay": "BAY",
            "chita": "chee-TAH",
            "kanpe": "kan-PEH",
            
            # ============================================================
            # COMMON NOUNS / NON KOMEN
            # ============================================================
            "kay": "KAY",
            "moun": "MOON",
            "timoun": "tee-MOON",
            "fanmi": "fan-MEE",
            "zanmi": "zan-MEE",
            "manje": "man-ZHEH",
            "dlo": "DLOH",
            "pen": "PEN",
            "lajan": "lah-ZHAN",
            "wout": "WOOT",
            "machin": "mah-SHEEN",
            "kay": "KAY",
            "kote": "koh-TEH",
            "tan": "TAN",
            
            # ============================================================
            # ADJECTIVES / ADJEKTIF
            # ============================================================
            "bèl": "BEL",
            "bon": "BON",
            "move": "moh-VEH",
            "gran": "GRAN",
            "piti": "pee-TEE",
            "jon": "ZHON",
            "vye": "VYEH",
            "cho": "CHOH",
            "frèt": "FRET",
            
            # ============================================================
            # NUMBERS / NIM
            # ============================================================
            "youn": "YOON",
            "de": "DEH",
            "twa": "TWAH",
            "kat": "KAT",
            "senk": "SENK",
            "sis": "SEES",
            "sèt": "SET",
            "uit": "WEET",
            "nèf": "NEF",
            "dis": "DEES",
            
            # ============================================================
            # QUESTIONS / KESYON
            # ============================================================
            "ki": "KEE",
            "kisa": "kee-SAH",
            "kilès": "kee-LES",
            "konbyen": "kon-BYEN",
            "kote": "koh-TEH",
            "kilè": "kee-LEH",
            "pouki": "poo-KEE",
            "kijan": "kee-ZHAN",
            
            # ============================================================
            # COMMON PHRASES / FRAZ KOMEN
            # ============================================================
            "sa k ap fèt": "sah kahp FET",
            "m ap vini": "mahp vee-NEE",
            "m ap ale": "mahp ah-LEH",
            "pa gen pwoblèm": "pah gen pwoh-BLEM",
            "tout bagay": "toot bah-GAY",
            "anpil": "an-PEEL",
            "tigout": "tee-GOOT",
            
            # ============================================================
            # SPECIAL CREOLE SOUNDS
            # ============================================================
            "en": "en",  # nasalized
            "an": "an",  # nasalized
            "on": "on",  # nasalized
            "oun": "oon",  # nasalized
        }
    
    def _load_common_patterns(self) -> List[tuple]:
        """Load common pronunciation patterns"""
        return [
            # Final consonants often silent or softened
            (r"(\w+)n$", r"\1n"),  # Keep final n
            (r"(\w+)m$", r"\1m"),  # Keep final m
            
            # Nasal vowels
            (r"an(?![aeiou])", "an"),
            (r"en(?![aeiou])", "en"),
            (r"on(?![aeiou])", "on"),
            
            # R pronunciation (rolled)
            (r"r", "r"),
            
            # French-influenced sounds
            (r"ch", "sh"),
            (r"j", "zh"),
            
            # Vowel combinations
            (r"ou", "oo"),
            (r"ai", "ay"),
            (r"ei", "ay"),
        ]
    
    def _load_nasalized_vowels(self) -> Dict[str, str]:
        """Nasalized vowel patterns specific to Creole"""
        return {
            "an": "ã",  # as in "manje"
            "en": "ẽ",  # as in "renmen"
            "on": "õ",  # as in "bon"
            "in": "ĩ",  # as in "vin"
            "un": "ũ",  # as in "youn"
        }
    
    def get_pronunciation(self, word: str) -> Optional[str]:
        """
        Get pronunciation for a Creole word
        
        Args:
            word: Creole word
        
        Returns:
            Phonetic pronunciation or None
        """
        word_lower = word.lower().strip()
        
        # Exact match
        if word_lower in self.dictionary:
            return self.dictionary[word_lower]
        
        # Try with patterns
        for pattern, replacement in self.common_patterns:
            if re.search(pattern, word_lower):
                return re.sub(pattern, replacement, word_lower)
        
        return None
    
    def process_text(self, text: str) -> str:
        """
        Process entire text and replace words with pronunciations
        
        Args:
            text: Creole text
        
        Returns:
            Text with pronunciation hints
        """
        words = text.split()
        processed_words = []
        
        for word in words:
            # Clean punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            pronunciation = self.get_pronunciation(clean_word)
            
            if pronunciation:
                # Keep original punctuation
                if word != clean_word:
                    punct = word[len(clean_word):]
                    processed_words.append(pronunciation + punct)
                else:
                    processed_words.append(pronunciation)
            else:
                processed_words.append(word)
        
        return ' '.join(processed_words)
    
    def add_word(self, word: str, pronunciation: str):
        """Add new word to dictionary"""
        self.dictionary[word.lower()] = pronunciation
    
    def save_to_file(self, filepath: Path):
        """Save dictionary to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.dictionary, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filepath: Path):
        """Load dictionary from JSON file"""
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                custom_dict = json.load(f)
                self.dictionary.update(custom_dict)
    
    def get_stats(self) -> Dict:
        """Get dictionary statistics"""
        return {
            "total_words": len(self.dictionary),
            "categories": {
                "greetings": 9,
                "pronouns": 5,
                "verbs": 16,
                "nouns": 13,
                "adjectives": 9,
                "numbers": 10,
                "questions": 8,
                "phrases": 7
            }
        }


# ============================================================
# CREOLE PHONETIC RULES
# ============================================================

class CreolePhoneticRules:
    """
    Phonetic rules specific to Haitian Creole
    Règ fonetik espesifik pou Kreyòl Ayisyen
    """
    
    @staticmethod
    def apply_nasalization(text: str) -> str:
        """Apply nasal vowel rules"""
        # Replace nasal vowel combinations
        replacements = {
            "an": "ã",
            "en": "ẽ",
            "on": "õ",
            "in": "ĩ",
            "un": "ũ"
        }
        
        for pattern, replacement in replacements.items():
            # Only replace when not followed by another vowel
            text = re.sub(f"{pattern}(?![aeiou])", replacement, text)
        
        return text
    
    @staticmethod
    def apply_rhythm(text: str) -> str:
        """Apply Creole rhythm patterns"""
        # Creole typically has even stress, unlike French
        # This is a simplified representation
        words = text.split()
        
        # Mark stress on final syllable for multi-syllable words
        stressed_words = []
        for word in words:
            if len(word) > 4:  # Multi-syllable word
                # Add stress marker (for TTS engines that support it)
                stressed_words.append(word.upper())
            else:
                stressed_words.append(word)
        
        return ' '.join(stressed_words)


# ============================================================
# TESTING & USAGE EXAMPLES
# ============================================================

def test_pronunciation_dictionary():
    """Test the pronunciation dictionary"""
    print("🧪 Testing Creole Pronunciation Dictionary\n")
    
    dict = CreolePronunciationDictionary()
    
    # Test individual words
    test_words = ["bonjou", "mwen", "gade", "manje", "renmen"]
    
    print("Individual Words:")
    for word in test_words:
        pronunciation = dict.get_pronunciation(word)
        print(f"  {word} → {pronunciation}")
    
    print("\nFull Text Processing:")
    test_text = "Bonjou! Kòman ou ye? Mwen byen, mèsi."
    processed = dict.process_text(test_text)
    print(f"  Original: {test_text}")
    print(f"  Processed: {processed}")
    
    print(f"\nDictionary Stats:")
    stats = dict.get_stats()
    print(f"  Total words: {stats['total_words']}")
    for category, count in stats['categories'].items():
        print(f"  {category}: {count}")


if __name__ == "__main__":
    test_pronunciation_dictionary()

