"""
Professional Slide Generator Module - v3.0 (Text-Only)

Generates Instagram-ready carousel slides with text content only.
This is the main orchestration module that:
- Coordinates content and rendering
- Produces professional text-based output
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .config import Config


class SlideGenerator:
    """
    Professional Instagram carousel slide generator (text-only).
    Focuses on clean, readable text content without images.
    """

    # Available themes
    AVAILABLE_THEMES = [
        "dark_mode",
        "minimal_light",
        "ocean_gradient",
        "sunset_gradient",
        "neon_nights",
        "warm_cream",
        "dark_gradient",
    ]

    def __init__(self, theme: str = "dark_mode"):
        """
        Initialize SlideGenerator with theme.

        Args:
            theme: Theme name
        """
        self.theme_name = theme if theme in self.AVAILABLE_THEMES else "dark_mode"

    def set_theme(self, theme: str):
        """Change the current theme."""
        if theme in self.AVAILABLE_THEMES:
            self.theme_name = theme

    def get_available_themes(self) -> List[str]:
        """Get list of available themes."""
        return self.AVAILABLE_THEMES.copy()

    def _clean_slide_text(self, text: str) -> str:
        """Clean slide text of debug markers and formatting artifacts."""
        # Remove debug markers
        text = re.sub(r'\[(?:SLIDE \d+|FINAL SLIDE|HOOK|CTA)\]\s*', '', text)

        # Remove ENGAGEMENT OPTIMIZATION section and everything after it
        text = re.sub(r'\[ENGAGEMENT OPTIMIZATION\].*', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Remove any lines that look like analysis metadata
        text = re.sub(r'^-\s*Primary target:.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        text = re.sub(r'^-\s*Hook type.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        text = re.sub(r'^-\s*Psychological triggers:.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        text = re.sub(r'^-\s*Why it will perform:.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)

        # Remove MEME SUGGESTIONS section
        text = re.sub(r'\[MEME SUGGESTIONS\].*', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Remove HOOK ALTERNATIVES section
        text = re.sub(r'\[HOOK ALTERNATIVES\].*', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Clean up extra whitespace and newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        return text

    def generate_carousel(
        self,
        slides: List[str],
        highlight_data: Optional[List[Dict]] = None,
        output_dir: Optional[Path] = None,
        project_name: str = "carousel",
        **kwargs  # Accept but ignore legacy parameters
    ) -> Tuple[List[str], List[Path]]:
        """
        Generate full carousel with all slides (text-only).

        Args:
            slides: List of slide texts
            highlight_data: Highlight data from rewriter.extract_highlights()
            output_dir: Output directory
            project_name: Name for this carousel project

        Returns:
            Tuple of (list of cleaned slide texts, list of saved file paths)
        """
        output_dir = output_dir or Config.OUTPUT_DIR
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create project subfolder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = output_dir / f"{project_name}_{timestamp}"
        project_dir.mkdir(exist_ok=True)

        # Process slides - clean text and save
        cleaned_slides = []
        saved_paths = []

        for i, slide_text in enumerate(slides):
            slide_num = i + 1
            clean_text = self._clean_slide_text(slide_text)
            cleaned_slides.append(clean_text)

            # Save as text file
            output_path = project_dir / f"slide_{slide_num:02d}.txt"
            output_path.write_text(clean_text, encoding='utf-8')
            saved_paths.append(output_path)

        return cleaned_slides, saved_paths

    def _get_theme_colors(self) -> dict:
        """Get theme colors."""
        # Theme colors for potential future use
        theme_colors = {
            "dark_mode": {
                "background": "#0a0a0a",
                "text_primary": "#FFFFFF",
                "text_secondary": "#666666",
                "accent": "#FFD93D"
            },
            "minimal_light": {
                "background": "#FFFFFF",
                "text_primary": "#1a1a1a",
                "text_secondary": "#666666",
                "accent": "#FFD93D"
            },
            "ocean_gradient": {
                "background": "#0c2340",
                "text_primary": "#FFFFFF",
                "text_secondary": "#88a8c8",
                "accent": "#00d4ff"
            },
            "sunset_gradient": {
                "background": "#1a0a2e",
                "text_primary": "#FFFFFF",
                "text_secondary": "#c8a8d8",
                "accent": "#ff6b6b"
            },
            "neon_nights": {
                "background": "#0a0a1a",
                "text_primary": "#FFFFFF",
                "text_secondary": "#8888ff",
                "accent": "#00ff88"
            },
            "warm_cream": {
                "background": "#faf8f5",
                "text_primary": "#2d2d2d",
                "text_secondary": "#888888",
                "accent": "#e07b39"
            },
            "dark_gradient": {
                "background": "#0f0f0f",
                "text_primary": "#FFFFFF",
                "text_secondary": "#888888",
                "accent": "#FFD93D"
            },
        }

        return theme_colors.get(self.theme_name, theme_colors["dark_mode"])


# Convenience function for simple usage
def generate_carousel_simple(
    slides: List[str],
    theme: str = "dark_mode",
    output_dir: str = "output",
    highlights: List[List[str]] = None
) -> List[str]:
    """
    Simple function to generate carousel text files.

    Args:
        slides: List of slide texts
        theme: Theme name
        output_dir: Output directory
        highlights: Optional list of highlight words per slide (ignored in text-only mode)

    Returns:
        List of output text file paths
    """
    generator = SlideGenerator(theme=theme)
    _, paths = generator.generate_carousel(
        slides=slides,
        output_dir=Path(output_dir)
    )

    return [str(p) for p in paths]
