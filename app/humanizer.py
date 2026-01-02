"""
Humanizer Module - Enhanced Anti-AI Detection Layer

Analyzes content for AI patterns and makes it sound more authentically human.
Now with Indonesian Gen-Z cultural markers and punchy rewrite capabilities.
"""

import re
import random
from typing import Dict, List, Tuple, Optional
from .config import Config
from .ai_client import get_ai_client


# ============================================================================
# CULTURAL MARKERS FOR AUTHENTIC INDONESIAN GEN-Z VOICE
# ============================================================================

GENZ_MARKERS = {
    # Authentic slang patterns (not forced)
    "pronouns": {
        "formal": ["saya", "anda", "kita"],
        "casual": ["gua", "gue", "lu", "lo", "kita"],
        "edgy": ["w", "u", "gw"]
    },
    "intensifiers": {
        "formal": ["sangat", "sekali", "amat"],
        "casual": ["banget", "bgt", "parah", "gila"],
        "edgy": ["anjir", "gokil", "ngeri"]
    },
    "transitions": {
        "formal": ["namun", "akan tetapi", "selain itu"],
        "casual": ["tapi", "soalnya", "btw", "anyway"],
        "edgy": ["nah", "jadi gini", "hold up", "wait"]
    },
    "reactions": {
        "surprise": ["anjir", "gila", "what", "hah", "wait"],
        "agreement": ["bener", "facts", "fr", "real", "setuju bgt"],
        "pain": ["sakit bgt", "boncos", "tewas", "mampus"],
        "realization": ["baru nyadar", "ternyata", "oh shit", "damn"]
    }
}

# AI tells that MUST be removed
AI_PATTERNS = {
    "english": [
        r"in today's (?:fast-paced |digital |modern )?world",
        r"it'?s important to note that",
        r"let'?s dive in(?:to)?",
        r"without further ado",
        r"first and foremost",
        r"in conclusion",
        r"at the end of the day",
        r"it goes without saying",
        r"needless to say",
        r"as you can see",
        r"moving forward",
        r"leverage(?:ing)?",
        r"synerg(?:y|ize)",
        r"empower(?:ing)?",
        r"utilize",
        r"facilitate",
        r"paradigm shift",
        r"best practices",
        r"game[- ]?changer",
        r"deep dive",
        r"circle back",
        r"touch base",
        r"low[- ]?hanging fruit",
    ],
    "indonesian": [
        r"tidak dapat dipungkiri bahwa",
        r"di era (?:modern|digital|globalisasi) ini",
        r"mari kita bahas",
        r"perlu dicatat bahwa",
        r"pada akhirnya",
        r"dapat disimpulkan bahwa",
        r"dalam rangka",
        r"sebagaimana diketahui",
        r"dengan demikian",
        r"selanjutnya",
        r"berkaitan dengan hal tersebut",
        r"perlu digarisbawahi",
        r"tidak kalah penting(?:nya)?",
        r"seiring berjalannya waktu",
        r"tak bisa dipungkiri",
    ]
}

# Replacement suggestions for punchy rewrites
PUNCHY_REPLACEMENTS = {
    "very important": ["crucial", "key", "ini yang penting"],
    "you need to": ["harus", "wajib", "kudu"],
    "it is": ["ini", ""],
    "there is": ["ada", ""],
    "that being said": ["tapi", "but"],
    "in order to": ["buat", "untuk"],
    "the fact that": ["fakta:", ""],
    "it should be noted": ["note:", "btw"],
}


class Humanizer:
    """
    Analyzes and improves content to remove AI patterns and increase human authenticity.
    Enhanced with Indonesian Gen-Z cultural markers.
    """

    def __init__(self):
        self.client = get_ai_client()
        self.ai_patterns = AI_PATTERNS
        self.genz_markers = GENZ_MARKERS

    def load_humanizer_prompt(self) -> str:
        """Load humanizer master prompt"""
        prompt_path = Config.PROMPTS_DIR / "humanizer.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Humanizer prompt not found: {prompt_path}")
        return prompt_path.read_text(encoding='utf-8')

    def detect_language(self, text: str) -> str:
        """Detect if text is primarily Indonesian or English."""
        indo_words = ["yang", "dan", "ini", "itu", "untuk", "dengan", "tidak", "dari", "ke", "di"]
        eng_words = ["the", "and", "is", "are", "to", "for", "with", "you", "your", "this"]

        text_lower = text.lower()
        indo_count = sum(1 for word in indo_words if f" {word} " in f" {text_lower} ")
        eng_count = sum(1 for word in eng_words if f" {word} " in f" {text_lower} ")

        return "indonesian" if indo_count > eng_count else "english"

    def calculate_human_score(self, text: str) -> Dict[str, any]:
        """
        Calculate how human the text sounds on a 0-100 scale.
        Enhanced with cultural authenticity checks.
        """
        score = 100
        issues = []
        breakdown = {}
        language = self.detect_language(text)

        # === 1. Sentence variety check ===
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) >= 3:
            lengths = [len(s.split()) for s in sentences]
            avg_length = sum(lengths) / len(lengths)
            variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)

            if variance < 5:  # Very uniform = robotic
                score -= 10
                issues.append("Sentence lengths too uniform (robotic)")
                breakdown["sentence_variety"] = -10
            elif variance < 15:
                score -= 5
                issues.append("Could use more sentence variety")
                breakdown["sentence_variety"] = -5
            else:
                breakdown["sentence_variety"] = 15  # Good variety
        else:
            breakdown["sentence_variety"] = 5

        # === 2. AI phrase detection (critical) ===
        ai_count = 0
        patterns = self.ai_patterns.get(language, []) + self.ai_patterns.get("english", [])

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            ai_count += len(matches)
            if matches:
                issues.append(f"AI phrase: '{matches[0]}'")

        ai_penalty = min(ai_count * 12, 40)  # Max 40 point penalty
        score -= ai_penalty
        breakdown["ai_phrases"] = -ai_penalty if ai_penalty > 0 else 10

        # === 3. Personal voice check ===
        if language == "indonesian":
            personal_patterns = r'\b(gua|gue|gw|aku|saya|kita|lu|lo|kamu)\b'
        else:
            personal_patterns = r'\b(I|me|my|we|you|your)\b'

        personal_count = len(re.findall(personal_patterns, text, re.IGNORECASE))
        if personal_count >= 2:
            breakdown["personal_voice"] = 15
        elif personal_count == 1:
            breakdown["personal_voice"] = 5
        else:
            score -= 10
            issues.append("No personal pronouns - feels impersonal")
            breakdown["personal_voice"] = -10

        # === 4. Conversational markers ===
        if language == "indonesian":
            conv_patterns = [
                r'\bjadi gini\b', r'\bnah\b', r'\btapi\b', r'\bsoalnya\b',
                r'\basli\b', r'\bserius\b', r'\bhonestly\b', r'\bbtw\b',
                r'\breal talk\b', r'\bfr\b'
            ]
        else:
            conv_patterns = [
                r'\breal talk\b', r'\bhonestly\b', r'\blook\b', r'\bhere\'?s the thing\b',
                r'\bbut\b', r'\bso\b', r'\bactually\b', r'\bbtw\b'
            ]

        conv_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in conv_patterns)
        if conv_count >= 2:
            breakdown["conversational"] = 15
        elif conv_count == 1:
            breakdown["conversational"] = 5
        else:
            breakdown["conversational"] = 0

        # === 5. Starting sentences with conjunctions (human trait) ===
        conjunction_starts = len(re.findall(r'(?:^|\n)(?:And|But|So|Tapi|Dan|Soalnya|Nah|Jadi)\s+', text, re.IGNORECASE))
        if conjunction_starts > 0:
            breakdown["natural_flow"] = 10
        else:
            breakdown["natural_flow"] = 0

        # === 6. Emoji usage check ===
        emoji_pattern = r'[\U0001F300-\U0001F9FF]'
        emoji_count = len(re.findall(emoji_pattern, text))
        words = len(text.split())

        if words > 0:
            emoji_ratio = emoji_count / words
            if emoji_ratio > 0.15:  # More than 1 emoji per 6-7 words
                score -= 10
                issues.append("Emoji overload (looks like spam)")
                breakdown["emoji_usage"] = -10
            elif emoji_ratio > 0.08:
                score -= 5
                issues.append("Too many emojis")
                breakdown["emoji_usage"] = -5
            elif emoji_count > 0:
                breakdown["emoji_usage"] = 5  # Some emojis = human
            else:
                breakdown["emoji_usage"] = 0

        # === 7. Specificity check (numbers, details) ===
        specific_indicators = [
            r'\d+(?:\.\d+)?%',  # Percentages
            r'\b\d{4}\b',  # Years
            r'(?:Rp|IDR|\$|USD)\s*\d+',  # Money amounts
            r'\b\d+\s*(?:juta|ribu|k|rb|million|billion|tahun|bulan|hari)\b',  # Specific numbers
            r'\b(?:januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\b',
        ]

        specific_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in specific_indicators)
        if specific_count >= 2:
            breakdown["specificity"] = 15
        elif specific_count == 1:
            breakdown["specificity"] = 8
        else:
            score -= 5
            issues.append("Lacks specific details (numbers, dates)")
            breakdown["specificity"] = -5

        # === 8. Word count check (slides should be punchy) ===
        if words > 50:
            score -= 5
            issues.append(f"Too long ({words} words) - slides should be punchy")
            breakdown["brevity"] = -5
        elif words <= 35:
            breakdown["brevity"] = 10  # Good, punchy length
        else:
            breakdown["brevity"] = 0

        # === 9. Cultural authenticity (Indonesian content) ===
        if language == "indonesian":
            # Check for natural slang usage
            slang_patterns = [r'\bbanget\b', r'\bbgt\b', r'\bdong\b', r'\bsih\b', r'\baja\b', r'\bnih\b']
            slang_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in slang_patterns)

            if slang_count >= 2:
                breakdown["cultural_auth"] = 10
            elif slang_count == 1:
                breakdown["cultural_auth"] = 5
            else:
                breakdown["cultural_auth"] = 0

        # Final score
        score = max(0, min(100, score))

        return {
            "score": score,
            "breakdown": breakdown,
            "issues": issues,
            "language": language,
            "word_count": words,
            "passes_threshold": score >= Config.MIN_HUMAN_SCORE
        }

    def make_punchy(self, text: str, max_words: int = 35) -> str:
        """
        Make text punchier by cutting fluff and tightening language.
        Does NOT use AI - purely rule-based for speed.
        """
        # Remove filler phrases
        filler_patterns = [
            (r'\bit is (?:important|worth noting|essential) (?:to note )?that\b', ''),
            (r'\bthe fact (?:of the matter )?is (?:that )?\b', ''),
            (r'\bin order to\b', 'to'),
            (r'\bat this point in time\b', 'now'),
            (r'\bdue to the fact that\b', 'because'),
            (r'\bfor the purpose of\b', 'for'),
            (r'\bin the event that\b', 'if'),
            (r'\bwith regards to\b', 'about'),
            (r'\bin terms of\b', 'for'),
            (r'\btake into consideration\b', 'consider'),
            (r'\bmake a decision\b', 'decide'),
            (r'\bcome to a conclusion\b', 'conclude'),
            (r'\bhave the ability to\b', 'can'),
            (r'\bvery\s+', ''),  # Remove "very" - use stronger words
            (r'\breally\s+', ''),  # Remove "really"
            (r'\bjust\s+', ''),  # Remove filler "just"
        ]

        result = text
        for pattern, replacement in filler_patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result).strip()

        # If still too long, truncate intelligently
        words = result.split()
        if len(words) > max_words:
            # Try to find a natural break point
            truncated = ' '.join(words[:max_words])

            # End at sentence boundary if possible
            last_period = truncated.rfind('.')
            last_question = truncated.rfind('?')
            last_exclaim = truncated.rfind('!')

            best_break = max(last_period, last_question, last_exclaim)
            if best_break > len(truncated) * 0.6:  # Only if it's past 60% of text
                truncated = truncated[:best_break + 1]

            result = truncated

        return result

    def humanize_content(
        self,
        text: str,
        current_score: Optional[Dict] = None,
        tone: str = "casual"
    ) -> Dict[str, any]:
        """
        Make content sound more human using AI.
        Enhanced with tone-specific rewrites.
        """
        if current_score is None:
            current_score = self.calculate_human_score(text)

        # Quick path: if already good, just make punchy
        if current_score["score"] >= 85:
            punchy = self.make_punchy(text)
            new_score = self.calculate_human_score(punchy)
            return {
                "humanized_text": punchy,
                "old_score": current_score["score"],
                "new_score": new_score["score"],
                "changes_made": ["Made punchier"],
                "passes_threshold": new_score["passes_threshold"]
            }

        humanizer_prompt = self.load_humanizer_prompt()
        language = current_score.get("language", "english")

        # Build tone-specific instructions
        tone_instructions = {
            "casual": "Use natural slang, keep it conversational. Think talking to a friend.",
            "edgy": "Be bold, slightly provocative. Use Gen-Z slang naturally (not forced).",
            "professional": "Keep it professional but not corporate. Avoid jargon."
        }.get(tone, "Keep it natural and conversational.")

        user_prompt = f"""Rewrite this content to sound MORE HUMAN and LESS AI.

**Current Human Score:** {current_score['score']}/100

**Detected Issues:**
{chr(10).join(f"- {issue}" for issue in current_score['issues']) if current_score['issues'] else "None"}

**Language:** {language}
**Tone:** {tone} - {tone_instructions}

**Content to Humanize:**
{text}

---

RULES:
1. MAX 35 words (be punchy!)
2. Remove ALL AI phrases
3. Add personal pronouns (gua/lu for Indonesian, I/you for English)
4. Start some sentences with "But" "So" "And" "Tapi" "Nah"
5. Use specific numbers where possible
6. NO translation parentheticals
7. ONE language only

Provide:

[HUMANIZED VERSION]
(the improved text - MAX 35 words)

[CHANGES MADE]
- (list changes)
"""

        try:
            content = self.client.chat(
                messages=[{"role": "user", "content": user_prompt}],
                system_prompt=humanizer_prompt,
                max_tokens=1000,
                temperature=0.8
            )

            # Parse response
            humanized_text = ""
            changes = []

            sections = content.split('[')
            for section in sections:
                if section.startswith('HUMANIZED VERSION]'):
                    humanized_text = section.split(']', 1)[1].strip()
                    # Clean up any trailing sections
                    if '[CHANGES MADE]' in humanized_text:
                        humanized_text = humanized_text.split('[CHANGES MADE]')[0].strip()
                    if '[HUMAN SCORE' in humanized_text:
                        humanized_text = humanized_text.split('[HUMAN SCORE')[0].strip()

                elif section.startswith('CHANGES MADE]'):
                    changes_text = section.split(']', 1)[1].strip()
                    changes = [line.strip('- ').strip() for line in changes_text.split('\n') if line.strip().startswith('-')]

            # Apply punchiness as final pass
            if humanized_text:
                humanized_text = self.make_punchy(humanized_text)
                new_score = self.calculate_human_score(humanized_text)
            else:
                humanized_text = self.make_punchy(text)
                new_score = self.calculate_human_score(humanized_text)
                changes = ["Made punchier (AI rewrite failed)"]

            return {
                "humanized_text": humanized_text,
                "old_score": current_score["score"],
                "new_score": new_score["score"],
                "changes_made": changes,
                "score_breakdown": new_score["breakdown"],
                "passes_threshold": new_score["passes_threshold"]
            }

        except Exception as e:
            # Fallback: just make punchy
            punchy = self.make_punchy(text)
            new_score = self.calculate_human_score(punchy)
            return {
                "humanized_text": punchy,
                "old_score": current_score["score"],
                "new_score": new_score["score"],
                "changes_made": [f"Fallback: made punchy (error: {str(e)[:50]})"],
                "passes_threshold": new_score["passes_threshold"]
            }

    def batch_humanize_slides(
        self,
        slides: List[str],
        tone: str = "casual"
    ) -> List[Dict[str, any]]:
        """
        Humanize multiple slides, returning results for each.
        """
        results = []

        for i, slide in enumerate(slides):
            score = self.calculate_human_score(slide)

            if score["passes_threshold"] and score["score"] >= 80:
                # Already human enough - just ensure punchiness
                punchy = self.make_punchy(slide)
                new_score = self.calculate_human_score(punchy)
                results.append({
                    "slide_num": i + 1,
                    "original": slide,
                    "humanized": punchy,
                    "score": new_score["score"],
                    "needed_humanization": False
                })
            else:
                # Needs humanization
                humanized = self.humanize_content(slide, score, tone)
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
        """
        score_data = self.calculate_human_score(text)

        status = "PASS" if score_data['passes_threshold'] else "NEEDS WORK"
        report = f"""
HUMAN SCORE: {score_data['score']}/100 [{status}]
Language: {score_data['language']} | Words: {score_data['word_count']}

Score Breakdown:
"""

        for category, points in score_data['breakdown'].items():
            indicator = "+" if points > 0 else "-" if points < 0 else "="
            report += f"  {indicator} {category.replace('_', ' ').title()}: {points:+d}\n"

        if score_data['issues']:
            report += f"\nIssues Found:\n"
            for issue in score_data['issues']:
                report += f"  ! {issue}\n"
        else:
            report += f"\nNo issues detected!\n"

        return report

    def suggest_improvements(self, text: str) -> List[str]:
        """
        Get specific improvement suggestions without rewriting.
        Useful for UI feedback.
        """
        score_data = self.calculate_human_score(text)
        suggestions = []

        # Based on breakdown
        if score_data['breakdown'].get('sentence_variety', 0) < 0:
            suggestions.append("Vary your sentence lengths - mix short punchy lines with longer ones")

        if score_data['breakdown'].get('ai_phrases', 0) < -5:
            suggestions.append("Remove AI-sounding phrases like 'it's important to note' or 'let's dive in'")

        if score_data['breakdown'].get('personal_voice', 0) < 0:
            suggestions.append("Add personal pronouns (I, you, we / gua, lu, kita)")

        if score_data['breakdown'].get('conversational', 0) == 0:
            suggestions.append("Add conversational markers (but, so, nah, btw)")

        if score_data['breakdown'].get('specificity', 0) < 0:
            suggestions.append("Add specific numbers, percentages, or dates")

        if score_data['breakdown'].get('brevity', 0) < 0:
            suggestions.append(f"Too long ({score_data['word_count']} words) - trim to under 35 words")

        if not suggestions:
            suggestions.append("Content looks good! Consider making it even punchier.")

        return suggestions
