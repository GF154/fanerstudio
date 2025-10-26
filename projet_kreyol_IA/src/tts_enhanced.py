#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced TTS Module with Multiple Voice Options
Support for natural Haitian Creole pronunciation
"""

import logging
from pathlib import Path
from typing import Optional
from gtts import gTTS

logger = logging.getLogger('KreyolAI.TTS_Enhanced')


class EnhancedTTS:
    """
    Enhanced Text-to-Speech with multiple engine support
    Optimized for Haitian Creole pronunciation
    """
    
    def __init__(self):
        """Initialize TTS with available engines"""
        self.available_engines = self._detect_engines()
        logger.info(f"Available TTS engines: {list(self.available_engines.keys())}")
    
    def _detect_engines(self) -> dict:
        """Detect available TTS engines"""
        engines = {}
        
        # 1. gTTS (always available)
        engines['gtts'] = {
            'name': 'Google TTS',
            'quality': 'high',
            'creole_support': False,
            'available': True
        }
        
        # 2. Try pyttsx3 (offline)
        try:
            import pyttsx3
            engines['pyttsx3'] = {
                'name': 'Offline TTS',
                'quality': 'medium',
                'creole_support': False,
                'available': True
            }
        except ImportError:
            engines['pyttsx3'] = {
                'name': 'Offline TTS',
                'quality': 'medium',
                'creole_support': False,
                'available': False
            }
        
        # 3. Try edge-tts (Microsoft Edge TTS)
        try:
            import edge_tts
            engines['edge'] = {
                'name': 'Microsoft Edge TTS',
                'quality': 'very_high',
                'creole_support': False,
                'available': True
            }
        except ImportError:
            engines['edge'] = {
                'name': 'Microsoft Edge TTS',
                'quality': 'very_high',
                'creole_support': False,
                'available': False
            }
        
        return engines
    
    def generate_gtts_french(
        self,
        text: str,
        output_path: Path,
        slow: bool = False
    ) -> Path:
        """
        Generate audio using gTTS with French voice (best for Creole)
        French pronunciation is closest to Haitian Creole
        """
        try:
            logger.info(f"Generating with gTTS (French mode)")
            tts = gTTS(text=text, lang='fr', slow=slow)
            tts.save(str(output_path))
            return output_path
        except Exception as e:
            logger.error(f"gTTS French generation failed: {e}")
            raise
    
    def generate_gtts_canadian_french(
        self,
        text: str,
        output_path: Path,
        slow: bool = False
    ) -> Path:
        """
        Generate audio using Canadian French (fr-CA)
        Often sounds more natural for Creole
        """
        try:
            logger.info(f"Generating with gTTS (Canadian French)")
            # Try Canadian French accent
            tts = gTTS(text=text, lang='fr', tld='ca', slow=slow)
            tts.save(str(output_path))
            return output_path
        except Exception as e:
            logger.warning(f"Canadian French not available, using standard French")
            return self.generate_gtts_french(text, output_path, slow)
    
    async def generate_edge_tts(
        self,
        text: str,
        output_path: Path,
        voice: str = "fr-FR-DeniseNeural"
    ) -> Path:
        """
        Generate audio using Microsoft Edge TTS
        Supports multiple French voices that work well for Creole
        
        Recommended voices:
        - fr-FR-DeniseNeural (Female, clear)
        - fr-FR-HenriNeural (Male, professional)
        - fr-CA-SylvieNeural (Canadian French, female)
        - fr-CA-AntoineNeural (Canadian French, male)
        """
        try:
            import edge_tts
            
            logger.info(f"Generating with Edge TTS (voice: {voice})")
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_path))
            return output_path
        except Exception as e:
            logger.error(f"Edge TTS generation failed: {e}")
            raise
    
    def generate_pyttsx3(
        self,
        text: str,
        output_path: Path,
        rate: int = 150
    ) -> Path:
        """
        Generate audio using pyttsx3 (offline)
        Works without internet but lower quality
        """
        try:
            import pyttsx3
            
            logger.info(f"Generating with pyttsx3 (offline)")
            engine = pyttsx3.init()
            
            # Set French voice if available
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Set rate (speed)
            engine.setProperty('rate', rate)
            
            # Save to file
            engine.save_to_file(text, str(output_path))
            engine.runAndWait()
            
            return output_path
        except Exception as e:
            logger.error(f"pyttsx3 generation failed: {e}")
            raise
    
    def generate_best_available(
        self,
        text: str,
        output_path: Path,
        prefer_quality: bool = True
    ) -> tuple[Path, str]:
        """
        Generate audio using the best available engine
        
        Priority order (quality mode):
        1. Edge TTS (if available) - highest quality
        2. gTTS Canadian French - very good
        3. gTTS French - good
        4. pyttsx3 - offline fallback
        
        Returns:
            tuple: (output_path, engine_used)
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        
        # Try Edge TTS first (best quality)
        if self.available_engines['edge']['available'] and prefer_quality:
            try:
                import asyncio
                asyncio.run(self.generate_edge_tts(text, output_path))
                return output_path, "Microsoft Edge TTS (fr-FR-DeniseNeural)"
            except Exception as e:
                logger.warning(f"Edge TTS failed, falling back: {e}")
        
        # Try gTTS Canadian French
        try:
            self.generate_gtts_canadian_french(text, output_path)
            return output_path, "Google TTS (Canadian French)"
        except Exception as e:
            logger.warning(f"Canadian French failed: {e}")
        
        # Try gTTS standard French
        try:
            self.generate_gtts_french(text, output_path)
            return output_path, "Google TTS (French)"
        except Exception as e:
            logger.warning(f"gTTS failed: {e}")
        
        # Last resort: pyttsx3 offline
        if self.available_engines['pyttsx3']['available']:
            try:
                self.generate_pyttsx3(text, output_path)
                return output_path, "Offline TTS (pyttsx3)"
            except Exception as e:
                logger.error(f"All TTS engines failed: {e}")
                raise RuntimeError("No TTS engine available")
        
        raise RuntimeError("No TTS engine available for audio generation")
    
    def get_recommendations_for_creole(self) -> dict:
        """
        Get recommendations for best Creole pronunciation
        """
        return {
            'best_online': {
                'engine': 'edge',
                'voice': 'fr-FR-DeniseNeural',
                'reason': 'Clear French pronunciation, natural intonation',
                'install': 'pip install edge-tts'
            },
            'best_offline': {
                'engine': 'pyttsx3',
                'voice': 'French voice (if available)',
                'reason': 'Works without internet',
                'install': 'pip install pyttsx3'
            },
            'current': {
                'engine': 'gtts',
                'voice': 'fr-CA (Canadian French)',
                'reason': 'Good balance of quality and availability',
                'install': 'Already installed'
            },
            'tips': [
                'Canadian French (fr-CA) often sounds more natural for Creole',
                'Microsoft Edge TTS has the highest quality',
                'Adjust speech rate if pronunciation is too fast',
                'Consider recording native Creole speakers for best results'
            ]
        }


def get_enhanced_tts() -> EnhancedTTS:
    """Factory function to get enhanced TTS instance"""
    return EnhancedTTS()

