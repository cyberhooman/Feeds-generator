"""
Meme Author Agent - AI-Powered Original Meme Creation

This agent generates ORIGINAL memes using AI instead of fetching/matching existing ones.
It creates unique meme scripts that are culturally current and human-authentic.

Key differences from legacy meme system:
- Creates ORIGINAL content (no template matching)
- Produces meme scripts (SETUP + REACTION format)
- Generates image reaction types for visual rendering
- Self-validates content for authenticity

Output can be used with:
1. Image generation APIs (DALL-E, Midjourney, etc.)
2. Stock photo + text overlay systems
3. Custom illustration pipelines
"""

import re
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum

# Handle relative import for when running as module vs standalone
try:
    from .ai_client import get_ai_client
except ImportError:
    from ai_client import get_ai_client

logger = logging.getLogger(__name__)


# ============================================================================
# MEME INTENT TYPES
# ============================================================================

class MemeIntent(Enum):
    """Allowed meme intents - exactly one per meme."""
    SMUG_SUPERIORITY = "smug superiority"
    DELAYED_REGRET = "delayed regret"
    FAKE_OPTIMISM = "fake optimism"
    PAINFUL_SELF_AWARENESS = "painful self-awareness"
    QUIET_DISAPPOINTMENT = "quiet disappointment"
    IRONIC_CONFIDENCE = "ironic confidence"
    SUDDEN_REALIZATION = "sudden realization"


# ============================================================================
# IMAGE REACTION ARCHETYPES
# ============================================================================

IMAGE_REACTION_ARCHETYPES = [
    "disbelief stare",
    "forced smile hiding regret",
    "confident gesture before failure",
    "quiet rejection",
    "fake calm under stress",
    "smug knowing look",
    "exhausted acceptance",
    "nervous laughter",
    "dead inside smile",
    "moment of clarity",
    "subtle panic",
    "performative confidence",
    "hollow victory",
    "resigned acceptance",
]


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class MemeScript:
    """A generated original meme script."""
    intent: str
    setup: str  # Max 8 words
    reaction: str  # Max 6 words
    image_reaction_type: str
    is_valid: bool = True
    abort_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent": self.intent,
            "setup": self.setup,
            "reaction": self.reaction,
            "image_reaction_type": self.image_reaction_type,
            "is_valid": self.is_valid,
            "abort_reason": self.abort_reason
        }

    def __str__(self) -> str:
        if not self.is_valid:
            return f"ABORT: {self.abort_reason}"
        return f"INTENT: {self.intent}\nSETUP: {self.setup}\nREACTION: {self.reaction}\nIMAGE_REACTION_TYPE: {self.image_reaction_type}"


@dataclass
class TrendContext:
    """Optional trend context for meme generation."""
    emotional_tone: str  # e.g., "ironic", "exhausted", "chaotic"
    phrasing_style: str  # e.g., "short", "blunt", "deadpan"
    reaction_bias: str  # e.g., "disbelief > excitement"

    def to_prompt_section(self) -> str:
        return f"""TREND CONTEXT:
- Dominant emotional tone: {self.emotional_tone}
- Preferred phrasing style: {self.phrasing_style}
- Reaction bias: {self.reaction_bias}

Use this for STYLE guidance only. Do NOT quote or reuse any phrases."""


# ============================================================================
# MEME AUTHOR AGENT
# ============================================================================

MEME_AUTHOR_SYSTEM_PROMPT = """You are a Meme Author AI.

IMPORTANT CONSTRAINTS (non-negotiable):
- You must NOT search for, reference, copy, or reuse existing memes.
- You must NOT name or select specific meme templates.
- You must NOT browse KnowYourMeme, Reddit memes, or image-based meme sites.
- You must NOT reproduce jokes or captions found online.

Your job is to create ORIGINAL memes by:
1. Sensing current language and emotional trends (text-only signals)
2. Deciding the best meme logic
3. Producing a new meme script that feels human and current

You will receive:
- A factual or explanatory caption from another AI
- (Optional) A trend summary derived from recent text posts

---

STEP 1 — TREND INTERPRETATION
If trend data is provided, infer:
- dominant emotional tone (choose ONE)
- preferred phrasing style (short, blunt, deadpan, ironic, etc.)
- reaction bias (e.g. disbelief > excitement)

DO NOT quote or reuse any phrases verbatim.
This step is for STYLE only, not content.

---

STEP 2 — MEME INTENT
Choose exactly ONE intent:
- smug superiority
- delayed regret
- fake optimism
- painful self-awareness
- quiet disappointment
- ironic confidence
- sudden realization

---

STEP 3 — MEME SCRIPT (STRICT LIMITS)
Write a meme as a 2-part script:

SETUP:
- Max 8 words
- No explanation
- No commentary

REACTION or TWIST:
- Max 6 words
- Must emotionally contradict or resolve the setup

Rules:
- Must work even without an image
- If it sounds like a tweet, it is too long
- If it explains itself, ABORT

---

STEP 4 — IMAGE REACTION TYPE
Describe ONLY the reaction archetype, not a meme:
Examples:
- disbelief stare
- forced smile hiding regret
- confident gesture before failure
- quiet rejection
- fake calm under stress

---

STEP 5 — SELF-CHECK (MANDATORY)
Answer internally:
- Would a real human post this without context?
- Is this culturally current, not dated?
- Is this original and non-derivative?

If any answer is NO:
Output exactly:
ABORT: not meme-worthy

---

OUTPUT FORMAT (EXACT):
INTENT:
SETUP:
REACTION:
IMAGE_REACTION_TYPE:"""


class MemeAuthorAgent:
    """
    AI Agent that creates original memes from content captions.

    This replaces the template-matching approach with pure AI creativity,
    generating unique meme scripts that can be rendered with various backends.
    """

    def __init__(self, temperature: float = 0.8):
        """
        Initialize the Meme Author Agent.

        Args:
            temperature: AI temperature for creativity (0.7-0.9 recommended)
        """
        self.ai_client = get_ai_client()
        self.temperature = temperature
        logger.info("MemeAuthorAgent initialized")

    def create_meme(
        self,
        caption: str,
        trend_context: Optional[TrendContext] = None,
        language: str = "en"
    ) -> MemeScript:
        """
        Create an original meme from a caption.

        Args:
            caption: The factual/explanatory caption to turn into a meme
            trend_context: Optional trend context for style guidance
            language: Target language ("en" or "id" for Indonesian)

        Returns:
            MemeScript with the generated meme content
        """
        # Build the prompt
        user_prompt = self._build_prompt(caption, trend_context, language)

        try:
            response = self.ai_client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=MEME_AUTHOR_SYSTEM_PROMPT,
                max_tokens=500,
                temperature=self.temperature
            )

            # Parse the response
            meme_script = self._parse_response(response)

            # Validate the meme
            if meme_script.is_valid:
                meme_script = self._validate_meme(meme_script)

            return meme_script

        except Exception as e:
            logger.error(f"Meme creation failed: {e}")
            return MemeScript(
                intent="",
                setup="",
                reaction="",
                image_reaction_type="",
                is_valid=False,
                abort_reason=f"AI error: {str(e)}"
            )

    def create_memes_for_slides(
        self,
        slides: List[str],
        topic: str = None,
        trend_context: Optional[TrendContext] = None,
        language: str = "en",
        skip_first_last: bool = True
    ) -> Dict[int, MemeScript]:
        """
        Create original memes for a list of carousel slides.

        Args:
            slides: List of slide texts
            topic: Optional topic context (e.g., "finance", "tech")
            trend_context: Optional trend context for style
            language: Target language
            skip_first_last: Skip hook (first) and CTA (last) slides

        Returns:
            Dict mapping slide numbers (1-indexed) to MemeScript objects
        """
        memes = {}
        total_slides = len(slides)

        for i, slide_text in enumerate(slides, 1):
            # Skip first and last slides if requested
            if skip_first_last:
                if i == 1 or i == total_slides:
                    logger.info(f"Skipping slide {i} (hook/CTA)")
                    continue

            # Create context-aware caption
            caption = slide_text
            if topic:
                caption = f"[Topic: {topic}] {slide_text}"

            # Generate meme
            meme = self.create_meme(caption, trend_context, language)

            if meme.is_valid:
                memes[i] = meme
                logger.info(f"Slide {i}: Created meme with intent '{meme.intent}'")
            else:
                logger.info(f"Slide {i}: Meme aborted - {meme.abort_reason}")

        return memes

    def _build_prompt(
        self,
        caption: str,
        trend_context: Optional[TrendContext],
        language: str
    ) -> str:
        """Build the user prompt for meme generation."""
        parts = []

        # Add caption
        parts.append(f"CAPTION TO MEME-IFY:\n\"{caption}\"")

        # Add trend context if provided
        if trend_context:
            parts.append(trend_context.to_prompt_section())

        # Add language instruction
        if language == "id":
            parts.append("""
LANGUAGE: Indonesian (Bahasa Indonesia)
- Use Indonesian slang/casual language
- Target Gen-Z Indonesian audience
- Can mix with English words naturally""")
        else:
            parts.append("""
LANGUAGE: English
- Use current internet English
- Keep it universally relatable""")

        # Add generation instruction
        parts.append("""
Now create an ORIGINAL meme following the exact format:
INTENT:
SETUP:
REACTION:
IMAGE_REACTION_TYPE:

Remember: If it's not meme-worthy, output ABORT: not meme-worthy""")

        return "\n\n".join(parts)

    def _parse_response(self, response: str) -> MemeScript:
        """Parse AI response into MemeScript."""
        response = response.strip()

        # Check for abort
        if response.startswith("ABORT:") or "ABORT:" in response:
            abort_match = re.search(r'ABORT:\s*(.+)', response)
            reason = abort_match.group(1).strip() if abort_match else "not meme-worthy"
            return MemeScript(
                intent="",
                setup="",
                reaction="",
                image_reaction_type="",
                is_valid=False,
                abort_reason=reason
            )

        # Parse the structured output
        intent = self._extract_field(response, "INTENT")
        setup = self._extract_field(response, "SETUP")
        reaction = self._extract_field(response, "REACTION")
        image_reaction = self._extract_field(response, "IMAGE_REACTION_TYPE")

        # Validate required fields
        if not all([intent, setup, reaction, image_reaction]):
            return MemeScript(
                intent=intent or "",
                setup=setup or "",
                reaction=reaction or "",
                image_reaction_type=image_reaction or "",
                is_valid=False,
                abort_reason="Missing required fields in response"
            )

        return MemeScript(
            intent=intent,
            setup=setup,
            reaction=reaction,
            image_reaction_type=image_reaction,
            is_valid=True
        )

    def _extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract a field value from the response."""
        pattern = rf'{field_name}:\s*(.+?)(?=\n[A-Z_]+:|$)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _validate_meme(self, meme: MemeScript) -> MemeScript:
        """Validate meme script constraints."""
        # Check word counts
        setup_words = len(meme.setup.split())
        reaction_words = len(meme.reaction.split())

        if setup_words > 8:
            return MemeScript(
                intent=meme.intent,
                setup=meme.setup,
                reaction=meme.reaction,
                image_reaction_type=meme.image_reaction_type,
                is_valid=False,
                abort_reason=f"Setup too long ({setup_words} words, max 8)"
            )

        if reaction_words > 6:
            return MemeScript(
                intent=meme.intent,
                setup=meme.setup,
                reaction=meme.reaction,
                image_reaction_type=meme.image_reaction_type,
                is_valid=False,
                abort_reason=f"Reaction too long ({reaction_words} words, max 6)"
            )

        # Check intent is valid
        valid_intents = [i.value for i in MemeIntent]
        if meme.intent.lower() not in valid_intents:
            logger.warning(f"Non-standard intent: {meme.intent}")
            # Don't fail for this, just warn

        return meme

    def get_image_generation_prompt(self, meme: MemeScript) -> str:
        """
        Generate a prompt for image generation APIs (DALL-E, Midjourney, etc.).

        Args:
            meme: The MemeScript to generate an image for

        Returns:
            Image generation prompt string
        """
        if not meme.is_valid:
            return ""

        # Build image generation prompt
        prompt = f"""Create a meme-style reaction image.

REACTION TYPE: {meme.image_reaction_type}

Style requirements:
- Clean, simple composition
- Focus on facial expression or body language
- Suitable for text overlay
- Modern, relatable aesthetic
- No text in the image itself

The image should convey: {meme.intent}

This will be paired with:
SETUP: "{meme.setup}"
REACTION: "{meme.reaction}"

Generate a versatile reaction image that works with this emotional beat."""

        return prompt

    def get_stock_photo_keywords(self, meme: MemeScript) -> List[str]:
        """
        Generate keywords for finding appropriate stock photos.

        Args:
            meme: The MemeScript to find images for

        Returns:
            List of search keywords
        """
        if not meme.is_valid:
            return []

        # Map reaction types to search keywords
        reaction_to_keywords = {
            "disbelief stare": ["shocked face", "surprised person", "disbelief expression"],
            "forced smile hiding regret": ["fake smile", "nervous smile", "awkward smile"],
            "confident gesture before failure": ["confident person", "thumbs up", "overconfident"],
            "quiet rejection": ["saying no", "rejection", "disappointed face"],
            "fake calm under stress": ["calm under pressure", "pretending calm", "stressed smile"],
            "smug knowing look": ["smug face", "knowing smile", "satisfied expression"],
            "exhausted acceptance": ["tired person", "exhausted", "resigned"],
            "nervous laughter": ["nervous laugh", "awkward laugh", "uncomfortable smile"],
            "dead inside smile": ["fake happiness", "dead eyes smile", "hollow smile"],
            "moment of clarity": ["realization", "aha moment", "sudden understanding"],
            "subtle panic": ["hidden panic", "worried face", "subtle fear"],
            "performative confidence": ["fake confidence", "showing off", "bravado"],
            "hollow victory": ["empty win", "pyrrhic victory", "bittersweet"],
            "resigned acceptance": ["acceptance", "giving up", "resigned sigh"],
        }

        # Get keywords for this reaction type
        keywords = []
        for reaction, kws in reaction_to_keywords.items():
            if reaction.lower() in meme.image_reaction_type.lower():
                keywords.extend(kws)
                break

        # Add intent-based keywords
        intent_keywords = {
            "smug superiority": ["smug", "superior", "condescending"],
            "delayed regret": ["regret", "hindsight", "mistake"],
            "fake optimism": ["false hope", "optimistic", "denial"],
            "painful self-awareness": ["self-aware", "cringe", "realization"],
            "quiet disappointment": ["disappointed", "let down", "sad"],
            "ironic confidence": ["ironic", "sarcastic", "confident"],
            "sudden realization": ["epiphany", "realization", "surprised"],
        }

        if meme.intent.lower() in intent_keywords:
            keywords.extend(intent_keywords[meme.intent.lower()])

        return list(set(keywords))[:5]  # Return unique, max 5


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_meme_from_caption(
    caption: str,
    language: str = "en",
    emotional_tone: str = None,
    phrasing_style: str = None
) -> MemeScript:
    """
    Quick function to create a single meme from a caption.

    Args:
        caption: The text to turn into a meme
        language: "en" or "id"
        emotional_tone: Optional emotional tone guidance
        phrasing_style: Optional phrasing style guidance

    Returns:
        MemeScript object
    """
    agent = MemeAuthorAgent()

    trend_context = None
    if emotional_tone or phrasing_style:
        trend_context = TrendContext(
            emotional_tone=emotional_tone or "neutral",
            phrasing_style=phrasing_style or "blunt",
            reaction_bias="authentic > performative"
        )

    return agent.create_meme(caption, trend_context, language)


def create_memes_for_carousel(
    slides: List[str],
    topic: str = None,
    language: str = "en"
) -> Dict[int, MemeScript]:
    """
    Quick function to create memes for carousel slides.

    Args:
        slides: List of slide texts
        topic: Optional topic context
        language: "en" or "id"

    Returns:
        Dict mapping slide numbers to MemeScript objects
    """
    agent = MemeAuthorAgent()
    return agent.create_memes_for_slides(slides, topic, language=language)


# ============================================================================
# TEST / DEMO
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Testing MemeAuthorAgent...")
    print("=" * 60)

    agent = MemeAuthorAgent()

    # Test single meme creation
    test_captions = [
        "90% of traders lose money because they don't have a proper risk management strategy",
        "Working from home means your cat is now your coworker",
        "Learning a new programming language takes about 3 months of consistent practice",
        "Most people check their phone 96 times per day on average",
    ]

    print("\n1. SINGLE MEME CREATION TEST")
    print("-" * 40)

    for caption in test_captions:
        print(f"\nCaption: {caption[:50]}...")
        meme = agent.create_meme(caption, language="en")
        print(f"Result:\n{meme}")

        if meme.is_valid:
            print(f"\nStock photo keywords: {agent.get_stock_photo_keywords(meme)}")
        print("-" * 40)

    # Test carousel creation
    print("\n2. CAROUSEL MEME CREATION TEST")
    print("-" * 40)

    carousel_slides = [
        "Why 90% of traders fail",  # Hook - will be skipped
        "They think more trades = more profits. But actually, overtrading kills your account.",
        "The real secret? Wait for high-probability setups. Quality over quantity.",
        "Step 1: Define your strategy\nStep 2: Backtest it\nStep 3: Stick to it",
        "Follow for more trading tips!"  # CTA - will be skipped
    ]

    print("\nCreating memes for carousel (5 slides, skipping first/last)...")
    memes = agent.create_memes_for_slides(carousel_slides, topic="trading", language="en")

    print(f"\nGenerated {len(memes)} memes:")
    for slide_num, meme in memes.items():
        print(f"\nSlide {slide_num}:")
        print(f"  Original: {carousel_slides[slide_num-1][:40]}...")
        print(f"  {meme}")

    # Test Indonesian
    print("\n3. INDONESIAN MEME TEST")
    print("-" * 40)

    indo_caption = "Banyak orang gagal investasi karena FOMO beli di puncak"
    meme = agent.create_meme(indo_caption, language="id")
    print(f"\nCaption: {indo_caption}")
    print(f"Result:\n{meme}")

    print("\n" + "=" * 60)
    print("Testing complete!")
