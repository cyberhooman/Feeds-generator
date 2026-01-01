"""
Caption Generator Module

Generates engaging Instagram captions with strategic hashtags and CTAs.
"""

from typing import Dict, List
from .config import Config
from .ai_client import get_ai_client


class CaptionGenerator:
    """
    Generates Instagram captions optimized for engagement.
    """

    def __init__(self):
        self.client = get_ai_client()

    def load_caption_writer_prompt(self) -> str:
        """Load caption writer prompt"""
        prompt_path = Config.PROMPTS_DIR / "caption_writer.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Caption writer prompt not found: {prompt_path}")
        return prompt_path.read_text(encoding='utf-8')

    def generate_caption(
        self,
        slides: List[str],
        tone: str = "santai_gaul",
        language: str = "bahasa",
        versions: int = 2
    ) -> List[Dict]:
        """
        Generate Instagram caption for carousel.

        Args:
            slides: List of slide texts
            tone: Tone to match
            language: Language to use
            versions: Number of caption variations

        Returns:
            List of caption variations with metadata
        """
        caption_prompt = self.load_caption_writer_prompt()

        slides_summary = "\n".join([f"Slide {i+1}: {slide[:100]}..." if len(slide) > 100 else f"Slide {i+1}: {slide}"
                                     for i, slide in enumerate(slides[:3])])  # First 3 slides for context

        user_prompt = f"""Generate {versions} Instagram caption variation(s) for this carousel.

**Carousel Content Summary:**
{slides_summary}

**Tone:** {tone}
**Language:** {language}

---

For each version, provide:

=== CAPTION VERSION [number]: [Strategy Name] ===

[Full caption text with natural line breaks]

[HASHTAGS]
#hashtag1 #hashtag2 #hashtag3 ...

[CTA ALTERNATIVES]
- Alternative 1: [text]
- Alternative 2: [text]

[WHY THIS WORKS]
Brief explanation of the strategy used.
"""

        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=caption_prompt,
                max_tokens=2500,
                temperature=0.7
            )

            # Parse caption versions
            captions = []
            version_splits = content.split("=== CAPTION VERSION")

            for version_text in version_splits[1:]:
                caption_data = {
                    "caption": "",
                    "hashtags": [],
                    "cta_alternatives": [],
                    "strategy": "",
                    "reasoning": ""
                }

                lines = version_text.split('\n')

                # Extract strategy name from first line
                if ':' in lines[0]:
                    caption_data["strategy"] = lines[0].split(':', 1)[1].strip(' =').strip()

                # Parse sections
                current_section = "caption"
                caption_lines = []

                for line in lines[1:]:
                    line_stripped = line.strip()

                    if line_stripped.startswith('[HASHTAGS]'):
                        current_section = "hashtags"
                        if caption_lines:
                            caption_data["caption"] = "\n".join(caption_lines).strip()
                        continue

                    elif line_stripped.startswith('[CTA ALTERNATIVES]'):
                        current_section = "cta"
                        continue

                    elif line_stripped.startswith('[WHY THIS WORKS]'):
                        current_section = "reasoning"
                        continue

                    # Collect content based on section
                    if current_section == "caption" and line_stripped and not line_stripped.startswith('==='):
                        caption_lines.append(line.rstrip())

                    elif current_section == "hashtags" and line_stripped:
                        # Extract hashtags
                        hashtags = [tag.strip() for tag in line_stripped.split() if tag.startswith('#')]
                        caption_data["hashtags"].extend(hashtags)

                    elif current_section == "cta" and line_stripped.startswith('-'):
                        cta_text = line_stripped.lstrip('- ').lstrip('Alternative 1: ').lstrip('Alternative 2: ').lstrip('Alternative 3: ')
                        if cta_text:
                            caption_data["cta_alternatives"].append(cta_text)

                    elif current_section == "reasoning" and line_stripped:
                        caption_data["reasoning"] += line_stripped + " "

                if caption_data["caption"]:
                    captions.append(caption_data)

            return captions if captions else [{"caption": content, "hashtags": [], "cta_alternatives": [], "strategy": "default", "reasoning": ""}]

        except Exception as e:
            raise Exception(f"DeepSeek API error during caption generation: {str(e)}")

    def format_caption_with_hashtags(self, caption_data: Dict, hashtags_position: str = "end") -> str:
        """
        Format caption with hashtags in specified position.

        Args:
            caption_data: Caption data dict from generate_caption
            hashtags_position: 'end' or 'first_comment'

        Returns:
            Formatted caption string
        """
        caption = caption_data["caption"]
        hashtags = " ".join(caption_data["hashtags"])

        if hashtags_position == "end" and hashtags:
            return f"{caption}\n\n{hashtags}"
        else:
            return caption

    def suggest_hashtags(
        self,
        slides: List[str],
        niche: str,
        language: str = "bahasa"
    ) -> Dict[str, List[str]]:
        """
        Suggest strategic hashtags for carousel.

        Args:
            slides: List of slide texts
            niche: Content niche/industry
            language: Language for hashtags

        Returns:
            Dict with categorized hashtag suggestions
        """
        slides_summary = " ".join(slides[:2])[:500]  # First 2 slides, max 500 chars

        user_prompt = f"""Suggest strategic hashtags for this Instagram carousel.

**Content:** {slides_summary}
**Niche:** {niche}
**Language:** {language}

Provide hashtags in these categories:

**BIG (100k-1M+ posts):**
#tag1 #tag2 #tag3

**MEDIUM (10k-100k posts):**
#tag1 #tag2 #tag3

**NICHE (1k-10k posts):**
#tag1 #tag2 #tag3

Only suggest active, relevant hashtags that match the content.
"""

        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=800,
                temperature=0.6
            )

            # Parse hashtag categories
            hashtags = {
                "big": [],
                "medium": [],
                "niche": []
            }

            lines = content.split('\n')
            current_category = None

            for line in lines:
                line_stripped = line.strip()

                if "BIG" in line_stripped.upper() and ":" in line_stripped:
                    current_category = "big"
                    # Extract hashtags from same line if present
                    if '#' in line_stripped:
                        tags = [tag.strip() for tag in line_stripped.split() if tag.startswith('#')]
                        hashtags["big"].extend(tags)

                elif "MEDIUM" in line_stripped.upper() and ":" in line_stripped:
                    current_category = "medium"
                    if '#' in line_stripped:
                        tags = [tag.strip() for tag in line_stripped.split() if tag.startswith('#')]
                        hashtags["medium"].extend(tags)

                elif "NICHE" in line_stripped.upper() and ":" in line_stripped:
                    current_category = "niche"
                    if '#' in line_stripped:
                        tags = [tag.strip() for tag in line_stripped.split() if tag.startswith('#')]
                        hashtags["niche"].extend(tags)

                elif current_category and '#' in line_stripped:
                    tags = [tag.strip() for tag in line_stripped.split() if tag.startswith('#')]
                    hashtags[current_category].extend(tags)

            return hashtags

        except Exception as e:
            raise Exception(f"DeepSeek API error during hashtag generation: {str(e)}")
