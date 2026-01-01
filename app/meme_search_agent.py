"""
Meme Search Agent - Automatically finds and downloads memes matching content

Uses AI to analyze content emotional beats, then searches for matching memes.
"""

import os
import json
import re
import hashlib
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse, quote_plus
from .config import Config
from .ai_client import get_ai_client


class MemeSearchAgent:
    """
    AI-powered agent that automatically finds memes matching content themes.
    """

    def __init__(self):
        self.client = get_ai_client()
        self.meme_dir = Config.MEME_IMAGES_DIR
        self.metadata_path = Config.MEME_METADATA_PATH
        self.metadata = self._load_metadata()

        # Ensure meme directory exists
        self.meme_dir.mkdir(parents=True, exist_ok=True)

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

        Returns list of meme requirements per slide.
        """
        slides_text = "\n\n".join([f"Slide {i+1}: {slide}" for i, slide in enumerate(slides)])

        prompt = f"""Analyze this Instagram carousel content and suggest specific memes for each slide.

CONTENT:
{slides_text}

For each slide, determine:
1. The emotional beat (shock, pain, realization, humor, etc.)
2. The specific meme that would work best
3. Search keywords to find that meme

Focus on popular, recognizable memes that match the emotion. Consider:
- Shocked Pikachu - for obvious/ironic revelations
- Clown makeup - for self-deprecating irony
- This is fine dog - for denial/coping
- Crying cat/wojak - for financial pain
- Drake format - for comparisons
- Stonks/Not stonks - for financial gains/losses
- Galaxy brain - for explanations
- Trade offer - for deals/trade-offs
- Distracted boyfriend - for wrong priorities
- And other popular memes

Respond in this exact JSON format:
{{
    "slides": [
        {{
            "slide_num": 1,
            "emotional_beat": "shock/curiosity",
            "needs_meme": true,
            "meme_suggestion": "shocked pikachu",
            "search_keywords": ["shocked pikachu meme", "surprised pikachu template"],
            "reason": "Perfect for revealing surprising data"
        }},
        {{
            "slide_num": 2,
            "emotional_beat": "explanation",
            "needs_meme": false,
            "meme_suggestion": null,
            "search_keywords": [],
            "reason": "Text-focused slide, meme would distract"
        }}
    ]
}}

Only suggest memes where they genuinely add value. Some slides work better text-only.
"""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )

            # Parse JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("slides", [])
            return []

        except Exception as e:
            print(f"Error analyzing content: {e}")
            return []

    def search_meme_urls(self, keywords: List[str], num_results: int = 5) -> List[Dict]:
        """
        Search for meme image URLs using multiple sources.

        Returns list of potential meme URLs with metadata.
        """
        results = []

        # Use AI to generate search-optimized queries and find memes
        search_prompt = f"""I need to find meme images for these keywords: {', '.join(keywords)}

Suggest the best sources and direct image URLs where I can find this meme template.
Common meme sources:
- Know Your Meme (knowyourmeme.com)
- Imgflip (imgflip.com)
- Reddit meme subreddits
- Pinterest meme boards

For each keyword, provide:
1. The most recognizable version of this meme
2. Alternative names people might call it
3. Suggested filename for saving

Respond in JSON:
{{
    "meme_name": "Shocked Pikachu",
    "alt_names": ["Surprised Pikachu", "Pikachu Meme"],
    "suggested_filename": "shocked_pikachu.jpg",
    "emotions": ["shocked", "surprised", "disbelief"],
    "best_for": ["revelations", "obvious outcomes", "ironic surprise"],
    "search_query": "shocked pikachu meme template transparent"
}}
"""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": search_prompt}],
                max_tokens=1000,
                temperature=0.3
            )

            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                meme_info = json.loads(json_match.group())
                results.append(meme_info)

        except Exception as e:
            print(f"Error searching memes: {e}")

        return results

    def check_meme_exists(self, meme_name: str) -> Optional[str]:
        """
        Check if we already have a meme matching this name.
        Returns filename if exists, None otherwise.
        """
        # Normalize meme name for comparison
        normalized = meme_name.lower().replace(" ", "_").replace("-", "_")

        for filename in self.metadata.keys():
            file_normalized = filename.lower().replace(" ", "_").replace("-", "_")
            file_normalized = file_normalized.rsplit(".", 1)[0]  # Remove extension

            if normalized in file_normalized or file_normalized in normalized:
                return filename

        # Also check actual files in directory
        for file_path in self.meme_dir.glob("*"):
            if file_path.is_file():
                file_normalized = file_path.stem.lower().replace(" ", "_").replace("-", "_")
                if normalized in file_normalized or file_normalized in normalized:
                    return file_path.name

        return None

    def generate_meme_metadata(self, meme_name: str, context: str = "") -> Dict:
        """
        Use AI to generate proper metadata for a meme.
        """
        prompt = f"""Generate metadata for this meme: "{meme_name}"
Context where it will be used: {context if context else "General economics/social content"}

Provide metadata in this exact JSON format:
{{
    "emotions": ["emotion1", "emotion2", "emotion3"],
    "context": ["context1", "context2"],
    "energy": "high/medium/low",
    "source": "Original source (movie, show, etc)",
    "best_for": ["use case 1", "use case 2", "use case 3"],
    "language_fit": ["indo", "english"],
    "caption_vibe": "One line describing when to use this meme"
}}
"""

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

        # Default metadata
        return {
            "emotions": ["general"],
            "context": ["general"],
            "energy": "medium",
            "source": "Unknown",
            "best_for": ["general content"],
            "language_fit": ["indo", "english"],
            "caption_vibe": meme_name
        }

    def add_meme_to_library(self, filename: str, metadata: Dict) -> bool:
        """
        Add a meme to the library metadata.
        """
        self.metadata[filename] = metadata
        self._save_metadata()
        return True

    def find_memes_for_content(
        self,
        slides: List[str],
        auto_download: bool = False
    ) -> Dict:
        """
        Main method: Analyze content and find/suggest memes.

        Args:
            slides: List of slide texts
            auto_download: Whether to attempt downloading missing memes

        Returns:
            Dict with analysis and recommendations
        """
        result = {
            "analysis": [],
            "available_memes": [],
            "missing_memes": [],
            "recommendations": []
        }

        # Step 1: Analyze content
        analysis = self.analyze_content_for_memes(slides)
        result["analysis"] = analysis

        # Step 2: Check which memes we have
        for slide_analysis in analysis:
            if not slide_analysis.get("needs_meme"):
                continue

            meme_suggestion = slide_analysis.get("meme_suggestion", "")
            if not meme_suggestion:
                continue

            # Check if we have this meme
            existing = self.check_meme_exists(meme_suggestion)

            if existing:
                result["available_memes"].append({
                    "slide_num": slide_analysis["slide_num"],
                    "meme_name": meme_suggestion,
                    "filename": existing,
                    "reason": slide_analysis.get("reason", "")
                })
                result["recommendations"].append({
                    "slide_num": slide_analysis["slide_num"],
                    "filename": existing,
                    "confidence": 9,
                    "reason": slide_analysis.get("reason", "")
                })
            else:
                # We don't have this meme
                meme_info = {
                    "slide_num": slide_analysis["slide_num"],
                    "meme_name": meme_suggestion,
                    "search_keywords": slide_analysis.get("search_keywords", []),
                    "reason": slide_analysis.get("reason", ""),
                    "suggested_filename": meme_suggestion.lower().replace(" ", "_") + ".jpg"
                }

                # Generate metadata for when user adds it
                metadata = self.generate_meme_metadata(
                    meme_suggestion,
                    slides[slide_analysis["slide_num"] - 1] if slide_analysis["slide_num"] <= len(slides) else ""
                )
                meme_info["suggested_metadata"] = metadata

                result["missing_memes"].append(meme_info)

        return result

    def get_meme_download_instructions(self, missing_memes: List[Dict]) -> str:
        """
        Generate instructions for manually downloading missing memes.
        """
        if not missing_memes:
            return "All required memes are already in your library!"

        instructions = "## Missing Memes - Download Instructions\n\n"
        instructions += f"Save these memes to: `{self.meme_dir}`\n\n"

        for meme in missing_memes:
            instructions += f"### {meme['meme_name']}\n"
            instructions += f"- **Save as:** `{meme['suggested_filename']}`\n"
            instructions += f"- **Search:** {', '.join(meme.get('search_keywords', [meme['meme_name'] + ' meme']))}\n"
            instructions += f"- **Best sources:** Know Your Meme, Imgflip, Google Images\n"
            instructions += f"- **Used for:** {meme.get('reason', 'N/A')}\n\n"

        instructions += "---\n"
        instructions += "After downloading, the memes will be automatically detected and added to your library.\n"

        return instructions

    def sync_library(self) -> Dict:
        """
        Sync meme library - detect new files and generate metadata.

        Returns summary of changes.
        """
        changes = {
            "new_memes": [],
            "existing": [],
            "removed": []
        }

        # Get all image files in meme directory
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        current_files = set()

        for file_path in self.meme_dir.glob("*"):
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                current_files.add(file_path.name)

        # Check for new files
        for filename in current_files:
            if filename not in self.metadata:
                # New meme detected - generate metadata
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

        # Save updated metadata
        self._save_metadata()

        return changes

    def suggest_memes_for_topic(self, topic: str, num_suggestions: int = 10) -> List[Dict]:
        """
        Suggest memes that would work well for a given topic.
        """
        prompt = f"""Suggest {num_suggestions} popular memes that would work well for Instagram carousel content about: "{topic}"

For each meme, provide:
1. Meme name
2. Why it works for this topic
3. Example caption/context
4. Emotional beat it serves

Focus on:
- Highly recognizable memes
- Memes that match economics/social commentary
- Memes popular with Indonesian Gen-Z audience

Respond in JSON format:
{{
    "suggestions": [
        {{
            "meme_name": "Meme Name",
            "why_it_works": "Explanation",
            "example_use": "Example of how to use it",
            "emotional_beat": "shock/humor/pain/etc",
            "search_keywords": ["keyword1", "keyword2"]
        }}
    ]
}}
"""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.5
            )

            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
                return result.get("suggestions", [])

        except Exception as e:
            print(f"Error suggesting memes: {e}")

        return []


def create_meme_agent() -> MemeSearchAgent:
    """Factory function to create meme search agent."""
    return MemeSearchAgent()
