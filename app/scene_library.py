"""
Scene Library - Curated Visual Content for Professional Carousels

This module provides a CURATED library of high-quality scene screenshots
from popular shows and movies, organized by SITUATION/EMOTION.

Unlike web scraping, this ensures:
1. Consistent high quality
2. Relevant scene matching (situation, not just emotion)
3. No text overlays or meme captions
4. Professional appearance

Inspired by @theeconomicinfluence.id style carousels.
"""

import os
import requests
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class SceneCategory(Enum):
    """Categories for scene situations."""
    # Emotional states
    CONTEMPLATION = "contemplation"  # Thinking, reflecting, sunset moments
    CHAOS = "chaos"  # Everything on fire, disaster
    SUCCESS = "success"  # Money, winning, celebration
    STRUGGLE = "struggle"  # Working hard, exhausted
    SADNESS = "sadness"  # Lonely, depressed, crying
    ANXIETY = "anxiety"  # Worried, stressed, nervous
    REALIZATION = "realization"  # Aha moment, understanding
    DESPERATION = "desperation"  # Hopeless, giving up
    DENIAL = "denial"  # "This is fine" moments
    IRONY = "irony"  # Contradictory situations

    # Situational
    WORKING = "working"  # Job, office, labor
    MONEY_PROBLEMS = "money_problems"  # Financial stress
    LIFESTYLE = "lifestyle"  # Luxury, appearances
    SOCIAL_PRESSURE = "social_pressure"  # Keeping up with others
    HIDDEN_TRUTH = "hidden_truth"  # Behind the scenes reality


@dataclass
class CuratedScene:
    """A curated scene with metadata."""
    id: str
    name: str
    source: str  # "spongebob", "simpsons", "movie", "wojak", etc.
    category: SceneCategory
    situations: List[str]  # List of situations this scene matches
    emotions: List[str]  # List of emotions this conveys
    url: str  # Direct URL to high-quality image
    description: str
    priority: int = 5  # 1-10, higher = better match


# =============================================================================
# CURATED SCENE DATABASE
# =============================================================================

CURATED_SCENES: List[CuratedScene] = [
    # ---------------------------------------------------------------------
    # SPONGEBOB SCENES - Most versatile for Indonesian content
    # ---------------------------------------------------------------------
    CuratedScene(
        id="spongebob_sunset_krabs",
        name="Mr. Krabs Sunset Contemplation",
        source="spongebob",
        category=SceneCategory.CONTEMPLATION,
        situations=["reflecting on life", "thinking about money", "end of era", "nostalgia", "deep thoughts"],
        emotions=["contemplative", "peaceful", "melancholic", "thoughtful"],
        url="https://i.imgur.com/JpQT8vB.jpg",  # Mr Krabs on dock at sunset
        description="Mr. Krabs watching sunset on wooden dock - perfect for contemplative content",
        priority=9
    ),
    CuratedScene(
        id="spongebob_fire",
        name="Spongebob Fire Chaos",
        source="spongebob",
        category=SceneCategory.CHAOS,
        situations=["everything falling apart", "disaster", "chaos", "life on fire", "stress"],
        emotions=["panic", "chaos", "overwhelmed", "stressed"],
        url="https://i.imgur.com/8Xk5V4M.jpg",  # Spongebob surrounded by fire
        description="Spongebob surrounded by flames - perfect for 'everything is chaos' content",
        priority=10
    ),
    CuratedScene(
        id="spongebob_tired_working",
        name="Spongebob Exhausted at Work",
        source="spongebob",
        category=SceneCategory.STRUGGLE,
        situations=["overworked", "exhausted", "tired from job", "burnout", "working hard"],
        emotions=["exhausted", "tired", "drained", "worn out"],
        url="https://i.imgur.com/QJX3mKv.jpg",  # Tired Spongebob
        description="Exhausted Spongebob - perfect for work burnout content",
        priority=8
    ),
    CuratedScene(
        id="spongebob_hello_normal",
        name="Spongebob 'Hello I'm Normal'",
        source="spongebob",
        category=SceneCategory.DENIAL,
        situations=["pretending to be okay", "fake confidence", "hiding struggles", "social mask"],
        emotions=["fake happiness", "denial", "pretending", "uncomfortable"],
        url="https://i.imgur.com/kRW5nJH.jpg",  # Spongebob with "hello I'm normal" nametag
        description="Spongebob wearing 'Hello I'm Normal' - perfect for social anxiety content",
        priority=9
    ),

    # ---------------------------------------------------------------------
    # SIMPSONS SCENES
    # ---------------------------------------------------------------------
    CuratedScene(
        id="simpsons_homer_money",
        name="Homer Money Rain",
        source="simpsons",
        category=SceneCategory.SUCCESS,
        situations=["getting money", "feeling rich", "financial success", "winning", "prosperity"],
        emotions=["happy", "excited", "wealthy", "successful"],
        url="https://i.imgur.com/Yd9LXZM.jpg",  # Homer with money raining
        description="Homer Simpson with money raining down - perfect for success/money content",
        priority=9
    ),
    CuratedScene(
        id="simpsons_job_listings",
        name="Spongebob Job Listings Newspaper",
        source="spongebob",
        category=SceneCategory.WORKING,
        situations=["job hunting", "looking for work", "career search", "unemployment", "job market"],
        emotions=["hopeful", "searching", "determined", "worried"],
        url="https://i.imgur.com/NmK4GvH.jpg",  # Character reading job listings
        description="Reading job listings newspaper - perfect for career/job content",
        priority=8
    ),

    # ---------------------------------------------------------------------
    # WOJAK/DOOMER ART - For deeper emotional content
    # ---------------------------------------------------------------------
    CuratedScene(
        id="wojak_doomer_computer",
        name="Doomer at Computer Night",
        source="wojak",
        category=SceneCategory.SADNESS,
        situations=["late night scrolling", "lonely night", "isolated", "depressed browsing", "alone at night"],
        emotions=["lonely", "depressed", "isolated", "melancholic"],
        url="https://i.imgur.com/HkQJfYL.jpg",  # Wojak/doomer at computer in dark room
        description="Doomer character at computer in dark room - perfect for isolation/loneliness",
        priority=9
    ),
    CuratedScene(
        id="wojak_sad_room",
        name="Sad Person in Dark Room",
        source="wojak",
        category=SceneCategory.SADNESS,
        situations=["feeling down", "depression", "sitting alone", "contemplating life", "dark thoughts"],
        emotions=["sad", "depressed", "hopeless", "lonely"],
        url="https://i.imgur.com/VxS3QpB.jpg",  # Person sitting in dark room
        description="Silhouette in dark room - perfect for depression/sadness content",
        priority=8
    ),

    # ---------------------------------------------------------------------
    # MOVIE SCENES - For dramatic content
    # ---------------------------------------------------------------------
    CuratedScene(
        id="movie_car_fire",
        name="Man Walking from Burning Car",
        source="movie",
        category=SceneCategory.CHAOS,
        situations=["walking away from disaster", "leaving chaos", "dramatic exit", "everything burning"],
        emotions=["dramatic", "intense", "determined", "leaving behind"],
        url="https://i.imgur.com/8Ld3JmK.jpg",  # Silhouette walking from burning car
        description="Dramatic silhouette walking from burning car - perfect for 'leaving chaos behind' hooks",
        priority=10
    ),
    CuratedScene(
        id="movie_throwing_money",
        name="Person Throwing Money",
        source="movie",
        category=SceneCategory.SUCCESS,
        situations=["spending money", "rich lifestyle", "flaunting wealth", "money to burn"],
        emotions=["carefree", "wealthy", "extravagant", "careless"],
        url="https://i.imgur.com/pQR7vXN.jpg",  # Person throwing money in air
        description="Person throwing money - perfect for lifestyle inflation content",
        priority=8
    ),

    # ---------------------------------------------------------------------
    # ADDITIONAL SCENES FOR COMMON SITUATIONS
    # ---------------------------------------------------------------------
    CuratedScene(
        id="scene_coffee_expensive",
        name="Expensive Coffee Lifestyle",
        source="stock",
        category=SceneCategory.LIFESTYLE,
        situations=["expensive coffee", "lifestyle spending", "social status", "keeping appearances"],
        emotions=["sophisticated", "pretentious", "status-seeking"],
        url="https://i.imgur.com/KjL9mNQ.jpg",
        description="Expensive coffee shop aesthetic - for lifestyle inflation topics",
        priority=7
    ),
    CuratedScene(
        id="scene_office_stress",
        name="Office Worker Stress",
        source="stock",
        category=SceneCategory.ANXIETY,
        situations=["office stress", "work pressure", "corporate anxiety", "deadline panic"],
        emotions=["stressed", "anxious", "pressured", "overwhelmed"],
        url="https://i.imgur.com/Rk3JpLm.jpg",
        description="Person stressed at office - for work anxiety content",
        priority=7
    ),
]


class SceneLibrary:
    """
    Curated scene library for professional carousel visuals.

    Provides reliable, high-quality scene selection based on
    content situation matching (not just emotion keywords).
    """

    def __init__(self, cache_dir: str = None):
        """Initialize the scene library."""
        from .config import Config
        self.cache_dir = Path(cache_dir or Config.OUTPUT_DIR / "scene_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Index scenes by category and situation
        self._by_category: Dict[SceneCategory, List[CuratedScene]] = {}
        self._by_situation: Dict[str, List[CuratedScene]] = {}
        self._by_emotion: Dict[str, List[CuratedScene]] = {}

        self._build_indexes()
        logger.info(f"SceneLibrary initialized with {len(CURATED_SCENES)} scenes")

    def _build_indexes(self):
        """Build search indexes for fast lookup."""
        for scene in CURATED_SCENES:
            # Index by category
            if scene.category not in self._by_category:
                self._by_category[scene.category] = []
            self._by_category[scene.category].append(scene)

            # Index by situation keywords
            for situation in scene.situations:
                situation_lower = situation.lower()
                if situation_lower not in self._by_situation:
                    self._by_situation[situation_lower] = []
                self._by_situation[situation_lower].append(scene)

            # Index by emotion keywords
            for emotion in scene.emotions:
                emotion_lower = emotion.lower()
                if emotion_lower not in self._by_emotion:
                    self._by_emotion[emotion_lower] = []
                self._by_emotion[emotion_lower].append(scene)

    def find_scene_for_text(
        self,
        text: str,
        topic: Optional[str] = None,
        preferred_source: Optional[str] = None
    ) -> Optional[CuratedScene]:
        """
        Find the best matching scene for given text content.

        Uses situation matching (not just emotion) for professional results.

        Args:
            text: Slide text content
            topic: Optional topic hint
            preferred_source: Prefer scenes from specific source (spongebob, simpsons, movie)

        Returns:
            Best matching CuratedScene or None
        """
        text_lower = text.lower()

        # Score each scene by relevance
        scored_scenes: List[Tuple[CuratedScene, float]] = []

        for scene in CURATED_SCENES:
            score = 0.0

            # Check situation matches (highest weight)
            for situation in scene.situations:
                if situation.lower() in text_lower:
                    score += 10.0
                # Partial word matches
                for word in situation.lower().split():
                    if len(word) > 3 and word in text_lower:
                        score += 2.0

            # Check emotion matches (medium weight)
            for emotion in scene.emotions:
                if emotion.lower() in text_lower:
                    score += 5.0

            # Boost by priority
            score += scene.priority * 0.5

            # Boost preferred source
            if preferred_source and scene.source == preferred_source:
                score += 5.0

            # Topic-based boosts
            if topic:
                topic_lower = topic.lower()
                if "finance" in topic_lower or "money" in topic_lower:
                    if scene.category in [SceneCategory.MONEY_PROBLEMS, SceneCategory.SUCCESS]:
                        score += 8.0
                if "work" in topic_lower or "career" in topic_lower:
                    if scene.category in [SceneCategory.WORKING, SceneCategory.STRUGGLE]:
                        score += 8.0
                if "mental" in topic_lower or "anxiety" in topic_lower:
                    if scene.category in [SceneCategory.ANXIETY, SceneCategory.SADNESS]:
                        score += 8.0

            if score > 0:
                scored_scenes.append((scene, score))

        # Sort by score and return best match
        if scored_scenes:
            scored_scenes.sort(key=lambda x: x[1], reverse=True)
            best_scene = scored_scenes[0][0]
            logger.info(f"Selected scene: {best_scene.name} (score: {scored_scenes[0][1]:.1f})")
            return best_scene

        logger.warning(f"No matching scene found for: {text[:50]}...")
        return None

    def find_scenes_for_carousel(
        self,
        slides: List[str],
        topic: Optional[str] = None,
        skip_first_last: bool = True
    ) -> Dict[int, CuratedScene]:
        """
        Find scenes for all slides in a carousel.

        Args:
            slides: List of slide texts
            topic: Topic hint for entire carousel
            skip_first_last: Skip hook (1) and CTA (last) slides

        Returns:
            Dict of {slide_number: CuratedScene}
        """
        results = {}
        total_slides = len(slides)
        used_scenes = set()  # Avoid repeating same scene

        for i, slide_text in enumerate(slides, 1):
            # Skip first and last if requested
            if skip_first_last and (i == 1 or i == total_slides):
                logger.info(f"Slide {i}: Skipping (hook/CTA)")
                continue

            # Find best scene not yet used
            scene = self.find_scene_for_text(slide_text, topic)

            # Avoid duplicates
            if scene and scene.id in used_scenes:
                # Try to find alternative
                alt_scenes = [s for s, _ in self._score_all_scenes(slide_text, topic) if s.id not in used_scenes]
                scene = alt_scenes[0] if alt_scenes else scene

            if scene:
                results[i] = scene
                used_scenes.add(scene.id)
                logger.info(f"Slide {i}: {scene.name} ({scene.source})")
            else:
                logger.warning(f"Slide {i}: No scene found")

        return results

    def _score_all_scenes(self, text: str, topic: Optional[str] = None) -> List[Tuple[CuratedScene, float]]:
        """Score all scenes for given text."""
        text_lower = text.lower()
        scored = []

        for scene in CURATED_SCENES:
            score = 0.0
            for situation in scene.situations:
                if situation.lower() in text_lower:
                    score += 10.0
            for emotion in scene.emotions:
                if emotion.lower() in text_lower:
                    score += 5.0
            score += scene.priority * 0.5
            scored.append((scene, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def download_scene(self, scene: CuratedScene) -> Optional[str]:
        """
        Download scene image to cache.

        Returns:
            Local path to cached image or None if failed
        """
        # Generate cache filename
        cache_key = f"{scene.id}.jpg"
        cache_path = self.cache_dir / cache_key

        # Return cached if exists
        if cache_path.exists():
            logger.debug(f"Using cached scene: {scene.id}")
            return str(cache_path)

        # Download
        try:
            response = requests.get(
                scene.url,
                timeout=15,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )

            if response.status_code == 200:
                cache_path.write_bytes(response.content)
                logger.info(f"Downloaded scene: {scene.name}")
                return str(cache_path)
            else:
                logger.warning(f"Failed to download {scene.id}: HTTP {response.status_code}")

        except Exception as e:
            logger.error(f"Download error for {scene.id}: {e}")

        return None

    def get_scene_path(self, scene: CuratedScene) -> Optional[str]:
        """Get local path for scene, downloading if needed."""
        return self.download_scene(scene)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_scenes_for_slides(
    slides: List[str],
    topic: Optional[str] = None
) -> Dict[int, str]:
    """
    Get scene image paths for carousel slides.

    Returns dict of {slide_number: local_image_path}
    """
    library = SceneLibrary()
    scenes = library.find_scenes_for_carousel(slides, topic)

    # Download and return paths
    paths = {}
    for slide_num, scene in scenes.items():
        path = library.get_scene_path(scene)
        if path:
            paths[slide_num] = path

    return paths


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Testing SceneLibrary...")
    print("=" * 80)

    # Test slides from the reference carousel
    test_slides = [
        "Ada banyak orang yang bekerja, gajinya tinggi, dan punya posisi bagus di kantor, tapi kok ekonominya rapuh.",
        "Pendidikan mereka tinggi, posisi kerja mapan, dan aktivitas di media sosial selalu tampak meyakinkan.",
        "Tapi saat obrolan mulai masuk lebih dalam, cerita yang sebenarnya pun mulai terungkap.",
        "Kenyataannya, banyak dari mereka menjalani hidup tanpa tabungan sama sekali.",
        "Emosi yang mereka rasakan adalah kecemasan yang senyap. Tekanan sosial untuk terus terlihat setara begitu kuat.",
        "Pertama, sistem upah di banyak sektor yang kenaikannya tertinggal jauh dari harga properti.",
    ]

    library = SceneLibrary()
    scenes = library.find_scenes_for_carousel(test_slides, topic="ekonomi finansial")

    print("\nSCENE SELECTION RESULTS:")
    print("-" * 80)
    for slide_num, scene in scenes.items():
        print(f"\nSlide {slide_num}:")
        print(f"  Scene: {scene.name}")
        print(f"  Source: {scene.source}")
        print(f"  Category: {scene.category.value}")
        print(f"  Description: {scene.description}")

    print("\n" + "=" * 80)
    print("Done!")
