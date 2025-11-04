#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AI Script Generator for Faner Studio
Generate podcast scripts using AI (GPT-4, Claude, or local models)

Features:
- Podcast script generation
- Interview-style dialogues
- News summaries
- Educational content
- Storytelling scripts
- Multi-speaker conversation generation
"""

import os
import json
import httpx
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger('FanerStudio.AIScriptGenerator')


class ScriptType(str, Enum):
    """Types of scripts that can be generated"""
    INTERVIEW = "interview"
    NEWS = "news"
    EDUCATIONAL = "educational"
    STORYTELLING = "storytelling"
    CONVERSATION = "conversation"
    DEBATE = "debate"
    REVIEW = "review"


class AIProvider(str, Enum):
    """AI providers"""
    OPENAI = "openai"  # GPT-4
    ANTHROPIC = "anthropic"  # Claude
    HUGGINGFACE = "huggingface"  # Open source models
    LOCAL = "local"  # Local LLM


@dataclass
class ScriptRequest:
    """Script generation request"""
    topic: str
    script_type: ScriptType
    duration_minutes: int = 10
    num_speakers: int = 2
    tone: str = "casual"  # casual, formal, humorous, serious
    language: str = "ht"  # Haitian Creole by default
    target_audience: str = "general"
    include_intro: bool = True
    include_outro: bool = True
    
    # AI parameters
    temperature: float = 0.7
    max_tokens: int = 2000


class AIScriptGenerator:
    """
    Generate podcast scripts using AI
    Jeneratè script podcast avèk AI
    """
    
    def __init__(
        self,
        provider: AIProvider = AIProvider.OPENAI,
        api_key: Optional[str] = None
    ):
        """
        Initialize AI script generator
        
        Args:
            provider: AI provider to use
            api_key: API key for the provider
        """
        self.provider = provider
        self.api_key = api_key or self._get_api_key(provider)
        
        if not self.api_key and provider != AIProvider.LOCAL:
            logger.warning(f"No API key found for {provider}")
    
    def _get_api_key(self, provider: AIProvider) -> Optional[str]:
        """Get API key from environment"""
        key_map = {
            AIProvider.OPENAI: "OPENAI_API_KEY",
            AIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            AIProvider.HUGGINGFACE: "HUGGINGFACE_API_KEY"
        }
        return os.getenv(key_map.get(provider, ""))
    
    async def generate_script(
        self,
        request: ScriptRequest
    ) -> Dict[str, any]:
        """
        Generate podcast script using AI
        
        Args:
            request: Script generation request
        
        Returns:
            Generated script with metadata
        """
        logger.info(f"🤖 Generating {request.script_type} script on {request.topic}")
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Generate with selected provider
        if self.provider == AIProvider.OPENAI:
            script = await self._generate_with_openai(prompt, request)
        elif self.provider == AIProvider.ANTHROPIC:
            script = await self._generate_with_anthropic(prompt, request)
        elif self.provider == AIProvider.HUGGINGFACE:
            script = await self._generate_with_huggingface(prompt, request)
        else:
            script = self._generate_fallback(request)
        
        # Parse and format script
        formatted_script = self._format_script(script, request)
        
        return {
            "script": formatted_script,
            "topic": request.topic,
            "type": request.script_type.value,
            "duration_estimate": request.duration_minutes,
            "speakers": request.num_speakers,
            "language": request.language,
            "metadata": {
                "provider": self.provider.value,
                "tokens_used": len(script.split()),
                "tone": request.tone
            }
        }
    
    def _build_prompt(self, request: ScriptRequest) -> str:
        """Build AI prompt for script generation"""
        
        base_prompt = f"""
Generate a {request.script_type.value} podcast script in {self._get_language_name(request.language)}.

Topic: {request.topic}
Duration: {request.duration_minutes} minutes
Number of speakers: {request.num_speakers}
Tone: {request.tone}
Target audience: {request.target_audience}

Requirements:
1. Write dialogue for {request.num_speakers} speakers
2. Include stage directions in [brackets] for emotions and pauses
3. Make it engaging and natural
4. Appropriate for {request.tone} tone
5. Total speaking time should be approximately {request.duration_minutes} minutes
"""
        
        if request.include_intro:
            base_prompt += "\n6. Start with an engaging intro"
        
        if request.include_outro:
            base_prompt += "\n7. End with a memorable outro"
        
        # Add type-specific instructions
        if request.script_type == ScriptType.INTERVIEW:
            base_prompt += """

Format as an interview with:
- Host asking thoughtful questions
- Guest providing detailed answers
- Natural back-and-forth conversation
"""
        elif request.script_type == ScriptType.NEWS:
            base_prompt += """

Format as news report with:
- Clear headline/intro
- Key facts and information
- Professional delivery
- Optional: Reporter in the field
"""
        elif request.script_type == ScriptType.EDUCATIONAL:
            base_prompt += """

Format as educational content with:
- Clear explanations
- Examples and analogies
- Engaging questions
- Key takeaways at the end
"""
        elif request.script_type == ScriptType.STORYTELLING:
            base_prompt += """

Format as a story with:
- Compelling narrative arc
- Character development
- Descriptive language
- Emotional moments
"""
        
        base_prompt += """

Output format:
[INTRO - Background: Corporate]
Speaker1 (emotion): Dialogue text
[SFX: sound_effect_name]

[MAIN - Background: Calm]
Speaker1: Dialogue
Speaker2 (emotion): Response
[Pause: 1.0]

[OUTRO - Background: Upbeat]
Speaker1: Closing remarks
"""
        
        return base_prompt
    
    def _get_language_name(self, code: str) -> str:
        """Get language name from code"""
        languages = {
            "ht": "Haitian Creole (Kreyòl Ayisyen)",
            "en": "English",
            "fr": "French (Français)",
            "es": "Spanish (Español)"
        }
        return languages.get(code, code)
    
    async def _generate_with_openai(
        self,
        prompt: str,
        request: ScriptRequest
    ) -> str:
        """Generate script using OpenAI GPT-4"""
        if not self.api_key:
            logger.warning("OpenAI API key not available, using fallback")
            return self._generate_fallback(request)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a professional podcast script writer who creates engaging, natural-sounding scripts in multiple languages, including Haitian Creole."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": request.temperature,
                        "max_tokens": request.max_tokens
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    script = data['choices'][0]['message']['content']
                    logger.info("✅ Script generated with OpenAI")
                    return script
                else:
                    logger.error(f"OpenAI API error: {response.status_code}")
                    return self._generate_fallback(request)
        
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return self._generate_fallback(request)
    
    async def _generate_with_anthropic(
        self,
        prompt: str,
        request: ScriptRequest
    ) -> str:
        """Generate script using Anthropic Claude"""
        if not self.api_key:
            return self._generate_fallback(request)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-3-sonnet-20240229",
                        "max_tokens": request.max_tokens,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    script = data['content'][0]['text']
                    logger.info("✅ Script generated with Claude")
                    return script
                else:
                    return self._generate_fallback(request)
        
        except Exception as e:
            logger.error(f"Claude generation failed: {e}")
            return self._generate_fallback(request)
    
    async def _generate_with_huggingface(
        self,
        prompt: str,
        request: ScriptRequest
    ) -> str:
        """Generate script using Hugging Face models"""
        # Use a text generation model
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"inputs": prompt, "parameters": {"max_length": request.max_tokens}}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        script = result[0].get('generated_text', '')
                        logger.info("✅ Script generated with Hugging Face")
                        return script
                
                return self._generate_fallback(request)
        
        except Exception as e:
            logger.error(f"Hugging Face generation failed: {e}")
            return self._generate_fallback(request)
    
    def _generate_fallback(self, request: ScriptRequest) -> str:
        """Generate a template-based script when AI is not available"""
        logger.info("Using fallback template-based generation")
        
        templates = {
            ScriptType.INTERVIEW: self._template_interview,
            ScriptType.NEWS: self._template_news,
            ScriptType.EDUCATIONAL: self._template_educational,
            ScriptType.STORYTELLING: self._template_storytelling
        }
        
        template_func = templates.get(request.script_type, self._template_conversation)
        return template_func(request)
    
    def _template_interview(self, request: ScriptRequest) -> str:
        """Template for interview-style podcast"""
        return f"""[INTRO - Background: Corporate, Volume: 0.3]
Host (excited): Byenveni nan emisyon nou an! Jodi a, n ap pale sou {request.topic}.
[SFX: intro_swoosh]
Host (professional): Nou gen yon envite espesyal pou pale ak nou sou sijè sa a.

[MAIN - Background: Calm]
Host: Kòman {request.topic} enpòtan?
Guest (thoughtful): Se yon kesyon trè enteresan. {request.topic} enpòtan paske...
[Pause: 1.0]
Host (curious): Eske ou ka bay nou yon egzanp?
Guest (enthusiastic): Wi, byen sou! Paregzanp...

[OUTRO - Background: Upbeat]
Host (happy): Mèsi anpil pou tan ou! Sa te trè enteresan.
Guest: Mèsi pou envitasyon an!
[SFX: outro_fade]
"""
    
    def _template_news(self, request: ScriptRequest) -> str:
        """Template for news-style podcast"""
        return f"""[INTRO - Background: Tech, Volume: 0.2]
Anchor (professional): Bonjou. Men dènye nouvèl yo.
[SFX: notification]

[MAIN - Background: Corporate]
Anchor: Jodi a, nou ap pale sou {request.topic}.
Reporter (excited): Mwen la sou teren, ak plis detay sou {request.topic}!
Anchor (serious): Di nou plis, tanpri.
Reporter: Selon enfòmasyon nou jwenn...

[OUTRO - Background: Corporate]
Anchor (professional): Se tout pou jodi a. Mèsi pou nou te gade.
[SFX: outro_fade]
"""
    
    def _template_educational(self, request: ScriptRequest) -> str:
        """Template for educational podcast"""
        return f"""[INTRO - Background: Calm]
Teacher (friendly): Bonjou elèv! Jodi a, nou pral aprann sou {request.topic}.

[MAIN - Background: Calm]
Teacher (explaining): Premyèman, ann konprann kisa {request.topic} ye.
[Pause: 1.0]
Teacher: Se yon konse ki...
Student (curious): Eske ou ka eksplike pi byen?
Teacher (patient): Byen sou! Ann gade yon egzanp.

[OUTRO - Background: Upbeat]
Teacher (encouraging): Sonje, {request.topic} enpòtan. Pratike l chak jou!
"""
    
    def _template_storytelling(self, request: ScriptRequest) -> str:
        """Template for storytelling podcast"""
        return f"""[INTRO - Background: Dramatic, Volume: 0.4]
Narrator (mysterious): Gen yon istwa sou {request.topic}...
[SFX: intro_swoosh]

[MAIN - Background: Calm]
Narrator (engaging): Yon jou, te gen...
[Pause: 2.0]
Character1 (surprised): Mwen pa t ka kwè sa!
Character2 (calm): Men se verite.

[OUTRO - Background: Calm]
Narrator (reflective): Epi se konsa istwa a fini.
[SFX: outro_fade]
"""
    
    def _template_conversation(self, request: ScriptRequest) -> str:
        """Template for general conversation"""
        return f"""[INTRO]
Speaker1: Bonjou! Ann pale sou {request.topic}.
Speaker2: Wi, se yon bon sijè!

[MAIN]
Speaker1: Kisa w panse sou {request.topic}?
Speaker2: Mwen panse ke...
Speaker1: Enterésan!

[OUTRO]
Speaker1: Mèsi pou konvèsasyon an!
Speaker2: Mèsi!
"""
    
    def _format_script(self, script: str, request: ScriptRequest) -> str:
        """Format and validate generated script"""
        # Ensure script has proper segments
        if "[INTRO" not in script and request.include_intro:
            script = "[INTRO]\n" + script
        
        if "[OUTRO" not in script and request.include_outro:
            script = script + "\n[OUTRO]\nSpeaker: Mèsi!"
        
        return script.strip()


# ============================================================
# SCRIPT TEMPLATES LIBRARY
# ============================================================

class ScriptTemplatesLibrary:
    """Library of pre-made script templates"""
    
    @staticmethod
    def list_templates() -> List[Dict]:
        """List all available templates"""
        return [
            {
                "id": "interview_tech",
                "name": "Tech Interview",
                "type": ScriptType.INTERVIEW,
                "description": "Interview about technology topics",
                "duration": 15
            },
            {
                "id": "news_daily",
                "name": "Daily News",
                "type": ScriptType.NEWS,
                "description": "Daily news summary format",
                "duration": 10
            },
            {
                "id": "edu_language",
                "name": "Language Lesson",
                "type": ScriptType.EDUCATIONAL,
                "description": "Educational language lesson",
                "duration": 20
            },
            {
                "id": "story_folktale",
                "name": "Haitian Folktale",
                "type": ScriptType.STORYTELLING,
                "description": "Traditional Haitian story",
                "duration": 15
            }
        ]


# ============================================================
# TESTING
# ============================================================

async def test_script_generator():
    """Test AI script generator"""
    print("🧪 Testing AI Script Generator\n")
    
    generator = AIScriptGenerator(provider=AIProvider.LOCAL)
    
    request = ScriptRequest(
        topic="Teknoloji ak edikasyon",
        script_type=ScriptType.INTERVIEW,
        duration_minutes=10,
        num_speakers=2,
        tone="casual",
        language="ht"
    )
    
    print(f"Generating {request.script_type.value} script on: {request.topic}")
    result = await generator.generate_script(request)
    
    print("\n📝 Generated Script:")
    print("="*60)
    print(result['script'])
    print("="*60)
    print(f"\nMetadata: {result['metadata']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_script_generator())

