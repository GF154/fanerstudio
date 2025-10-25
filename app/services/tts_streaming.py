#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 Streaming TTS Service
Generate audio progressively for better UX
"""

from pathlib import Path
from datetime import datetime
import uuid
import sys
import asyncio
from typing import AsyncGenerator, List

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class StreamingTTSService:
    """
    TTS Service with streaming/progressive generation support
    
    Features:
    - Generate audio in chunks
    - Play while generating
    - Progress callbacks
    - Memory efficient
    """
    
    def __init__(self):
        """Initialize streaming TTS service"""
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.chunks_dir = self.output_dir / "chunks"
        self.chunks_dir.mkdir(exist_ok=True)
        print("✅ Streaming TTS Service initialized")
    
    async def generate_audio_stream(
        self,
        text: str,
        voice: str = "creole-native",
        chunk_size: int = 500  # Characters per chunk
    ) -> AsyncGenerator[dict, None]:
        """
        Generate audio in chunks (streaming)
        
        Args:
            text: Text to convert
            voice: Voice to use
            chunk_size: Characters per chunk
        
        Yields:
            dict: Chunk information
                - chunk_id: Chunk number
                - total_chunks: Total number of chunks
                - audio_file: Path to chunk audio file
                - progress: Progress percentage (0-100)
                - text_chunk: Text for this chunk
        """
        # Split text into chunks by sentence boundaries
        chunks = self._split_text_smart(text, chunk_size)
        total_chunks = len(chunks)
        
        print(f"\n🎵 STREAMING TTS START")
        print(f"   Total text: {len(text)} chars")
        print(f"   Chunks: {total_chunks}")
        print(f"   Chunk size: ~{chunk_size} chars\n")
        
        from generer_audio_huggingface import generer_audio_creole
        
        for i, chunk_text in enumerate(chunks):
            # Generate unique filename for this chunk
            chunk_file = self.chunks_dir / f"chunk_{uuid.uuid4().hex[:8]}_{i:03d}.mp3"
            
            # Generate audio for chunk
            try:
                generer_audio_creole(chunk_text, chunk_file)
                
                # Calculate progress
                progress = ((i + 1) / total_chunks) * 100
                
                yield {
                    "chunk_id": i,
                    "total_chunks": total_chunks,
                    "audio_file": str(chunk_file),
                    "audio_url": f"/output/chunks/{chunk_file.name}",
                    "progress": progress,
                    "text_chunk": chunk_text[:100] + "..." if len(chunk_text) > 100 else chunk_text,
                    "status": "ready"
                }
                
                print(f"   ✓ Chunk {i+1}/{total_chunks} ready ({progress:.1f}%)")
                
            except Exception as e:
                print(f"   ⚠️  Chunk {i+1} failed: {e}")
                yield {
                    "chunk_id": i,
                    "total_chunks": total_chunks,
                    "audio_file": None,
                    "progress": ((i + 1) / total_chunks) * 100,
                    "text_chunk": chunk_text[:100],
                    "status": "error",
                    "error": str(e)
                }
    
    async def generate_audiobook_progressive(
        self,
        text: str,
        voice: str = "creole-native",
        chunk_size: int = 500,
        callback = None
    ) -> dict:
        """
        Generate audiobook progressively with downloadable chunks
        
        Args:
            text: Full text
            voice: Voice to use
            chunk_size: Characters per chunk
            callback: Optional async callback(chunk_data)
        
        Returns:
            dict: Final audiobook info with all chunks
        """
        print(f"\n📚 PROGRESSIVE AUDIOBOOK GENERATION")
        print(f"   Text length: {len(text)} chars")
        print(f"   Voice: {voice}\n")
        
        chunk_files = []
        chunk_urls = []
        
        # Generate chunks
        async for chunk_data in self.generate_audio_stream(text, voice, chunk_size):
            if chunk_data["status"] == "ready":
                chunk_files.append(Path(chunk_data["audio_file"]))
                chunk_urls.append(chunk_data["audio_url"])
            
            # Call callback if provided
            if callback:
                await callback(chunk_data)
        
        print(f"\n✅ All chunks generated: {len(chunk_files)}")
        
        # Merge all chunks into final file
        final_filename = f"audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        final_path = self.output_dir / final_filename
        
        print(f"   Merging chunks into: {final_filename}...")
        
        try:
            await self._merge_audio_files(chunk_files, final_path)
            print(f"   ✅ Final audiobook created!")
        except Exception as e:
            print(f"   ⚠️  Merge failed: {e}")
            print(f"   Individual chunks still available")
        
        return {
            "status": "completed",
            "final_audio": f"/output/{final_filename}",
            "chunks": chunk_urls,
            "total_chunks": len(chunk_urls),
            "text_length": len(text)
        }
    
    def _split_text_smart(self, text: str, chunk_size: int) -> List[str]:
        """
        Split text into chunks at sentence boundaries
        
        Args:
            text: Text to split
            chunk_size: Target chunk size in characters
        
        Returns:
            List of text chunks
        """
        # Split by sentence markers
        import re
        sentences = re.split(r'([.!?]\s+)', text)
        
        chunks = []
        current_chunk = ""
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            separator = sentences[i+1] if i+1 < len(sentences) else ""
            full_sentence = sentence + separator
            
            if len(current_chunk) + len(full_sentence) <= chunk_size:
                current_chunk += full_sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = full_sentence
        
        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # If no sentence boundaries, fall back to simple chunking
        if not chunks:
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        return chunks
    
    async def _merge_audio_files(
        self,
        audio_files: List[Path],
        output_file: Path
    ):
        """
        Merge multiple audio files into one
        
        Args:
            audio_files: List of audio file paths
            output_file: Output file path
        """
        try:
            # Try using pydub if available
            from pydub import AudioSegment
            
            combined = AudioSegment.empty()
            
            for audio_file in audio_files:
                audio = AudioSegment.from_mp3(audio_file)
                combined += audio
            
            combined.export(output_file, format="mp3")
            
        except ImportError:
            # Fallback: use ffmpeg directly
            import subprocess
            
            # Create file list for ffmpeg
            list_file = output_file.parent / f"concat_list_{uuid.uuid4().hex[:8]}.txt"
            with open(list_file, 'w') as f:
                for audio_file in audio_files:
                    f.write(f"file '{audio_file.absolute()}'\n")
            
            # Run ffmpeg
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(list_file),
                '-c', 'copy',
                str(output_file)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Cleanup
            list_file.unlink()


# ============================================================
# STANDALONE FUNCTIONS
# ============================================================

async def generate_audio_progressive(
    text: str,
    output_dir: Path,
    voice: str = "creole-native",
    chunk_size: int = 500
) -> dict:
    """
    Helper function for progressive audio generation
    
    Args:
        text: Text to convert
        output_dir: Output directory
        voice: Voice to use
        chunk_size: Characters per chunk
    
    Returns:
        dict: Generation result
    """
    service = StreamingTTSService()
    return await service.generate_audiobook_progressive(text, voice, chunk_size)


if __name__ == "__main__":
    print("🎵 Streaming TTS Service")
    print("=" * 60)
    print("Features:")
    print("  • Progressive audio generation")
    print("  • Play while generating")
    print("  • Memory efficient")
    print("  • Downloadable chunks")
    print("=" * 60)

