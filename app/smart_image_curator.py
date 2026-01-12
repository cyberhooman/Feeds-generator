"""
Smart Image Curator - AI-Powered Visual Content Finder

This agent acts like a professional content creator, intelligently finding
relevant images from the web without using mainstream meme templates.

It can find:
- Reaction images
- Movie/TV scenes
- Meme images (but contextually relevant)
- Stock photos
- Real-life situations
- Abstract visuals

Uses web scraping (no paid APIs) to find the perfect image.
"""

import requests
import re
import io
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from PIL import Image
import logging
import time
import random
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup

try:
    from .ai_client import get_ai_client
    from .config import Config
except ImportError:
    from ai_client import get_ai_client
    from config import Config

logger = logging.getLogger(__name__)


@dataclass
class ImageResult:
    """A found image with metadata."""
    url: str
    local_path: str
    source: str  # google, bing, imgur, etc.
    relevance_score: float
    description: str
    image_type: str  # meme, photo, scene, abstract


class SmartImageCurator:
    """
    AI agent that intelligently finds relevant images from the web.

    Acts like a professional content creator who knows exactly what
    visual will work best for each piece of content.
    """

    def __init__(self, cache_dir: str = None):
        """Initialize the image curator."""
        self.ai_client = get_ai_client()
        self.cache_dir = Path(cache_dir or Config.OUTPUT_DIR / "image_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # User agents for scraping
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

        logger.info("SmartImageCurator initialized")

    def _get_headers(self) -> Dict[str, str]:
        """Get random headers for web scraping."""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def _detect_indonesian(self, text: str) -> bool:
        """Detect if text is primarily Indonesian."""
        indonesian_indicators = [
            'yang', 'ini', 'itu', 'adalah', 'dengan', 'untuk',
            'tidak', 'atau', 'ke', 'di', 'dari', 'pada',
            'saya', 'anda', 'kita', 'mereka', 'akan', 'sudah',
            'bisa', 'harus', 'cuma', 'gua', 'lu', 'gw', 'aja',
            'kayak', 'banget', 'dong', 'sih', 'lho', 'kok'
        ]

        text_lower = text.lower()
        matches = sum(1 for word in indonesian_indicators if f' {word} ' in f' {text_lower} ')

        # If 2+ Indonesian words found, likely Indonesian
        return matches >= 2

    def _detect_content_type(self, text: str, topic: str = None) -> str:
        """
        Detect if content is news or emotional/meme.

        Returns:
            "news" - Factual news content (needs entity extraction)
            "emotional" - Emotional/reaction content (needs facial expressions)
        """
        # News indicators
        news_keywords = [
            'president', 'minister', 'government', 'parliament', 'senate',
            'elected', 'announced', 'declared', 'signed', 'banned',
            'crisis', 'war', 'conflict', 'treaty', 'agreement',
            'economy', 'inflation', 'recession', 'market', 'stock',
            'breaking', 'update', 'latest', 'just in', 'reports',
            'according to', 'sources say', 'officials',
            # Indonesian news terms
            'presiden', 'menteri', 'pemerintah', 'parlemen', 'DPR',
            'diumumkan', 'ditandatangani', 'dilarang', 'krisis'
        ]

        # Emotional indicators (already have reactions)
        emotional_keywords = [
            'when you', 'me trying', 'tfw', 'that moment',
            'realization', 'feeling', 'mood', 'vibes',
            # Indonesian emotional terms
            'rasanya', 'kayak', 'waktu lu', 'gua pas'
        ]

        text_lower = text.lower()

        # Count matches
        news_score = sum(1 for kw in news_keywords if kw in text_lower)
        emotional_score = sum(1 for kw in emotional_keywords if kw in text_lower)

        # If topic is explicitly news-related
        if topic and any(kw in topic.lower() for kw in ['news', 'breaking', 'update', 'politik', 'ekonomi']):
            news_score += 2

        # Decision
        if news_score > emotional_score:
            return "news"
        else:
            return "emotional"

    def analyze_content_for_visuals(self, text: str, topic: str = None) -> Dict:
        """
        Enhanced AI analysis with Indonesian context understanding.

        Translates emotional context to universal search terms for better image matching.
        """
        # Detect language
        is_indonesian = self._detect_indonesian(text)

        prompt = f"""You are a professional social media content creator who understands BOTH English and Indonesian audiences.

TEXT: "{text}"
TOPIC: {topic or "general"}
LANGUAGE DETECTED: {"Indonesian" if is_indonesian else "English"}

YOUR JOB:
1. Understand the EMOTIONAL CONTEXT and SITUATION (not literal words)
2. Determine what UNIVERSAL REACTION IMAGE would work best
3. Create search queries that will find CLEAN IMAGES (no text overlays)

IMPORTANT RULES:
- If text is Indonesian, translate the EMOTION/SITUATION to universal English search terms
- Focus on FACIAL EXPRESSIONS, BODY LANGUAGE, or SCENES that convey the emotion
- DO NOT search for literal words - search for the FEELING
- Prefer: "shocked face", "thinking person", "celebrating" over specific Indonesian phrases

EXAMPLES:
Input (ID): "Realization: Harga naik/turun itu cuma gejala"
Analysis: This is an "aha moment" / realization / mind-blown situation
Search: "shocked realization face", "mind blown reaction", "lightbulb moment"

Input (ID): "Manusia Indonesia enggan bertanggung jawab"
Analysis: This is disappointment / frustration / facepalm situation
Search: "disappointed face", "frustrated person", "facepalm reaction"

Input (EN): "When you realize the meeting could have been an email"
Analysis: Exasperated / wasted time / facepalm
Search: "exasperated face", "waste of time reaction", "annoyed expression"

Return ONLY a JSON object:
{{
    "language_detected": "id|en",
    "emotional_context": "describe the emotion/situation in English",
    "image_type": "reaction|scene|photo",
    "mood": "one word universal emotion",
    "search_query": "universal English search (facial expression or body language)",
    "backup_queries": [
        "alternative universal search 1",
        "alternative universal search 2",
        "alternative universal search 3"
    ],
    "avoid_keywords": ["text", "caption", "words", "meme text"]
}}

Be VERY specific with facial expressions and body language."""

        try:
            response = self.ai_client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )

            # Parse JSON from response
            import json
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                logger.info(f"Language: {analysis.get('language_detected', 'unknown')}")
                logger.info(f"Emotional context: {analysis.get('emotional_context', 'N/A')}")
                return analysis

        except Exception as e:
            logger.warning(f"AI analysis failed: {e}")

        # Fallback: basic emotional keywords for common situations
        return {
            "language_detected": "id" if is_indonesian else "en",
            "emotional_context": "neutral situation",
            "image_type": "reaction",
            "mood": "neutral",
            "search_query": "neutral face expression",
            "backup_queries": ["thinking person", "contemplating face", "serious expression"],
            "avoid_keywords": ["text", "caption"]
        }

    def analyze_news_for_visuals(self, text: str, topic: str = None) -> Dict:
        """
        AI analysis for NEWS content - extracts entities and creates search queries.

        Different from emotional analysis:
        - Extracts people, places, organizations, events
        - Searches for news photos (not reactions)
        - Focuses on factual visual representation
        """
        is_indonesian = self._detect_indonesian(text)

        prompt = f"""You are a professional news photo researcher who finds relevant images for news stories.

TEXT: "{text}"
TOPIC: {topic or "general news"}
LANGUAGE: {"Indonesian" if is_indonesian else "English"}

YOUR JOB:
1. Extract KEY ENTITIES from the news text (people, places, events, organizations)
2. Determine what NEWS PHOTO would best illustrate this story
3. Create search queries for PROFESSIONAL NEWS IMAGES (not reactions or memes)

IMPORTANT RULES:
- Extract PROPER NAMES of people, places, organizations
- Focus on the MAIN SUBJECT of the news
- Search for REAL PHOTOS of the event/person/location
- Use English search terms even if text is Indonesian
- Prefer specific names over generic terms

EXAMPLES:

Input (EN): "Venezuela president Nicolas Maduro announces new economic policy"
Entities: Nicolas Maduro, Venezuela, economic policy
Image type: Political leader speaking
Search: "Nicolas Maduro Venezuela president", "Maduro announcement", "Venezuela government"

Input (ID): "Presiden Jokowi bertemu dengan PM India membahas kerjasama ekonomi"
Entities: Jokowi, Prime Minister of India, Indonesia-India relations
Image type: Diplomatic meeting
Search: "Jokowi India PM meeting", "Indonesia India summit", "Jokowi bilateral"

Input (EN): "Breaking: Major earthquake hits Turkey, hundreds affected"
Entities: Turkey, earthquake, disaster
Image type: Natural disaster scene
Search: "Turkey earthquake", "Turkey disaster scene", "earthquake damage Turkey"

Input (ID): "Bank Indonesia naikkan suku bunga untuk tekan inflasi"
Entities: Bank Indonesia, interest rate, inflation
Image type: Economic/financial visual
Search: "Bank Indonesia", "BI building Jakarta", "Indonesia central bank"

Return ONLY a JSON object:
{{
    "content_type": "news",
    "language_detected": "id|en",
    "entities": {{
        "people": ["person names"],
        "places": ["location names"],
        "organizations": ["org names"],
        "events": ["event description"]
    }},
    "main_subject": "who or what this news is primarily about",
    "image_type": "political|economic|disaster|diplomatic|general_news",
    "search_query": "primary search with proper names",
    "backup_queries": [
        "alternative with different entity focus",
        "broader search if primary fails",
        "generic fallback search"
    ],
    "avoid_keywords": ["meme", "cartoon", "illustration", "drawing"]
}}

Be VERY specific with proper names and locations."""

        try:
            response = self.ai_client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.5  # Lower temp for factual extraction
            )

            # Parse JSON
            import json
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                logger.info(f"Content type: NEWS")
                logger.info(f"Main subject: {analysis.get('main_subject', 'N/A')}")
                logger.info(f"Entities: {analysis.get('entities', {})}")
                return analysis

        except Exception as e:
            logger.warning(f"News analysis failed: {e}")

        # Fallback
        return {
            "content_type": "news",
            "language_detected": "id" if is_indonesian else "en",
            "entities": {},
            "main_subject": "general news",
            "image_type": "general_news",
            "search_query": f"{text[:50]} news photo",
            "backup_queries": ["breaking news photo", "news event photo"],
            "avoid_keywords": ["meme", "cartoon"]
        }

    def analyze_entertainment_for_visuals(self, text: str, topic: str = None, content_type: str = "cartoon_scene") -> Dict:
        """
        AI analysis for ENTERTAINMENT content - PROFESSIONAL QUALITY.

        Optimized for @theeconomicinfluence.id style:
        - Spongebob, Simpsons, popular cartoon scenes
        - Movie/TV screenshots (no meme text overlays)
        - Situation-matching (not just emotion)
        """
        is_indonesian = self._detect_indonesian(text)

        # PROFESSIONAL CARTOON SCENE MODE (default for Indonesian content creators)
        if content_type == "cartoon_scene":
            content_instruction = """
YOUR JOB: Analyze the text and intelligently find the BEST cartoon/movie/anime scene that matches.

YOU ARE FREE TO CHOOSE ANY:
- Cartoon show (Spongebob, Simpsons, Family Guy, South Park, Adventure Time, Regular Show, etc.)
- Anime (any popular anime that fits)
- Movie scene (any iconic movie)
- Meme format (Pepe, Wojak, Doge, This is Fine, etc.)
- Character (ANY character from ANY show/movie)

CRITICAL THINKING REQUIRED:
1. What is the EXACT situation/emotion in this text?
2. What cartoon/movie character or scene PERFECTLY represents this?
3. Think creatively - don't limit yourself to common choices
4. Vary your choices - avoid repeating same show/character

SEARCH QUERY FORMAT:
- "[character name] [show/movie] [specific action/emotion] scene screenshot"
- Be VERY specific about the action or emotion
- Add "scene screenshot" to avoid meme templates with text

EXAMPLES OF GOOD SEARCH QUERIES:
- "Patrick Star sleeping under rock lazy Spongebob scene screenshot"
- "Squidward Tentacles depressed alone window Spongebob scene screenshot"
- "Homer Simpson eating donuts lazy couch scene screenshot"
- "Pepe frog crying sad meme original scene"
- "Gojo Satoru confident smiling Jujutsu Kaisen scene screenshot"
- "This is fine dog fire burning comic scene"
- "Rick Sanchez drunk existential Rick and Morty scene screenshot"

CRITICAL RULES:
1. Be SPECIFIC about the action/situation in search query
2. Use "scene screenshot" to get clean images
3. Think freely - ANY cartoon/anime/movie is valid
4. Prioritize relevance over familiarity"""

        elif content_type == "movie_scene":
            content_instruction = """
YOUR JOB: Find ANY iconic movie/TV scene that perfectly matches the situation.

YOU ARE FREE TO CHOOSE:
- ANY movie (classic, modern, international, etc.)
- ANY TV show scene
- ANY genre (drama, comedy, action, thriller, etc.)
- Think creatively - obscure films are valid if they match perfectly

SEARCH QUERY FORMAT:
- "[movie/show title] [character if known] [specific scene/action] screenshot"
- Be VERY specific about what's happening in the scene
- Add "scene screenshot" to avoid promotional posters

EXAMPLES:
- "Wolf of Wall Street Leonardo DiCaprio money throwing scene screenshot"
- "Joker stairs dance rain scene screenshot"
- "Parasite basement flooding chaos scene screenshot"
- "The Office Jim looking at camera awkward scene screenshot"
- "Fight Club Edward Norton insomnia mirror scene screenshot"

THINK FREELY: Choose based on RELEVANCE, not popularity!"""

        else:  # fallback to cartoon_scene
            content_instruction = """
FIND: Popular cartoon scenes matching the emotional context.
Default to Spongebob/Simpsons scenes - most recognizable and versatile.
SEARCH FORMAT: "[character] [show] [situation] scene" """

        prompt = f"""You are a PROFESSIONAL content curator for Indonesian Instagram carousels.
Your job: Find the PERFECT cartoon/movie scene for this slide content.

TEXT: "{text}"
TOPIC: {topic or "general"}
LANGUAGE: {"Indonesian" if is_indonesian else "English"}

{content_instruction}

ANALYZE THE TEXT:
1. What SITUATION is being described? (not just emotion)
2. What popular cartoon/movie scene shows this EXACT situation?
3. Create a search query with: [character] + [show/movie] + [situation] + "scene"

EXAMPLE ANALYSES (showing creativity and variety):

Example 1 - "orang yang kerja keras tapi ekonomi rapuh"
→ Situation: Working hard every day but still financially struggling
→ Perfect match: "Squidward Tentacles exhausted cashier Krusty Krab scene screenshot"
→ Why: Squidward embodies working hard with no reward

Example 2 - "tekanan sosial untuk terlihat sukses"
→ Situation: Social pressure to appear successful while hiding struggles
→ Perfect match: "Patrick Star fake mustache business Spongebob scene screenshot"
→ Why: Patrick pretending to be sophisticated/successful is iconic

Example 3 - "procrastination bener-bener ngerusak mental"
→ Situation: Procrastination destroying mental health
→ Perfect match: "Mordecai Rigby avoiding work Regular Show scene screenshot"
→ Why: They're the ultimate procrastinators (different from previous slides)

Example 4 - "anxiety overwhelm everything"
→ Situation: Anxiety taking over, feeling overwhelmed
→ Perfect match: "Chihiro crying anxious Spirited Away scene screenshot"
→ Why: Powerful depiction of anxiety in a beautiful anime scene

Example 5 - "dulu naif, sekarang burnout"
→ Situation: Used to be naive/hopeful, now burned out
→ Perfect match: "Bojack Horseman depressed couch drinking scene screenshot"
→ Why: Bojack perfectly shows the transition from hope to burnout

KEY INSIGHT: Think FREELY and choose the MOST FITTING scene regardless of show popularity!

Return ONLY a JSON object:
{{
    "situation": "describe the situation in the text",
    "emotion": "primary emotion (one word)",
    "best_character": "Spongebob/Homer/Squidward/etc",
    "best_show": "Spongebob/Simpsons/etc",
    "search_query": "[character] [show] [situation] scene screenshot",
    "backup_queries": [
        "alternative character same situation",
        "different show same emotion",
        "generic [emotion] cartoon scene"
    ]
}}"""

        try:
            response = self.ai_client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )

            import json
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                logger.info(f"Content match: {analysis.get('content_match', 'N/A')}")
                logger.info(f"Search: {analysis.get('search_query', 'N/A')}")
                return analysis

        except Exception as e:
            logger.warning(f"Entertainment analysis failed: {e}")

        # Fallback based on content type
        fallback_queries = {
            "movie_scene": ["iconic movie scene reaction", "famous film still emotion"],
            "meme_reaction": ["popular reaction meme", "viral meme template"],
            "cartoon": ["cartoon character reaction", "illustration emotion"]
        }

        return {
            "emotional_context": "general emotion",
            "content_match": f"generic {content_type.replace('_', ' ')}",
            "search_query": fallback_queries.get(content_type, ["reaction image"])[0],
            "backup_queries": fallback_queries.get(content_type, ["reaction image"]),
            "mood": "neutral"
        }

    def analyze_if_needs_infographic(self, text: str, topic: str = None) -> Dict:
        """
        AI decides if this slide needs an infographic/chart/graph/theory visual.

        Returns:
            - needs_visual: bool
            - visual_type: "chart", "graph", "diagram", "theory", "framework", "none"
            - reason: why it needs/doesn't need a visual
            - search_query: what to search for if needs visual
        """
        is_indonesian = self._detect_indonesian(text)

        prompt = f"""You are an expert content strategist deciding if this slide needs an EDUCATIONAL VISUAL (chart/graph/diagram/theory).

TEXT: "{text}"
TOPIC: {topic or "general"}
LANGUAGE: {"Indonesian" if is_indonesian else "English"}

RULES FOR WHEN TO ADD VISUALS:
✅ ADD VISUAL IF:
- Contains data, statistics, percentages, numbers that need visualization
- Explains a process, system, or framework (needs diagram)
- Compares multiple things (needs comparison chart)
- Shows trends, growth, change over time (needs graph)
- Explains a theory, model, or concept (needs theory diagram)
- Lists steps or stages (needs flowchart/infographic)

❌ SKIP VISUAL IF:
- Pure storytelling or personal narrative
- Emotional/motivational content
- Opinion or hot take without data
- Simple statement or quote
- Hook/intro slide (text-only stronger)
- Call-to-action slide (text-only stronger)

EXAMPLES:
✅ "Pasar kripto naik 300% dalam 5 tahun terakhir" → NEEDS chart/graph
✅ "Ada 3 tahap membangun bisnis: ideation, validation, scaling" → NEEDS framework diagram
✅ "Hukum supply & demand mengatur harga" → NEEDS theory diagram
❌ "Dulu gue miskin, sekarang sukses" → NO VISUAL (story)
❌ "Hot take: Hustle culture itu toxic" → NO VISUAL (opinion)
❌ "Save this carousel! Tag teman yang butuh ini" → NO VISUAL (CTA)

Return ONLY a JSON object:
{{
    "needs_visual": true/false,
    "visual_type": "chart" | "graph" | "diagram" | "theory" | "framework" | "infographic" | "none",
    "reason": "brief explanation why needs/doesn't need visual",
    "search_query": "specific search query for the visual (if needs_visual=true)",
    "backup_queries": ["alternative searches if needed"]
}}"""

        try:
            response = self.ai_client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3  # Lower temp for more consistent decision-making
            )

            import json
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                logger.info(f"Infographic decision: {analysis.get('needs_visual')} - {analysis.get('reason')}")
                return analysis

        except Exception as e:
            logger.warning(f"Infographic analysis failed: {e}")

        # Fallback: Skip visual by default (text-only safer)
        return {
            "needs_visual": False,
            "visual_type": "none",
            "reason": "Analysis failed, defaulting to text-only",
            "search_query": "",
            "backup_queries": []
        }

    def scrape_google_images(self, query: str, limit: int = 10) -> List[str]:
        """
        Scrape image URLs from Google Images.

        Note: This is for educational purposes. Respect robots.txt and rate limits.
        """
        image_urls = []

        try:
            # Google Images search URL
            search_url = f"https://www.google.com/search?q={quote(query)}&tbm=isch&hl=en"

            response = requests.get(search_url, headers=self._get_headers(), timeout=10)

            if response.status_code == 200:
                # Find image URLs in the HTML
                # Google Images embeds URLs in various formats
                patterns = [
                    r'"(https?://[^"]+\.(?:jpg|jpeg|png|gif|webp))"',
                    r'data-src="(https?://[^"]+)"',
                    r'src="(https?://[^"]+\.(?:jpg|jpeg|png|gif|webp))"'
                ]

                for pattern in patterns:
                    urls = re.findall(pattern, response.text)
                    image_urls.extend(urls)

                # Remove duplicates and filter valid URLs
                seen = set()
                valid_urls = []
                for url in image_urls:
                    if url not in seen and self._is_valid_image_url(url):
                        seen.add(url)
                        valid_urls.append(url)
                        if len(valid_urls) >= limit:
                            break

                return valid_urls[:limit]

        except Exception as e:
            logger.error(f"Google Images scraping failed: {e}")

        return []

    def scrape_bing_images(self, query: str, limit: int = 10) -> List[str]:
        """Scrape image URLs from Bing Images (often easier than Google)."""
        image_urls = []

        try:
            search_url = f"https://www.bing.com/images/search?q={quote(query)}&first=1"

            response = requests.get(search_url, headers=self._get_headers(), timeout=10)

            if response.status_code == 200:
                # Bing stores image URLs in data-src attributes
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all image tags
                for img in soup.find_all('img', class_='mimg'):
                    src = img.get('src') or img.get('data-src')
                    if src and self._is_valid_image_url(src):
                        image_urls.append(src)
                        if len(image_urls) >= limit:
                            break

                # Also check for links with image data
                for link in soup.find_all('a', class_='iusc'):
                    m = link.get('m')
                    if m:
                        try:
                            import json
                            data = json.loads(m)
                            if 'murl' in data:
                                image_urls.append(data['murl'])
                                if len(image_urls) >= limit:
                                    break
                        except:
                            pass

                return image_urls[:limit]

        except Exception as e:
            logger.error(f"Bing Images scraping failed: {e}")

        return []

    def scrape_imgur_search(self, query: str, limit: int = 5) -> List[str]:
        """Scrape images from Imgur (good for memes and reactions)."""
        image_urls = []

        try:
            search_url = f"https://imgur.com/search?q={quote(query)}"

            response = requests.get(search_url, headers=self._get_headers(), timeout=10)

            if response.status_code == 200:
                # Imgur image pattern
                pattern = r'//i\.imgur\.com/([a-zA-Z0-9]+)\.(?:jpg|png|gif)'
                matches = re.findall(pattern, response.text)

                for match in matches:
                    url = f"https://i.imgur.com/{match}.jpg"
                    image_urls.append(url)
                    if len(image_urls) >= limit:
                        break

                return image_urls

        except Exception as e:
            logger.error(f"Imgur scraping failed: {e}")

        return []

    def scrape_reuters_images(self, query: str, limit: int = 5) -> List[str]:
        """
        Scrape Reuters image search.

        Reuters has high-quality news photos but may be harder to scrape.
        We'll try their public search and fall back to Google Images site:reuters.com
        """
        image_urls = []

        try:
            # Option 1: Try Reuters Pictures search
            search_url = f"https://www.reuters.com/search/news?blob={quote(query)}"

            response = requests.get(search_url, headers=self._get_headers(), timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find image elements (Reuters-specific selectors)
                for img in soup.find_all('img', limit=limit * 2):
                    src = img.get('src') or img.get('data-src')
                    if src and 'cloudfront' in src:  # Reuters uses CloudFront CDN
                        if not src.startswith('http'):
                            src = urljoin('https://www.reuters.com', src)
                        image_urls.append(src)
                        if len(image_urls) >= limit:
                            break

            # Option 2: Fallback to Google Images site:reuters.com
            if len(image_urls) < limit:
                site_query = f"site:reuters.com {query}"
                google_results = self.scrape_google_images(site_query, limit=limit)
                image_urls.extend(google_results)

        except Exception as e:
            logger.warning(f"Reuters scraping failed: {e}")

        logger.info(f"Found {len(image_urls)} Reuters images for '{query}'")
        return image_urls[:limit]

    def scrape_ap_images(self, query: str, limit: int = 5) -> List[str]:
        """
        Scrape AP News image search.

        Similar approach to Reuters - try direct search then fallback.
        """
        image_urls = []

        try:
            # Use Google Images site:apnews.com
            site_query = f"site:apnews.com {query}"
            google_results = self.scrape_google_images(site_query, limit=limit)
            image_urls.extend(google_results)

        except Exception as e:
            logger.warning(f"AP News scraping failed: {e}")

        logger.info(f"Found {len(image_urls)} AP images for '{query}'")
        return image_urls[:limit]

    def scrape_getty_images(self, query: str, limit: int = 5) -> List[str]:
        """
        Scrape Getty Images search.

        Getty has watermarks but good quality news photos.
        Note: Getty images will have watermarks - user should be aware.
        """
        image_urls = []

        try:
            # Use Google Images site:gettyimages.com
            site_query = f"site:gettyimages.com {query}"
            google_results = self.scrape_google_images(site_query, limit=limit)
            image_urls.extend(google_results)

        except Exception as e:
            logger.warning(f"Getty scraping failed: {e}")

        logger.info(f"Found {len(image_urls)} Getty images for '{query}'")
        return image_urls[:limit]

    def _is_valid_image_url(self, url: str) -> bool:
        """Check if URL looks like a valid image URL."""
        if not url or not url.startswith('http'):
            return False

        # Skip base64, data URIs, and tiny images
        if 'data:' in url or 'base64' in url:
            return False

        # Skip google's own logos and icons
        if 'google' in url.lower() and any(x in url.lower() for x in ['logo', 'icon', 'gstatic']):
            return False

        # Must have image extension or be from known image host
        image_hosts = ['imgur.com', 'i.redd.it', 'media.giphy.com', 'tenor.com']
        has_extension = any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
        is_image_host = any(host in url.lower() for host in image_hosts)

        return has_extension or is_image_host

    def download_image(self, url: str) -> Optional[str]:
        """Download image and save to cache."""
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=15, stream=True)

            if response.status_code == 200:
                # Generate cache filename
                url_hash = hashlib.md5(url.encode()).hexdigest()
                ext = '.jpg'
                for e in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    if e in url.lower():
                        ext = e
                        break

                cache_path = self.cache_dir / f"{url_hash}{ext}"

                # Save image
                with open(cache_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Verify it's a valid image
                try:
                    img = Image.open(cache_path)
                    img.verify()

                    # Check minimum size (avoid tiny images)
                    img = Image.open(cache_path)
                    if img.width >= 200 and img.height >= 200:
                        return str(cache_path)
                    else:
                        cache_path.unlink()  # Delete tiny image

                except Exception as e:
                    logger.warning(f"Invalid image file: {e}")
                    if cache_path.exists():
                        cache_path.unlink()

        except Exception as e:
            logger.warning(f"Failed to download {url}: {e}")

        return None

    def _has_text_overlay(self, image_path: str) -> bool:
        """
        Check if image has text overlay using OCR.

        Returns True if text detected (should be rejected).
        """
        try:
            import pytesseract  # OCR library

            img = Image.open(image_path)

            # Run OCR to detect text
            text = pytesseract.image_to_string(img)

            # If more than 10 characters detected, likely has text overlay
            if len(text.strip()) > 10:
                logger.info(f"Image has text overlay: {text[:50]}...")
                return True

            return False

        except ImportError:
            # Fallback: No OCR available, can't detect text
            logger.debug("pytesseract not installed - cannot detect text overlays")
            return False
        except Exception as e:
            logger.warning(f"Text detection failed: {e}")
            return False

    def _score_image_relevance(
        self,
        image_path: str,
        expected_emotion: str,
        expected_context: str
    ) -> float:
        """
        Score image relevance using basic heuristics (0-10).

        Returns relevance score where:
        - 0-3: Not relevant
        - 4-6: Somewhat relevant
        - 7-8: Good match
        - 9-10: Perfect match
        """
        try:
            img = Image.open(image_path)

            # Basic heuristics (can be enhanced with AI vision later)
            score = 5.0  # Default neutral score

            # Prefer images with certain aspect ratios (portrait or square for faces)
            aspect_ratio = img.width / img.height
            if 0.7 <= aspect_ratio <= 1.3:
                score += 1.5  # Square-ish images often have faces

            # Prefer certain size ranges (not too small, not too large)
            if 400 <= img.width <= 1200 and 400 <= img.height <= 1200:
                score += 1.0

            # Bonus for good resolution (likely professional/high quality)
            if img.width >= 600 and img.height >= 600:
                score += 0.5

            return min(10.0, score)

        except Exception as e:
            logger.warning(f"Image scoring failed: {e}")
            return 5.0  # Neutral score on error

    def find_image_for_content(
        self,
        text: str,
        topic: str = None,
        max_results: int = 10,
        min_relevance_score: float = 5.5,
        content_type: str = None  # NEW: Allow explicit override
    ) -> Optional[ImageResult]:
        """
        Enhanced image finding for both emotional and news content.

        Automatically detects content type and uses appropriate search strategy.
        """
        # Step 1: Detect content type if not specified
        if not content_type:
            content_type = self._detect_content_type(text, topic)

        # BLEND MODE: AI intelligently decides the best visual type for this specific content
        if content_type == "blend":
            # Use cartoon_scene as default - AI will freely choose any cartoon/movie/anime/meme
            # The AI prompt already allows complete freedom, so this is the most flexible option
            content_type = "cartoon_scene"
            logger.info(f"Blend mode: AI will intelligently choose the best visual type")

        # SMART INFOGRAPHIC MODE: AI decides if this slide needs a chart/graph/theory visual
        if content_type == "smart_infographic":
            needs_infographic = self.analyze_if_needs_infographic(text, topic)
            if not needs_infographic['needs_visual']:
                logger.info(f"Smart mode: Skipping visual for this slide - {needs_infographic['reason']}")
                return None
            # Switch to infographic content type
            content_type = "infographic"
            logger.info(f"Smart mode: Adding {needs_infographic['visual_type']} - {needs_infographic['reason']}")

        logger.info(f"Content type: {content_type.upper()}")

        # Step 2: Route to appropriate analysis method based on content type
        if content_type == "news":
            analysis = self.analyze_news_for_visuals(text, topic)
        elif content_type == "infographic":
            # INFOGRAPHIC: Use the analysis from analyze_if_needs_infographic
            analysis = needs_infographic  # Already analyzed above
        elif content_type in ["movie_scene", "meme_reaction", "cartoon", "cartoon_scene"]:
            # NEW: Specialized analysis for entertainment content (cartoon_scene is the default)
            analysis = self.analyze_entertainment_for_visuals(text, topic, content_type)
        else:  # emotional/meme content (default)
            analysis = self.analyze_content_for_visuals(text, topic)

        logger.info(f"Search query: {analysis['search_query']}")

        # Step 3: Search multiple sources based on content type
        all_urls = []

        if content_type == "news":
            # NEWS SOURCES: Reuters, AP, Getty, then general
            reuters_urls = self.scrape_reuters_images(analysis['search_query'], limit=3)
            all_urls.extend([(url, 'reuters') for url in reuters_urls])

            ap_urls = self.scrape_ap_images(analysis['search_query'], limit=3)
            all_urls.extend([(url, 'ap') for url in ap_urls])

            getty_urls = self.scrape_getty_images(analysis['search_query'], limit=3)
            all_urls.extend([(url, 'getty') for url in getty_urls])

            # Fallback to general news search
            bing_urls = self.scrape_bing_images(f"{analysis['search_query']} news photo", limit=5)
            all_urls.extend([(url, 'bing') for url in bing_urls])

        elif content_type == "cartoon_scene":
            # PROFESSIONAL CARTOON SCENE SOURCES
            # Priority: Clean cartoon screenshots from popular shows
            search_query = analysis.get('search_query', '')

            # 1. Bing Images - usually best for cartoon screenshots
            bing_urls = self.scrape_bing_images(f"{search_query}", limit=max_results)
            all_urls.extend([(url, 'bing') for url in bing_urls])

            # 2. Google Images with specific filters
            google_urls = self.scrape_google_images(f"{search_query} -meme -template", limit=max_results)
            all_urls.extend([(url, 'google') for url in google_urls])

            # 3. Try backup queries if character-specific
            for backup in analysis.get('backup_queries', [])[:2]:
                backup_urls = self.scrape_bing_images(backup, limit=5)
                all_urls.extend([(url, 'bing_backup') for url in backup_urls])

            logger.info(f"Cartoon scene search: {search_query}")

        elif content_type == "movie_scene":
            # MOVIE/TV SOURCES: Search for iconic scenes
            bing_urls = self.scrape_bing_images(f"{analysis['search_query']} scene screenshot -meme", limit=max_results)
            all_urls.extend([(url, 'bing') for url in bing_urls])

            google_urls = self.scrape_google_images(f"{analysis['search_query']} film scene screenshot", limit=max_results)
            all_urls.extend([(url, 'google') for url in google_urls])

        elif content_type == "meme_reaction":
            # MEME/REACTION SOURCES: Search for popular memes
            bing_urls = self.scrape_bing_images(f"{analysis['search_query']} meme reaction", limit=max_results)
            all_urls.extend([(url, 'bing') for url in bing_urls])

            google_urls = self.scrape_google_images(f"{analysis['search_query']} reaction meme", limit=max_results)
            all_urls.extend([(url, 'google') for url in google_urls])

            # Also try imgur for memes
            imgur_urls = self.scrape_imgur_search(analysis['search_query'], limit=5)
            all_urls.extend([(url, 'imgur') for url in imgur_urls])

        elif content_type == "cartoon":
            # CARTOON/ILLUSTRATION SOURCES (legacy - use cartoon_scene instead)
            bing_urls = self.scrape_bing_images(f"{analysis['search_query']} cartoon scene", limit=max_results)
            all_urls.extend([(url, 'bing') for url in bing_urls])

            google_urls = self.scrape_google_images(f"{analysis['search_query']} animated scene", limit=max_results)
            all_urls.extend([(url, 'google') for url in google_urls])

        elif content_type == "infographic":
            # INFOGRAPHIC/EDUCATIONAL SOURCES: Search for charts, graphs, diagrams, theory visuals
            visual_type = analysis.get('visual_type', 'infographic')

            # Add specific keywords based on visual type
            search_suffixes = {
                "chart": "chart diagram infographic",
                "graph": "graph data visualization",
                "diagram": "diagram flowchart illustration",
                "theory": "theory framework diagram",
                "framework": "framework model infographic",
                "infographic": "infographic visual explanation"
            }
            suffix = search_suffixes.get(visual_type, "infographic diagram")

            # Primary search: General infographics and educational visuals
            bing_urls = self.scrape_bing_images(f"{analysis['search_query']} {suffix}", limit=max_results)
            all_urls.extend([(url, 'bing') for url in bing_urls])

            google_urls = self.scrape_google_images(f"{analysis['search_query']} {suffix} educational", limit=max_results)
            all_urls.extend([(url, 'google') for url in google_urls])

            # Academic sources: Search for journal papers, dissertations, research visuals
            # These often have high-quality charts, graphs, and theory diagrams
            journal_urls = self.scrape_bing_images(f"{analysis['search_query']} journal paper figure", limit=5)
            all_urls.extend([(url, 'bing_academic') for url in journal_urls])

            # Research gate, academia.edu often have good academic visuals
            research_urls = self.scrape_google_images(f"{analysis['search_query']} research paper graph filetype:pdf", limit=5)
            all_urls.extend([(url, 'google_academic') for url in research_urls])

        else:
            # DEFAULT: EMOTIONAL SOURCES: Bing, Google (existing)
            bing_urls = self.scrape_bing_images(analysis['search_query'], limit=max_results)
            all_urls.extend([(url, 'bing') for url in bing_urls])

            google_urls = self.scrape_google_images(analysis['search_query'], limit=max_results)
            all_urls.extend([(url, 'google') for url in google_urls])

        # Try backup queries if not enough results
        if len(all_urls) < max_results:
            for backup_query in analysis.get('backup_queries', [])[:2]:
                if content_type == "news":
                    backup_urls = self.scrape_bing_images(f"{backup_query} news photo", limit=3)
                else:
                    backup_urls = self.scrape_bing_images(backup_query, limit=5)

                all_urls.extend([(url, 'backup') for url in backup_urls])

                if len(all_urls) >= max_results * 2:
                    break

        logger.info(f"Found {len(all_urls)} candidate URLs from {len(set(src for _, src in all_urls))} sources")

        # Step 3: Download, filter, and score images
        candidates = []

        for url, source in all_urls:
            local_path = self.download_image(url)
            if not local_path:
                continue

            # NEW: Check for text overlay
            if self._has_text_overlay(local_path):
                logger.info(f"Rejected (text overlay): {url[:60]}...")
                Path(local_path).unlink()  # Delete image
                continue

            # NEW: Score relevance
            score = self._score_image_relevance(
                local_path,
                expected_emotion=analysis.get('mood', analysis.get('main_subject', '')),
                expected_context=analysis.get('emotional_context', analysis.get('main_subject', ''))
            )

            logger.info(f"Image score: {score:.1f}/10")

            if score >= min_relevance_score:
                candidates.append({
                    'url': url,
                    'local_path': local_path,
                    'source': source,
                    'score': score
                })
                logger.info(f"✓ Added candidate (score: {score:.1f})")
            else:
                logger.info(f"Rejected (low score: {score:.1f})")
                Path(local_path).unlink()  # Delete low-score image

            # Rate limiting
            time.sleep(0.5)

            # Stop if we have enough good candidates
            if len(candidates) >= 3:
                break

        # Step 4: Return best candidate
        if candidates:
            # Sort by score, return highest
            best = max(candidates, key=lambda x: x['score'])

            logger.info(f"Selected best image (score: {best['score']:.1f}) from {best['source']}")

            return ImageResult(
                url=best['url'],
                local_path=best['local_path'],
                source=best['source'],
                relevance_score=best['score'],
                description=analysis['search_query'],
                image_type=analysis.get('image_type', 'photo')
            )

        logger.warning(f"No suitable images found for: {text[:50]}")
        return None

    def find_images_for_slides(
        self,
        slides: List[str],
        topic: str = None,
        skip_first_last: bool = True,
        content_type: str = None
    ) -> Dict[int, ImageResult]:
        """Find images for all slides in a carousel."""
        results = {}
        total_slides = len(slides)

        for i, slide_text in enumerate(slides, 1):
            # Skip first (hook) and last (CTA) slides if requested
            if skip_first_last and (i == 1 or i == total_slides):
                logger.info(f"Skipping slide {i} (hook/CTA)")
                continue

            logger.info(f"Finding image for slide {i}...")

            result = self.find_image_for_content(slide_text, topic, content_type=content_type)
            if result:
                results[i] = result
                logger.info(f"✓ Slide {i}: Found {result.image_type} from {result.source}")
            else:
                logger.warning(f"✗ Slide {i}: No suitable image found")

            # Rate limiting between requests
            time.sleep(1)

        return results

    def cleanup_cache(self, keep_recent: int = 100):
        """Clean up old cached images."""
        try:
            files = sorted(self.cache_dir.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)
            for file in files[keep_recent:]:
                file.unlink()
            logger.info(f"Cleaned up cache, kept {min(len(files), keep_recent)} recent files")
        except Exception as e:
            logger.warning(f"Cache cleanup failed: {e}")


# Convenience function
def find_smart_images_for_carousel(
    slides: List[str],
    topic: str = None
) -> Dict[int, str]:
    """
    Quick function to find images for carousel slides.

    Returns dict of {slide_number: local_image_path}
    """
    curator = SmartImageCurator()
    results = curator.find_images_for_slides(slides, topic)

    # Return just the paths
    return {num: result.local_path for num, result in results.items()}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Testing SmartImageCurator...")
    print("=" * 60)

    curator = SmartImageCurator()

    # Test single image search
    test_texts = [
        "When you realize the meeting could have been an email",
        "Trying to explain crypto to your parents",
        "Me pretending to understand the codebase on day 1"
    ]

    for text in test_texts:
        print(f"\nSearching for: {text[:50]}...")
        result = curator.find_image_for_content(text)
        if result:
            print(f"✓ Found: {result.source} - {result.description}")
            print(f"  Saved to: {result.local_path}")
        else:
            print("✗ No image found")

    print("\n" + "=" * 60)
    print("Done!")
