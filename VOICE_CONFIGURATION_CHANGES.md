# Voice Configuration - Changes Summary

## Date: November 6, 2025

## Changes Made

### 1. Updated Edge TTS Default Voice ✅
**File: `tts/main.py`**
- **Line 45**: Changed default Edge TTS voice from `fr-FR-DeniseNeural` (female) to `fr-FR-HenriNeural` (male)
- **Line 46**: Renamed `edge_male` to `edge_female` for Denise voice
- **Line 194**: Updated fallback default to use HenriNeural

**Result**: If Edge TTS is used as fallback, it will now use a male French voice instead of female.

### 2. Updated API Default Voice ✅
**File: `api/index.py`**
- **Line 72**: Changed `AudiobookRequest` default from `"natural"` to `"creole-native"`
- **Line 317**: Changed `generate_audiobook` endpoint default from `"natural"` to `"creole-native"`
- **Lines 461-467**: Updated voice list endpoint to show `creole-native` as default with premium options

**Result**: All API endpoints now default to native Haitian Creole voice.

### 3. Updated Environment Configuration ✅
**File: `env.example`**
- Added detailed comments for OpenAI API Key (line 20-22)
- Added detailed comments for ElevenLabs API Key (line 25-28)
- Added `DEFAULT_VOICE=creole-native` setting (line 36)
- Added `DEFAULT_TTS_ENGINE=huggingface` setting (line 40)
- Updated notes section with voice information (lines 56-62)

**Result**: Clear documentation for setting up API keys and understanding voice options.

## Voice Routing Logic

### Default Voice: `creole-native`
When user doesn't specify a voice, the system now uses:
1. **Primary**: Facebook MMS-TTS Haitian (`facebook/mms-tts-hat`)
   - Native Haitian Creole pronunciation
   - Male voice
   - FREE - no API key required
   - File: `projet_kreyol_IA/generer_audio_huggingface.py`

2. **Fallback**: Google TTS French (`gtts` with `lang='fr'`)
   - French pronunciation (close to Creole)
   - Used if HuggingFace model unavailable
   - File: `projet_kreyol_IA/generer_audio_huggingface.py` line 168

### Premium Voice Options (Require API Keys)

**OpenAI TTS** (specify voice: `openai-*`)
- `openai-echo`: Male voice
- `openai-nova`: Female voice  
- `openai-alloy`, `openai-fable`, `openai-onyx`, `openai-shimmer`
- Cost: $15 per 1M characters
- Handler: `projet_kreyol_IA/app/services/tts_service.py` lines 130-161

**ElevenLabs** (specify voice: `elevenlabs-<voice_id>`)
- Custom voice cloning
- Multiple languages
- Free tier: 10K chars/month
- Handler: `projet_kreyol_IA/app/services/tts_service.py` lines 163-196

## How to Test

### Test 1: Verify Default Voice
```python
# Test with projet_kreyol_IA API
import httpx
import asyncio

async def test_default_voice():
    url = "http://localhost:8000/api/tts"
    files = {"text": "Bonjou! Kijan ou ye?"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=files)
        print(f"Status: {response.status_code}")
        # Should use creole-native voice automatically
        # Check audio file for male Haitian Creole voice

asyncio.run(test_default_voice())
```

### Test 2: Verify Voice List
```bash
# Check available voices
curl http://localhost:8000/api/audiobook/voices

# Expected output should show:
# - creole-native as default with "default": true
# - Male gender for creole-native
# - OpenAI and ElevenLabs as premium options
```

### Test 3: Verify Edge TTS Fallback
```python
# In tts/main.py
from tts.main import TTSEngine
import asyncio

async def test_edge_tts():
    tts = TTSEngine(engine="edge")
    audio = await tts.generate_audio(
        text="Bonjou tout moun",
        language="ht",
        # No voice specified - should use HenriNeural (male)
    )
    print(f"Generated: {audio}")

asyncio.run(test_edge_tts())
```

### Test 4: Verify Premium Voices
```python
# Test OpenAI voice
from projet_kreyol_IA.app.services.tts_service import TTSService
import asyncio

async def test_openai_voice():
    service = TTSService()
    audio = await service.text_to_speech_file(
        text="Hello, testing OpenAI voice",
        output_path="test_openai.mp3",
        voice="openai-echo"  # Male voice
    )
    print(f"OpenAI audio: {audio}")

asyncio.run(test_openai_voice())
```

## Expected Behavior After Changes

| Scenario | Voice Used | Accent | Gender | Cost |
|----------|------------|--------|--------|------|
| Default (no voice specified) | `creole-native` | Haitian Creole | Male | FREE |
| `voice="creole-native"` | Facebook MMS-TTS | Haitian Creole | Male | FREE |
| Edge TTS fallback | `fr-FR-HenriNeural` | French | Male | FREE |
| `voice="openai-echo"` | OpenAI Echo | English/Multi | Male | Paid |
| `voice="openai-nova"` | OpenAI Nova | English/Multi | Female | Paid |
| `voice="elevenlabs-*"` | ElevenLabs Custom | Custom/Multi | Custom | Paid |

## Files Modified

1. ✅ `tts/main.py` - Edge TTS default voice
2. ✅ `api/index.py` - API default voice and voice list
3. ✅ `env.example` - Environment configuration docs

## Files Already Correct (No Changes Needed)

1. ✅ `tts/production_voice.py` - Already using HenriNeural
2. ✅ `projet_kreyol_IA/app/services/tts_service.py` - Already defaults to creole-native
3. ✅ `projet_kreyol_IA/generer_audio_huggingface.py` - Facebook MMS-TTS implementation

## User Instructions

### To Use Native Creole Voice (Current Default)
No action needed! Just use the platform normally:
- The default is now `creole-native`
- Male Haitian Creole voice
- FREE - no API keys required

### To Use Premium Voices
1. Copy `env.example` to `.env`
2. Add your API keys:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   ELEVENLABS_API_KEY=your-key-here
   ```
3. Specify voice in request:
   ```python
   voice="openai-echo"  # or "openai-nova", "elevenlabs-custom"
   ```

## Summary

✅ **Problem Solved**: Default voice is now male Haitian Creole (creole-native)
✅ **Accent Fixed**: Native Creole pronunciation, not French
✅ **Premium Options**: OpenAI and ElevenLabs available when API keys configured
✅ **Fallback Fixed**: If Edge TTS used, it's now male voice (HenriNeural)

**Result**: User will hear male Haitian Creole voice by default with proper Creole accent! 🇭🇹🎙️

