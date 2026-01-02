"""
Meme Matcher Module - Enhanced Version

Analyzes content emotional beats and matches with appropriate memes from library.
Now with expanded emotion mappings, irony detection, and twist generation.
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .config import Config
from .ai_client import get_ai_client


# ============================================================================
# EXPANDED EMOTION-TO-MEME MAPPINGS
# These are based on actual meme culture usage, not generic emotion matching
# ============================================================================

EMOTION_MEME_MATRIX = {
    # Core emotions -> memes with cultural context
    "irony": {
        "memes": ["distracted_boyfriend.jpg", "clown_makeup.jpg", "this_is_fine.jpg"],
        "context": "When the obvious choice is ignored for something worse",
        "twist_template": "Kamu: {wrong_action}\nYang seharusnya: {right_action}"
    },
    "revelation": {
        "memes": ["galaxy_brain.jpg", "drake_format.jpg", "think_about_it.jpg"],
        "context": "When truth hits different, escalating understanding",
        "twist_template": "Level 1: {basic}\nLevel 999: {enlightened}"
    },
    "painful_truth": {
        "memes": ["crying_cat.jpg", "sad_pablo_escobar.jpg", "waiting_skeleton.jpg"],
        "context": "Financial/emotional loss, relatable pain",
        "twist_template": "Gua setelah {action}: *{consequence}*"
    },
    "predictable_disaster": {
        "memes": ["shocked_pikachu.jpg", "clown_makeup.jpg"],
        "context": "Obvious bad outcome everyone saw coming",
        "twist_template": "Everyone: {warning}\nMe: {ignores}\nResult: *surprised pikachu*"
    },
    "copium": {
        "memes": ["this_is_fine.jpg", "stonks.jpg", "not_stonks.jpg"],
        "context": "Denial, fake optimism, coping mechanism",
        "twist_template": "Market crash -50%\nGua: 'iNi DiScOuNt SeAsOn'"
    },
    "comparison": {
        "memes": ["drake_format.jpg", "distracted_boyfriend.jpg", "two_buttons.jpg"],
        "context": "Better vs worse option, preference",
        "twist_template": "{bad_option} ❌\n{good_option} ✓"
    },
    "escalation": {
        "memes": ["galaxy_brain.jpg", "clown_makeup.jpg", "gru_plan.jpg"],
        "context": "Things getting progressively better/worse",
        "twist_template": "Step 1: {start}\nStep 4: {disaster}"
    },
    "confusion": {
        "memes": ["monkey_puppet.jpg", "woman_yelling_cat.jpg"],
        "context": "Awkward realization, conflicting info",
        "twist_template": "Wait... {realization}"
    },
    "triumph": {
        "memes": ["stonks.jpg", "galaxy_brain.jpg"],
        "context": "Winning, big brain moves",
        "twist_template": "Mereka: {doubt}\nGua: *{wins}*"
    },
    "regret": {
        "memes": ["clown_makeup.jpg", "crying_cat.jpg", "gru_plan.jpg"],
        "context": "Hindsight, poor decisions",
        "twist_template": "Past me: {bad_decision}\nCurrent me: 🤡"
    },
    "shock": {
        "memes": ["shocked_pikachu.jpg", "monkey_puppet.jpg"],
        "context": "Unexpected outcome (ironic or genuine)",
        "twist_template": "{expectation}\nReality: {shocking_result}"
    },
    "waiting": {
        "memes": ["waiting_skeleton.jpg", "sad_pablo_escobar.jpg"],
        "context": "Long wait, patience tested",
        "twist_template": "Me waiting for {thing}: *skeleton*"
    }
}

# Indonesian Gen-Z slang mappings for authentic voice
SLANG_TRANSLATIONS = {
    "i": ["gua", "gue", "aku", "w"],
    "you": ["lu", "lo", "kamu", "u"],
    "very": ["bgt", "banget", "parah"],
    "money": ["duit", "cuan", "uang"],
    "profit": ["cuan", "profit", "untung"],
    "loss": ["boncos", "rugi", "loss"],
    "understand": ["paham", "ngerti", "mudeng"],
    "know": ["tau", "tahu", "ngerti"],
    "actually": ["aslinya", "sebenernya", "real talk"],
    "but": ["tapi", "tapi kan", "but"],
    "because": ["soalnya", "karena", "gegara"],
}

# Topic-specific meme recommendations (for smarter matching)
TOPIC_MEME_MATRIX = {
    "trading": {
        "primary": ["crying_cat.jpg", "stonks.jpg", "clown_makeup.jpg"],
        "scenarios": {
            "loss": "crying_cat.jpg",
            "fomo": "clown_makeup.jpg",
            "leverage": "shocked_pikachu.jpg",
            "denial": "this_is_fine.jpg"
        }
    },
    "finance": {
        "primary": ["drake_format.jpg", "galaxy_brain.jpg", "sad_pablo_escobar.jpg"],
        "scenarios": {
            "comparison": "drake_format.jpg",
            "inflation": "this_is_fine.jpg",
            "waiting": "waiting_skeleton.jpg",
            "revelation": "galaxy_brain.jpg"
        }
    },
    "economics": {
        "primary": ["galaxy_brain.jpg", "this_is_fine.jpg", "distracted_boyfriend.jpg"],
        "scenarios": {
            "government": "clown_makeup.jpg",
            "inequality": "distracted_boyfriend.jpg",
            "data_reveal": "shocked_pikachu.jpg"
        }
    },
    "productivity": {
        "primary": ["drake_format.jpg", "galaxy_brain.jpg", "distracted_boyfriend.jpg"],
        "scenarios": {
            "comparison": "drake_format.jpg",
            "procrastination": "clown_makeup.jpg",
            "burnout": "this_is_fine.jpg"
        }
    },
    "relationships": {
        "primary": ["distracted_boyfriend.jpg", "crying_cat.jpg", "woman_yelling_cat.jpg"],
        "scenarios": {
            "choice": "distracted_boyfriend.jpg",
            "pain": "crying_cat.jpg",
            "argument": "woman_yelling_cat.jpg"
        }
    }
}


class MemeMatcher:
    """
    Analyzes carousel content and matches with perfect memes from library.
    Enhanced with irony detection, twist generation, and cultural context.
    """

    def __init__(self):
        self.client = get_ai_client()
        self.metadata = self.load_metadata()
        self.emotion_matrix = EMOTION_MEME_MATRIX
        self.topic_matrix = TOPIC_MEME_MATRIX

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

    def detect_topic(self, text: str) -> str:
        """
        Detect the primary topic of the content.
        Returns topic key for matrix lookup.
        """
        text_lower = text.lower()

        topic_keywords = {
            "trading": ["trading", "trade", "forex", "saham", "crypto", "leverage", "margin", "stop loss", "take profit"],
            "finance": ["investasi", "invest", "uang", "duit", "tabungan", "gaji", "income", "passive income", "compound"],
            "economics": ["ekonomi", "inflasi", "gdp", "resesi", "subsidi", "pemerintah", "bank sentral", "suku bunga", "fiskal"],
            "productivity": ["produktif", "productive", "habits", "routine", "focus", "kerja", "work", "hustle", "grind"],
            "relationships": ["pacaran", "relationship", "dating", "love", "teman", "friend", "komunikasi", "trust"]
        }

        scores = {}
        for topic, keywords in topic_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[topic] = score

        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return "general"

    def detect_emotional_beat(self, text: str, slide_position: str = "body") -> Dict:
        """
        Detect the emotional beat of a slide with context.

        Args:
            text: Slide text
            slide_position: "hook", "body", "cta"

        Returns:
            Dict with emotion, intensity, and meme suggestions
        """
        text_lower = text.lower()

        # Emotion detection patterns with weights
        emotion_patterns = {
            "irony": [
                (r"padahal|seharusnya|malah|instead|actually", 2),
                (r"bukannya|rather than|should be", 2),
                (r"tapi ternyata|but actually", 3)
            ],
            "revelation": [
                (r"ternyata|rahasia|secret|truth|sebenarnya", 2),
                (r"nobody tells|ga ada yang bilang|hidden", 2),
                (r"baru tau|just realized|mind blown", 3)
            ],
            "painful_truth": [
                (r"rugi|loss|boncos|sakit|hurt", 2),
                (r"menyesal|regret|shouldnt have", 2),
                (r"kehilangan|lost|gone", 2)
            ],
            "predictable_disaster": [
                (r"obviously|jelas|pasti|tentu|sudah tau", 2),
                (r"ya gimana|of course|no wonder", 2),
                (r"siapa suruh|who told you", 2)
            ],
            "copium": [
                (r"fine|baik-baik|okay|santai|tenang", 1),
                (r"its okay|gpp|ga papa|chill", 2),
                (r"discount|sale|opportunity", 2)
            ],
            "comparison": [
                (r"vs|versus|dibanding|compared|bukan.*tapi", 2),
                (r"lebih baik|better|worse|rather", 2),
                (r"pilih|choose|option", 1)
            ],
            "escalation": [
                (r"level|step|stage|dari.*ke|makin", 2),
                (r"semakin|progressively|getting", 2),
                (r"akhirnya|finally|in the end", 2)
            ],
            "shock": [
                (r"what|apa|hah|wow|gila|crazy", 2),
                (r"unexpected|ga nyangka|surprised", 3),
                (r"plot twist|tiba-tiba|suddenly", 3)
            ],
            "regret": [
                (r"dulu|past|kemarin|before|waktu itu", 1),
                (r"seandainya|if only|shouldve", 3),
                (r"menyesal|regret|mistake", 2)
            ]
        }

        import re
        emotion_scores = {}

        for emotion, patterns in emotion_patterns.items():
            score = 0
            for pattern, weight in patterns:
                if re.search(pattern, text_lower):
                    score += weight
            emotion_scores[emotion] = score

        # Get primary emotion
        if max(emotion_scores.values()) > 0:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
        else:
            # Default based on position
            position_defaults = {
                "hook": "shock",
                "body": "revelation",
                "cta": "comparison"
            }
            primary_emotion = position_defaults.get(slide_position, "revelation")

        # Get meme suggestions from matrix
        emotion_data = self.emotion_matrix.get(primary_emotion, {})
        suggested_memes = emotion_data.get("memes", ["drake_format.jpg"])

        return {
            "primary_emotion": primary_emotion,
            "intensity": min(max(emotion_scores.values()), 10),
            "suggested_memes": suggested_memes,
            "context": emotion_data.get("context", ""),
            "twist_template": emotion_data.get("twist_template", "")
        }

    def generate_meme_twist(self, slide_text: str, meme_type: str, topic: str) -> Dict:
        """
        Generate a plot twist for the meme that's genuinely funny.
        Uses AI to create subversive, relatable humor.
        """
        prompt = f"""You are a meme expert who understands Indonesian Gen-Z humor. Generate a funny meme twist.

SLIDE CONTENT: {slide_text}
MEME TYPE: {meme_type}
TOPIC: {topic}

Rules for GENUINE humor:
1. SUBVERSION - The punchline should flip expectations
2. SPECIFICITY - Use exact numbers, real situations (not generic)
3. SELF-DEPRECATING - Making fun of common mistakes we all make
4. CULTURAL - Reference Indonesian/Gen-Z experiences
5. IRONY - The setup should make the punchline land harder

For {meme_type}, generate:
- If Drake format: "reject" panel (bad thing) and "approve" panel (unexpectedly worse/funny alternative)
- If Clown makeup: 4 steps of increasingly bad decisions leading to disaster
- If Shocked Pikachu: Obvious cause -> predictable effect presented as "surprise"
- If Crying cat: Setup that makes the reader say "too real"
- If Galaxy brain: 4 levels from normie to galaxy brain take (with twist at the end)

Respond ONLY in this JSON format:
{{
    "meme_type": "{meme_type}",
    "panels": {{}},  // For template memes
    "setup_text": "",  // For reaction memes
    "caption": "",  // For reaction memes
    "humor_type": "irony/self-deprecating/absurdist/relatable",
    "why_its_funny": "brief explanation"
}}

Make it actually funny - not corporate humor. Think Twitter/TikTok viral, not LinkedIn."""

        try:
            response = self.client.chat(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.8  # Higher for more creative responses
            )

            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            print(f"Twist generation error: {e}")

        # Fallback: Return basic structure
        return {
            "meme_type": meme_type,
            "panels": {},
            "setup_text": slide_text[:50],
            "caption": "* visible pain *",
            "humor_type": "relatable",
            "why_its_funny": "fallback"
        }

    def analyze_content_emotions(self, slides: List[str]) -> List[Dict]:
        """
        Analyze emotional beats of each slide with enhanced detection.
        """
        emotions = []
        total_slides = len(slides)

        for i, slide in enumerate(slides):
            # Determine slide position
            if i == 0:
                position = "hook"
            elif i == total_slides - 1:
                position = "cta"
            else:
                position = "body"

            # Detect topic and emotion
            topic = self.detect_topic(slide)
            emotion_data = self.detect_emotional_beat(slide, position)

            emotions.append({
                "slide_num": i + 1,
                "position": position,
                "topic": topic,
                "emotion": emotion_data["primary_emotion"],
                "intensity": emotion_data["intensity"],
                "energy": "high" if emotion_data["intensity"] > 5 else "medium",
                "tone": self._infer_tone(slide),
                "key_moment": position,
                "suggested_memes": emotion_data["suggested_memes"],
                "twist_template": emotion_data["twist_template"]
            })

        return emotions

    def _infer_tone(self, text: str) -> str:
        """Infer the tone of text (casual/professional/edgy)"""
        text_lower = text.lower()

        # Slang indicators
        slang_words = ["gua", "lu", "bgt", "banget", "anjir", "asli", "literally", "fr", "ngl"]
        slang_count = sum(1 for word in slang_words if word in text_lower)

        if slang_count >= 2:
            return "casual_edgy"
        elif slang_count >= 1:
            return "casual"
        else:
            return "neutral"

    def match_memes(
        self,
        slides: List[str],
        emotions: Optional[List[Dict]] = None,
        generate_twists: bool = True
    ) -> List[Dict]:
        """
        Match memes to slides based on emotional analysis.
        Now with twist generation and variety.
        """
        if not self.metadata:
            # Still try to match even without library
            pass

        if emotions is None:
            emotions = self.analyze_content_emotions(slides)

        recommendations = []
        used_memes = set()  # Track used memes for variety

        for emotion_data in emotions:
            slide_num = emotion_data["slide_num"]
            slide_text = slides[slide_num - 1] if slide_num <= len(slides) else ""

            # Get meme suggestions
            suggested = emotion_data.get("suggested_memes", [])
            topic = emotion_data.get("topic", "general")

            # Add topic-specific memes
            topic_memes = self.topic_matrix.get(topic, {}).get("primary", [])
            all_suggestions = list(dict.fromkeys(suggested + topic_memes))  # Preserve order, remove dupes

            # Filter for variety (don't repeat same meme too much)
            available = [m for m in all_suggestions if m not in used_memes]
            if not available:
                available = all_suggestions  # Reset if all used

            # Determine if slide needs meme
            needs_meme = self._should_have_meme(emotion_data, slide_num, len(slides))

            rec = {
                "slide_num": slide_num,
                "needs_meme": needs_meme,
                "recommendations": []
            }

            if needs_meme and available:
                # Rank memes with some randomization for variety
                ranked = self._rank_memes(available, emotion_data, slide_text)

                for meme_file, confidence in ranked[:3]:
                    meme_rec = {
                        "filename": meme_file,
                        "confidence": confidence,
                        "emotion_match": emotion_data["emotion"],
                        "reason": f"Matches {emotion_data['emotion']} emotion for {topic} content"
                    }

                    # Generate twist if enabled
                    if generate_twists and confidence >= 7:
                        twist = self.generate_meme_twist(slide_text, meme_file, topic)
                        meme_rec["twist"] = twist

                    rec["recommendations"].append(meme_rec)

                # Track used meme
                if rec["recommendations"]:
                    used_memes.add(rec["recommendations"][0]["filename"])

            recommendations.append(rec)

        return recommendations

    def _should_have_meme(self, emotion_data: Dict, slide_num: int, total_slides: int) -> bool:
        """Determine if a slide should have a meme."""
        position = emotion_data.get("position", "body")
        intensity = emotion_data.get("intensity", 5)

        # Rules for meme placement
        if position == "cta":
            return False  # Usually no meme on CTA
        if slide_num == 1:
            return intensity > 5  # Hook needs strong emotional moment
        if slide_num == 2:
            return True  # Backup hook benefits from meme
        if position == "body":
            # Body slides: 60% chance if medium+ intensity
            return intensity >= 4

        return False

    def _rank_memes(self, memes: List[str], emotion_data: Dict, text: str) -> List[Tuple[str, int]]:
        """
        Rank memes by relevance with some randomization.
        Returns list of (filename, confidence_score).
        """
        emotion = emotion_data.get("emotion", "")
        intensity = emotion_data.get("intensity", 5)

        ranked = []
        for meme in memes:
            base_score = 5

            # Boost for emotion match
            emotion_memes = self.emotion_matrix.get(emotion, {}).get("memes", [])
            if meme in emotion_memes:
                base_score += 3

            # Boost for intensity
            if intensity > 7:
                base_score += 1

            # Add some randomness for variety (0-1)
            randomness = random.random()
            final_score = min(10, base_score + randomness)

            ranked.append((meme, int(final_score)))

        # Sort by score descending
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    def get_meme_path(self, filename: str) -> Optional[Path]:
        """Get full path to meme file, checking multiple locations."""
        # Check meme library
        meme_path = Config.MEME_IMAGES_DIR / filename
        if meme_path.exists():
            return meme_path

        # Check cache
        cache_path = Config.BASE_DIR / "cache" / "memes" / filename
        if cache_path.exists():
            return cache_path

        return None

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

    def suggest_meme_for_text(self, text: str) -> Dict:
        """
        Quick method to get a meme suggestion for any text.
        Useful for UI previews.
        """
        topic = self.detect_topic(text)
        emotion_data = self.detect_emotional_beat(text)

        suggested = emotion_data.get("suggested_memes", [])
        if not suggested:
            suggested = self.topic_matrix.get(topic, {}).get("primary", ["drake_format.jpg"])

        return {
            "topic": topic,
            "emotion": emotion_data["primary_emotion"],
            "suggested_meme": suggested[0] if suggested else "drake_format.jpg",
            "alternatives": suggested[1:3] if len(suggested) > 1 else [],
            "twist_template": emotion_data.get("twist_template", "")
        }
