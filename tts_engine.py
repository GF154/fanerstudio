#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗣️ Text-to-Speech (TTS) Engine for Audiobook Generation
Motè TTS pou jenere audiobook
"""

import io
import os
import tempfile
from typing import Optional, Literal, List
from pathlib import Path

# gTTS - Google Text-to-Speech (Simple & Free)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS not available - install with: pip install gtts")

# pyttsx3 - Offline TTS
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("⚠️ pyttsx3 not available - install with: pip install pyttsx3")

# pydub - Audio processing
try:
    from pydub import AudioSegment
    from pydub.effects import speedup, normalize
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("⚠️ pydub not available - install with: pip install pydub")


class TTSEngine:
    """Text-to-Speech engine for audiobook generation"""
    
    def __init__(self, engine: str = "gtts"):
        """
        Initialize TTS engine
        
        Args:
            engine: TTS engine to use ('gtts' or 'pyttsx3')
        """
        self.engine = engine
        
        if engine == "gtts" and not GTTS_AVAILABLE:
            raise ImportError("gTTS not installed. Install with: pip install gtts")
        
        if engine == "pyttsx3" and not PYTTSX3_AVAILABLE:
            raise ImportError("pyttsx3 not installed. Install with: pip install pyttsx3")
    
    def generate_audio_gtts(
        self,
        text: str,
        output_file: str,
        lang: str = "en",
        slow: bool = False
    ) -> str:
        """
        Generate audio using gTTS
        
        Args:
            text: Text to convert
            output_file: Output file path
            lang: Language code (en, fr, ht, etc.)
            slow: Slow speed
            
        Returns:
            Path to generated audio file
        """
        try:
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(output_file)
            return output_file
        
        except Exception as e:
            raise Exception(f"gTTS error: {str(e)}")
    
    def generate_audio_pyttsx3(
        self,
        text: str,
        output_file: str,
        rate: int = 150,
        volume: float = 1.0,
        voice_gender: Optional[str] = None
    ) -> str:
        """
        Generate audio using pyttsx3 (offline)
        
        Args:
            text: Text to convert
            output_file: Output file path
            rate: Speech rate (words per minute)
            volume: Volume (0.0 to 1.0)
            voice_gender: 'male' or 'female' (optional)
            
        Returns:
            Path to generated audio file
        """
        try:
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            
            # Set voice if specified
            if voice_gender:
                voices = engine.getProperty('voices')
                for voice in voices:
                    if voice_gender.lower() in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Save to file
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            
            return output_file
        
        except Exception as e:
            raise Exception(f"pyttsx3 error: {str(e)}")
    
    def generate_audio(
        self,
        text: str,
        output_file: Optional[str] = None,
        voice: str = "natural",
        speed: float = 1.0,
        pitch: int = 0,
        format: str = "mp3",
        lang: str = "en",
        progress_callback: Optional[callable] = None
    ) -> str:
        """
        Generate audio from text with advanced processing
        
        Args:
            text: Text to convert
            output_file: Output file path (auto-generated if None)
            voice: Voice type ('natural', 'male', 'female')
            speed: Speech speed (0.5 to 2.0)
            pitch: Pitch adjustment (-2 to +2)
            format: Output format ('mp3', 'wav')
            lang: Language code
            progress_callback: Function to call with progress updates
            
        Returns:
            Path to generated audio file
        """
        # Generate output file if not provided
        if not output_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}') as tmp:
                output_file = tmp.name
        
        if progress_callback:
            progress_callback(10, "Initializing TTS...")
        
        # Split text into manageable chunks
        chunks = self.chunk_text(text, max_length=4900)  # gTTS limit is 5000
        
        if progress_callback:
            progress_callback(20, f"Processing {len(chunks)} text chunks...")
        
        # Generate audio for each chunk
        temp_files = []
        for i, chunk in enumerate(chunks):
            if progress_callback:
                progress = 20 + (60 * (i + 1) / len(chunks))
                progress_callback(int(progress), f"Generating audio chunk {i+1}/{len(chunks)}...")
            
            # Create temp file for this chunk
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Generate audio
            if self.engine == "gtts" or GTTS_AVAILABLE:
                slow = speed < 1.0
                self.generate_audio_gtts(chunk, temp_file.name, lang, slow)
            elif self.engine == "pyttsx3" or PYTTSX3_AVAILABLE:
                rate = int(150 * speed)
                voice_gender = None
                if voice == "male":
                    voice_gender = "male"
                elif voice == "female":
                    voice_gender = "female"
                self.generate_audio_pyttsx3(chunk, temp_file.name, rate, 1.0, voice_gender)
            
            temp_files.append(temp_file.name)
        
        if progress_callback:
            progress_callback(85, "Combining audio chunks...")
        
        # Combine all chunks if more than one
        if len(temp_files) > 1 and PYDUB_AVAILABLE:
            combined = self.combine_audio_files(temp_files)
            
            # Apply speed adjustment if needed and different from gTTS slow
            if speed != 1.0 and PYDUB_AVAILABLE:
                if progress_callback:
                    progress_callback(90, "Adjusting speed...")
                combined = self.adjust_speed(combined, speed)
            
            # Normalize audio
            if progress_callback:
                progress_callback(95, "Normalizing audio...")
            combined = normalize(combined)
            
            # Export
            combined.export(output_file, format=format)
            
            # Clean up temp files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        elif len(temp_files) == 1:
            # Just one file, copy it
            import shutil
            shutil.copy(temp_files[0], output_file)
            os.unlink(temp_files[0])
        
        else:
            # No pydub, just use first file (or combine manually)
            import shutil
            shutil.copy(temp_files[0], output_file)
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        if progress_callback:
            progress_callback(100, "Complete!")
        
        return output_file
    
    @staticmethod
    def get_available_engines():
        """Return list of available TTS engines"""
        engines = {
            "gtts": GTTS_AVAILABLE,
            "pyttsx3": PYTTSX3_AVAILABLE
        }
        return engines
    
    @staticmethod
    def chunk_text(text: str, max_length: int = 4900) -> List[str]:
        """
        Split text into chunks for processing
        
        Args:
            text: Full text
            max_length: Maximum characters per chunk (gTTS limit is 5000)
            
        Returns:
            List of text chunks
        """
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            # If adding this paragraph exceeds limit, save current and start new
            if len(current_chunk) + len(para) > max_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # If still too long, split by sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > max_length:
                sentences = chunk.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
                sub_chunk = ""
                for sentence in sentences:
                    if len(sub_chunk) + len(sentence) > max_length and sub_chunk:
                        final_chunks.append(sub_chunk.strip())
                        sub_chunk = sentence
                    else:
                        sub_chunk += " " + sentence if sub_chunk else sentence
                if sub_chunk:
                    final_chunks.append(sub_chunk.strip())
            else:
                final_chunks.append(chunk)
        
        return final_chunks if final_chunks else [text[:max_length]]
    
    @staticmethod
    def combine_audio_files(file_paths: List[str]):
        """
        Combine multiple audio files into one
        
        Args:
            file_paths: List of audio file paths
            
        Returns:
            Combined AudioSegment
        """
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub not installed. Install with: pip install pydub")
        
        from pydub import AudioSegment
        
        combined = AudioSegment.empty()
        
        for file_path in file_paths:
            audio = AudioSegment.from_mp3(file_path)
            # Add small pause between chunks (200ms)
            combined += audio + AudioSegment.silent(duration=200)
        
        return combined
    
    @staticmethod
    def adjust_speed(audio, speed: float):
        """
        Adjust audio playback speed
        
        Args:
            audio: AudioSegment to adjust
            speed: Speed multiplier (0.5 to 2.0)
            
        Returns:
            Speed-adjusted AudioSegment
        """
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub not installed. Install with: pip install pydub")
        
        # Change frame rate to adjust speed
        # Higher frame rate = faster playback
        adjusted = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed)
        })
        
        # Convert back to original frame rate to maintain compatibility
        return adjusted.set_frame_rate(audio.frame_rate)
    
    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """
        Get duration of audio file in seconds
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Duration in seconds
        """
        if not PYDUB_AVAILABLE:
            return 0.0
        
        try:
            audio = AudioSegment.from_file(file_path)
            return len(audio) / 1000.0  # Convert ms to seconds
        except:
            return 0.0
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration as MM:SS
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


# Quick test function
if __name__ == "__main__":
    tts = TTSEngine()
    
    print("🗣️ Text-to-Speech Engine")
    print("=" * 50)
    print("\n✅ Available engines:")
    for engine, available in tts.get_available_engines().items():
        status = "✅" if available else "❌"
        print(f"  {status} {engine}")
    
    print("\n💡 Usage:")
    print("  from tts_engine import TTSEngine")
    print('  tts = TTSEngine()')
    print('  audio_file = tts.generate_audio("Your text here", output_file="output.mp3")')
    
    # Test if available
    if GTTS_AVAILABLE:
        print("\n🧪 Running quick test...")
        try:
            test_file = "test_audio.mp3"
            tts.generate_audio("Hello, this is a test.", output_file=test_file)
            print(f"✅ Test successful! Audio saved to: {test_file}")
        except Exception as e:
            print(f"❌ Test failed: {e}")

