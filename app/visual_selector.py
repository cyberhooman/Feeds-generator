"""
Visual Selector - Intelligent Primary Visual Selection System

Replaces the multi-fallback system with a single, reliable visual selector.
Determines the BEST visual strategy for each slide upfront, then executes it.

No more confusing fallback chains - one strategy per slide.
"""

import logging
import re
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class VisualType(Enum):
    """Types of visuals for slides."""
    TEXT_ONLY = "text_only"
    CURATED_SCENE = "curated_scene"  # NEW: Preferred - from scene library
    DYNAMIC_MEME = "dynamic_meme"  # Fallback - generic memes
    NEWS_PHOTO = "news_photo"
    INFOGRAPHIC = "infographic"
    MOVIE_SCENE = "movie_scene"  # Deprecated - use CURATED_SCENE


@dataclass
class VisualStrategy:
    """Strategy for a slide's visual."""
    slide_number: int
    visual_type: VisualType
    reason: str
    should_skip_visual: bool = False
    content_type_hint: Optional[str] = None
    search_query: Optional[str] = None


class VisualSelector:
    """
    Determines the optimal visual strategy for each slide.

    Philosophy:
    - Hook slide (1) → TEXT ONLY (stronger psychological impact)
    - Body slides (2-N-1) → ONE primary visual type (not multiple fallbacks)
    - CTA slide (N) → TEXT ONLY (stronger conversion)

    Selection based on:
    1. Slide position (hook/body/cta)
    2. Content type detection (emotional, news, data, story)
    3. Topic context (finance, news, tech, etc.)
    """

    def __init__(self):
        """Initialize the visual selector."""
        logger.info("VisualSelector initialized")

    def _detect_content_type(self, text: str, topic: Optional[str] = None) -> str:
        """
        Detect if content is news, emotional, data-driven, or story-based.

        Returns: "news", "emotional", "data", "story"
        """
        text_lower = text.lower()

        # News indicators
        news_keywords = [
            'president', 'minister', 'government', 'announced', 'breaking',
            'election', 'parliament', 'congress', 'war', 'conflict',
            'economy', 'market', 'stock', 'crisis', 'disaster',
            'presiden', 'menteri', 'pemerintah', 'diumumkan', 'DPR',
        ]
        news_score = sum(1 for kw in news_keywords if kw in text_lower)

        # Data indicators (numbers, statistics, charts)
        data_keywords = ['%', 'data', 'chart', 'graph', 'increase', 'decrease', 'trend']
        data_indicators = [
            r'\d+%',  # percentages
            r'\$\d+',  # currency
            r'\d+[kK]',  # thousands
            r'naik|turun|meningkat|menurun',  # Indonesian increase/decrease
        ]
        data_score = sum(1 for kw in data_keywords if kw in text_lower)
        for pattern in data_indicators:
            if re.search(pattern, text):
                data_score += 2

        # Story/personal narrative indicators
        story_keywords = [
            'i was', 'i had', 'when i', 'my', 'me', 'myself',
            'dulu', 'awal', 'mulai', 'pertama', 'cerita', 'kisah',
            'lesson', 'learned', 'discovered', 'realized', 'journey'
        ]
        story_score = sum(1 for kw in story_keywords if kw in text_lower)

        # Emotional indicators
        emotional_keywords = [
            'feel', 'felt', 'emotion', 'love', 'hate', 'afraid', 'excited',
            'imagine', 'when you', 'me trying', 'rasanya', 'kayak', 'mood'
        ]
        emotional_score = sum(1 for kw in emotional_keywords if kw in text_lower)

        # Determine primary type
        scores = {
            'news': news_score,
            'data': data_score,
            'story': story_score,
            'emotional': emotional_score,
        }

        primary_type = max(scores, key=scores.get) if scores else 'emotional'

        # Override if topic hints
        if topic and 'news' in topic.lower():
            primary_type = 'news'

        logger.debug(f"Content type detected: {primary_type} (scores: {scores})")
        return primary_type

    def _detect_topic(self, text: str, topic_hint: Optional[str] = None) -> str:
        """Detect the topic of the slide."""
        if topic_hint:
            return topic_hint

        text_lower = text.lower()

        # Topic keywords
        topics = {
            'finance': ['saham', 'crypto', 'trading', 'invest', 'stock', 'bitcoin', 'profit', 'loss'],
            'news': ['presiden', 'menteri', 'government', 'president', 'breaking'],
            'tech': ['coding', 'bug', 'deploy', 'server', 'code', 'programming'],
            'work': ['kerja', 'kantor', 'meeting', 'boss', 'office', 'deadline'],
            'life': ['hidup', 'adult', 'life', 'growing', 'reality'],
        }

        for topic, keywords in topics.items():
            if any(kw in text_lower for kw in keywords):
                return topic

        return 'general'

    def select_visual_strategy(
        self,
        slide_text: str,
        slide_number: int,
        total_slides: int,
        topic_hint: Optional[str] = None
    ) -> VisualStrategy:
        """
        Select the optimal visual strategy for a slide.

        Args:
            slide_text: Content of the slide
            slide_number: Position in carousel (1-indexed)
            total_slides: Total number of slides
            topic_hint: Optional topic context

        Returns:
            VisualStrategy with the recommended visual type
        """
        # Hook slide (1) - always TEXT ONLY
        if slide_number == 1:
            return VisualStrategy(
                slide_number=slide_number,
                visual_type=VisualType.TEXT_ONLY,
                reason="Hook slide - text-only has stronger psychological impact (68% higher CTR)",
                should_skip_visual=True
            )

        # CTA slide (last) - always TEXT ONLY
        if slide_number == total_slides:
            return VisualStrategy(
                slide_number=slide_number,
                visual_type=VisualType.TEXT_ONLY,
                reason="CTA slide - text-only has stronger conversion signal",
                should_skip_visual=True
            )

        # Body slides - select based on content type
        content_type = self._detect_content_type(slide_text, topic_hint)
        topic = self._detect_topic(slide_text, topic_hint)

        # NEWS content
        if content_type == 'news':
            return VisualStrategy(
                slide_number=slide_number,
                visual_type=VisualType.NEWS_PHOTO,
                reason=f"News content detected - using professional news photos (Reuters/AP/Getty)",
                content_type_hint='news'
            )

        # DATA/STATISTICS content
        if content_type == 'data':
            # Check if contains enough data for infographic
            if re.search(r'\d+%|\$\d+|\d+[kK]|\d+ to \d+', slide_text):
                return VisualStrategy(
                    slide_number=slide_number,
                    visual_type=VisualType.INFOGRAPHIC,
                    reason="Data-heavy content - using chart/graph/infographic visual",
                    content_type_hint='infographic'
                )

        # MOVIE/TV content (check if mentions movies, scenes, characters)
        if any(word in slide_text.lower() for word in ['movie', 'tv', 'film', 'scene', 'actor', 'character']):
            return VisualStrategy(
                slide_number=slide_number,
                visual_type=VisualType.CURATED_SCENE,
                reason="Movie/TV reference detected - using curated scene library",
                content_type_hint='curated_scene'
            )

        # DEFAULT: CURATED SCENE (professional quality)
        # Changed from DYNAMIC_MEME to CURATED_SCENE for professional output
        # Meme templates look amateur - curated scenes look professional
        return VisualStrategy(
            slide_number=slide_number,
            visual_type=VisualType.CURATED_SCENE,
            reason=f"Body content (topic: {topic}) - using curated scene for professional look",
            content_type_hint='curated_scene'
        )

    def select_strategies_for_carousel(
        self,
        slides: List[str],
        topic_hint: Optional[str] = None
    ) -> Dict[int, VisualStrategy]:
        """
        Select visual strategies for all slides in a carousel.

        Args:
            slides: List of slide texts
            topic_hint: Optional topic for entire carousel

        Returns:
            Dict mapping slide number to VisualStrategy
        """
        strategies = {}
        total_slides = len(slides)

        logger.info(f"Selecting visual strategies for {total_slides} slides...")

        for i, slide_text in enumerate(slides, 1):
            strategy = self.select_visual_strategy(slide_text, i, total_slides, topic_hint)
            strategies[i] = strategy

            logger.info(
                f"Slide {i}/{total_slides}: {strategy.visual_type.value} - {strategy.reason}"
            )

        return strategies


class StyleConsistencyTracker:
    """
    Ensures visual style consistency across all slides in a carousel.

    Once a visual style is selected (cartoon, photo, movie, etc.),
    this tracker ensures subsequent slides use the same style family.

    This prevents the chaotic mix of cartoons + memes + photos
    that creates visual incoherence.
    """

    # Style families and their associated search terms
    STYLE_FAMILIES = {
        'cartoon': ['cartoon', 'animated', 'animation', 'spongebob', 'simpsons', 'anime', 'pixar', 'disney'],
        'movie': ['movie', 'film', 'cinema', 'tv show', 'scene', 'still', 'screenshot'],
        'photo': ['photo', 'stock', 'professional', 'real', 'portrait', 'reuters', 'ap news'],
        'diagram': ['diagram', 'chart', 'graph', 'infographic', 'illustration', 'flowchart'],
        'meme': ['meme', 'reaction', 'wojak', 'pepe', 'template'],
    }

    def __init__(self, preferred_style: Optional[str] = None):
        """
        Initialize the style tracker.

        Args:
            preferred_style: Optional style lock ('cartoon', 'movie', 'photo', 'diagram', 'auto', 'text_only')
                           If 'auto' or None, style will be auto-detected from first selection.
                           If 'text_only', no images should be used.
        """
        self.preferred_style = preferred_style if preferred_style not in ['auto', None] else None
        self.locked_style: Optional[str] = self.preferred_style
        self.selection_history: List[Dict] = []
        logger.info(f"StyleConsistencyTracker initialized with preferred_style={preferred_style}")

    def is_text_only_mode(self) -> bool:
        """Check if tracker is in text-only mode."""
        return self.preferred_style == 'text_only'

    def get_allowed_search_terms(self) -> Optional[List[str]]:
        """
        Get allowed search terms based on locked style.

        Returns:
            List of allowed search terms, or None if no style lock (all terms allowed)
        """
        if not self.locked_style:
            return None

        return self.STYLE_FAMILIES.get(self.locked_style, None)

    def get_blocked_search_terms(self) -> List[str]:
        """
        Get search terms that should be blocked (other style families).

        Returns:
            List of terms to exclude from search
        """
        if not self.locked_style:
            return []

        blocked = []
        for style, terms in self.STYLE_FAMILIES.items():
            if style != self.locked_style:
                blocked.extend(terms)

        return blocked

    def record_selection(self, source: str, search_query: str, image_url: str):
        """
        Record a visual selection and auto-lock style if not already locked.

        Args:
            source: Source of the image (e.g., 'bing', 'google', 'reuters')
            search_query: The search query used
            image_url: URL of the selected image
        """
        # Infer style from search query and source
        inferred_style = self._infer_style(search_query, source)

        self.selection_history.append({
            'source': source,
            'query': search_query,
            'url': image_url,
            'inferred_style': inferred_style
        })

        # Auto-lock style from first selection
        if not self.locked_style and inferred_style:
            self.locked_style = inferred_style
            logger.info(f"Style auto-locked to '{inferred_style}' based on first selection")

    def _infer_style(self, search_query: str, source: str) -> Optional[str]:
        """Infer the visual style from search query and source."""
        query_lower = search_query.lower()
        source_lower = source.lower()

        # Check each style family
        for style, terms in self.STYLE_FAMILIES.items():
            for term in terms:
                if term in query_lower or term in source_lower:
                    return style

        # Source-based inference
        if source_lower in ['reuters', 'ap', 'getty']:
            return 'photo'

        return None

    def should_use_image(self, slide_number: int, total_slides: int) -> bool:
        """
        Determine if a slide should have an image based on style settings.

        Args:
            slide_number: 1-indexed slide number
            total_slides: Total slides in carousel

        Returns:
            True if image should be used, False for text-only
        """
        # Text-only mode
        if self.is_text_only_mode():
            return False

        # Hook and CTA slides typically don't need images
        if slide_number == 1 or slide_number == total_slides:
            return False

        return True

    def filter_search_query(self, original_query: str) -> str:
        """
        Filter search query to match locked style.

        Adds style-specific terms and removes conflicting terms.

        Args:
            original_query: The original search query

        Returns:
            Modified query optimized for style consistency
        """
        if not self.locked_style:
            return original_query

        # Add style hint to query
        style_hint = self.STYLE_FAMILIES.get(self.locked_style, [''])[0]

        # Remove conflicting terms
        filtered_query = original_query
        for style, terms in self.STYLE_FAMILIES.items():
            if style != self.locked_style:
                for term in terms:
                    # Remove term if it appears as a whole word
                    filtered_query = re.sub(rf'\b{re.escape(term)}\b', '', filtered_query, flags=re.IGNORECASE)

        # Clean up extra spaces
        filtered_query = ' '.join(filtered_query.split())

        # Add style hint if not already present
        if style_hint and style_hint not in filtered_query.lower():
            filtered_query = f"{filtered_query} {style_hint}"

        return filtered_query.strip()

    def get_style_report(self) -> Dict:
        """Get a report of style tracking status."""
        return {
            'preferred_style': self.preferred_style,
            'locked_style': self.locked_style,
            'is_text_only': self.is_text_only_mode(),
            'selection_count': len(self.selection_history),
            'allowed_terms': self.get_allowed_search_terms(),
        }


# Convenience function
def select_carousel_visuals(
    slides: List[str],
    topic: Optional[str] = None
) -> Dict[int, VisualStrategy]:
    """
    Quick function to select visual strategies for carousel slides.

    Returns dict of {slide_number: VisualStrategy}
    """
    selector = VisualSelector()
    return selector.select_strategies_for_carousel(slides, topic)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Testing VisualSelector...")
    print("=" * 80)

    test_slides = [
        "Tapi creator economy bukan cuma soal influencer.",  # Hook - should be TEXT_ONLY
        "Ini soal transformasi fundamental: Dari tukang yang dibayar per jam...",  # Body - emotional
        "Ada 50 juta+ creator di Indonesia",  # Body - data
        "Presiden umumkan new policy untuk creator economy",  # Body - news
        "Follow untuk tips creator lainnya!",  # CTA - should be TEXT_ONLY
    ]

    selector = VisualSelector()
    strategies = selector.select_strategies_for_carousel(test_slides, topic="creative")

    print("\n" + "=" * 80)
    print("VISUAL STRATEGIES:")
    for num, strategy in strategies.items():
        print(f"\nSlide {num}:")
        print(f"  Visual Type: {strategy.visual_type.value}")
        print(f"  Skip Visual: {strategy.should_skip_visual}")
        print(f"  Reason: {strategy.reason}")
        if strategy.content_type_hint:
            print(f"  Content Hint: {strategy.content_type_hint}")

    print("\n" + "=" * 80)
    print("Done!")
