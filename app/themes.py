"""
Theme definitions for Instagram carousel slides.

Provides multiple professional themes with color palettes optimized for Instagram.
Includes: Dark (Economic Influence), Gradient (Modern), Minimal (Clean), and more.
"""

from typing import Dict, Any, List, Tuple


# ============================================================================
# THEME DEFINITIONS
# ============================================================================

THEMES: Dict[str, Dict[str, Any]] = {
    # Dark Mode - The Economic Influence Style
    "dark": {
        "name": "Dark Mode",
        "description": "Bold, dark aesthetic perfect for finance & serious content",
        "background": "#0D0D0D",
        "background_secondary": "#1A1A2E",
        "background_gradient": None,  # Solid color
        "text_primary": "#FFFFFF",
        "text_secondary": "#E8E8E8",
        "accent": "#FFD93D",  # Yellow highlight
        "accent_secondary": "#FF6B6B",  # Red accent
        "highlight_bg": "#FFD93D",  # Background for highlighted text
        "highlight_text": "#0D0D0D",  # Text color on highlight
        "muted": "#888888",
        "success": "#6BCB77",
        "swipe_indicator": "#666666",
        "border_color": "#333333",
        "shadow": True,
        "overlay_opacity": 0.7,  # For images
    },

    # Light Minimal - Clean & Premium
    "minimal": {
        "name": "Minimal Light",
        "description": "Clean, premium aesthetic with lots of whitespace",
        "background": "#FFFFFF",
        "background_secondary": "#FAFAFA",
        "background_gradient": None,
        "text_primary": "#1A1A1A",
        "text_secondary": "#444444",
        "accent": "#000000",  # Black accent
        "accent_secondary": "#666666",
        "highlight_bg": "#000000",
        "highlight_text": "#FFFFFF",
        "muted": "#999999",
        "success": "#2E8B57",
        "swipe_indicator": "#CCCCCC",
        "border_color": "#E0E0E0",
        "shadow": False,
        "overlay_opacity": 0.5,
    },

    # Gradient Blue - Modern & Trendy
    "gradient_blue": {
        "name": "Ocean Gradient",
        "description": "Modern blue gradient, trendy and eye-catching",
        "background": "#667eea",
        "background_secondary": "#764ba2",
        "background_gradient": ["#667eea", "#764ba2"],  # Top to bottom
        "text_primary": "#FFFFFF",
        "text_secondary": "#F0F0F0",
        "accent": "#FFFFFF",
        "accent_secondary": "#FFD93D",
        "highlight_bg": "#FFFFFF",
        "highlight_text": "#667eea",
        "muted": "#D0D0D0",
        "success": "#6BCB77",
        "swipe_indicator": "#FFFFFF",
        "border_color": "#8B9FE8",
        "shadow": True,
        "overlay_opacity": 0.6,
    },

    # Gradient Sunset - Warm & Vibrant
    "gradient_sunset": {
        "name": "Sunset Gradient",
        "description": "Warm sunset colors, vibrant and energetic",
        "background": "#f093fb",
        "background_secondary": "#f5576c",
        "background_gradient": ["#f093fb", "#f5576c"],
        "text_primary": "#FFFFFF",
        "text_secondary": "#FFF5F5",
        "accent": "#FFFFFF",
        "accent_secondary": "#FFD93D",
        "highlight_bg": "#FFFFFF",
        "highlight_text": "#f5576c",
        "muted": "#FFD0D0",
        "success": "#6BCB77",
        "swipe_indicator": "#FFFFFF",
        "border_color": "#F5A0B0",
        "shadow": True,
        "overlay_opacity": 0.6,
    },

    # Gradient Dark - Dark with subtle gradient
    "gradient_dark": {
        "name": "Dark Gradient",
        "description": "Sophisticated dark gradient, professional feel",
        "background": "#0f0c29",
        "background_secondary": "#24243e",
        "background_gradient": ["#0f0c29", "#302b63", "#24243e"],
        "text_primary": "#FFFFFF",
        "text_secondary": "#E0E0E0",
        "accent": "#00D9FF",  # Cyan
        "accent_secondary": "#FF6B6B",
        "highlight_bg": "#00D9FF",
        "highlight_text": "#0f0c29",
        "muted": "#888888",
        "success": "#6BCB77",
        "swipe_indicator": "#666666",
        "border_color": "#444466",
        "shadow": True,
        "overlay_opacity": 0.75,
    },

    # Cream/Beige - Soft & Approachable
    "cream": {
        "name": "Warm Cream",
        "description": "Soft, warm aesthetic perfect for lifestyle content",
        "background": "#FDF6E3",
        "background_secondary": "#F5EDDA",
        "background_gradient": None,
        "text_primary": "#2C2C2C",
        "text_secondary": "#5C5C5C",
        "accent": "#D4A574",  # Warm brown
        "accent_secondary": "#8B7355",
        "highlight_bg": "#D4A574",
        "highlight_text": "#FFFFFF",
        "muted": "#A0937D",
        "success": "#6B8E6B",
        "swipe_indicator": "#C4B7A0",
        "border_color": "#E0D5C5",
        "shadow": False,
        "overlay_opacity": 0.5,
    },

    # Neon - Bold & Attention-grabbing
    "neon": {
        "name": "Neon Nights",
        "description": "Bold neon accents on dark, maximum impact",
        "background": "#0A0A0A",
        "background_secondary": "#121212",
        "background_gradient": None,
        "text_primary": "#FFFFFF",
        "text_secondary": "#E0E0E0",
        "accent": "#00FF88",  # Neon green
        "accent_secondary": "#FF00FF",  # Magenta
        "highlight_bg": "#00FF88",
        "highlight_text": "#0A0A0A",
        "muted": "#666666",
        "success": "#00FF88",
        "swipe_indicator": "#00FF88",
        "border_color": "#00FF88",
        "shadow": True,
        "overlay_opacity": 0.8,
    },
}

# Legacy alias
THEMES["light"] = THEMES["minimal"]


# ============================================================================
# TYPOGRAPHY SETTINGS
# ============================================================================

TYPOGRAPHY = {
    "hook": {
        "font_size": 72,  # Larger for impact
        "font_weight": "bold",
        "line_height": 1.15,
        "max_chars_per_line": 18,
        "letter_spacing": -1,  # Tighter for headlines
    },
    "body": {
        "font_size": 44,
        "font_weight": "regular",
        "line_height": 1.5,
        "max_chars_per_line": 28,
        "letter_spacing": 0,
    },
    "cta": {
        "font_size": 52,
        "font_weight": "bold",
        "line_height": 1.3,
        "max_chars_per_line": 22,
        "letter_spacing": 0,
    },
    "highlight": {
        "font_size": 48,  # Slightly larger for highlighted text
        "font_weight": "bold",
        "padding": (12, 20),  # Vertical, horizontal padding
    },
    "small": {
        "font_size": 28,
        "font_weight": "regular",
        "line_height": 1.4,
    }
}


# ============================================================================
# LAYOUT SETTINGS
# ============================================================================

LAYOUT = {
    "width": 1080,
    "height": 1350,
    "padding": {
        "top": 100,
        "bottom": 120,
        "left": 70,
        "right": 70
    },
    "meme_max_height_ratio": 0.40,  # Max 40% of slide for meme
    "image_max_height_ratio": 0.45,  # Max 45% for context images
    "swipe_indicator_size": 24,
    "text_area_margin": 30,  # Margin around text area
    "highlight_border_radius": 8,
}


# ============================================================================
# SLIDE TEMPLATES
# ============================================================================

SLIDE_TEMPLATES = {
    "hook_centered": {
        "name": "Centered Hook",
        "text_align": "center",
        "text_valign": "center",
        "image_position": None,
    },
    "hook_with_image_bottom": {
        "name": "Hook + Image Bottom",
        "text_align": "center",
        "text_valign": "top",
        "image_position": "bottom",
        "image_height_ratio": 0.35,
    },
    "body_centered": {
        "name": "Centered Body",
        "text_align": "center",
        "text_valign": "center",
        "image_position": None,
    },
    "body_with_image_top": {
        "name": "Image Top + Text",
        "text_align": "center",
        "text_valign": "bottom",
        "image_position": "top",
        "image_height_ratio": 0.40,
    },
    "body_with_image_bottom": {
        "name": "Text + Image Bottom",
        "text_align": "center",
        "text_valign": "top",
        "image_position": "bottom",
        "image_height_ratio": 0.35,
    },
    "split_left_image": {
        "name": "Split - Image Left",
        "text_align": "left",
        "text_valign": "center",
        "image_position": "left",
        "image_width_ratio": 0.45,
    },
    "cta_centered": {
        "name": "CTA Centered",
        "text_align": "center",
        "text_valign": "center",
        "image_position": None,
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_theme(theme_name: str = "dark") -> Dict[str, Any]:
    """Get theme by name, defaults to dark."""
    return THEMES.get(theme_name, THEMES["dark"])


def get_all_themes() -> Dict[str, Dict[str, Any]]:
    """Get all available themes."""
    return THEMES


def get_theme_names() -> List[str]:
    """Get list of theme names."""
    return list(THEMES.keys())


def get_theme_display_options() -> List[Dict[str, str]]:
    """Get themes formatted for UI display."""
    return [
        {"value": name, "label": theme["name"], "description": theme["description"]}
        for name, theme in THEMES.items()
        if name != "light"  # Skip legacy alias
    ]


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def interpolate_color(color1: str, color2: str, factor: float) -> str:
    """Interpolate between two hex colors."""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    result = tuple(int(rgb1[i] + (rgb2[i] - rgb1[i]) * factor) for i in range(3))
    return rgb_to_hex(result)


def get_gradient_colors(gradient: List[str], steps: int) -> List[str]:
    """Generate gradient color steps."""
    if not gradient or len(gradient) < 2:
        return [gradient[0]] * steps if gradient else ["#000000"] * steps

    colors = []
    segments = len(gradient) - 1
    steps_per_segment = steps // segments

    for i in range(segments):
        for j in range(steps_per_segment):
            factor = j / steps_per_segment
            colors.append(interpolate_color(gradient[i], gradient[i + 1], factor))

    # Fill remaining steps
    while len(colors) < steps:
        colors.append(gradient[-1])

    return colors[:steps]
