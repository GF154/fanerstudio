#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 AI Service
Sèvis pou jenere kontni ak IA (OpenAI, Anthropic, elatriye)
"""

import os
import httpx
from pathlib import Path
from typing import Optional, Dict, List

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


class AIService:
    """Sèvis pou jenere kontni ak IA"""
    
    def __init__(self):
        """Initialize AI service"""
        self.openai_available = bool(OPENAI_API_KEY)
        self.anthropic_available = bool(ANTHROPIC_API_KEY)
        
        if self.openai_available:
            print("✅ OpenAI API configured")
        if self.anthropic_available:
            print("✅ Anthropic API configured")
        
        if not (self.openai_available or self.anthropic_available):
            print("⚠️  No AI API keys configured - using fallback responses")
    
    async def generate_script(
        self,
        prompt: str,
        style: str = "conversational",
        length: str = "medium",
        language: str = "ht"
    ) -> Dict[str, str]:
        """
        Jenere yon script ak IA
        
        Args:
            prompt: Sijè/pwòm pou script la
            style: Stil (conversational, formal, humorous, dramatic)
            length: Longè (short=1-2min, medium=3-5min, long=5-10min)
            language: Lang (ht=Kreyòl, fr=Frans, en=Anglè)
        
        Returns:
            dict: Script ki jenere ak metadata
        """
        try:
            # Try OpenAI first
            if self.openai_available:
                return await self._generate_with_openai(prompt, style, length, language)
            # Fallback to Anthropic
            elif self.anthropic_available:
                return await self._generate_with_anthropic(prompt, style, length, language)
            else:
                # Fallback: generate basic script
                return self._generate_fallback_script(prompt, style, length, language)
                
        except Exception as e:
            print(f"❌ Error generating script: {e}")
            # Return fallback on error
            return self._generate_fallback_script(prompt, style, length, language)
    
    async def _generate_with_openai(
        self,
        prompt: str,
        style: str,
        length: str,
        language: str
    ) -> Dict[str, str]:
        """Generate script using OpenAI API"""
        
        # Map parameters
        lang_names = {"ht": "Haitian Creole", "fr": "French", "en": "English"}
        length_words = {"short": "100-200", "medium": "300-500", "long": "500-800"}
        
        # Build system prompt
        system_prompt = f"""You are a professional script writer for audio/video content. 
Write in {lang_names.get(language, 'Haitian Creole')} language.
Style: {style}
Length: {length_words.get(length, '300-500')} words.

Include:
- Engaging introduction
- Clear main points
- Strong conclusion
- Natural flow for narration"""

        # Call OpenAI API
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4",  # or gpt-3.5-turbo for faster/cheaper
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1500
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            script = data["choices"][0]["message"]["content"]
            
            return {
                "status": "success",
                "script": script,
                "word_count": len(script.split()),
                "style": style,
                "length": length,
                "language": language,
                "model": "openai-gpt4"
            }
    
    async def _generate_with_anthropic(
        self,
        prompt: str,
        style: str,
        length: str,
        language: str
    ) -> Dict[str, str]:
        """Generate script using Anthropic Claude API"""
        
        lang_names = {"ht": "Haitian Creole", "fr": "French", "en": "English"}
        length_words = {"short": "100-200", "medium": "300-500", "long": "500-800"}
        
        system_prompt = f"""Write a professional script in {lang_names.get(language, 'Haitian Creole')}.
Style: {style}
Length: {length_words.get(length, '300-500')} words.
Topic: {prompt}"""

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 1500,
                    "messages": [
                        {"role": "user", "content": system_prompt}
                    ]
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            script = data["content"][0]["text"]
            
            return {
                "status": "success",
                "script": script,
                "word_count": len(script.split()),
                "style": style,
                "length": length,
                "language": language,
                "model": "anthropic-claude"
            }
    
    def _generate_fallback_script(
        self,
        prompt: str,
        style: str,
        length: str,
        language: str
    ) -> Dict[str, str]:
        """Generate a basic fallback script when no AI API available"""
        
        templates = {
            "ht": """
Byenvini! Jodi a nou pral pale sou: {prompt}

Kòmansman:
{prompt} se yon sijè ki enpòtan anpil. Li gen yon gwo enpak sou lavi nou chak jou.

Pwen Prensipal:
Premye bagay nou dwe konprann se ke {prompt} gen plizyè aspè. Chak aspè gen enpòtans li.

Dezyèm bagay, nou ka wè ke {prompt} afekte nou tout nan diferan fason. Se poutèt sa nou bezwen fè atansyon.

Twazyèm pwen, si nou vle jwenn bon rezilta ak {prompt}, nou dwe prepare byen epi suiv bon pratik yo.

Konklizyon:
Pou fini, {prompt} se yon sijè ki merite atansyon nou. Avèk enfòmasyon sa yo, ou ka fè bon desizyon.

Mèsi pou ou te koute! N ap pale ankò!
""",
            "fr": """
Bienvenue! Aujourd'hui nous allons parler de: {prompt}

Introduction:
{prompt} est un sujet très important. Il a un grand impact sur nos vies quotidiennes.

Points Principaux:
La première chose à comprendre est que {prompt} a plusieurs aspects. Chaque aspect a son importance.

Deuxièmement, nous pouvons voir que {prompt} nous affecte tous de différentes manières. C'est pourquoi nous devons faire attention.

Troisièmement, si nous voulons obtenir de bons résultats avec {prompt}, nous devons bien nous préparer et suivre les bonnes pratiques.

Conclusion:
Pour finir, {prompt} est un sujet qui mérite notre attention. Avec ces informations, vous pouvez prendre de bonnes décisions.

Merci de votre écoute! À bientôt!
""",
            "en": """
Welcome! Today we're going to talk about: {prompt}

Introduction:
{prompt} is a very important topic. It has a major impact on our daily lives.

Main Points:
The first thing to understand is that {prompt} has multiple aspects. Each aspect has its importance.

Secondly, we can see that {prompt} affects us all in different ways. That's why we need to pay attention.

Thirdly, if we want to get good results with {prompt}, we must prepare well and follow best practices.

Conclusion:
To conclude, {prompt} is a topic that deserves our attention. With this information, you can make good decisions.

Thank you for listening! See you soon!
"""
        }
        
        script = templates.get(language, templates["ht"]).format(prompt=prompt)
        
        return {
            "status": "success",
            "script": script.strip(),
            "word_count": len(script.split()),
            "style": style,
            "length": length,
            "language": language,
            "model": "fallback-template",
            "note": "Generated with fallback template. Configure AI API keys for better results."
        }
    
    async def generate_music_prompt(
        self,
        video_description: str,
        mood: str = "upbeat",
        genre: str = "instrumental"
    ) -> str:
        """
        Jenere yon prompt pou AI music generation
        
        Args:
            video_description: Deskripsyon videyo a
            mood: Mood (upbeat, calm, dramatic, sad, happy)
            genre: Genre (instrumental, electronic, acoustic, cinematic)
        
        Returns:
            str: Prompt pou AI music
        """
        if self.openai_available:
            # Use AI to generate better prompt
            async with httpx.AsyncClient(timeout=30.0) as client:
                try:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "gpt-3.5-turbo",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "Generate a concise music prompt for AI music generation."
                                },
                                {
                                    "role": "user",
                                    "content": f"Create music prompt for: {video_description}. Mood: {mood}, Genre: {genre}"
                                }
                            ],
                            "max_tokens": 100
                        }
                    )
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                except:
                    pass
        
        # Fallback: simple template
        return f"{mood} {genre} music for {video_description}"


# Global instance
ai_service = AIService()


if __name__ == "__main__":
    import asyncio
    
    print("🤖 AI Service Test")
    print("=" * 60)
    
    async def test():
        # Test script generation
        result = await ai_service.generate_script(
            prompt="Istwa Ayiti",
            style="conversational",
            length="short",
            language="ht"
        )
        
        print(f"Model: {result['model']}")
        print(f"Words: {result['word_count']}")
        print(f"\nScript:\n{result['script']}")
    
    asyncio.run(test())

