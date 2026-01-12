"""
Content Rewriter Module - The Content Creator Brain

This module handles the core content transformation using DeepSeek API.
It thinks like a professional content creator and applies copywriting frameworks.
Now includes AI-powered keyword highlighting for visual emphasis.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .config import Config
from .ai_client import get_ai_client


class ContentRewriter:
    """
    Professional content creator brain powered by DeepSeek.
    Transforms rough ideas into compelling carousel content.
    """

    def __init__(self):
        self.client = get_ai_client()

    def load_prompt_template(self, template_name: str) -> str:
        """Load a prompt template from file"""
        template_path = Config.PROMPTS_DIR / f"{template_name}.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {template_path}")
        return template_path.read_text(encoding='utf-8')

    def load_tone_definition(self, tone_name: str, language: str) -> str:
        """Load tone definition file"""
        # Map language to directory
        lang_map = {
            'bahasa': 'bahasa',
            'english': 'english',
            'mixed': 'mixed'
        }

        tone_dir = Config.TONES_DIR / lang_map.get(language, 'bahasa')
        tone_path = tone_dir / f"{tone_name}.txt"

        if not tone_path.exists():
            raise FileNotFoundError(f"Tone file not found: {tone_path}")

        return tone_path.read_text(encoding='utf-8')

    def load_angle_template(self, angle_name: str) -> str:
        """
        Load content angle template or use custom angle description.

        If angle_name contains spaces or is longer than typical preset names,
        treat it as a custom description rather than a filename.
        """
        # Check if this is a custom angle description (contains spaces or long text)
        # Preset angle names are simple identifiers like "story_personal", "hot_take"
        if ' ' in angle_name or len(angle_name) > 30:
            # This is a custom angle description - use it directly
            return f"Content Angle: {angle_name}"

        # Otherwise, try to load from file (preset angle)
        angle_path = Config.ANGLES_DIR / f"{angle_name}.txt"

        if not angle_path.exists():
            # If file doesn't exist but it's a short name, treat as custom too
            return f"Content Angle: {angle_name}"

        return angle_path.read_text(encoding='utf-8')

    def load_viral_framework(self) -> str:
        """Load the viral success framework"""
        framework_path = Config.PROMPTS_DIR / "viral_framework.txt"
        if framework_path.exists():
            return framework_path.read_text(encoding='utf-8')
        return ""

    def load_narrative_arc(self, content_purpose: str) -> str:
        """Load the narrative arc prompt for a content purpose."""
        arc_path = Config.PROMPTS_DIR / f"arc_{content_purpose}.txt"
        if arc_path.exists():
            return arc_path.read_text(encoding='utf-8')
        return ""

    def rewrite_content(
        self,
        rough_idea: str,
        tone: str = "santai_gaul",
        language: str = "bahasa",
        angle: str = "story_personal",
        versions: int = 1,
        content_purpose: str = "storytelling"
    ) -> List[Dict[str, any]]:
        """
        Rewrite rough idea into polished carousel content.

        Args:
            rough_idea: The user's rough content idea
            tone: Tone to use (e.g., 'santai_gaul', 'profesional', 'casual_friendly')
            language: Language category ('bahasa', 'english', 'mixed')
            angle: Content angle ('story_personal', 'hot_take', 'tips_listicle', etc.)
            versions: Number of alternative versions to generate
            content_purpose: Content type ('educational', 'motivational', 'storytelling')

        Returns:
            List of content versions with slides and metadata
        """
        # Load templates
        master_prompt = self.load_prompt_template("content_creator")
        viral_framework = self.load_viral_framework()
        tone_definition = self.load_tone_definition(tone, language)
        angle_template = self.load_angle_template(angle)
        narrative_arc = self.load_narrative_arc(content_purpose)

        # Build the full prompt
        system_prompt = f"""{master_prompt}

---

## VIRAL SUCCESS FRAMEWORK (Apply These Principles):

{viral_framework}

---

## NARRATIVE ARC (CRITICAL - Follow This Structure):

{narrative_arc}

---

## TONE TO USE:

{tone_definition}

---

## CONTENT ANGLE TO FOLLOW:

{angle_template}

---

Remember: Apply the copywriting frameworks, follow the NARRATIVE ARC structure strictly, match the tone perfectly, and make it sound 100% human.
IMPORTANT: Each slide MUST include a [BEAT: BEAT_NAME] marker to identify its narrative function.
"""

        user_prompt = f"""Transform this rough idea into a VIRAL Instagram carousel:

**Rough Idea:**
{rough_idea}

**Requirements:**
- Language: {language}
- Tone: {tone}
- Angle: {angle}
- Content Purpose: {content_purpose.upper()}
- Generate {versions} version(s)
- STRICTLY follow the NARRATIVE ARC for {content_purpose} content
- Apply the viral framework (hook psychology, algorithm optimization, engagement triggers)
- 5-7 slides maximum
- Include explicit CTA optimized for saves/shares/comments

Provide the output in this format:

=== VERSION 1 ===

[SLIDE 1 - BEAT: BEAT_NAME]
[Content following the narrative arc beat]

[SLIDE 2 - BEAT: BEAT_NAME]
[Content following the narrative arc beat]

[SLIDE 3 - BEAT: BEAT_NAME]
[Content following the narrative arc beat]

[SLIDE 4 - BEAT: BEAT_NAME]
[Content following the narrative arc beat]

[SLIDE 5 - BEAT: BEAT_NAME]
[Content following the narrative arc beat]

[SLIDE 6 - BEAT: BEAT_NAME]
[Content following the narrative arc beat]

[SLIDE 7 - BEAT: CTA]
[Key insight + explicit CTA]

[ENGAGEMENT OPTIMIZATION]
- Primary target: [SAVES/SHARES/COMMENTS]
- Hook type used: [Question/Shock/Promise/Mistake/Curiosity/Unpopular]
- Psychological triggers: [list 2-3 used]
- Why it will perform: [brief explanation]

[MEME SUGGESTIONS]
Slide X: [emotional beat] - suggest: [emotion/energy]

[HOOK ALTERNATIVES]
- Alternative 1: [text]
- Alternative 2: [text]

{"=== VERSION 2 ===" if versions > 1 else ""}
(repeat format if multiple versions)
"""

        # Call DeepSeek API
        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                max_tokens=4000,
                temperature=0.7
            )

            # Parse the response
            versions_data = self._parse_response(content, versions)

            return versions_data

        except Exception as e:
            raise Exception(f"DeepSeek API error: {str(e)}")

    def _parse_response(self, response_text: str, expected_versions: int) -> List[Dict]:
        """
        Parse Claude's response into structured data.

        Returns list of dicts with:
        - slides: List of slide texts
        - narrative_beats: Dict of slide_num -> beat name (NEW)
        - meme_suggestions: Dict of slide_num -> suggestion
        - hook_alternatives: List of alternative hooks
        - engagement_optimization: Dict with viral strategy info
        """
        versions = []

        # Split by version markers
        version_splits = response_text.split("=== VERSION")

        for version_text in version_splits[1:]:  # Skip first empty split
            version_data = {
                "slides": [],
                "narrative_beats": {},  # NEW: Maps slide_num -> beat_name
                "meme_suggestions": {},
                "hook_alternatives": [],
                "engagement_optimization": {
                    "primary_target": "",
                    "hook_type": "",
                    "triggers": [],
                    "performance_reason": ""
                }
            }

            # Extract slides
            lines = version_text.split('\n')
            current_slide = ""
            in_slide = False
            slide_num = 0

            for line in lines:
                line = line.strip()

                # Check for slide markers (now with BEAT)
                # Format: [SLIDE 1 - BEAT: PAIN_POINT] or [SLIDE 1]
                if line.startswith('[SLIDE '):
                    if current_slide and in_slide:
                        version_data["slides"].append(current_slide.strip())
                    current_slide = ""
                    in_slide = True
                    slide_num += 1

                    # Extract narrative beat if present
                    if 'BEAT:' in line:
                        try:
                            beat_part = line.split('BEAT:')[1]
                            beat_name = beat_part.strip().rstrip(']').strip().lower()
                            version_data["narrative_beats"][slide_num] = beat_name
                        except:
                            pass
                    continue

                # Check for section markers
                if line.startswith('[ENGAGEMENT OPTIMIZATION]'):
                    if current_slide and in_slide:
                        version_data["slides"].append(current_slide.strip())
                    in_slide = False
                    current_slide = ""
                    continue

                if line.startswith('[MEME SUGGESTIONS]'):
                    if current_slide and in_slide:
                        version_data["slides"].append(current_slide.strip())
                    in_slide = False
                    current_slide = ""
                    continue

                if line.startswith('[HOOK ALTERNATIVES]'):
                    in_slide = False
                    current_slide = ""
                    continue

                # Parse engagement optimization
                if line.startswith('- Primary target:'):
                    version_data["engagement_optimization"]["primary_target"] = line.split(':', 1)[1].strip()
                if line.startswith('- Hook type used:'):
                    version_data["engagement_optimization"]["hook_type"] = line.split(':', 1)[1].strip()
                if line.startswith('- Psychological triggers:'):
                    triggers = line.split(':', 1)[1].strip()
                    version_data["engagement_optimization"]["triggers"] = [t.strip() for t in triggers.split(',')]
                if line.startswith('- Why it will perform:'):
                    version_data["engagement_optimization"]["performance_reason"] = line.split(':', 1)[1].strip()

                # Collect slide content
                if in_slide and line and not line.startswith('==='):
                    current_slide += line + "\n"

                # Parse meme suggestions
                if line.startswith('Slide ') and ':' in line and 'suggest:' in line:
                    try:
                        parts = line.split('-')
                        slide_ref = parts[0].strip()
                        suggestion = parts[1].strip() if len(parts) > 1 else ""
                        slide_n = int(slide_ref.split()[1].rstrip(':'))
                        version_data["meme_suggestions"][slide_n] = suggestion
                    except:
                        pass

                # Parse hook alternatives
                if line.startswith('- Alternative ') or line.startswith('- '):
                    alt_text = line.lstrip('- ').lstrip('Alternative 1: ').lstrip('Alternative 2: ').lstrip('Alternative 3: ')
                    if alt_text:
                        version_data["hook_alternatives"].append(alt_text)

            # Add last slide if exists
            if current_slide and in_slide:
                version_data["slides"].append(current_slide.strip())

            if version_data["slides"]:
                versions.append(version_data)

        return versions if versions else [{"slides": [response_text], "narrative_beats": {}, "meme_suggestions": {}, "hook_alternatives": []}]

    def refine_slides(
        self,
        slides: List[str],
        refinement_request: str,
        tone: str = "santai_gaul",
        language: str = "bahasa"
    ) -> List[str]:
        """
        Refine existing slides based on user feedback.

        Args:
            slides: List of current slide texts
            refinement_request: What to change/improve
            tone: Tone to maintain
            language: Language to use

        Returns:
            Refined list of slides
        """
        tone_definition = self.load_tone_definition(tone, language)

        slides_text = "\n\n".join([f"[SLIDE {i+1}]\n{slide}" for i, slide in enumerate(slides)])

        system_prompt = f"""You are a professional content editor helping refine Instagram carousel content.

Maintain this tone:
{tone_definition}

Keep the content human, engaging, and on-brand."""

        user_prompt = f"""Current slides:

{slides_text}

Refinement request:
{refinement_request}

Provide the refined slides in the same format:

[SLIDE 1]
[refined text]

[SLIDE 2]
[refined text]

etc.
"""

        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                max_tokens=3000,
                temperature=0.7
            )

            refined = self._parse_response(content, 1)

            return refined[0]["slides"] if refined else slides

        except Exception as e:
            raise Exception(f"DeepSeek API error during refinement: {str(e)}")

    def extract_highlights(
        self,
        slides: List[str],
        max_highlights_per_slide: int = 3
    ) -> List[Dict[str, any]]:
        """
        Use AI to identify key words/phrases to highlight in each slide.

        Args:
            slides: List of slide texts
            max_highlights_per_slide: Maximum words to highlight per slide

        Returns:
            List of dicts with slide text and highlight positions
        """
        slides_text = "\n\n".join([f"[SLIDE {i+1}]\n{slide}" for i, slide in enumerate(slides)])

        system_prompt = """You are an expert visual content designer. Your job is to identify the most impactful words or short phrases (max 3 words) to highlight in Instagram carousel slides.

Rules for highlighting:
1. Choose words that create visual emphasis and grab attention
2. Highlight numbers, statistics, and data points
3. Highlight emotional words (pain points, benefits, outcomes)
4. Highlight key concepts and action words
5. NEVER highlight common words like "dan", "yang", "untuk", "the", "is", "and"
6. Max 3 highlights per slide
7. Prioritize the most impactful word if slide is short

Output format:
SLIDE_1: word1, word2, word3
SLIDE_2: phrase one, word2
etc."""

        user_prompt = f"""Identify the key words/phrases to highlight for visual emphasis in these Instagram carousel slides:

{slides_text}

For each slide, list the 1-3 most impactful words or short phrases to highlight.
Output format:
SLIDE_1: word1, word2
SLIDE_2: phrase1, word2
etc."""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                max_tokens=1000,
                temperature=0.3
            )

            # Parse response
            highlights = self._parse_highlights(response, slides)
            return highlights

        except Exception as e:
            # Fallback: use simple keyword detection
            return self._fallback_highlights(slides, max_highlights_per_slide)

    def _parse_highlights(
        self,
        response: str,
        slides: List[str]
    ) -> List[Dict[str, any]]:
        """Parse AI response into highlight data."""
        results = []

        for i, slide in enumerate(slides):
            slide_num = i + 1
            highlights = []

            # Find the line for this slide
            pattern = rf"SLIDE_{slide_num}:\s*(.+?)(?:\n|$)"
            match = re.search(pattern, response, re.IGNORECASE)

            if match:
                # Parse comma-separated highlights
                highlight_text = match.group(1).strip()
                raw_highlights = [h.strip() for h in highlight_text.split(',')]

                # Find positions in original slide text
                for highlight in raw_highlights:
                    if not highlight:
                        continue

                    # Clean up the highlight
                    highlight = highlight.strip('"\'')

                    # Find in slide (case-insensitive)
                    slide_lower = slide.lower()
                    highlight_lower = highlight.lower()

                    start = slide_lower.find(highlight_lower)
                    if start >= 0:
                        # Get the actual text from slide (preserve case)
                        actual_text = slide[start:start + len(highlight)]
                        highlights.append({
                            "text": actual_text,
                            "start": start,
                            "end": start + len(highlight)
                        })

            results.append({
                "slide_num": slide_num,
                "original_text": slide,
                "highlights": highlights[:3]  # Max 3
            })

        return results

    def _fallback_highlights(
        self,
        slides: List[str],
        max_per_slide: int = 3
    ) -> List[Dict[str, any]]:
        """
        Fallback keyword detection when AI is not available.
        Uses simple rules to detect important words.
        """
        # Words that are usually good to highlight
        important_patterns = [
            r'\b\d+[%+]?\b',  # Numbers and percentages
            r'\bRp\.?\s*[\d.,]+\b',  # Currency
            r'\b\d+x\b',  # Multipliers
            r'\b(juta|ribu|miliar|billion|million|thousand)\b',
        ]

        # Important keywords in both languages
        keywords = {
            # Indonesian
            'gratis', 'rahasia', 'terbukti', 'sukses', 'gagal', 'penting',
            'uang', 'gaji', 'investasi', 'kaya', 'miskin', 'mahal', 'murah',
            'cepat', 'mudah', 'susah', 'ribet', 'stuck', 'breakthrough',
            'salah', 'benar', 'bohong', 'fakta', 'realita', 'mitos',
            # English
            'free', 'secret', 'proven', 'success', 'fail', 'important',
            'money', 'salary', 'invest', 'rich', 'poor', 'expensive', 'cheap',
            'fast', 'easy', 'hard', 'wrong', 'right', 'lie', 'fact', 'myth',
            'never', 'always', 'only', 'first', 'last', 'best', 'worst',
        }

        results = []

        for i, slide in enumerate(slides):
            highlights = []
            words_found = set()

            # Find pattern matches (numbers, currency, etc.)
            for pattern in important_patterns:
                for match in re.finditer(pattern, slide, re.IGNORECASE):
                    if match.group() not in words_found:
                        highlights.append({
                            "text": match.group(),
                            "start": match.start(),
                            "end": match.end()
                        })
                        words_found.add(match.group().lower())

            # Find keyword matches
            for keyword in keywords:
                pattern = rf'\b{re.escape(keyword)}\b'
                for match in re.finditer(pattern, slide, re.IGNORECASE):
                    if match.group().lower() not in words_found:
                        highlights.append({
                            "text": match.group(),
                            "start": match.start(),
                            "end": match.end()
                        })
                        words_found.add(match.group().lower())

            # Sort by position and limit
            highlights.sort(key=lambda x: x["start"])

            results.append({
                "slide_num": i + 1,
                "original_text": slide,
                "highlights": highlights[:max_per_slide]
            })

        return results

    def get_slides_with_highlights(
        self,
        slides: List[str]
    ) -> List[Dict[str, any]]:
        """
        Get slides with marked highlight positions.

        This is the main method to call for getting highlight data.

        Args:
            slides: List of slide texts

        Returns:
            List of dicts with original text and highlight info
        """
        return self.extract_highlights(slides)
