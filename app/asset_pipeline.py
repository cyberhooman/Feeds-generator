"""
Asset Pipeline Module

Manages meme and image assets for carousel slides.
Downloads, caches, and provides local paths for memes.
"""

import os
import re
import hashlib
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from .config import Config


# Built-in meme templates - URLs verified to work
# Using multiple sources for reliability
# has_text: False = no text overlay (universal), True = has English text
# Memes with has_text=True should only be used with English content
BUILTIN_MEMES = {
    "shocked_pikachu": {
        "url": "https://imgflip.com/s/meme/Surprised-Pikachu.jpg",
        "alt_names": ["surprised pikachu", "pikachu meme"],
        "emotions": ["shocked", "surprised", "disbelief"],
        "has_text": False  # No text - universal
    },
    "drake_format": {
        "url": "https://imgflip.com/s/meme/Drake-Hotline-Bling.jpg",
        "alt_names": ["drake meme", "drake hotline bling"],
        "emotions": ["comparison", "preference", "choice"],
        "has_text": False  # No text - universal
    },
    "distracted_boyfriend": {
        "url": "https://imgflip.com/s/meme/Distracted-Boyfriend.jpg",
        "alt_names": ["guy looking at other girl", "distracted bf"],
        "emotions": ["distracted", "temptation", "unfaithful"],
        "has_text": False  # No text - universal
    },
    "this_is_fine": {
        "url": "https://i.imgflip.com/1nh6z0.jpg",
        "alt_names": ["dog fire meme", "everything is fine"],
        "emotions": ["denial", "coping", "disaster"],
        "has_text": True  # Has "This is fine" text
    },
    "galaxy_brain": {
        "url": "https://imgflip.com/s/meme/Expanding-Brain.jpg",
        "alt_names": ["expanding brain", "brain levels"],
        "emotions": ["escalation", "enlightenment", "irony"],
        "has_text": False  # No text - universal
    },
    "change_my_mind": {
        "url": "https://imgflip.com/s/meme/Change-My-Mind.jpg",
        "alt_names": ["steven crowder", "prove me wrong"],
        "emotions": ["challenge", "debate", "opinion"],
        "has_text": True  # Has "Change my mind" text
    },
    "two_buttons": {
        "url": "https://imgflip.com/s/meme/Two-Buttons.jpg",
        "alt_names": ["sweating buttons", "hard choice"],
        "emotions": ["dilemma", "difficult choice", "anxiety"],
        "has_text": False  # No text - universal
    },
    "woman_yelling_cat": {
        "url": "https://imgflip.com/s/meme/Woman-Yelling-At-Cat.jpg",
        "alt_names": ["woman screaming at cat", "confused cat"],
        "emotions": ["argument", "confusion", "confrontation"],
        "has_text": False  # No text - universal
    },
    "stonks": {
        "url": "https://i.kym-cdn.com/entries/icons/original/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg",
        "alt_names": ["meme man stonks", "stonks meme"],
        "emotions": ["success", "profit", "winning"],
        "has_text": True  # Has "Stonks" text
    },
    "not_stonks": {
        "url": "https://i.kym-cdn.com/photos/images/newsfeed/001/653/316/af3.jpg",
        "alt_names": ["stinks meme", "stonks down"],
        "emotions": ["failure", "loss", "regret"],
        "has_text": True  # Has text
    },
    "sad_pablo_escobar": {
        "url": "https://imgflip.com/s/meme/Sad-Pablo-Escobar.jpg",
        "alt_names": ["waiting pablo", "sad narcos"],
        "emotions": ["lonely", "waiting", "sad"],
        "has_text": False  # No text - universal
    },
    "monkey_puppet": {
        "url": "https://imgflip.com/s/meme/Monkey-Puppet.jpg",
        "alt_names": ["awkward look monkey", "side eye puppet"],
        "emotions": ["awkward", "uncomfortable", "nervous"],
        "has_text": False  # No text - universal
    },
    "clown_makeup": {
        "url": "https://i.imgflip.com/38el31.jpg",
        "alt_names": ["clown applying makeup", "becoming clown"],
        "emotions": ["self-deprecating", "irony", "regret"],
        "has_text": False  # No text - universal
    },
    "trade_offer": {
        "url": "https://i.kym-cdn.com/photos/images/newsfeed/002/055/498/e24.jpg",
        "alt_names": ["tiktok trade offer", "i receive you receive"],
        "emotions": ["bargain", "deal", "trade"],
        "has_text": True  # Has English text
    },
    "gru_plan": {
        "url": "https://imgflip.com/s/meme/Grus-Plan.jpg",
        "alt_names": ["gru board", "gru presentation"],
        "emotions": ["planning", "backfire", "realization"],
        "has_text": False  # No text - universal
    },
    "thinking_face": {
        "url": "https://i.kym-cdn.com/photos/images/newsfeed/001/256/183/9d5.png",
        "alt_names": ["thinking emoji", "hmm"],
        "emotions": ["thinking", "considering", "skeptical"],
        "has_text": False  # No text - universal
    },
    "uno_draw_25": {
        "url": "https://imgflip.com/s/meme/UNO-Draw-25-Cards.jpg",
        "alt_names": ["uno draw cards", "draw 25"],
        "emotions": ["stubbornness", "refusal", "choice"],
        "has_text": False  # No text - universal
    },
    "crying_cat": {
        "url": "https://i.kym-cdn.com/photos/images/original/001/384/545/7b9.jpg",
        "alt_names": ["sad cat", "cat crying"],
        "emotions": ["sad", "crying", "emotional"],
        "has_text": False  # No text - universal
    },
    "waiting_skeleton": {
        "url": "https://imgflip.com/s/meme/Waiting-Skeleton.jpg",
        "alt_names": ["skeleton waiting", "still waiting"],
        "emotions": ["waiting", "patience", "eternal"],
        "has_text": False  # No text - universal
    },
    "think_about_it": {
        "url": "https://imgflip.com/s/meme/Roll-Safe-Think-About-It.jpg",
        "alt_names": ["roll safe", "tapping head", "smart thinking"],
        "emotions": ["clever", "smart", "lifehack"],
        "has_text": False  # No text - universal
    },
}


def filter_memes_by_language(memes: List[Dict], target_lang: str) -> List[Dict]:
    """
    Filter memes to prefer text-free memes for non-English content.

    Args:
        memes: List of meme dicts with 'name' key
        target_lang: Target language ('en', 'id', etc.)

    Returns:
        Filtered list preferring text-free memes for non-English
    """
    if target_lang == 'en':
        # English content can use all memes
        return memes

    # For non-English, prefer memes without text
    text_free = []
    with_text = []

    for meme in memes:
        meme_name = meme.get('name', '').lower().replace(' ', '_').replace('-', '_')
        meme_info = BUILTIN_MEMES.get(meme_name, {})

        if not meme_info.get('has_text', False):
            text_free.append(meme)
        else:
            with_text.append(meme)

    # Return text-free first, then with-text as fallback
    return text_free + with_text


class AssetPipeline:
    """
    Manages meme and image assets for carousel slides.

    Features:
    - Download memes from URLs
    - Search local meme library
    - Cache downloaded assets
    - Map meme recommendations to local files
    """

    # Common meme sources (for future expansion)
    MEME_SOURCES = {
        "imgflip": "https://imgflip.com/",
        "knowyourmeme": "https://knowyourmeme.com/",
    }

    # Supported image formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

    def __init__(self, assets_dir: str = None, cache_dir: str = None):
        """
        Initialize the asset pipeline.

        Args:
            assets_dir: Directory for permanent meme library
            cache_dir: Directory for downloaded/temporary assets
        """
        if assets_dir is None:
            assets_dir = Config.BASE_DIR / "assets" / "memes"
        if cache_dir is None:
            cache_dir = Config.BASE_DIR / "cache" / "memes"

        self.assets_dir = Path(assets_dir)
        self.cache_dir = Path(cache_dir)

        # Create directories
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Build meme index
        self._meme_index = self._build_meme_index()

    def _build_meme_index(self) -> Dict[str, Path]:
        """
        Build index of available memes in the library.

        Returns:
            Dict mapping normalized names to file paths
        """
        index = {}

        # Scan assets directory
        for file_path in self.assets_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                # Create normalized name (lowercase, no extension, underscores)
                name = file_path.stem.lower().replace("-", "_").replace(" ", "_")
                index[name] = file_path

                # Also index by original name
                index[file_path.stem.lower()] = file_path

        # Also scan cache
        for file_path in self.cache_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                name = file_path.stem.lower().replace("-", "_").replace(" ", "_")
                if name not in index:  # Don't override library memes
                    index[name] = file_path

        return index

    def _normalize_name(self, name: str) -> str:
        """Normalize meme name for matching."""
        # Remove common suffixes/prefixes
        name = name.lower().strip()
        name = re.sub(r'\.(jpg|jpeg|png|gif|webp)$', '', name)
        name = name.replace("-", "_").replace(" ", "_")
        name = re.sub(r'_+', '_', name)  # Multiple underscores to one
        return name

    def _extract_meme_keywords(self, text: str) -> List[str]:
        """
        Extract potential meme keywords from a description.

        Args:
            text: Meme description or recommendation text

        Returns:
            List of keywords to search for
        """
        # Common meme name patterns
        keywords = []

        # Clean the text
        text = text.lower().strip()

        # Remove common phrases
        text = re.sub(r'suggest(ed)?:?\s*', '', text)
        text = re.sub(r'meme:?\s*', '', text)
        text = re.sub(r'reaction:?\s*', '', text)
        text = re.sub(r'energy:?\s*', '', text)
        text = re.sub(r'emotional beat:?\s*', '', text)

        # Split by common delimiters
        parts = re.split(r'[,/|;-]', text)

        for part in parts:
            part = part.strip()
            if part and len(part) > 2:
                keywords.append(self._normalize_name(part))

        # Also try the whole text as one keyword
        if text:
            keywords.append(self._normalize_name(text))

        return keywords

    def get_meme_path(self, meme_name: str, auto_download: bool = True) -> Optional[str]:
        """
        Get local path if meme exists in library or cache.
        If auto_download is True, will try to download from built-in library.

        Args:
            meme_name: Name or description of the meme
            auto_download: Whether to auto-download if not found locally

        Returns:
            Local file path or None if not found
        """
        normalized = self._normalize_name(meme_name)

        # Direct match
        if normalized in self._meme_index:
            return str(self._meme_index[normalized])

        # Partial match
        for index_name, path in self._meme_index.items():
            if normalized in index_name or index_name in normalized:
                return str(path)

        # Try keywords
        keywords = self._extract_meme_keywords(meme_name)
        for keyword in keywords:
            if keyword in self._meme_index:
                return str(self._meme_index[keyword])

            # Partial keyword match
            for index_name, path in self._meme_index.items():
                if keyword in index_name:
                    return str(path)

        # Try to auto-download from built-in memes
        if auto_download:
            downloaded_path = self._try_download_builtin(meme_name)
            if downloaded_path:
                return downloaded_path

        return None

    def _try_download_builtin(self, meme_name: str) -> Optional[str]:
        """
        Try to download a meme from the built-in meme library.

        Args:
            meme_name: Name or description of the meme

        Returns:
            Local file path if downloaded, None otherwise
        """
        normalized = self._normalize_name(meme_name)

        # Find matching built-in meme
        matched_key = None

        for key, meme_info in BUILTIN_MEMES.items():
            # Direct match
            if normalized == key or normalized in key or key in normalized:
                matched_key = key
                break

            # Check alt names
            for alt in meme_info.get("alt_names", []):
                alt_norm = self._normalize_name(alt)
                if normalized in alt_norm or alt_norm in normalized:
                    matched_key = key
                    break

            # Check emotions
            for emotion in meme_info.get("emotions", []):
                if emotion in normalized or normalized in emotion:
                    matched_key = key
                    break

            if matched_key:
                break

        if not matched_key:
            return None

        # Download the meme
        meme_info = BUILTIN_MEMES[matched_key]
        url = meme_info["url"]

        try:
            # Determine extension from URL
            ext = ".jpg"
            if ".png" in url:
                ext = ".png"
            elif ".gif" in url:
                ext = ".gif"

            filename = f"{matched_key}{ext}"
            save_path = self.cache_dir / filename

            # Check if already downloaded
            if save_path.exists():
                self._meme_index[matched_key] = save_path
                return str(save_path)

            # Download
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Save
            with open(save_path, 'wb') as f:
                f.write(response.content)

            # Update index
            self._meme_index[matched_key] = save_path
            print(f"Downloaded meme: {matched_key} -> {save_path}")

            return str(save_path)

        except Exception as e:
            print(f"Failed to download built-in meme {matched_key}: {e}")
            return None

    def download_all_builtin_memes(self) -> Dict[str, str]:
        """
        Download all built-in memes to the cache.

        Returns:
            Dict of {meme_name: local_path}
        """
        downloaded = {}

        for key in BUILTIN_MEMES.keys():
            path = self._try_download_builtin(key)
            if path:
                downloaded[key] = path

        return downloaded

    def download_meme(
        self,
        meme_name: str,
        source_url: str = None,
        timeout: int = 30
    ) -> Optional[str]:
        """
        Download meme from URL and cache locally.

        Args:
            meme_name: Name to save the meme as
            source_url: URL to download from
            timeout: Download timeout in seconds

        Returns:
            Local file path or None if download failed
        """
        if not source_url:
            return None

        try:
            # Parse URL to get extension
            parsed = urlparse(source_url)
            path = parsed.path.lower()

            # Determine file extension
            ext = '.jpg'  # Default
            for fmt in self.SUPPORTED_FORMATS:
                if path.endswith(fmt):
                    ext = fmt
                    break

            # Create filename using hash for uniqueness
            url_hash = hashlib.md5(source_url.encode()).hexdigest()[:8]
            filename = f"{self._normalize_name(meme_name)}_{url_hash}{ext}"

            # Check if already cached
            cache_path = self.cache_dir / filename
            if cache_path.exists():
                return str(cache_path)

            # Download
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(
                source_url,
                headers=headers,
                timeout=timeout,
                stream=True
            )
            response.raise_for_status()

            # Verify it's an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None

            # Save to cache
            with open(cache_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Update index
            normalized = self._normalize_name(meme_name)
            self._meme_index[normalized] = cache_path

            return str(cache_path)

        except Exception as e:
            print(f"Failed to download meme: {e}")
            return None

    def search_meme(self, query: str, limit: int = 5) -> List[Tuple[str, str]]:
        """
        Search local meme library for matches.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of (name, path) tuples
        """
        results = []
        query_normalized = self._normalize_name(query)
        query_keywords = self._extract_meme_keywords(query)

        scored_results = []

        for name, path in self._meme_index.items():
            score = 0

            # Exact match
            if query_normalized == name:
                score = 100
            # Query contained in name
            elif query_normalized in name:
                score = 80
            # Name contained in query
            elif name in query_normalized:
                score = 60
            else:
                # Keyword matching
                for keyword in query_keywords:
                    if keyword in name:
                        score = max(score, 40)
                    elif name in keyword:
                        score = max(score, 30)

            if score > 0:
                scored_results.append((score, name, str(path)))

        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)

        # Return top results
        return [(name, path) for _, name, path in scored_results[:limit]]

    def ensure_memes_ready(
        self,
        meme_recommendations: Dict[int, str],
        download_missing: bool = False
    ) -> Dict[int, Optional[str]]:
        """
        Takes meme recommendations and returns dict of local paths.

        Args:
            meme_recommendations: Dict of {slide_number: meme_description}
            download_missing: Whether to attempt downloading missing memes

        Returns:
            Dict of {slide_number: local_meme_path or None}
        """
        result = {}

        for slide_num, recommendation in meme_recommendations.items():
            if not recommendation:
                result[slide_num] = None
                continue

            # Try to find in local library
            local_path = self.get_meme_path(recommendation)

            if local_path:
                result[slide_num] = local_path
            else:
                # Could not find locally
                result[slide_num] = None

        return result

    def list_available_memes(self) -> List[Dict[str, str]]:
        """
        List all available memes in the library.

        Returns:
            List of dicts with 'name' and 'path' keys
        """
        seen_paths = set()
        memes = []

        for name, path in sorted(self._meme_index.items()):
            path_str = str(path)
            if path_str not in seen_paths:
                seen_paths.add(path_str)
                memes.append({
                    'name': name,
                    'path': path_str,
                    'filename': path.name
                })

        return memes

    def add_meme_to_library(
        self,
        source_path: str,
        meme_name: str = None
    ) -> str:
        """
        Add a meme to the permanent library.

        Args:
            source_path: Path to the source image
            meme_name: Name to use (defaults to filename)

        Returns:
            Path in the library
        """
        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        if meme_name is None:
            meme_name = source.stem

        # Normalize name
        normalized = self._normalize_name(meme_name)
        ext = source.suffix.lower()

        if ext not in self.SUPPORTED_FORMATS:
            ext = '.jpg'

        # Create destination path
        dest_path = self.assets_dir / f"{normalized}{ext}"

        # Copy file
        import shutil
        shutil.copy2(source, dest_path)

        # Update index
        self._meme_index[normalized] = dest_path

        return str(dest_path)

    def refresh_index(self):
        """Refresh the meme index from disk."""
        self._meme_index = self._build_meme_index()

    def get_placeholder_meme(self) -> Optional[str]:
        """
        Get a placeholder meme for testing.

        Returns:
            Path to placeholder or first available meme
        """
        # Look for placeholder
        placeholder_names = ['placeholder', 'default', 'test']
        for name in placeholder_names:
            if name in self._meme_index:
                return str(self._meme_index[name])

        # Return first available
        if self._meme_index:
            return str(next(iter(self._meme_index.values())))

        return None


class MemeRecommendationParser:
    """
    Parses AI meme recommendations and maps them to usable assets.
    """

    # Common meme emotions/energies and their typical meme matches
    EMOTION_MAPPINGS = {
        # Positive
        'excited': ['excited', 'happy', 'celebration', 'yes'],
        'happy': ['happy', 'smile', 'joy', 'celebration'],
        'confident': ['confident', 'cool', 'chad', 'success'],
        'surprised': ['surprised', 'shocked', 'omg', 'wow'],
        'proud': ['proud', 'success', 'achievement', 'winning'],

        # Negative
        'frustrated': ['frustrated', 'angry', 'facepalm', 'annoyed'],
        'sad': ['sad', 'crying', 'tears', 'disappointed'],
        'confused': ['confused', 'thinking', 'question', 'huh'],
        'tired': ['tired', 'exhausted', 'sleepy', 'done'],
        'angry': ['angry', 'mad', 'rage', 'furious'],

        # Reactions
        'thinking': ['thinking', 'hmm', 'consider', 'ponder'],
        'mind_blown': ['mind_blown', 'galaxy_brain', 'enlightened', 'wow'],
        'skeptical': ['skeptical', 'doubt', 'suspicious', 'side_eye'],
        'agreeing': ['agree', 'yes', 'nodding', 'exactly'],
        'disagreeing': ['disagree', 'no', 'shake_head', 'wrong'],
    }

    @classmethod
    def parse_recommendation(cls, recommendation: str) -> Dict[str, any]:
        """
        Parse a meme recommendation string into structured data.

        Args:
            recommendation: Raw recommendation text from AI

        Returns:
            Dict with 'emotion', 'keywords', 'suggested_memes'
        """
        result = {
            'emotion': None,
            'keywords': [],
            'suggested_memes': [],
            'raw': recommendation
        }

        if not recommendation:
            return result

        text = recommendation.lower()

        # Extract emotion
        for emotion, keywords in cls.EMOTION_MAPPINGS.items():
            if emotion in text:
                result['emotion'] = emotion
                result['suggested_memes'].extend(keywords)
                break

        # Extract keywords from the recommendation
        # Look for patterns like "suggest: xyz" or "energy: xyz"
        patterns = [
            r'suggest(?:ed)?:?\s*([^,\n]+)',
            r'energy:?\s*([^,\n]+)',
            r'meme:?\s*([^,\n]+)',
            r'vibe:?\s*([^,\n]+)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                cleaned = match.strip()
                if cleaned:
                    result['keywords'].append(cleaned)

        # If no specific suggestions, use the whole text
        if not result['keywords'] and not result['suggested_memes']:
            result['keywords'] = [text.strip()]

        return result

    @classmethod
    def get_best_match(
        cls,
        recommendation: str,
        pipeline: AssetPipeline
    ) -> Optional[str]:
        """
        Get the best matching meme path for a recommendation.

        Args:
            recommendation: Meme recommendation text
            pipeline: AssetPipeline instance

        Returns:
            Path to best matching meme or None
        """
        parsed = cls.parse_recommendation(recommendation)

        # Try suggested memes first
        for meme_name in parsed['suggested_memes']:
            path = pipeline.get_meme_path(meme_name)
            if path:
                return path

        # Try keywords
        for keyword in parsed['keywords']:
            path = pipeline.get_meme_path(keyword)
            if path:
                return path

        # Try raw recommendation
        path = pipeline.get_meme_path(parsed['raw'])
        if path:
            return path

        return None


# Convenience function
def get_asset_pipeline() -> AssetPipeline:
    """Get a configured AssetPipeline instance."""
    return AssetPipeline()
