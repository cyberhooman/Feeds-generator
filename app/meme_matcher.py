"""
Meme Matcher Module

Analyzes content emotional beats and matches with appropriate memes from library.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from .config import Config
from .ai_client import get_ai_client


class MemeMatcher:
    """
    Analyzes carousel content and matches with perfect memes from library.
    """

    def __init__(self):
        self.client = get_ai_client()
        self.metadata = self.load_metadata()

    def load_metadata(self) -> Dict:
        """Load meme library metadata"""
        if not Config.MEME_METADATA_PATH.exists():
            return {}

        try:
            with open(Config.MEME_METADATA_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_metadata(self, metadata: Dict):
        """Save metadata back to file"""
        Config.MEME_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
        with open(Config.MEME_METADATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def load_meme_analyzer_prompt(self) -> str:
        """Load meme analyzer prompt"""
        prompt_path = Config.PROMPTS_DIR / "meme_analyzer.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Meme analyzer prompt not found: {prompt_path}")
        return prompt_path.read_text(encoding='utf-8')

    def analyze_content_emotions(self, slides: List[str]) -> List[Dict]:
        """
        Analyze emotional beats of each slide.

        Args:
            slides: List of slide texts

        Returns:
            List of emotional analysis for each slide
        """
        analyzer_prompt = self.load_meme_analyzer_prompt()

        slides_text = "\n\n".join([f"**Slide {i+1}:**\n{slide}" for i, slide in enumerate(slides)])

        system_prompt = analyzer_prompt

        user_prompt = f"""Analyze the emotional beats of this Instagram carousel content:

{slides_text}

---

For each slide, provide:

**Slide [number]:**
- Primary Emotion: [emotion]
- Energy Level: [High/Medium/Low]
- Tone: [tone]
- Key Moment: [hook/revelation/payoff/etc]

Then summarize the overall emotional journey.
"""

        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.6
            )

            # Parse emotional analysis
            emotions = []
            lines = content.split('\n')

            current_slide = None
            for line in lines:
                line = line.strip()

                if line.startswith('**Slide ') and ':' in line:
                    if current_slide:
                        emotions.append(current_slide)
                    current_slide = {
                        "slide_num": len(emotions) + 1,
                        "emotion": "",
                        "energy": "",
                        "tone": "",
                        "key_moment": ""
                    }

                if current_slide:
                    if '- Primary Emotion:' in line or 'Primary Emotion:' in line:
                        current_slide["emotion"] = line.split(':', 1)[1].strip()
                    elif '- Energy Level:' in line or 'Energy Level:' in line:
                        current_slide["energy"] = line.split(':', 1)[1].strip()
                    elif '- Tone:' in line or 'Tone:' in line:
                        current_slide["tone"] = line.split(':', 1)[1].strip()
                    elif '- Key Moment:' in line or 'Key Moment:' in line:
                        current_slide["key_moment"] = line.split(':', 1)[1].strip()

            if current_slide:
                emotions.append(current_slide)

            return emotions

        except Exception as e:
            raise Exception(f"DeepSeek API error during emotional analysis: {str(e)}")

    def match_memes(
        self,
        slides: List[str],
        emotions: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Match memes to slides based on emotional analysis.

        Args:
            slides: List of slide texts
            emotions: Optional pre-calculated emotions

        Returns:
            List of meme recommendations for each slide
        """
        if not self.metadata:
            return [{"slide_num": i+1, "recommendations": [], "note": "No meme library found"} for i in range(len(slides))]

        if emotions is None:
            emotions = self.analyze_content_emotions(slides)

        # Build meme library context for Claude
        meme_library_text = "Available memes:\n\n"
        for filename, data in self.metadata.items():
            meme_library_text += f"**{filename}**\n"
            meme_library_text += f"  Emotions: {', '.join(data.get('emotions', []))}\n"
            meme_library_text += f"  Context: {', '.join(data.get('context', []))}\n"
            meme_library_text += f"  Energy: {data.get('energy', 'unknown')}\n"
            meme_library_text += f"  Best for: {', '.join(data.get('best_for', []))}\n"
            meme_library_text += f"  Vibe: {data.get('caption_vibe', 'N/A')}\n\n"

        # Build emotions context
        emotions_text = "\n".join([
            f"Slide {e['slide_num']}: {e['emotion']} | {e['energy']} energy | {e['tone']} tone"
            for e in emotions
        ])

        analyzer_prompt = self.load_meme_analyzer_prompt()

        user_prompt = f"""Match memes to these slides based on emotional analysis.

**Content Emotional Analysis:**
{emotions_text}

**Available Meme Library:**
{meme_library_text}

---

For each slide, recommend top 3 memes (if applicable). Some slides work better without memes.

Format:

**Slide [number]:**
1. [filename] - Confidence: X/10
   Reason: [why it works]

2. [filename] - Confidence: X/10
   Reason: [why it works]

(Or state "No meme recommended - text-only works better")
"""

        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=analyzer_prompt,
                max_tokens=2500,
                temperature=0.6
            )

            # Parse recommendations
            recommendations = []
            lines = content.split('\n')

            current_slide_recs = None
            for line in lines:
                line = line.strip()

                if line.startswith('**Slide '):
                    if current_slide_recs:
                        recommendations.append(current_slide_recs)

                    slide_num = int(line.split()[1].rstrip(':').rstrip(']').rstrip('**'))
                    current_slide_recs = {
                        "slide_num": slide_num,
                        "recommendations": []
                    }

                elif line.startswith(('1. ', '2. ', '3. ')) and current_slide_recs:
                    # Parse meme recommendation
                    parts = line.split(' - Confidence:', 1)
                    filename = parts[0].lstrip('1234. ').strip()

                    confidence = 5
                    reason = ""

                    if len(parts) > 1:
                        conf_parts = parts[1].split('Reason:', 1)
                        try:
                            confidence = int(conf_parts[0].split('/')[0].strip())
                        except:
                            pass

                        if len(conf_parts) > 1:
                            reason = conf_parts[1].strip()

                    current_slide_recs["recommendations"].append({
                        "filename": filename,
                        "confidence": confidence,
                        "reason": reason
                    })

                elif "no meme" in line.lower() and current_slide_recs:
                    current_slide_recs["text_only"] = True

            if current_slide_recs:
                recommendations.append(current_slide_recs)

            return recommendations

        except Exception as e:
            raise Exception(f"DeepSeek API error during meme matching: {str(e)}")

    def get_meme_path(self, filename: str) -> Optional[Path]:
        """Get full path to meme file"""
        meme_path = Config.MEME_IMAGES_DIR / filename
        return meme_path if meme_path.exists() else None

    def list_available_memes(self) -> List[Dict]:
        """List all memes in library with metadata"""
        memes = []
        for filename, data in self.metadata.items():
            meme_path = self.get_meme_path(filename)
            memes.append({
                "filename": filename,
                "exists": meme_path is not None,
                "path": str(meme_path) if meme_path else None,
                "metadata": data
            })
        return memes
