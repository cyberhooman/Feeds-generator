"""
Meme Search Agent - Enhanced Version

Automatically finds and downloads memes matching content.
Now with dynamic twist generation, cultural context, and variety.
"""

import os
import json
import re
import hashlib
import random
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, quote_plus
from .config import Config
from .ai_client import get_ai_client
from .meme_matcher import EMOTION_MEME_MATRIX, TOPIC_MEME_MATRIX


# ============================================================================
# MEME TWIST TEMPLATES - For genuinely funny content
# ============================================================================

TWIST_TEMPLATES = {
    "drake_format.jpg": {
        "type": "template",
        "structure": {
            "reject": "The 'wrong' choice that everyone does",
            "approve": "The twist - either ironically worse or unexpectedly good"
        },
        "examples": [
            {"reject": "Invest ke saham blue chip", "approve": "YOLO semua ke shitcoin"},
            {"reject": "Baca analisis fundamental", "approve": "Percaya 'sinyal' dari grup WA"},
            {"reject": "Diversifikasi portfolio", "approve": "ALL IN satu saham doang"}
        ],
        "humor_style": "ironic_comparison"
    },
    "clown_makeup.jpg": {
        "type": "template",
        "structure": {
            "step1": "First reasonable-sounding mistake",
            "step2": "Doubling down on mistake",
            "step3": "Even worse decision",
            "step4": "Final disaster realization"
        },
        "examples": [
            {
                "step1": "Ini pasti cuma koreksi",
                "step2": "Saatnya average down",
                "step3": "Pake margin biar cuan gede",
                "step4": "Liqiudated -100%"
            }
        ],
        "humor_style": "self_deprecating_escalation"
    },
    "galaxy_brain.jpg": {
        "type": "template",
        "structure": {
            "small_brain": "Normie take (what everyone thinks)",
            "medium_brain": "Slightly better understanding",
            "big_brain": "Advanced take",
            "galaxy_brain": "Twist - either enlightened or absurdly dumb"
        },
        "examples": [
            {
                "small_brain": "Nabung di bank",
                "medium_brain": "Invest di reksadana",
                "big_brain": "Diversifikasi asset class",
                "galaxy_brain": "Duit semua jadi kuota buat scroll TikTok"
            }
        ],
        "humor_style": "escalating_absurdity"
    },
    "shocked_pikachu.jpg": {
        "type": "reaction",
        "structure": {
            "setup_text": "Action with obvious consequence",
            "caption": "The obvious consequence presented as surprise"
        },
        "examples": [
            {"setup_text": "Pake leverage 100x tanpa stop loss:", "caption": "Liquidated"},
            {"setup_text": "Skip research, langsung all-in:", "caption": "-80%"}
        ],
        "humor_style": "ironic_surprise"
    },
    "crying_cat.jpg": {
        "type": "reaction",
        "structure": {
            "setup_text": "Relatable painful situation",
            "caption": "Short punchline (pain)"
        },
        "examples": [
            {"setup_text": "Gua yakin ini bottom", "caption": "Bottom terus setiap hari"},
            {"setup_text": "Cuman check portfolio bentar", "caption": "-2 juta dalam 5 menit"}
        ],
        "humor_style": "relatable_pain"
    },
    "this_is_fine.jpg": {
        "type": "reaction",
        "structure": {
            "setup_text": "Disaster happening",
            "caption": "Denial/copium statement"
        },
        "examples": [
            {"setup_text": "Portfolio -50%", "caption": "iNi DiScOuNt SeAsOn"},
            {"setup_text": "Inflasi 6%, gaji naik 3%", "caption": "Masih bersyukur ada kerjaan"}
        ],
        "humor_style": "copium_denial"
    },
    "distracted_boyfriend.jpg": {
        "type": "template",
        "structure": {
            "girlfriend": "What you should focus on",
            "boyfriend": "You (the distracted one)",
            "other_girl": "The distraction"
        },
        "examples": [
            {"girlfriend": "Emergency fund", "boyfriend": "Gua", "other_girl": "iPhone 15 Pro Max"}
        ],
        "humor_style": "ironic_priorities"
    },
    "stonks.jpg": {
        "type": "reaction",
        "structure": {
            "setup_text": "Questionable 'win'",
            "caption": "Stonks (ironic)"
        },
        "examples": [
            {"setup_text": "Rugi cuma 10% (bukan 50%)", "caption": "Basically profit"},
            {"setup_text": "Dapat cashback 5rb, belanja 500rb", "caption": "Stonks"}
        ],
        "humor_style": "ironic_victory"
    }
}

# Slang dictionary for authentic Indonesian Gen-Z voice
GENZ_SLANG = {
    "patterns": {
        "emphasis": ["bgt", "banget", "parah", "gila", "anjir"],
        "pain": ["boncos", "jebol", "tewas", "mampus", "hancur"],
        "profit": ["cuan", "profit", "untung gede", "jackpot"],
        "denial": ["gpp", "santai", "fine", "chill", "cope"],
        "realization": ["ternyata", "anjir", "baru nyadar", "wait", "hold up"]
    },
    "replacements": {
        "I": ["gua", "gue", "w"],
        "you": ["lu", "lo", "u"],
        "very": ["bgt", "banget"],
        "money": ["duit", "cuan"],
        "expensive": ["mahal bgt", "gila harganya"],
        "but": ["tapi", "tp"]
    }
}


class MemeSearchAgent:
    """
    AI-powered agent that automatically finds memes matching content themes.
    Enhanced with cultural twist generation and variety.
    """

    def __init__(self):
        self.client = get_ai_client()
        self.meme_dir = Config.MEME_IMAGES_DIR
        self.cache_dir = Config.BASE_DIR / "cache" / "memes"
        self.metadata_path = Config.MEME_METADATA_PATH
        self.metadata = self._load_metadata()
        self.twist_templates = TWIST_TEMPLATES

        # Ensure directories exist
        self.meme_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _load_metadata(self) -> Dict:
        """Load existing meme metadata"""
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_metadata(self):
        """Save metadata to file"""
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

    def analyze_content_for_memes(self, slides: List[str]) -> List[Dict]:
        """
        Analyze slides content and determine what memes would fit best.
        Returns list of meme requirements per slide with twists.
        """
        slides_text = "\n\n".join([f"Slide {i+1}: {slide}" for i, slide in enumerate(slides)])

        prompt = f"""Analyze this Instagram carousel and suggest SPECIFIC memes with FUNNY twists.

CONTENT:
{slides_text}

For each slide, provide:
1. Emotional beat (irony, pain, revelation, shock, comparison, escalation, denial)
2. Best meme match
3. SPECIFIC twist content (not generic!)

Available memes:
- drake_format.jpg (compare good vs bad, but with ironic twist)
- clown_makeup.jpg (4 steps of bad decisions)
- galaxy_brain.jpg (4 levels, twist at the end)
- shocked_pikachu.jpg (obvious cause -> "surprise" effect)
- crying_cat.jpg (relatable financial/emotional pain)
- this_is_fine.jpg (denial/copium)
- distracted_boyfriend.jpg (wrong priorities)
- stonks.jpg (ironic "wins")

IMPORTANT - Make the humor:
- SPECIFIC (exact numbers, real situations)
- SELF-DEPRECATING (we're all clowns together)
- CULTURALLY RELEVANT (Indonesian Gen-Z references)
- SUBVERSIVE (flip expectations)

Respond in JSON:
{{
    "slides": [
        {{
            "slide_num": 1,
            "emotional_beat": "shock",
            "needs_meme": true,
            "meme_suggestion": "shocked_pikachu.jpg",
            "meme_content": {{
                "setup_text": "All-in crypto pas ATH:",
                "caption": "-70% sebulan kemudian"
            }},
            "humor_type": "ironic_surprise",
            "reason": "Perfect for 'obvious disaster' humor"
        }}
    ]
}}

Some slides work better text-only. Don't force memes where they don't fit.
"""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2500,
                temperature=0.7  # Higher for more creative twists
            )

            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("slides", [])
            return []

        except Exception as e:
            print(f"Error analyzing content: {e}")
            return []

    def generate_meme_twist_for_slide(
        self,
        slide_text: str,
        meme_file: str,
        topic: str = "general"
    ) -> Dict:
        """
        Generate a specific, funny twist for a meme based on slide content.
        This is the core humor generation function.
        """
        template = self.twist_templates.get(meme_file, {})
        meme_type = template.get("type", "reaction")
        structure = template.get("structure", {})
        examples = template.get("examples", [])
        humor_style = template.get("humor_style", "ironic")

        # Build example text for AI
        example_text = ""
        if examples:
            example = random.choice(examples)
            example_text = f"Example style: {json.dumps(example, ensure_ascii=False)}"

        prompt = f"""Generate FUNNY meme content for this slide.

SLIDE TEXT: {slide_text}
MEME: {meme_file}
TOPIC: {topic}
HUMOR STYLE: {humor_style}

MEME STRUCTURE:
{json.dumps(structure, indent=2)}

{example_text}

RULES FOR ACTUAL HUMOR:
1. SPECIFICITY - Use exact numbers ("rugi 2.3 juta" not "rugi banyak")
2. SUBVERSION - The punchline flips expectations
3. RELATABILITY - Common experience we all share
4. CULTURAL CONTEXT - Indonesian Gen-Z references
5. BREVITY - Max 6-8 words per panel, 3-5 for punchlines

Examples of GOOD vs BAD humor:
- BAD: "Invest wisely" vs "Don't invest wisely"
- GOOD: "Invest di reksadana" vs "YOLO ke shitcoin based on TikTok tip"

- BAD: "I made a mistake"
- GOOD: "Portfolio -47% tapi yakin ini cuma koreksi sehat"

Return ONLY JSON with the meme content:
{{
    "meme_type": "{meme_type}",
    {"panels" if meme_type == "template" else "setup_text"}: ...,
    {"" if meme_type == "template" else "caption"}: ...,
    "humor_type": "{humor_style}",
    "punchline_strength": "1-10 rating"
}}"""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.85  # High for creative humor
            )

            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())

        except Exception as e:
            print(f"Twist generation error: {e}")

        # Fallback with template-specific defaults
        return self._get_fallback_twist(meme_file, slide_text)

    def _get_fallback_twist(self, meme_file: str, slide_text: str) -> Dict:
        """Generate a fallback twist if AI fails."""
        template = self.twist_templates.get(meme_file, {})
        meme_type = template.get("type", "reaction")

        if meme_type == "template":
            if "drake" in meme_file:
                return {
                    "meme_type": "template",
                    "panels": {
                        "reject": "Yang seharusnya dilakukan",
                        "approve": "Yang actually gua lakukan"
                    }
                }
            elif "clown" in meme_file:
                return {
                    "meme_type": "template",
                    "panels": {
                        "step1": "Langkah pertama",
                        "step2": "Makin parah",
                        "step3": "Lebih parah lagi",
                        "step4": "Disaster"
                    }
                }
            elif "galaxy" in meme_file or "brain" in meme_file:
                return {
                    "meme_type": "template",
                    "panels": {
                        "small_brain": "Normie level",
                        "medium_brain": "Getting there",
                        "big_brain": "Almost enlightened",
                        "galaxy_brain": "Plot twist"
                    }
                }
        else:
            return {
                "meme_type": "reaction",
                "setup_text": slide_text[:60] + ":",
                "caption": "* visible pain *"
            }

        return {"meme_type": "reaction", "setup_text": "", "caption": ""}

    def check_meme_exists(self, meme_name: str) -> Optional[str]:
        """
        Check if we already have a meme matching this name.
        Returns filename if exists, None otherwise.
        """
        normalized = meme_name.lower().replace(" ", "_").replace("-", "_")

        # Check metadata
        for filename in self.metadata.keys():
            file_normalized = filename.lower().replace(" ", "_").replace("-", "_")
            file_normalized = file_normalized.rsplit(".", 1)[0]
            if normalized in file_normalized or file_normalized in normalized:
                return filename

        # Check meme directory
        for file_path in self.meme_dir.glob("*"):
            if file_path.is_file():
                file_normalized = file_path.stem.lower().replace(" ", "_").replace("-", "_")
                if normalized in file_normalized or file_normalized in normalized:
                    return file_path.name

        # Check cache directory
        for file_path in self.cache_dir.glob("*"):
            if file_path.is_file():
                file_normalized = file_path.stem.lower().replace(" ", "_").replace("-", "_")
                if normalized in file_normalized or file_normalized in normalized:
                    return file_path.name

        return None

    def generate_meme_metadata(self, meme_name: str, context: str = "") -> Dict:
        """Use AI to generate proper metadata for a meme."""
        prompt = f"""Generate metadata for this meme: "{meme_name}"
Context: {context if context else "General content"}

Provide in JSON:
{{
    "emotions": ["primary emotion", "secondary", "tertiary"],
    "context": ["best use case 1", "best use case 2"],
    "energy": "high/medium/low",
    "source": "Origin (movie, show, viral moment)",
    "best_for": ["topic 1", "topic 2", "topic 3"],
    "language_fit": ["indo", "english"],
    "caption_vibe": "When to use this meme in one sentence",
    "humor_type": "irony/self-deprecating/absurdist/relatable"
}}"""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )

            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())

        except Exception as e:
            print(f"Error generating metadata: {e}")

        return {
            "emotions": ["general"],
            "context": ["general"],
            "energy": "medium",
            "source": "Unknown",
            "best_for": ["general content"],
            "language_fit": ["indo", "english"],
            "caption_vibe": meme_name,
            "humor_type": "general"
        }

    def add_meme_to_library(self, filename: str, metadata: Dict) -> bool:
        """Add a meme to the library metadata."""
        self.metadata[filename] = metadata
        self._save_metadata()
        return True

    def find_memes_for_content(
        self,
        slides: List[str],
        auto_download: bool = False,
        generate_twists: bool = True
    ) -> Dict:
        """
        Main method: Analyze content and find/suggest memes with twists.

        Args:
            slides: List of slide texts
            auto_download: Whether to attempt downloading missing memes
            generate_twists: Whether to generate funny content for memes

        Returns:
            Dict with analysis, recommendations, and generated content
        """
        result = {
            "analysis": [],
            "available_memes": [],
            "missing_memes": [],
            "recommendations": [],
            "generated_twists": []  # New: AI-generated funny content
        }

        # Step 1: Analyze content with AI
        analysis = self.analyze_content_for_memes(slides)
        result["analysis"] = analysis

        # Step 2: Check availability and generate twists
        for slide_analysis in analysis:
            if not slide_analysis.get("needs_meme"):
                continue

            slide_num = slide_analysis.get("slide_num", 0)
            meme_suggestion = slide_analysis.get("meme_suggestion", "")

            if not meme_suggestion:
                continue

            # Normalize meme name
            if not meme_suggestion.endswith(('.jpg', '.png')):
                meme_suggestion = meme_suggestion.lower().replace(" ", "_") + ".jpg"

            # Check if we have this meme
            existing = self.check_meme_exists(meme_suggestion)

            meme_info = {
                "slide_num": slide_num,
                "meme_name": meme_suggestion,
                "filename": existing or meme_suggestion,
                "reason": slide_analysis.get("reason", ""),
                "emotional_beat": slide_analysis.get("emotional_beat", ""),
                "humor_type": slide_analysis.get("humor_type", "")
            }

            # Get or generate twist content
            if generate_twists:
                # Use AI-generated content from analysis if available
                meme_content = slide_analysis.get("meme_content", {})
                if not meme_content:
                    # Generate new twist
                    slide_text = slides[slide_num - 1] if slide_num <= len(slides) else ""
                    meme_content = self.generate_meme_twist_for_slide(
                        slide_text, meme_suggestion
                    )
                meme_info["meme_content"] = meme_content

            if existing:
                result["available_memes"].append(meme_info)
                result["recommendations"].append({
                    "slide_num": slide_num,
                    "filename": existing,
                    "confidence": 9,
                    "reason": slide_analysis.get("reason", ""),
                    "meme_content": meme_info.get("meme_content", {})
                })
            else:
                # We don't have this meme
                meme_info["suggested_filename"] = meme_suggestion
                meme_info["search_keywords"] = slide_analysis.get(
                    "search_keywords",
                    [meme_suggestion.replace("_", " ").replace(".jpg", "")]
                )

                # Generate metadata for when user adds it
                metadata = self.generate_meme_metadata(
                    meme_suggestion,
                    slides[slide_num - 1] if slide_num <= len(slides) else ""
                )
                meme_info["suggested_metadata"] = metadata

                result["missing_memes"].append(meme_info)

        return result

    def get_meme_download_instructions(self, missing_memes: List[Dict]) -> str:
        """Generate instructions for manually downloading missing memes."""
        if not missing_memes:
            return "All required memes are already in your library!"

        instructions = "## Missing Memes - Download Instructions\n\n"
        instructions += f"Save these memes to: `{self.cache_dir}`\n\n"

        for meme in missing_memes:
            instructions += f"### {meme.get('meme_name', 'Unknown')}\n"
            instructions += f"- **Save as:** `{meme.get('suggested_filename', meme.get('meme_name', 'meme') + '.jpg')}`\n"
            keywords = meme.get('search_keywords', [meme.get('meme_name', 'meme')])
            instructions += f"- **Search:** {', '.join(keywords)}\n"
            instructions += f"- **Sources:** Know Your Meme, Imgflip, Google Images\n"
            instructions += f"- **Purpose:** {meme.get('reason', 'N/A')}\n\n"

        instructions += "---\n"
        instructions += "After downloading, run 'Sync Library' to detect new memes.\n"

        return instructions

    def sync_library(self) -> Dict:
        """
        Sync meme library - detect new files and generate metadata.
        Checks both meme_library and cache directories.
        """
        changes = {
            "new_memes": [],
            "existing": [],
            "removed": []
        }

        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        current_files = set()

        # Check both directories
        for directory in [self.meme_dir, self.cache_dir]:
            if not directory.exists():
                continue

            for file_path in directory.glob("*"):
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    current_files.add(file_path.name)

        # Check for new files
        for filename in current_files:
            if filename not in self.metadata:
                meme_name = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
                metadata = self.generate_meme_metadata(meme_name)
                self.metadata[filename] = metadata
                changes["new_memes"].append(filename)
            else:
                changes["existing"].append(filename)

        # Check for removed files
        for filename in list(self.metadata.keys()):
            if filename not in current_files:
                del self.metadata[filename]
                changes["removed"].append(filename)

        self._save_metadata()
        return changes

    def suggest_memes_for_topic(self, topic: str, num_suggestions: int = 10) -> List[Dict]:
        """Suggest memes that would work well for a given topic."""
        prompt = f"""Suggest {num_suggestions} memes for Instagram carousel about: "{topic}"

Focus on:
- Highly recognizable memes
- Match Indonesian Gen-Z humor
- Provide SPECIFIC example twists (not generic)

For each meme:
1. Name and why it fits
2. Concrete example with actual funny content
3. Emotional beat it serves

JSON format:
{{
    "suggestions": [
        {{
            "meme_name": "crying_cat.jpg",
            "why_it_works": "Perfect for relatable financial pain",
            "example_twist": {{
                "setup_text": "Gua yakin ini bottom",
                "caption": "Bottom terus setiap minggu"
            }},
            "emotional_beat": "painful_truth",
            "humor_type": "self_deprecating"
        }}
    ]
}}"""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.6
            )

            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("suggestions", [])

        except Exception as e:
            print(f"Error suggesting memes: {e}")

        return []

    def get_random_meme_for_emotion(self, emotion: str) -> Optional[Dict]:
        """
        Get a random meme that matches the given emotion.
        Useful for variety in carousel generation.
        """
        emotion_memes = EMOTION_MEME_MATRIX.get(emotion, {}).get("memes", [])

        if not emotion_memes:
            # Default memes
            emotion_memes = ["drake_format.jpg", "crying_cat.jpg", "shocked_pikachu.jpg"]

        # Filter to available memes
        available = []
        for meme in emotion_memes:
            if self.check_meme_exists(meme):
                available.append(meme)

        if not available:
            return None

        chosen = random.choice(available)
        return {
            "filename": chosen,
            "emotion": emotion,
            "twist_template": EMOTION_MEME_MATRIX.get(emotion, {}).get("twist_template", "")
        }


def create_meme_agent() -> MemeSearchAgent:
    """Factory function to create meme search agent."""
    return MemeSearchAgent()
