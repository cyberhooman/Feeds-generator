"""
Meme categorization and panel definitions for text rendering.

This module defines two categories of memes:
1. Template memes - Have text panels that need to be filled (Drake, Expanding Brain)
2. Reaction memes - Use caption below/on the image (Shocked Pikachu, Crying Cat)
"""

from typing import Dict, List, Tuple, Optional

MEME_CATEGORIES = {
    # ============================================
    # TEMPLATE MEMES - Text fills into panels
    # ============================================
    "template": {
        "drake_format.jpg": {
            "display_name": "Drake Approve/Reject",
            "panels": [
                {
                    "name": "reject",
                    "description": "Thing to reject/bad option",
                    "bbox": {"x": 545, "y": 0, "w": 545, "h": 545},
                    "text_color": "#000000",
                    "font_size": 42,
                    "max_chars": 50,
                    "bg_color": "#FFFFFF"
                },
                {
                    "name": "approve",
                    "description": "Thing to approve/good option",
                    "bbox": {"x": 545, "y": 545, "w": 545, "h": 545},
                    "text_color": "#000000",
                    "font_size": 42,
                    "max_chars": 50,
                    "bg_color": "#FFFFFF"
                }
            ]
        },
        "galaxy_brain.jpg": {
            "display_name": "Expanding Brain",
            "panels": [
                {
                    "name": "small_brain",
                    "description": "Basic/wrong idea",
                    "bbox": {"x": 0, "y": 0, "w": 326, "h": 217},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40,
                    "bg_color": "#FFFFFF"
                },
                {
                    "name": "medium_brain",
                    "description": "Slightly better idea",
                    "bbox": {"x": 0, "y": 217, "w": 326, "h": 217},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40,
                    "bg_color": "#FFFFFF"
                },
                {
                    "name": "big_brain",
                    "description": "Smart idea",
                    "bbox": {"x": 0, "y": 434, "w": 326, "h": 217},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40,
                    "bg_color": "#FFFFFF"
                },
                {
                    "name": "galaxy_brain",
                    "description": "Genius/enlightened idea",
                    "bbox": {"x": 0, "y": 651, "w": 326, "h": 217},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40,
                    "bg_color": "#FFFFFF"
                }
            ]
        },
        "distracted_boyfriend.jpg": {
            "display_name": "Distracted Boyfriend",
            "labels": [
                {
                    "name": "girlfriend",
                    "description": "What you should focus on",
                    "position": {"x": 145, "y": 420},
                    "text_color": "#FFFFFF",
                    "font_size": 28,
                    "stroke": True
                },
                {
                    "name": "boyfriend",
                    "description": "You/the person",
                    "position": {"x": 385, "y": 300},
                    "text_color": "#FFFFFF",
                    "font_size": 28,
                    "stroke": True
                },
                {
                    "name": "other_girl",
                    "description": "The distraction/temptation",
                    "position": {"x": 600, "y": 200},
                    "text_color": "#FFFFFF",
                    "font_size": 28,
                    "stroke": True
                }
            ]
        },
        "two_buttons.jpg": {
            "display_name": "Two Buttons",
            "panels": [
                {
                    "name": "button1",
                    "description": "First option",
                    "bbox": {"x": 75, "y": 75, "w": 200, "h": 80},
                    "text_color": "#000000",
                    "font_size": 18,
                    "max_chars": 30
                },
                {
                    "name": "button2",
                    "description": "Second option",
                    "bbox": {"x": 280, "y": 75, "w": 200, "h": 80},
                    "text_color": "#000000",
                    "font_size": 18,
                    "max_chars": 30
                }
            ]
        },
        "clown_makeup.jpg": {
            "display_name": "Clown Makeup",
            "panels": [
                {
                    "name": "step1",
                    "description": "First mistake/assumption",
                    "bbox": {"x": 0, "y": 0, "w": 250, "h": 170},
                    "text_color": "#000000",
                    "font_size": 20,
                    "max_chars": 35,
                    "bg_color": "#FFFFFF"
                },
                {
                    "name": "step2",
                    "description": "Second mistake",
                    "bbox": {"x": 0, "y": 170, "w": 250, "h": 170},
                    "text_color": "#000000",
                    "font_size": 20,
                    "max_chars": 35,
                    "bg_color": "#FFFFFF"
                },
                {
                    "name": "step3",
                    "description": "Third mistake",
                    "bbox": {"x": 0, "y": 340, "w": 250, "h": 170},
                    "text_color": "#000000",
                    "font_size": 20,
                    "max_chars": 35,
                    "bg_color": "#FFFFFF"
                },
                {
                    "name": "step4",
                    "description": "Final realization",
                    "bbox": {"x": 0, "y": 510, "w": 250, "h": 170},
                    "text_color": "#000000",
                    "font_size": 20,
                    "max_chars": 35,
                    "bg_color": "#FFFFFF"
                }
            ]
        },
        "gru_plan.jpg": {
            "display_name": "Gru's Plan",
            "panels": [
                {
                    "name": "step1",
                    "description": "First step of plan",
                    "bbox": {"x": 400, "y": 0, "w": 400, "h": 300},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40
                },
                {
                    "name": "step2",
                    "description": "Second step",
                    "bbox": {"x": 400, "y": 300, "w": 400, "h": 300},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40
                },
                {
                    "name": "step3",
                    "description": "Unexpected consequence",
                    "bbox": {"x": 400, "y": 600, "w": 400, "h": 300},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40
                },
                {
                    "name": "step4",
                    "description": "Same as step3 (realization)",
                    "bbox": {"x": 400, "y": 900, "w": 400, "h": 300},
                    "text_color": "#000000",
                    "font_size": 24,
                    "max_chars": 40
                }
            ]
        }
    },

    # ============================================
    # REACTION MEMES - Caption below/on image
    # ============================================
    "reaction": {
        "shocked_pikachu.jpg": {
            "display_name": "Shocked Pikachu",
            "caption_position": "bottom",
            "caption_style": "impact",
            "best_for": ["surprise", "obvious outcome", "predictable result", "shocked", "disbelief"],
            "has_text": False
        },
        "crying_cat.jpg": {
            "display_name": "Crying Cat",
            "caption_position": "bottom",
            "caption_style": "impact",
            "best_for": ["sadness", "loss", "regret", "pain", "emotional"],
            "has_text": False
        },
        "stonks.jpg": {
            "display_name": "Stonks",
            "caption_position": "overlay",
            "caption_style": "impact",
            "best_for": ["profit", "gains", "success", "ironic success", "winning"],
            "has_text": True
        },
        "not_stonks.jpg": {
            "display_name": "Not Stonks",
            "caption_position": "overlay",
            "caption_style": "impact",
            "best_for": ["loss", "failure", "decline", "regret"],
            "has_text": True
        },
        "this_is_fine.jpg": {
            "display_name": "This Is Fine",
            "caption_position": "overlay",
            "caption_style": "impact",
            "best_for": ["denial", "coping", "disaster", "chaos"],
            "has_text": True
        },
        "sad_pablo_escobar.jpg": {
            "display_name": "Sad Pablo Escobar",
            "caption_position": "bottom",
            "caption_style": "impact",
            "best_for": ["waiting", "loneliness", "boredom", "anticipation", "sad"],
            "has_text": False
        },
        "monkey_puppet.jpg": {
            "display_name": "Monkey Puppet",
            "caption_position": "bottom",
            "caption_style": "impact",
            "best_for": ["awkward", "uncomfortable", "nervous", "side eye"],
            "has_text": False
        },
        "think_about_it.jpg": {
            "display_name": "Roll Safe Think About It",
            "caption_position": "top",
            "caption_style": "impact",
            "best_for": ["clever", "smart", "lifehack", "big brain", "realization"],
            "has_text": False
        },
        "woman_yelling_cat.jpg": {
            "display_name": "Woman Yelling at Cat",
            "caption_position": "split",  # Special: text on both sides
            "caption_style": "impact",
            "best_for": ["argument", "confusion", "confrontation", "disagreement"],
            "has_text": False,
            "split_labels": ["yelling", "response"]
        },
        "waiting_skeleton.jpg": {
            "display_name": "Waiting Skeleton",
            "caption_position": "bottom",
            "caption_style": "impact",
            "best_for": ["waiting", "patience", "eternal", "still waiting"],
            "has_text": False
        },
        "uno_draw_25.jpg": {
            "display_name": "UNO Draw 25",
            "caption_position": "overlay",
            "caption_style": "impact",
            "best_for": ["stubbornness", "refusal", "choice", "would rather"],
            "has_text": False
        }
    }
}

# Aliases for common filename variations
MEME_ALIASES = {
    "drake": "drake_format.jpg",
    "drake_hotline_bling": "drake_format.jpg",
    "expanding_brain": "galaxy_brain.jpg",
    "brain_levels": "galaxy_brain.jpg",
    "pikachu": "shocked_pikachu.jpg",
    "surprised_pikachu": "shocked_pikachu.jpg",
    "clown": "clown_makeup.jpg",
    "becoming_clown": "clown_makeup.jpg",
    "boyfriend": "distracted_boyfriend.jpg",
    "distracted_bf": "distracted_boyfriend.jpg",
    "pablo": "sad_pablo_escobar.jpg",
    "waiting_pablo": "sad_pablo_escobar.jpg",
    "roll_safe": "think_about_it.jpg",
    "tapping_head": "think_about_it.jpg",
    "cat_yelling": "woman_yelling_cat.jpg",
    "yelling_cat": "woman_yelling_cat.jpg",
}


def normalize_meme_filename(filename: str) -> str:
    """Normalize meme filename to match our definitions."""
    # Remove path and extension variations
    name = filename.lower().replace("-", "_").replace(" ", "_")
    if not name.endswith(".jpg") and not name.endswith(".png"):
        name = name + ".jpg"

    # Check aliases
    base_name = name.replace(".jpg", "").replace(".png", "")
    if base_name in MEME_ALIASES:
        return MEME_ALIASES[base_name]

    return name


def get_meme_category(meme_filename: str) -> Tuple[str, dict]:
    """
    Returns (category_type, meme_config) for a given meme filename.
    category_type is either 'template' or 'reaction'.
    """
    normalized = normalize_meme_filename(meme_filename)

    # Check template memes
    if normalized in MEME_CATEGORIES["template"]:
        return ("template", MEME_CATEGORIES["template"][normalized])

    # Check reaction memes
    if normalized in MEME_CATEGORIES["reaction"]:
        return ("reaction", MEME_CATEGORIES["reaction"][normalized])

    # Default to reaction if unknown
    return ("reaction", {
        "display_name": meme_filename,
        "caption_position": "bottom",
        "caption_style": "impact",
        "best_for": [],
        "has_text": False
    })


def get_panel_descriptions(meme_filename: str) -> Dict[str, str]:
    """
    Returns panel descriptions for AI to generate content.
    Used in prompts to tell AI what text to generate for each panel.
    """
    category, config = get_meme_category(meme_filename)

    if category == "template":
        if "panels" in config:
            return {p["name"]: p["description"] for p in config["panels"]}
        elif "labels" in config:
            return {l["name"]: l["description"] for l in config["labels"]}

    return {}


def get_best_meme_for_emotion(emotion: str) -> Optional[str]:
    """
    Find the best meme for a given emotion/context.

    Args:
        emotion: The emotion or context (e.g., "shocked", "sad", "comparison")

    Returns:
        Meme filename or None
    """
    emotion_lower = emotion.lower()

    # Check reaction memes first (they have explicit best_for)
    for filename, config in MEME_CATEGORIES["reaction"].items():
        if emotion_lower in config.get("best_for", []):
            return filename

    # Check template memes by display name and common use
    template_emotions = {
        "drake_format.jpg": ["comparison", "preference", "choice", "vs", "better"],
        "galaxy_brain.jpg": ["escalation", "enlightenment", "levels", "progression"],
        "clown_makeup.jpg": ["self-deprecating", "mistakes", "regret", "fool"],
        "distracted_boyfriend.jpg": ["distracted", "temptation", "focus"],
        "two_buttons.jpg": ["dilemma", "difficult choice", "anxiety"],
        "gru_plan.jpg": ["planning", "backfire", "unexpected"],
    }

    for filename, emotions in template_emotions.items():
        if emotion_lower in emotions:
            return filename

    return None


def list_all_memes() -> List[Dict]:
    """List all available memes with their categories and descriptions."""
    memes = []

    for filename, config in MEME_CATEGORIES["template"].items():
        memes.append({
            "filename": filename,
            "category": "template",
            "display_name": config["display_name"],
            "has_panels": "panels" in config,
            "has_labels": "labels" in config,
        })

    for filename, config in MEME_CATEGORIES["reaction"].items():
        memes.append({
            "filename": filename,
            "category": "reaction",
            "display_name": config["display_name"],
            "best_for": config.get("best_for", []),
            "caption_position": config.get("caption_position", "bottom"),
        })

    return memes
