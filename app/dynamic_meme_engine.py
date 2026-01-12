"""
Dynamic Meme Engine - Intelligent Real-Time Meme Fetcher

This module provides a completely dynamic approach to meme selection:
1. Analyzes slide content for emotions, topics, and context
2. Generates intelligent search queries
3. Fetches fresh memes from internet APIs in real-time
4. Ranks and selects the best matching meme
5. Returns temporary image data - NO permanent storage

No local meme library needed. Always fresh, always relevant.
"""

import requests
import base64
import re
import io
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging

# Handle relative import for when running as module vs standalone
try:
    from .ai_client import get_ai_client
except ImportError:
    from ai_client import get_ai_client

logger = logging.getLogger(__name__)


# ============================================================================
# EMOTIONAL ANALYSIS FRAMEWORK
# ============================================================================

EMOTION_KEYWORDS = {
    "irony": ["padahal", "tapi", "ternyata", "meanwhile", "actually", "but", "however", "seharusnya"],
    "shock": ["kaget", "wtf", "gila", "parah", "shock", "surprised", "unexpected", "tiba-tiba"],
    "regret": ["nyesel", "menyesal", "seandainya", "kalau", "dulu", "should have", "wish", "mistake"],
    "triumph": ["berhasil", "sukses", "menang", "profit", "cuan", "win", "success", "nailed"],
    "pain": ["sakit", "rugi", "boncos", "loss", "gagal", "failed", "hurt", "suffer", "pain"],
    "confusion": ["bingung", "gimana", "kenapa", "confused", "why", "how", "what", "loh"],
    "escalation": ["makin", "semakin", "terus", "then", "next", "after", "worse", "better"],
    "comparison": ["vs", "banding", "atau", "pilih", "choose", "prefer", "better than", "worse than"],
    "denial": ["fine", "gapapa", "santai", "no problem", "it's okay", "cope", "copium"],
    "waiting": ["nunggu", "tunggu", "kapan", "when", "waiting", "still", "belum"],
    "realization": ["sadar", "ternyata", "oh", "realize", "turns out", "actually", "baru tau"],
    "sarcasm": ["ya gitu", "emang", "pasti", "sure", "totally", "definitely", "of course"],
}

TOPIC_IDENTIFIERS = {
    "finance": ["saham", "crypto", "trading", "invest", "portfolio", "stock", "bitcoin", "profit", "loss", "market"],
    "work": ["kerja", "kantor", "bos", "meeting", "deadline", "project", "office", "boss", "client"],
    "relationship": ["pacar", "gebetan", "jomblo", "crush", "single", "dating", "love", "couple"],
    "education": ["belajar", "kuliah", "ujian", "skripsi", "exam", "study", "school", "university"],
    "life": ["hidup", "dewasa", "adult", "life", "growing up", "reality", "dream"],
    "tech": ["coding", "bug", "deploy", "server", "code", "programming", "tech", "app"],
    "food": ["makan", "lapar", "food", "hungry", "diet", "eat"],
    "gaming": ["game", "main", "rank", "noob", "pro", "gaming", "play"],
}

# Meme format to emotion/context mapping for search query generation
MEME_FORMAT_CONTEXTS = {
    "drake": {
        "emotions": ["comparison", "irony", "sarcasm"],
        "search_terms": ["drake meme", "drake hotline bling", "drake yes no"],
        "use_when": "comparing two options, showing preference"
    },
    "pikachu": {
        "emotions": ["shock", "irony", "realization"],
        "search_terms": ["surprised pikachu", "shocked pikachu face"],
        "use_when": "obvious outcome that shouldn't be surprising"
    },
    "galaxy_brain": {
        "emotions": ["escalation", "triumph", "sarcasm"],
        "search_terms": ["expanding brain", "galaxy brain", "brain levels"],
        "use_when": "escalating ideas from simple to complex/absurd"
    },
    "clown": {
        "emotions": ["regret", "escalation", "irony"],
        "search_terms": ["clown makeup", "clown applying makeup"],
        "use_when": "progressively making bad decisions"
    },
    "distracted": {
        "emotions": ["comparison", "irony", "regret"],
        "search_terms": ["distracted boyfriend", "guy looking back"],
        "use_when": "choosing wrong option over right one"
    },
    "this_is_fine": {
        "emotions": ["denial", "pain", "irony"],
        "search_terms": ["this is fine", "dog fire meme", "everything fine fire"],
        "use_when": "pretending everything is okay when it's not"
    },
    "crying_cat": {
        "emotions": ["pain", "regret", "waiting"],
        "search_terms": ["crying cat", "sad cat", "cat crying thumbs up"],
        "use_when": "hiding pain behind fake smile"
    },
    "stonks": {
        "emotions": ["triumph", "sarcasm", "irony"],
        "search_terms": ["stonks meme", "meme man stonks"],
        "use_when": "fake financial wisdom or ironic profit"
    },
    "monkey_look": {
        "emotions": ["confusion", "shock", "realization"],
        "search_terms": ["monkey puppet", "awkward monkey", "monkey looking away"],
        "use_when": "awkward realization or avoiding eye contact"
    },
    "woman_cat": {
        "emotions": ["confusion", "comparison", "sarcasm"],
        "search_terms": ["woman yelling cat", "woman pointing cat"],
        "use_when": "two conflicting perspectives"
    },
    "gru_plan": {
        "emotions": ["escalation", "regret", "irony"],
        "search_terms": ["gru plan", "gru presentation"],
        "use_when": "plan that backfires at the end"
    },
    "two_buttons": {
        "emotions": ["comparison", "confusion"],
        "search_terms": ["two buttons meme", "sweating buttons"],
        "use_when": "difficult choice between options"
    },
    "waiting_skeleton": {
        "emotions": ["waiting", "pain"],
        "search_terms": ["waiting skeleton", "skeleton waiting"],
        "use_when": "waiting for something that takes forever"
    },
    "trade_offer": {
        "emotions": ["comparison", "sarcasm"],
        "search_terms": ["trade offer meme", "i receive you receive"],
        "use_when": "unfair exchange or trade"
    },
    "uno_reverse": {
        "emotions": ["triumph", "irony", "shock"],
        "search_terms": ["uno reverse card", "no u"],
        "use_when": "turning the tables on someone"
    }
}


@dataclass
class ContentAnalysis:
    """Analysis result for a piece of content."""
    text: str
    primary_emotion: str
    secondary_emotions: List[str]
    topic: str
    intensity: float  # 0-1
    has_contrast: bool  # for comparison memes
    has_escalation: bool  # for brain/clown memes
    key_elements: List[str]  # extracted key phrases
    suggested_meme_formats: List[str]
    search_queries: List[str]


@dataclass
class FetchedMeme:
    """A meme fetched from the internet."""
    url: str
    image_data: bytes  # The actual image bytes
    temp_path: str  # Temporary file path
    source: str  # imgflip, giphy, etc.
    title: str
    relevance_score: float
    format_type: str  # drake, pikachu, etc.


class DynamicMemeEngine:
    """
    Intelligent engine that dynamically fetches memes from the internet
    based on content analysis. No local storage required.

    Improvements:
    - Pre-caches all 15 meme templates at startup (reliable fallback)
    - Validates all URLs work before using
    - Adds retry logic with exponential backoff
    - Better error handling and logging
    """

    def __init__(self):
        """Initialize the dynamic meme engine."""
        self.ai_client = get_ai_client()
        self.temp_dir = Path(tempfile.gettempdir()) / "meme_cache"
        self.temp_dir.mkdir(exist_ok=True)

        # API endpoints
        self.imgflip_api = "https://api.imgflip.com/get_memes"
        self.giphy_search = "https://api.giphy.com/v1/gifs/search"

        # Cache for session (cleared after use)
        self._session_cache = {}

        # Pre-cache all meme templates at startup
        self._template_cache = {}
        self._precache_meme_templates()

        logger.info("DynamicMemeEngine initialized")

    def _precache_meme_templates(self):
        """
        Pre-cache all 15 meme templates at startup.

        This ensures we ALWAYS have a reliable fallback, even if APIs fail.
        """
        logger.info("Pre-caching meme templates...")

        DIRECT_URLS = {
            "drake": "https://i.imgflip.com/30b1gx.jpg",
            "pikachu": "https://imgflip.com/s/meme/Surprised-Pikachu.jpg",
            "galaxy_brain": "https://i.imgflip.com/2h7h1d.jpg",
            "clown": "https://i.imgflip.com/38el31.jpg",
            "distracted": "https://i.imgflip.com/1ur9b0.jpg",
            "this_is_fine": "https://i.imgflip.com/26am.jpg",
            "crying_cat": "https://i.imgflip.com/2hgfw.jpg",
            "stonks": "https://i.imgflip.com/3lmzyx.jpg",
            "monkey_look": "https://i.imgflip.com/1ihzfe.jpg",
            "woman_cat": "https://i.imgflip.com/345v97.jpg",
            "gru_plan": "https://i.imgflip.com/26jxvz.jpg",
            "two_buttons": "https://i.imgflip.com/1g8my4.jpg",
            "waiting_skeleton": "https://i.imgflip.com/2fm6x.jpg",
            "trade_offer": "https://i.imgflip.com/54hjww.jpg",
            "uno_reverse": "https://i.imgflip.com/3lmzyx.jpg",
        }

        for fmt, url in DIRECT_URLS.items():
            try:
                # Try to download and validate
                response = requests.get(
                    url,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )

                if response.status_code == 200:
                    # Validate it's actually an image
                    try:
                        from PIL import Image
                        img = Image.open(io.BytesIO(response.content))
                        img.verify()

                        # Cache it
                        cache_key = f"cached_{fmt}.jpg"
                        cache_path = self.temp_dir / cache_key
                        cache_path.write_bytes(response.content)

                        self._template_cache[fmt] = str(cache_path)
                        logger.debug(f"✓ Cached {fmt}")
                    except Exception as e:
                        logger.warning(f"Invalid image for {fmt}: {e}")
                else:
                    logger.warning(f"Failed to fetch {fmt}: HTTP {response.status_code}")

            except Exception as e:
                logger.warning(f"Pre-cache failed for {fmt}: {e}")

        logger.info(f"Pre-cached {len(self._template_cache)}/{len(DIRECT_URLS)} meme templates")

    def _is_url_valid(self, url: str, timeout: int = 5) -> bool:
        """
        Check if a URL is accessible and returns valid content.

        Returns: True if URL is valid and accessible
        """
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code == 200
        except:
            return False

    def _fetch_with_retry(self, url: str, max_retries: int = 3) -> Optional[bytes]:
        """
        Fetch URL with retry logic and exponential backoff.

        Args:
            url: URL to fetch
            max_retries: Maximum number of retries

        Returns:
            Response content or None if failed
        """
        import time

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )

                if response.status_code == 200:
                    return response.content

                logger.warning(f"Attempt {attempt + 1}: HTTP {response.status_code}")

            except requests.Timeout:
                logger.warning(f"Attempt {attempt + 1}: Timeout")
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}: {e}")

            # Exponential backoff: 0.5s, 1s, 2s
            if attempt < max_retries - 1:
                wait_time = 0.5 * (2 ** attempt)
                time.sleep(wait_time)

        return None

    def analyze_content(self, text: str, topic_hint: str = None) -> ContentAnalysis:
        """
        Deeply analyze content to understand emotions, context, and meme potential.

        Args:
            text: The slide text to analyze
            topic_hint: Optional topic hint (e.g., "trading", "finance")

        Returns:
            ContentAnalysis object with detailed breakdown
        """
        text_lower = text.lower()

        # Detect emotions
        emotion_scores = {}
        for emotion, keywords in EMOTION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                emotion_scores[emotion] = score

        # Sort by score
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        primary_emotion = sorted_emotions[0][0] if sorted_emotions else "general"
        secondary_emotions = [e[0] for e in sorted_emotions[1:4]]

        # Detect topic
        topic_scores = {}
        for topic, keywords in TOPIC_IDENTIFIERS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                topic_scores[topic] = score

        topic = topic_hint or (max(topic_scores, key=topic_scores.get) if topic_scores else "general")

        # Detect structural elements
        has_contrast = any(word in text_lower for word in ["vs", "tapi", "but", "padahal", "bukan", "beda"])
        has_escalation = any(word in text_lower for word in ["makin", "terus", "step", "level", "stage", "1.", "2.", "3."])

        # Calculate intensity (0-1)
        intensity_markers = ["!", "parah", "gila", "banget", "sangat", "very", "really", "seriously"]
        intensity = min(1.0, sum(0.15 for m in intensity_markers if m in text_lower))

        # Extract key elements (numbers, specific terms)
        key_elements = re.findall(r'\d+%|\d+[kK]|\$\d+|\d+\s*(?:juta|ribu|rb)', text)
        key_elements.extend(re.findall(r'(?:profit|loss|rugi|cuan|boncos)', text_lower))

        # Suggest meme formats based on analysis
        suggested_formats = self._suggest_meme_formats(
            primary_emotion, secondary_emotions, has_contrast, has_escalation, topic
        )

        # Generate search queries
        search_queries = self._generate_search_queries(
            suggested_formats, topic, primary_emotion, key_elements
        )

        return ContentAnalysis(
            text=text,
            primary_emotion=primary_emotion,
            secondary_emotions=secondary_emotions,
            topic=topic,
            intensity=intensity,
            has_contrast=has_contrast,
            has_escalation=has_escalation,
            key_elements=key_elements,
            suggested_meme_formats=suggested_formats,
            search_queries=search_queries
        )

    def _suggest_meme_formats(
        self,
        primary_emotion: str,
        secondary_emotions: List[str],
        has_contrast: bool,
        has_escalation: bool,
        topic: str
    ) -> List[str]:
        """Suggest meme formats based on analysis."""
        suggestions = []
        all_emotions = [primary_emotion] + secondary_emotions

        for fmt, info in MEME_FORMAT_CONTEXTS.items():
            # Check emotion match
            emotion_match = sum(1 for e in all_emotions if e in info["emotions"])
            if emotion_match > 0:
                suggestions.append((fmt, emotion_match))

        # Boost scores for structural matches
        boosted = []
        for fmt, score in suggestions:
            if has_contrast and fmt in ["drake", "distracted", "two_buttons", "woman_cat"]:
                score += 2
            if has_escalation and fmt in ["galaxy_brain", "clown", "gru_plan"]:
                score += 2
            if topic == "finance" and fmt in ["stonks", "this_is_fine", "crying_cat"]:
                score += 1
            boosted.append((fmt, score))

        # Sort by score and return top 3
        boosted.sort(key=lambda x: x[1], reverse=True)
        return [fmt for fmt, _ in boosted[:3]]

    def _generate_search_queries(
        self,
        suggested_formats: List[str],
        topic: str,
        emotion: str,
        key_elements: List[str]
    ) -> List[str]:
        """Generate intelligent search queries for meme APIs."""
        queries = []

        # Add format-specific queries
        for fmt in suggested_formats:
            if fmt in MEME_FORMAT_CONTEXTS:
                queries.extend(MEME_FORMAT_CONTEXTS[fmt]["search_terms"])

        # Add topic-specific queries
        topic_meme_terms = {
            "finance": ["stonks meme", "trading meme", "when you invest", "profit loss meme"],
            "work": ["office meme", "work meme", "boss meme", "deadline meme"],
            "relationship": ["relationship meme", "dating meme", "couple meme"],
            "life": ["life meme", "adulting meme", "reality meme"],
            "tech": ["programmer meme", "coding meme", "debug meme"],
        }
        if topic in topic_meme_terms:
            queries.extend(topic_meme_terms[topic][:2])

        # Add emotion-based generic queries
        emotion_queries = {
            "irony": ["ironic meme", "expectation vs reality"],
            "shock": ["shocked meme", "surprised meme"],
            "regret": ["regret meme", "mistakes were made"],
            "pain": ["pain meme", "suffering meme"],
            "triumph": ["success meme", "winning meme"],
        }
        if emotion in emotion_queries:
            queries.extend(emotion_queries[emotion])

        # Remove duplicates while preserving order
        seen = set()
        unique_queries = []
        for q in queries:
            if q not in seen:
                seen.add(q)
                unique_queries.append(q)

        return unique_queries[:5]  # Top 5 queries

    async def fetch_meme_from_imgflip(self, format_type: str) -> Optional[FetchedMeme]:
        """
        Fetch a meme template from Imgflip API.

        Args:
            format_type: The meme format to fetch

        Returns:
            FetchedMeme object or None if failed
        """
        try:
            response = requests.get(self.imgflip_api, timeout=10)
            if response.status_code != 200:
                return None

            data = response.json()
            if not data.get("success"):
                return None

            memes = data.get("data", {}).get("memes", [])

            # Find matching meme
            format_search_terms = MEME_FORMAT_CONTEXTS.get(format_type, {}).get("search_terms", [])

            for meme in memes:
                meme_name = meme.get("name", "").lower()
                for term in format_search_terms:
                    if any(word in meme_name for word in term.lower().split()):
                        # Download the image
                        img_url = meme.get("url")
                        img_response = requests.get(img_url, timeout=10)
                        if img_response.status_code == 200:
                            # Save to temp file
                            temp_path = self.temp_dir / f"{meme.get('id')}.jpg"
                            temp_path.write_bytes(img_response.content)

                            return FetchedMeme(
                                url=img_url,
                                image_data=img_response.content,
                                temp_path=str(temp_path),
                                source="imgflip",
                                title=meme.get("name", ""),
                                relevance_score=0.8,
                                format_type=format_type
                            )

            return None

        except Exception as e:
            logger.error(f"Imgflip fetch error: {e}")
            return None

    def fetch_meme_sync(self, format_type: str, search_queries: List[str]) -> Optional[FetchedMeme]:
        """
        Synchronous method to fetch a meme from the internet.

        Improved flow:
        1. Try Imgflip API (fresh content)
        2. Try pre-cached template (reliable fallback)
        3. Return None only if both fail
        """
        # Try Imgflip first (most reliable for meme templates)
        meme = self._fetch_from_imgflip_sync(format_type, search_queries)
        if meme:
            logger.info(f"✓ Fetched {format_type} from Imgflip API")
            return meme

        # Fallback to pre-cached template (guaranteed to exist if precache succeeded)
        if format_type in self._template_cache:
            cached_path = self._template_cache[format_type]
            try:
                with open(cached_path, 'rb') as f:
                    image_data = f.read()

                return FetchedMeme(
                    url=f"cached://{format_type}",
                    image_data=image_data,
                    temp_path=cached_path,
                    source="precache",
                    title=format_type.replace("_", " ").title(),
                    relevance_score=0.7,  # Pre-cached templates are good quality
                    format_type=format_type
                )
            except Exception as e:
                logger.warning(f"Failed to use cached {format_type}: {e}")

        logger.warning(f"✗ No meme available for {format_type}")
        return None

    def _fetch_from_imgflip_sync(self, format_type: str, search_queries: List[str]) -> Optional[FetchedMeme]:
        """Synchronously fetch from Imgflip API."""
        try:
            response = requests.get(self.imgflip_api, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Imgflip API returned {response.status_code}")
                return None

            data = response.json()
            if not data.get("success"):
                return None

            memes = data.get("data", {}).get("memes", [])

            # Score each meme by relevance to queries
            scored_memes = []
            for meme in memes:
                meme_name = meme.get("name", "").lower()
                score = 0

                # Check against search queries
                for query in search_queries:
                    query_words = query.lower().split()
                    matches = sum(1 for word in query_words if word in meme_name)
                    score += matches

                # Check against format type
                format_terms = MEME_FORMAT_CONTEXTS.get(format_type, {}).get("search_terms", [])
                for term in format_terms:
                    if any(word in meme_name for word in term.lower().split()):
                        score += 3

                if score > 0:
                    scored_memes.append((meme, score))

            # Sort by score and get best match
            scored_memes.sort(key=lambda x: x[1], reverse=True)

            if not scored_memes:
                return None

            best_meme = scored_memes[0][0]
            img_url = best_meme.get("url")

            # Download the image
            img_response = requests.get(img_url, timeout=10)
            if img_response.status_code != 200:
                return None

            # Save to temp file
            temp_path = self.temp_dir / f"meme_{best_meme.get('id')}.jpg"
            temp_path.write_bytes(img_response.content)

            return FetchedMeme(
                url=img_url,
                image_data=img_response.content,
                temp_path=str(temp_path),
                source="imgflip",
                title=best_meme.get("name", ""),
                relevance_score=scored_memes[0][1] / 10.0,
                format_type=format_type
            )

        except Exception as e:
            logger.error(f"Imgflip sync fetch error: {e}")
            return None

    def _fetch_from_direct_urls(self, format_type: str) -> Optional[FetchedMeme]:
        """Fallback: Fetch from known direct URLs."""
        # Direct URLs for common meme templates (as fallback)
        DIRECT_URLS = {
            "drake": "https://i.imgflip.com/30b1gx.jpg",
            "pikachu": "https://imgflip.com/s/meme/Surprised-Pikachu.jpg",
            "galaxy_brain": "https://i.imgflip.com/2h7h1d.jpg",
            "clown": "https://i.imgflip.com/38el31.jpg",
            "distracted": "https://i.imgflip.com/1ur9b0.jpg",
            "this_is_fine": "https://i.imgflip.com/26am.jpg",
            "crying_cat": "https://i.imgflip.com/2hgfw.jpg",
            "stonks": "https://i.imgflip.com/3lmzyx.jpg",
            "monkey_look": "https://i.imgflip.com/1ihzfe.jpg",
            "woman_cat": "https://i.imgflip.com/345v97.jpg",
            "gru_plan": "https://i.imgflip.com/26jxvz.jpg",
            "two_buttons": "https://i.imgflip.com/1g8my4.jpg",
            "waiting_skeleton": "https://i.imgflip.com/2fm6x.jpg",
            "trade_offer": "https://i.imgflip.com/54hjww.jpg",
            "uno_reverse": "https://i.imgflip.com/3lmzyx.jpg",
        }

        url = DIRECT_URLS.get(format_type)
        if not url:
            return None

        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            if response.status_code != 200:
                return None

            # Save to temp file
            temp_path = self.temp_dir / f"direct_{format_type}.jpg"
            temp_path.write_bytes(response.content)

            return FetchedMeme(
                url=url,
                image_data=response.content,
                temp_path=str(temp_path),
                source="direct",
                title=format_type.replace("_", " ").title(),
                relevance_score=0.6,  # Lower score for fallback
                format_type=format_type
            )

        except Exception as e:
            logger.error(f"Direct URL fetch error for {format_type}: {e}")
            return None

    def get_meme_for_slide(
        self,
        slide_text: str,
        slide_number: int,
        total_slides: int,
        topic_hint: str = None
    ) -> Optional[FetchedMeme]:
        """
        Main method: Analyze slide content and fetch the best matching meme.

        Args:
            slide_text: The text content of the slide
            slide_number: Current slide number (1-indexed)
            total_slides: Total number of slides
            topic_hint: Optional topic hint

        Returns:
            FetchedMeme object with fresh meme data, or None
        """
        # Skip first and last slides (hook and CTA)
        if slide_number == 1 or slide_number == total_slides:
            logger.info(f"Skipping meme for slide {slide_number} (hook/CTA)")
            return None

        # Analyze content
        analysis = self.analyze_content(slide_text, topic_hint)
        logger.info(f"Slide {slide_number} analysis: emotion={analysis.primary_emotion}, "
                   f"topic={analysis.topic}, formats={analysis.suggested_meme_formats}")

        # Try to fetch meme for each suggested format
        for format_type in analysis.suggested_meme_formats:
            meme = self.fetch_meme_sync(format_type, analysis.search_queries)
            if meme:
                logger.info(f"Fetched {meme.format_type} meme from {meme.source}: {meme.title}")
                return meme

        # Fallback: try a random popular format
        fallback_formats = ["drake", "pikachu", "this_is_fine"]
        for fmt in fallback_formats:
            meme = self._fetch_from_direct_urls(fmt)
            if meme:
                logger.info(f"Used fallback meme: {fmt}")
                return meme

        return None

    def get_memes_for_slides(
        self,
        slides: List[str],
        topic_hint: str = None
    ) -> Dict[int, FetchedMeme]:
        """
        Get memes for all slides in a carousel.

        Args:
            slides: List of slide texts
            topic_hint: Optional topic hint

        Returns:
            Dict mapping slide numbers to FetchedMeme objects
        """
        memes = {}
        total_slides = len(slides)

        for i, slide_text in enumerate(slides, 1):
            meme = self.get_meme_for_slide(slide_text, i, total_slides, topic_hint)
            if meme:
                memes[i] = meme

        logger.info(f"Fetched {len(memes)} memes for {total_slides} slides")
        return memes

    def cleanup_temp_files(self):
        """Clean up temporary meme files after use."""
        try:
            for file in self.temp_dir.glob("*.jpg"):
                file.unlink()
            for file in self.temp_dir.glob("*.png"):
                file.unlink()
            logger.info("Cleaned up temporary meme files")
        except Exception as e:
            logger.warning(f"Error cleaning temp files: {e}")

    def use_ai_for_analysis(self, slide_text: str, topic: str = None) -> ContentAnalysis:
        """
        Use AI to deeply analyze content for meme matching.
        This provides more nuanced understanding than keyword matching.
        """
        prompt = f"""Analyze this slide text for meme matching. Return JSON only.

TEXT: "{slide_text}"
TOPIC CONTEXT: {topic or "general"}

Analyze and return:
{{
    "primary_emotion": "one of: irony, shock, regret, triumph, pain, confusion, escalation, comparison, denial, waiting, realization, sarcasm",
    "intensity": 0.0-1.0,
    "has_contrast": true/false (comparing two things?),
    "has_escalation": true/false (things getting better/worse?),
    "best_meme_formats": ["format1", "format2"] (from: drake, pikachu, galaxy_brain, clown, distracted, this_is_fine, crying_cat, stonks, monkey_look, woman_cat, gru_plan, two_buttons),
    "search_terms": ["query1", "query2"] (specific search terms for finding relevant memes)
}}

Be specific. Match the emotional beat of the content."""

        try:
            response = self.ai_client.generate(prompt, max_tokens=300)

            # Parse JSON from response
            import json
            # Find JSON in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())

                return ContentAnalysis(
                    text=slide_text,
                    primary_emotion=data.get("primary_emotion", "general"),
                    secondary_emotions=[],
                    topic=topic or "general",
                    intensity=data.get("intensity", 0.5),
                    has_contrast=data.get("has_contrast", False),
                    has_escalation=data.get("has_escalation", False),
                    key_elements=[],
                    suggested_meme_formats=data.get("best_meme_formats", ["drake", "pikachu"]),
                    search_queries=data.get("search_terms", ["meme", "funny"])
                )
        except Exception as e:
            logger.warning(f"AI analysis failed, using keyword analysis: {e}")

        # Fallback to keyword analysis
        return self.analyze_content(slide_text, topic)


# Convenience function for easy integration
def get_dynamic_memes_for_slides(
    slides: List[str],
    topic: str = None,
    use_ai_analysis: bool = False
) -> Dict[int, str]:
    """
    Get fresh memes for slides dynamically from the internet.

    Args:
        slides: List of slide texts
        topic: Optional topic hint
        use_ai_analysis: Use AI for deeper content analysis

    Returns:
        Dict mapping slide numbers to temporary meme file paths
    """
    engine = DynamicMemeEngine()

    try:
        memes = engine.get_memes_for_slides(slides, topic)

        # Return paths dict for compatibility with existing code
        return {num: meme.temp_path for num, meme in memes.items()}

    finally:
        # Note: Don't cleanup here - let slide generator use the files first
        pass


if __name__ == "__main__":
    # Test the engine
    logging.basicConfig(level=logging.INFO)

    print("Testing DynamicMemeEngine...")

    test_slides = [
        "Kenapa 90% trader pemula gagal?",
        "Padahal udah belajar, tapi tetep boncos. Ternyata masalahnya bukan di strategi.",
        "Step 1: Baca buku trading\nStep 2: Buka akun\nStep 3: YOLO semua ke shitcoin\nStep 4: *surprised pikachu*",
        "Yang penting konsisten. Profit kecil tapi rutin > FOMO setiap hari",
        "Follow untuk tips trading lainnya!"
    ]

    engine = DynamicMemeEngine()

    print("\nAnalyzing slides...")
    for i, slide in enumerate(test_slides, 1):
        analysis = engine.analyze_content(slide, "finance")
        print(f"\nSlide {i}:")
        print(f"  Text: {slide[:50]}...")
        print(f"  Emotion: {analysis.primary_emotion}")
        print(f"  Suggested formats: {analysis.suggested_meme_formats}")
        print(f"  Search queries: {analysis.search_queries}")

    print("\nFetching memes...")
    memes = engine.get_memes_for_slides(test_slides, "finance")

    print(f"\nFetched {len(memes)} memes:")
    for num, meme in memes.items():
        print(f"  Slide {num}: {meme.title} ({meme.source}) -> {meme.temp_path}")

    # Cleanup
    engine.cleanup_temp_files()
    print("\nDone!")
