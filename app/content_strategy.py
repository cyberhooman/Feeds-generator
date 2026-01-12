"""
Content Strategy Module - Controls narrative arc and visual selection strategy.

This module defines the content purpose, visual role, and narrative beat system
that ensures visuals match the emotional arc of each carousel.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional


class ContentPurpose(Enum):
    """The primary purpose of the carousel content."""
    EDUCATIONAL = "educational"
    MOTIVATIONAL = "motivational"
    STORYTELLING = "storytelling"


class VisualRole(Enum):
    """How visuals should support the message."""
    AMPLIFY_EMOTION = "amplify_emotion"
    PROVIDE_EVIDENCE = "provide_evidence"
    MINIMAL = "minimal"


class VisualStyle(Enum):
    """Visual style family to maintain consistency."""
    AUTO = "auto"
    CARTOON = "cartoon"
    MOVIE = "movie"
    PHOTO = "photo"
    DIAGRAM = "diagram"
    TEXT_ONLY = "text_only"


class NarrativeBeat(Enum):
    """Narrative beats for slide-by-slide emotional arc."""
    # Educational beats
    PROBLEM_STATEMENT = "problem_statement"
    CONTEXT_SETTING = "context_setting"
    EXPLANATION = "explanation"
    APPLICATION = "application"
    SUMMARY = "summary"

    # Motivational beats
    PAIN_POINT = "pain_point"
    EMPATHY = "empathy"
    SHIFT_MOMENT = "shift_moment"
    NEW_PERSPECTIVE = "new_perspective"
    ACTION = "action"

    # Storytelling beats
    HOOK = "hook"
    TENSION_BUILD = "tension_build"
    CONFLICT_PEAK = "conflict_peak"
    RESOLUTION = "resolution"
    TAKEAWAY = "takeaway"

    # Common beats
    CTA = "cta"
    BODY = "body"  # Generic body slide


@dataclass
class BeatVisualMood:
    """Visual mood characteristics for a narrative beat."""
    mood: str
    energy: str
    search_hints: List[str]
    avoid_hints: List[str]


# Narrative arc definitions - which beats appear in which order
NARRATIVE_ARCS: Dict[ContentPurpose, List[NarrativeBeat]] = {
    ContentPurpose.EDUCATIONAL: [
        NarrativeBeat.PROBLEM_STATEMENT,  # Slide 1 - Hook with tension
        NarrativeBeat.CONTEXT_SETTING,     # Slide 2
        NarrativeBeat.EXPLANATION,         # Slides 3-5
        NarrativeBeat.EXPLANATION,
        NarrativeBeat.EXPLANATION,
        NarrativeBeat.APPLICATION,         # Slide 6
        NarrativeBeat.CTA,                 # Slide 7
    ],
    ContentPurpose.MOTIVATIONAL: [
        NarrativeBeat.PAIN_POINT,          # Slide 1 - Relatable struggle
        NarrativeBeat.EMPATHY,             # Slide 2
        NarrativeBeat.SHIFT_MOMENT,        # Slide 3
        NarrativeBeat.NEW_PERSPECTIVE,     # Slides 4-5
        NarrativeBeat.NEW_PERSPECTIVE,
        NarrativeBeat.ACTION,              # Slide 6
        NarrativeBeat.CTA,                 # Slide 7
    ],
    ContentPurpose.STORYTELLING: [
        NarrativeBeat.HOOK,                # Slide 1 - Dramatic opening
        NarrativeBeat.TENSION_BUILD,       # Slide 2
        NarrativeBeat.CONFLICT_PEAK,       # Slide 3
        NarrativeBeat.RESOLUTION,          # Slides 4-5
        NarrativeBeat.RESOLUTION,
        NarrativeBeat.TAKEAWAY,            # Slide 6
        NarrativeBeat.CTA,                 # Slide 7
    ],
}


# Beat to visual mood mapping - controls image search strategy
BEAT_VISUAL_MOODS: Dict[NarrativeBeat, BeatVisualMood] = {
    # Educational beats
    NarrativeBeat.PROBLEM_STATEMENT: BeatVisualMood(
        mood="confused",
        energy="tense",
        search_hints=["confusion", "frustrated person", "problem", "challenge", "stuck"],
        avoid_hints=["happy", "celebration", "success"]
    ),
    NarrativeBeat.CONTEXT_SETTING: BeatVisualMood(
        mood="observational",
        energy="calm",
        search_hints=["thinking", "analyzing", "observing", "background", "context"],
        avoid_hints=["action", "intense", "dramatic"]
    ),
    NarrativeBeat.EXPLANATION: BeatVisualMood(
        mood="clear",
        energy="focused",
        search_hints=["diagram", "framework", "illustration", "explaining", "teaching"],
        avoid_hints=["meme", "funny", "random"]
    ),
    NarrativeBeat.APPLICATION: BeatVisualMood(
        mood="motivated",
        energy="active",
        search_hints=["doing", "action", "applying", "working", "implementing"],
        avoid_hints=["passive", "confused", "stuck"]
    ),
    NarrativeBeat.SUMMARY: BeatVisualMood(
        mood="conclusive",
        energy="calm",
        search_hints=["conclusion", "summary", "key point", "takeaway"],
        avoid_hints=["question", "confusion", "problem"]
    ),

    # Motivational beats
    NarrativeBeat.PAIN_POINT: BeatVisualMood(
        mood="frustrated",
        energy="low",
        search_hints=["struggling", "exhausted", "frustrated", "tired", "overwhelmed"],
        avoid_hints=["happy", "success", "celebration", "excited"]
    ),
    NarrativeBeat.EMPATHY: BeatVisualMood(
        mood="understanding",
        energy="gentle",
        search_hints=["comfort", "support", "understanding", "listening", "compassion"],
        avoid_hints=["alone", "isolated", "aggressive"]
    ),
    NarrativeBeat.SHIFT_MOMENT: BeatVisualMood(
        mood="realization",
        energy="rising",
        search_hints=["aha moment", "realization", "lightbulb", "epiphany", "surprised"],
        avoid_hints=["confused", "sad", "stuck"]
    ),
    NarrativeBeat.NEW_PERSPECTIVE: BeatVisualMood(
        mood="hopeful",
        energy="rising",
        search_hints=["hope", "new beginning", "sunrise", "bright", "optimistic"],
        avoid_hints=["dark", "gloomy", "pessimistic"]
    ),
    NarrativeBeat.ACTION: BeatVisualMood(
        mood="determined",
        energy="high",
        search_hints=["determined", "moving forward", "action", "progress", "momentum"],
        avoid_hints=["passive", "waiting", "stuck"]
    ),

    # Storytelling beats
    NarrativeBeat.HOOK: BeatVisualMood(
        mood="intriguing",
        energy="high",
        search_hints=["dramatic", "attention", "opening", "mysterious", "compelling"],
        avoid_hints=["boring", "plain", "mundane"]
    ),
    NarrativeBeat.TENSION_BUILD: BeatVisualMood(
        mood="anxious",
        energy="rising",
        search_hints=["tension", "suspense", "anticipation", "building", "stakes"],
        avoid_hints=["relaxed", "calm", "peaceful"]
    ),
    NarrativeBeat.CONFLICT_PEAK: BeatVisualMood(
        mood="intense",
        energy="peak",
        search_hints=["climax", "confrontation", "intense", "peak", "turning point"],
        avoid_hints=["calm", "peaceful", "resolved"]
    ),
    NarrativeBeat.RESOLUTION: BeatVisualMood(
        mood="relieved",
        energy="calming",
        search_hints=["relief", "resolution", "peace", "solved", "transformed"],
        avoid_hints=["tension", "conflict", "problem"]
    ),
    NarrativeBeat.TAKEAWAY: BeatVisualMood(
        mood="wise",
        energy="calm",
        search_hints=["wisdom", "lesson", "reflection", "contemplation", "insight"],
        avoid_hints=["action", "intense", "dramatic"]
    ),

    # Common beats
    NarrativeBeat.CTA: BeatVisualMood(
        mood="inviting",
        energy="warm",
        search_hints=["invitation", "welcome", "join", "together"],
        avoid_hints=["aggressive", "pushy", "desperate"]
    ),
    NarrativeBeat.BODY: BeatVisualMood(
        mood="neutral",
        energy="moderate",
        search_hints=["relevant", "matching", "appropriate"],
        avoid_hints=["random", "unrelated", "off-topic"]
    ),
}


# Visual style to allowed sources mapping
STYLE_TO_SOURCES: Dict[VisualStyle, List[str]] = {
    VisualStyle.CARTOON: ["cartoon", "anime", "spongebob", "simpsons", "animated"],
    VisualStyle.MOVIE: ["movie scene", "film still", "tv show", "cinema"],
    VisualStyle.PHOTO: ["stock photo", "professional photo", "real photo"],
    VisualStyle.DIAGRAM: ["diagram", "chart", "infographic", "illustration", "graph"],
    VisualStyle.TEXT_ONLY: [],  # No images
    VisualStyle.AUTO: None,  # Allow all sources
}


# Content purpose to recommended visual styles
PURPOSE_VISUAL_RECOMMENDATIONS: Dict[ContentPurpose, Dict[VisualRole, List[VisualStyle]]] = {
    ContentPurpose.EDUCATIONAL: {
        VisualRole.AMPLIFY_EMOTION: [VisualStyle.DIAGRAM, VisualStyle.PHOTO],
        VisualRole.PROVIDE_EVIDENCE: [VisualStyle.DIAGRAM, VisualStyle.PHOTO],
        VisualRole.MINIMAL: [VisualStyle.TEXT_ONLY],
    },
    ContentPurpose.MOTIVATIONAL: {
        VisualRole.AMPLIFY_EMOTION: [VisualStyle.PHOTO, VisualStyle.MOVIE],
        VisualRole.PROVIDE_EVIDENCE: [VisualStyle.PHOTO],
        VisualRole.MINIMAL: [VisualStyle.TEXT_ONLY],
    },
    ContentPurpose.STORYTELLING: {
        VisualRole.AMPLIFY_EMOTION: [VisualStyle.MOVIE, VisualStyle.CARTOON, VisualStyle.PHOTO],
        VisualRole.PROVIDE_EVIDENCE: [VisualStyle.PHOTO, VisualStyle.MOVIE],
        VisualRole.MINIMAL: [VisualStyle.TEXT_ONLY],
    },
}


def get_narrative_beat_for_slide(
    slide_number: int,
    total_slides: int,
    content_purpose: ContentPurpose
) -> NarrativeBeat:
    """
    Get the appropriate narrative beat for a slide based on its position.

    Args:
        slide_number: 1-indexed slide number
        total_slides: Total number of slides in carousel
        content_purpose: The content purpose (educational, motivational, storytelling)

    Returns:
        The narrative beat for this slide position
    """
    arc = NARRATIVE_ARCS.get(content_purpose, NARRATIVE_ARCS[ContentPurpose.STORYTELLING])

    # Last slide is always CTA
    if slide_number == total_slides:
        return NarrativeBeat.CTA

    # Map slide position to arc beat
    # Arc has 7 beats, but carousel might have different number of slides
    arc_position = int((slide_number - 1) * (len(arc) - 1) / max(total_slides - 1, 1))
    arc_position = min(arc_position, len(arc) - 2)  # Don't include CTA in mapping

    return arc[arc_position]


def get_visual_mood_for_beat(beat: NarrativeBeat) -> BeatVisualMood:
    """Get the visual mood characteristics for a narrative beat."""
    return BEAT_VISUAL_MOODS.get(beat, BEAT_VISUAL_MOODS[NarrativeBeat.BODY])


def should_skip_visual(
    slide_number: int,
    total_slides: int,
    visual_role: VisualRole,
    narrative_beat: NarrativeBeat
) -> bool:
    """
    Determine if a slide should skip visual selection.

    Args:
        slide_number: 1-indexed slide number
        total_slides: Total number of slides
        visual_role: The visual role setting
        narrative_beat: The narrative beat for this slide

    Returns:
        True if visual should be skipped
    """
    # Minimal mode: skip most visuals
    if visual_role == VisualRole.MINIMAL:
        # Only allow visuals for EXPLANATION beats in minimal mode
        return narrative_beat != NarrativeBeat.EXPLANATION

    # CTA slides typically don't need visuals
    if narrative_beat == NarrativeBeat.CTA:
        return True

    # Hook slides (slide 1) often work better as text-only
    if slide_number == 1:
        return True

    return False


def get_search_modifiers_for_purpose(
    content_purpose: ContentPurpose,
    visual_role: VisualRole
) -> Dict[str, any]:
    """
    Get search query modifiers based on content purpose and visual role.

    Returns dict with:
        - exclude_terms: Terms to exclude from search
        - include_terms: Terms to include in search
        - source_preference: Preferred image sources
    """
    modifiers = {
        "exclude_terms": [],
        "include_terms": [],
        "source_preference": []
    }

    if content_purpose == ContentPurpose.EDUCATIONAL:
        modifiers["exclude_terms"] = ["meme", "funny", "joke", "reaction"]
        modifiers["include_terms"] = ["professional", "clean", "diagram"]
        modifiers["source_preference"] = ["diagram", "illustration", "stock"]

    elif content_purpose == ContentPurpose.MOTIVATIONAL:
        modifiers["exclude_terms"] = ["meme", "cartoon", "joke"]
        modifiers["include_terms"] = ["inspirational", "emotional", "powerful"]
        modifiers["source_preference"] = ["photo", "cinematic"]

    elif content_purpose == ContentPurpose.STORYTELLING:
        modifiers["exclude_terms"] = ["template", "generic"]
        modifiers["include_terms"] = ["scene", "narrative", "story"]
        modifiers["source_preference"] = ["movie", "cartoon", "scene"]

    # Visual role adjustments
    if visual_role == VisualRole.PROVIDE_EVIDENCE:
        modifiers["include_terms"].extend(["real", "authentic", "documentary"])
        modifiers["exclude_terms"].extend(["artistic", "abstract"])

    return modifiers
