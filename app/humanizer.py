"""
Humanizer Module - Anti-AI Detection Layer

This module analyzes content for AI patterns and makes it sound more authentically human.
"""

import re
from typing import Dict, List, Tuple, Optional
from .config import Config
from .ai_client import get_ai_client


class Humanizer:
    """
    Analyzes and improves content to remove AI patterns and increase human authenticity.
    """

    def __init__(self):
        self.client = get_ai_client()

        # AI pattern detection
        self.ai_phrases_english = [
            r"in today's (?:fast-paced )?world",
            r"it'?s important to note that",
            r"let'?s dive in",
            r"without further ado",
            r"first and foremost",
            r"in conclusion",
            r"at the end of the day",
            r"it goes without saying",
            r"needless to say"
        ]

        self.ai_phrases_indonesian = [
            r"tidak dapat dipungkiri bahwa",
            r"di era modern ini",
            r"mari kita bahas",
            r"perlu dicatat bahwa",
            r"pada akhirnya",
            r"dapat disimpulkan bahwa",
            r"dalam rangka",
            r"sebagaimana diketahui"
        ]

    def load_humanizer_prompt(self) -> str:
        """Load humanizer master prompt"""
        prompt_path = Config.PROMPTS_DIR / "humanizer.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Humanizer prompt not found: {prompt_path}")
        return prompt_path.read_text(encoding='utf-8')

    def calculate_human_score(self, text: str) -> Dict[str, any]:
        """
        Calculate how human the text sounds on a 0-100 scale.

        Returns:
            Dict with score, breakdown, and detected issues
        """
        score = 100
        issues = []
        breakdown = {}

        # Check sentence length variety
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) >= 3:
            lengths = [len(s.split()) for s in sentences]
            avg_length = sum(lengths) / len(lengths)
            variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)

            if variance < 10:  # Very similar lengths
                score -= 5
                issues.append("Sentence lengths too uniform")
                breakdown["sentence_variety"] = -5
            else:
                breakdown["sentence_variety"] = 20
        else:
            breakdown["sentence_variety"] = 10

        # Check for AI phrases
        ai_count = 0
        all_ai_phrases = self.ai_phrases_english + self.ai_phrases_indonesian

        for pattern in all_ai_phrases:
            matches = re.findall(pattern, text, re.IGNORECASE)
            ai_count += len(matches)
            if matches:
                issues.append(f"AI phrase detected: {matches[0]}")

        ai_penalty = min(ai_count * 10, 30)
        score -= ai_penalty
        breakdown["ai_phrases"] = -ai_penalty

        # Check for personal pronouns (good sign)
        personal_pronouns = len(re.findall(r'\b(I|me|my|gua|gue|aku|saya)\b', text, re.IGNORECASE))
        if personal_pronouns > 0:
            breakdown["personal_voice"] = 15
        else:
            score -= 10
            issues.append("No personal pronouns - feels impersonal")
            breakdown["personal_voice"] = -10

        # Check for conversational markers
        conversational_markers = [
            r'\breal talk\b', r'\bhonestly\b', r'\blook\b', r'\bhere\'?s the thing\b',
            r'\bjadi gini\b', r'\bnah ini\b', r'\basli\b', r'\bsumpah\b'
        ]

        conv_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in conversational_markers)
        if conv_count > 0:
            breakdown["conversational"] = 10
        else:
            breakdown["conversational"] = 0

        # Check for starting sentences with conjunctions (human trait)
        conjunction_starts = len(re.findall(r'(?:^|\n)(?:And|But|So|Tapi|Dan|Soalnya)\s+', text))
        if conjunction_starts > 0:
            breakdown["natural_flow"] = 10
        else:
            breakdown["natural_flow"] = 0

        # Check emoji overload
        emoji_pattern = r'[😀-🙏🌀-🗿🚀-🛿]'
        emoji_count = len(re.findall(emoji_pattern, text))
        words = len(text.split())
        if words > 0 and emoji_count / words > 0.1:  # More than 1 emoji per 10 words
            score -= 5
            issues.append("Emoji overload")
            breakdown["emoji_usage"] = -5
        else:
            breakdown["emoji_usage"] = 0

        # Check for specific details vs generalizations
        specific_indicators = [
            r'\d+(?:\.\d+)?%',  # Percentages
            r'\b\d{4}\b',  # Years
            r'\$\d+',  # Money amounts
            r'\b\d+\s+(?:years?|months?|days?|tahun|bulan|hari)\b'  # Time periods
        ]

        specific_count = sum(len(re.findall(pattern, text)) for pattern in specific_indicators)
        if specific_count >= 2:
            breakdown["specificity"] = 15
        elif specific_count == 1:
            breakdown["specificity"] = 10
        else:
            score -= 5
            issues.append("Lacks specific details")
            breakdown["specificity"] = -5

        # Final score
        score = max(0, min(100, score))

        return {
            "score": score,
            "breakdown": breakdown,
            "issues": issues,
            "passes_threshold": score >= Config.MIN_HUMAN_SCORE
        }

    def humanize_content(
        self,
        text: str,
        current_score: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Make content sound more human using Claude.

        Args:
            text: Content to humanize
            current_score: Optional pre-calculated human score

        Returns:
            Dict with humanized text, new score, and changes made
        """
        if current_score is None:
            current_score = self.calculate_human_score(text)

        humanizer_prompt = self.load_humanizer_prompt()

        system_prompt = humanizer_prompt

        user_prompt = f"""Humanize this content to make it sound more authentic and less AI-generated.

**Current Human Score:** {current_score['score']}/100

**Detected Issues:**
{chr(10).join(f"- {issue}" for issue in current_score['issues']) if current_score['issues'] else "None"}

**Content to Humanize:**
{text}

---

Provide:

[HUMANIZED VERSION]
(the improved text)

[HUMAN SCORE ESTIMATE]
(your estimate of new score)

[CHANGES MADE]
- (list of changes)
"""

        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=system_prompt,
                max_tokens=3000,
                temperature=0.8  # Slightly higher for more variety
            )

            # Parse response
            humanized_text = ""
            estimated_score = None
            changes = []

            sections = content.split('[')
            for section in sections:
                if section.startswith('HUMANIZED VERSION]'):
                    humanized_text = section.split(']', 1)[1].strip()
                    # Remove until next section
                    if '[HUMAN SCORE ESTIMATE]' in humanized_text:
                        humanized_text = humanized_text.split('[HUMAN SCORE ESTIMATE]')[0].strip()

                elif section.startswith('HUMAN SCORE ESTIMATE]'):
                    score_text = section.split(']', 1)[1].strip()
                    # Extract number
                    score_match = re.search(r'(\d+)', score_text)
                    if score_match:
                        estimated_score = int(score_match.group(1))

                elif section.startswith('CHANGES MADE]'):
                    changes_text = section.split(']', 1)[1].strip()
                    changes = [line.strip('- ').strip() for line in changes_text.split('\n') if line.strip().startswith('-')]

            # Calculate actual new score
            if humanized_text:
                new_score = self.calculate_human_score(humanized_text)
            else:
                humanized_text = text
                new_score = current_score

            return {
                "humanized_text": humanized_text,
                "old_score": current_score["score"],
                "new_score": new_score["score"],
                "estimated_score": estimated_score,
                "changes_made": changes,
                "score_breakdown": new_score["breakdown"],
                "passes_threshold": new_score["passes_threshold"]
            }

        except Exception as e:
            raise Exception(f"DeepSeek API error during humanization: {str(e)}")

    def batch_humanize_slides(self, slides: List[str]) -> List[Dict[str, any]]:
        """
        Humanize multiple slides, returning results for each.

        Args:
            slides: List of slide texts

        Returns:
            List of humanization results for each slide
        """
        results = []

        for i, slide in enumerate(slides):
            score = self.calculate_human_score(slide)

            if score["passes_threshold"]:
                # Already human enough
                results.append({
                    "slide_num": i + 1,
                    "original": slide,
                    "humanized": slide,
                    "score": score["score"],
                    "needed_humanization": False
                })
            else:
                # Needs humanization
                humanized = self.humanize_content(slide, score)
                results.append({
                    "slide_num": i + 1,
                    "original": slide,
                    "humanized": humanized["humanized_text"],
                    "old_score": humanized["old_score"],
                    "new_score": humanized["new_score"],
                    "changes": humanized["changes_made"],
                    "needed_humanization": True
                })

        return results

    def quick_check(self, text: str) -> str:
        """
        Quick human score check - returns formatted report.

        Args:
            text: Text to analyze

        Returns:
            Formatted string report
        """
        score_data = self.calculate_human_score(text)

        report = f"""
HUMAN SCORE: {score_data['score']}/100 {'✓ PASS' if score_data['passes_threshold'] else '✗ NEEDS WORK'}

Score Breakdown:
"""

        for category, points in score_data['breakdown'].items():
            indicator = "✓" if points > 0 else "✗"
            report += f"  {indicator} {category.replace('_', ' ').title()}: {points:+d}\n"

        if score_data['issues']:
            report += f"\nDetected Issues:\n"
            for issue in score_data['issues']:
                report += f"  • {issue}\n"
        else:
            report += f"\nNo issues detected! Content sounds human.\n"

        return report
