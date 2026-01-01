"""
Image Search Module

Fetches contextual images from Pexels API for carousel slides.
Falls back to meme library when no API key or suitable images found.
"""

import os
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from PIL import Image
import io
import hashlib
from .config import Config


class ImageSearchAgent:
    """
    Searches for contextual images using Pexels API.
    Caches downloaded images to avoid repeated API calls.
    """

    PEXELS_API_URL = "https://api.pexels.com/v1/search"

    def __init__(self):
        """Initialize with API key from environment."""
        self.api_key = os.getenv("PEXELS_API_KEY", "")
        self.cache_dir = Config.OUTPUT_DIR / "image_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def is_available(self) -> bool:
        """Check if Pexels API is available."""
        return bool(self.api_key)

    def search_images(
        self,
        query: str,
        per_page: int = 5,
        orientation: str = "portrait"
    ) -> List[Dict[str, Any]]:
        """
        Search for images on Pexels.

        Args:
            query: Search query
            per_page: Number of results (1-80)
            orientation: "portrait", "landscape", or "square"

        Returns:
            List of image results with urls and metadata
        """
        if not self.api_key:
            return []

        headers = {"Authorization": self.api_key}
        params = {
            "query": query,
            "per_page": min(per_page, 15),
            "orientation": orientation,
        }

        try:
            response = requests.get(
                self.PEXELS_API_URL,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for photo in data.get("photos", []):
                results.append({
                    "id": photo["id"],
                    "url": photo["src"]["large2x"],  # High quality
                    "url_medium": photo["src"]["large"],
                    "url_small": photo["src"]["medium"],
                    "width": photo["width"],
                    "height": photo["height"],
                    "photographer": photo["photographer"],
                    "alt": photo.get("alt", query),
                })

            return results

        except Exception as e:
            print(f"Pexels API error: {e}")
            return []

    def download_image(
        self,
        url: str,
        save_path: Optional[Path] = None
    ) -> Optional[Image.Image]:
        """
        Download image from URL and return as PIL Image.

        Args:
            url: Image URL
            save_path: Optional path to save the image

        Returns:
            PIL Image or None if failed
        """
        # Check cache first
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_path = self.cache_dir / f"{url_hash}.jpg"

        if cache_path.exists():
            try:
                return Image.open(cache_path)
            except Exception:
                pass

        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            img = Image.open(io.BytesIO(response.content))

            # Cache the image
            img.save(cache_path, "JPEG", quality=90)

            # Also save to specified path if provided
            if save_path:
                img.save(save_path)

            return img

        except Exception as e:
            print(f"Image download error: {e}")
            return None

    def get_image_for_content(
        self,
        content: str,
        slide_type: str = "body",
        emotion: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get the best matching image for slide content.

        Args:
            content: Slide text content
            slide_type: "hook", "body", or "cta"
            emotion: Optional emotion hint (e.g., "frustrated", "success")

        Returns:
            Image info dict with PIL Image, or None
        """
        if not self.api_key:
            return None

        # Generate search query from content
        query = self._generate_search_query(content, emotion)

        if not query:
            return None

        # Search for images
        results = self.search_images(query, per_page=3, orientation="portrait")

        if not results:
            # Try with simpler query
            simple_query = self._simplify_query(query)
            results = self.search_images(simple_query, per_page=3)

        if results:
            # Get the first (best) result
            best = results[0]
            img = self.download_image(best["url_medium"])

            if img:
                return {
                    "image": img,
                    "source": "pexels",
                    "query": query,
                    "photographer": best.get("photographer", "Unknown"),
                    "url": best["url"],
                }

        return None

    def _generate_search_query(
        self,
        content: str,
        emotion: Optional[str] = None
    ) -> str:
        """Generate a good search query from content."""
        # Keywords that work well for stock photos
        keyword_map = {
            # Finance/Economics
            "uang": "money finance",
            "gaji": "salary paycheck",
            "investasi": "investment stock market",
            "inflasi": "inflation economy",
            "harga": "price shopping",
            "rumah": "house real estate",
            "kerja": "work office",
            "bisnis": "business meeting",
            "ekonomi": "economy finance",

            # Emotions/States
            "stress": "stressed person",
            "capek": "tired exhausted",
            "sedih": "sad person",
            "senang": "happy success",
            "marah": "angry frustrated",
            "bingung": "confused thinking",
            "sukses": "success celebration",
            "gagal": "failure disappointed",

            # Actions
            "belajar": "studying learning",
            "menulis": "writing typing",
            "mikir": "thinking idea",
            "tidur": "sleeping tired",
            "makan": "eating food",
            "jalan": "walking lifestyle",

            # Lifestyle
            "kopi": "coffee cafe",
            "traveling": "travel adventure",
            "fitness": "gym fitness",
            "hustle": "entrepreneur laptop",
        }

        content_lower = content.lower()

        # Find matching keywords
        matches = []
        for indo, eng in keyword_map.items():
            if indo in content_lower:
                matches.append(eng)

        # Add emotion if provided
        if emotion:
            emotion_queries = {
                "shocked": "surprised shocked",
                "frustrated": "frustrated stressed",
                "sad": "sad disappointed",
                "happy": "happy success",
                "angry": "angry upset",
                "confused": "confused thinking",
                "motivated": "motivated success",
                "tired": "tired exhausted",
            }
            if emotion.lower() in emotion_queries:
                matches.append(emotion_queries[emotion.lower()])

        if matches:
            return matches[0]  # Use first match

        # Default fallback queries based on common themes
        return ""

    def _simplify_query(self, query: str) -> str:
        """Simplify query to just the first word."""
        words = query.split()
        return words[0] if words else ""


class ContentImageMatcher:
    """
    Matches images to slide content using AI analysis.
    Combines meme library with stock photos.
    """

    def __init__(self, ai_client=None):
        """
        Initialize matcher.

        Args:
            ai_client: Optional AI client for content analysis
        """
        self.image_search = ImageSearchAgent()
        self.ai_client = ai_client

    def analyze_slide_for_image(
        self,
        slide_text: str,
        slide_num: int,
        total_slides: int
    ) -> Dict[str, Any]:
        """
        Analyze a slide and determine what kind of image would work.

        Args:
            slide_text: The slide content
            slide_num: Current slide number
            total_slides: Total number of slides

        Returns:
            Analysis with image recommendations
        """
        # Determine slide type
        if slide_num == 1:
            slide_type = "hook"
        elif slide_num == total_slides:
            slide_type = "cta"
        else:
            slide_type = "body"

        # Analyze emotional tone
        emotion = self._detect_emotion(slide_text)

        # Determine if image would enhance this slide
        needs_image = self._should_have_image(slide_text, slide_type, slide_num)

        # Generate image query
        query = ""
        if needs_image:
            query = self.image_search._generate_search_query(slide_text, emotion)

        return {
            "slide_num": slide_num,
            "slide_type": slide_type,
            "emotion": emotion,
            "needs_image": needs_image,
            "image_query": query,
            "recommended_position": "bottom" if slide_type == "hook" else "top",
        }

    def _detect_emotion(self, text: str) -> str:
        """Simple emotion detection from text."""
        text_lower = text.lower()

        emotions = {
            "shocked": ["shock", "kaget", "gila", "wtf", "what", "seriously"],
            "frustrated": ["kesel", "capek", "stuck", "susah", "ribet", "stress"],
            "sad": ["sedih", "nyesel", "gagal", "rugi", "lost"],
            "happy": ["senang", "happy", "sukses", "berhasil", "yes"],
            "angry": ["marah", "kesal", "benci", "bullshit"],
            "confused": ["bingung", "gimana", "kenapa", "why"],
            "motivated": ["semangat", "bisa", "ayo", "let's go"],
        }

        for emotion, keywords in emotions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return emotion

        return "neutral"

    def _should_have_image(
        self,
        text: str,
        slide_type: str,
        slide_num: int
    ) -> bool:
        """Determine if this slide should have an image."""
        # Hook slides often benefit from images
        if slide_type == "hook":
            return True

        # CTA slides usually don't need images
        if slide_type == "cta":
            return False

        # Body slides - alternate or based on content length
        # Shorter content = more room for image
        word_count = len(text.split())
        if word_count < 30:
            return True

        # Even-numbered slides get images for visual rhythm
        return slide_num % 2 == 0

    def get_images_for_slides(
        self,
        slides: List[str],
        meme_recommendations: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Get images for all slides, combining memes and stock photos.

        Args:
            slides: List of slide texts
            meme_recommendations: Optional meme matching results

        Returns:
            List of image assignments per slide
        """
        results = []
        total_slides = len(slides)

        # Get meme assignments if available
        meme_map = {}
        if meme_recommendations:
            for meme in meme_recommendations.get('available_memes', []):
                slide_num = meme.get('slide_num', 0)
                if slide_num:
                    meme_map[slide_num] = meme

        for i, slide_text in enumerate(slides):
            slide_num = i + 1

            # Check if we have a meme for this slide
            if slide_num in meme_map:
                meme = meme_map[slide_num]
                results.append({
                    "slide_num": slide_num,
                    "has_image": True,
                    "source": "meme",
                    "filename": meme.get("filename"),
                    "path": Config.MEME_IMAGES_DIR / meme.get("filename", ""),
                    "position": "bottom",
                })
                continue

            # Analyze slide for stock photo
            analysis = self.analyze_slide_for_image(slide_text, slide_num, total_slides)

            if analysis["needs_image"] and self.image_search.is_available():
                # Try to get stock photo
                image_result = self.image_search.get_image_for_content(
                    slide_text,
                    slide_type=analysis["slide_type"],
                    emotion=analysis["emotion"]
                )

                if image_result:
                    results.append({
                        "slide_num": slide_num,
                        "has_image": True,
                        "source": "pexels",
                        "image": image_result["image"],
                        "photographer": image_result["photographer"],
                        "position": analysis["recommended_position"],
                    })
                    continue

            # No image for this slide
            results.append({
                "slide_num": slide_num,
                "has_image": False,
                "source": None,
            })

        return results
