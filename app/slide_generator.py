"""
Professional Slide Generator Module - v2.0

Generates Instagram-ready carousel slides using HTML/CSS templates and Playwright.
This is the main orchestration module that:
- Coordinates content, assets, and rendering
- Manages meme/image integration
- Produces professional PNG output
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from PIL import Image
import io

from .config import Config
from .render_engine import (
    SlideRenderer, SyncSlideRenderer,
    SlideContent, RenderOptions,
    TextFormatter, TemplateSelector
)
from .asset_pipeline import AssetPipeline, MemeRecommendationParser
from .meme_renderer import MemeRenderer
from .meme_categories import get_meme_category, get_panel_descriptions

# New AI Meme Agent imports
import logging

logger = logging.getLogger(__name__)


class SlideGenerator:
    """
    Professional Instagram carousel slide generator.
    Uses HTML/CSS templates and Playwright for high-quality PNG output.
    """

    # Available themes (maps to CSS files in templates/themes/)
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
            theme: Theme name (must match a CSS file in templates/themes/)
        """
        self.theme_name = theme if theme in self.AVAILABLE_THEMES else "dark_mode"
        self.renderer = SyncSlideRenderer()
        self.asset_pipeline = AssetPipeline()
        self.text_formatter = TextFormatter()
        self.template_selector = TemplateSelector()
        self.meme_renderer = MemeRenderer()

    def set_theme(self, theme: str):
        """Change the current theme."""
        if theme in self.AVAILABLE_THEMES:
            self.theme_name = theme

    def get_available_themes(self) -> List[str]:
        """Get list of available themes."""
        return self.AVAILABLE_THEMES.copy()

    def _clean_slide_text(self, text: str) -> str:
        """Clean slide text of debug markers and formatting artifacts."""
        import re

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

    def _prepare_slide_contents(
        self,
        slides: List[str],
        highlight_data: Optional[List[Dict]] = None,
        meme_paths: Optional[Dict[int, str]] = None,
    ) -> List[SlideContent]:
        """
        Prepare SlideContent objects for rendering.

        Args:
            slides: List of slide texts
            highlight_data: Highlight data from rewriter.extract_highlights()
            meme_paths: Dict of {slide_number: meme_path}

        Returns:
            List of SlideContent objects
        """
        total_slides = len(slides)
        contents = []

        # Build highlight map
        highlight_map = {}
        if highlight_data:
            for h_data in highlight_data:
                slide_num = h_data.get('slide_num', 0)
                highlights = h_data.get('highlights', [])
                # Extract just the text strings for highlighting
                highlight_texts = [h['text'] for h in highlights if 'text' in h]
                highlight_map[slide_num] = highlight_texts

        for i, slide_text in enumerate(slides):
            slide_num = i + 1

            # Clean the text
            clean_text = self._clean_slide_text(slide_text)

            # Get highlights for this slide
            highlights = highlight_map.get(slide_num, [])

            # Get meme path if available
            meme_path = meme_paths.get(slide_num) if meme_paths else None

            # Determine meme position based on slide type
            meme_position = None
            if meme_path:
                text_length = len(clean_text)
                if slide_num == 1:
                    # Hook slide - prefer meme at bottom or full
                    meme_position = "full" if text_length < 50 else "bottom"
                elif slide_num == total_slides:
                    # CTA slide - usually no meme
                    meme_path = None
                else:
                    # Body slide - position based on text length
                    meme_position = "bottom" if text_length > 100 else "right"

            # Determine split ratio based on text length for vertical layouts
            split_ratio = None
            if meme_path and meme_position in ['top', 'bottom']:
                text_length = len(clean_text)
                if text_length < 80:
                    split_ratio = "40-60"  # Short text, visual priority
                elif text_length > 150:
                    split_ratio = "60-40"  # Long text, text priority
                else:
                    split_ratio = "50-50"  # Balanced default

            # Determine template automatically
            template = self.template_selector.select_template(
                slide_number=slide_num,
                total_slides=total_slides,
                has_meme=bool(meme_path),
                meme_position=meme_position,
                text_length=len(clean_text)
            )

            contents.append(SlideContent(
                slide_number=slide_num,
                template=template,
                text=clean_text,
                highlights=highlights,
                meme_path=meme_path,
                meme_position=meme_position,
                split_ratio=split_ratio
            ))

        return contents

    def generate_carousel(
        self,
        slides: List[str],
        meme_recommendations: Optional[Dict] = None,
        image_assignments: Optional[List[Dict]] = None,
        highlight_data: Optional[List[Dict]] = None,
        output_dir: Optional[Path] = None,
        project_name: str = "carousel",
        show_logo: bool = False,
        logo_path: Optional[str] = None,
        show_slide_indicator: bool = False,
        show_swipe: bool = True,
        use_dynamic_memes: bool = True,
        topic_hint: str = None,
        use_ai_meme_agent: bool = False,
        content_type_override: str = None,
        meme_style: str = "dark_minimal",
        meme_language: str = "en"
    ) -> Tuple[List[Image.Image], List[Path]]:
        """
        Generate full carousel with all slides.

        Args:
            slides: List of slide texts
            meme_recommendations: Meme matching results from MemeMatcher (legacy)
            image_assignments: Image assignments (future: for stock photos)
            highlight_data: Highlight data from rewriter.extract_highlights()
            output_dir: Output directory
            project_name: Name for this carousel project
            show_logo: Whether to show logo on slides
            logo_path: Path to logo image
            show_slide_indicator: Whether to show slide dots
            show_swipe: Whether to show swipe indicator
            use_dynamic_memes: If True, fetch fresh memes from internet dynamically
            topic_hint: Topic hint for better meme matching (e.g., "finance", "tech")
            use_ai_meme_agent: If True, use AI to generate original memes (no templates)
            meme_style: Style for AI meme generation (dark_minimal, light_clean, etc.)
            meme_language: Language for AI meme content ("en" or "id")

        Returns:
            Tuple of (list of PIL Images, list of saved file paths)
        """
        output_dir = output_dir or Config.OUTPUT_DIR
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create project subfolder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = output_dir / f"{project_name}_{timestamp}"
        project_dir.mkdir(exist_ok=True)

        # Get meme paths - either from AI agent, dynamically, or from recommendations
        meme_paths = {}
        dynamic_engine = None
        ai_meme_images = {}  # For AI-generated meme images

        # NEW: Use Smart Image Curator (AI-powered web scraping)
        if use_ai_meme_agent:
            try:
                from .smart_image_curator import SmartImageCurator

                logger.info("Using Smart Image Curator - AI finds relevant images from the web")

                # Create curator
                curator = SmartImageCurator(cache_dir=str(project_dir / "curated_images"))

                # Find relevant images for each slide
                image_results = curator.find_images_for_slides(
                    slides=slides,
                    topic=topic_hint,
                    skip_first_last=True,  # Skip hook and CTA slides
                    content_type=content_type_override
                )

                # Use found images as meme paths
                for slide_num, result in image_results.items():
                    meme_paths[slide_num] = result.local_path

                logger.info(f"Curated {len(image_results)} contextual images from the web")

            except Exception as e:
                logger.warning(f"Smart Image Curator failed, falling back to dynamic memes: {e}")
                # Fall through to dynamic meme handling

        # If AI agent didn't provide memes, try dynamic memes
        if not meme_paths and use_dynamic_memes and meme_recommendations is not None:
            # NEW: Use dynamic meme engine - fetch fresh from internet
            try:
                from .dynamic_meme_engine import DynamicMemeEngine
                dynamic_engine = DynamicMemeEngine()

                # Fetch fresh memes based on slide content analysis
                fetched_memes = dynamic_engine.get_memes_for_slides(slides, topic_hint)

                # Use temporary file paths
                for slide_num, meme in fetched_memes.items():
                    meme_paths[slide_num] = meme.temp_path

            except Exception as e:
                logger.warning(f"Dynamic meme fetch failed, falling back to legacy: {e}")
                # Fall through to legacy handling

        # Legacy: Process meme recommendations to get local paths
        if not meme_paths and meme_recommendations:
            # Handle format from MemeMatcher - available_memes (already in library)
            available_memes = meme_recommendations.get('available_memes', [])
            for meme in available_memes:
                slide_num = meme.get('slide_num', 0)
                filename = meme.get('filename', '')
                if slide_num and filename:
                    meme_path = Config.MEME_IMAGES_DIR / filename
                    if meme_path.exists():
                        meme_paths[slide_num] = str(meme_path)

            # Process analysis to auto-download missing memes
            analysis = meme_recommendations.get('analysis', [])
            for slide_analysis in analysis:
                slide_num = slide_analysis.get('slide_num', 0)
                if slide_num in meme_paths:
                    continue  # Already have a meme for this slide

                if not slide_analysis.get('needs_meme', False):
                    continue  # Slide doesn't need a meme

                meme_suggestion = slide_analysis.get('meme_suggestion', '')
                if meme_suggestion:
                    # Try to get/download the meme via asset pipeline
                    path = self.asset_pipeline.get_meme_path(meme_suggestion, auto_download=True)
                    if path:
                        meme_paths[slide_num] = path

            # Also try missing_memes list
            missing_memes = meme_recommendations.get('missing_memes', [])
            for meme_info in missing_memes:
                slide_num = meme_info.get('slide_num', 0)
                if slide_num in meme_paths:
                    continue

                meme_name = meme_info.get('meme_name', '')
                if meme_name:
                    path = self.asset_pipeline.get_meme_path(meme_name, auto_download=True)
                    if path:
                        meme_paths[slide_num] = path

            # Finally try suggestions dict
            suggestions = meme_recommendations.get('suggestions', {})
            for slide_num, suggestion in suggestions.items():
                slide_num = int(slide_num)
                if slide_num not in meme_paths:
                    path = MemeRecommendationParser.get_best_match(
                        suggestion, self.asset_pipeline
                    )
                    if path:
                        meme_paths[slide_num] = path

        # Prepare slide contents
        slide_contents = self._prepare_slide_contents(
            slides, highlight_data, meme_paths
        )

        # Create render options
        render_options = RenderOptions(
            theme=self.theme_name,
            show_logo=show_logo,
            logo_path=logo_path,
            show_slide_indicator=show_slide_indicator,
            show_swipe=show_swipe,
            total_slides=len(slides)
        )

        # Render all slides
        try:
            saved_paths = self.renderer.render_carousel(
                slide_contents, render_options, str(project_dir)
            )
        except ImportError as e:
            # Playwright not installed - fall back to error message
            raise RuntimeError(
                "Playwright is required for rendering. "
                "Please install it with: pip install playwright && playwright install chromium"
            ) from e

        # Load saved images back as PIL Images for preview
        images = []
        path_objects = []
        for path_str in saved_paths:
            path = Path(path_str)
            path_objects.append(path)
            try:
                img = Image.open(path)
                images.append(img.copy())  # Copy to allow file to be closed
            except Exception as e:
                print(f"Warning: Could not load rendered image {path}: {e}")
                # Create placeholder
                images.append(Image.new('RGB', (1080, 1350), (50, 50, 50)))

        # Clean up temporary meme files from dynamic engine
        if dynamic_engine:
            try:
                dynamic_engine.cleanup_temp_files()
            except Exception:
                pass  # Ignore cleanup errors

        return images, path_objects

    def render_single_slide(
        self,
        text: str,
        slide_number: int = 1,
        total_slides: int = 1,
        template: str = None,
        highlights: List[str] = None,
        meme_path: str = None,
        meme_position: str = None,
        output_path: str = None
    ) -> Image.Image:
        """
        Render a single slide for preview.

        Args:
            text: Slide text
            slide_number: Current slide number
            total_slides: Total number of slides
            template: Template name (auto-selected if None)
            highlights: List of words to highlight
            meme_path: Path to meme image
            meme_position: Meme position
            output_path: Optional path to save the PNG

        Returns:
            PIL Image of the rendered slide
        """
        clean_text = self._clean_slide_text(text)

        # Auto-select template if not provided
        if template is None:
            template = self.template_selector.select_template(
                slide_number=slide_number,
                total_slides=total_slides,
                has_meme=bool(meme_path),
                meme_position=meme_position,
                text_length=len(clean_text)
            )

        content = SlideContent(
            slide_number=slide_number,
            template=template,
            text=clean_text,
            highlights=highlights or [],
            meme_path=meme_path,
            meme_position=meme_position
        )

        options = RenderOptions(
            theme=self.theme_name,
            total_slides=total_slides,
            show_swipe=slide_number < total_slides
        )

        # Use temp path if not provided
        if output_path is None:
            output_path = Config.OUTPUT_DIR / "temp" / f"preview_{slide_number}.png"
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            rendered_path = self.renderer.render_slide(content, options, str(output_path))
            img = Image.open(rendered_path)
            return img.copy()
        except Exception as e:
            print(f"Render error: {e}")
            # Return placeholder on error
            return Image.new('RGB', (1080, 1350), (50, 50, 50))

    def preview_theme(self, sample_text: str = "This is a Sample Hook") -> Image.Image:
        """
        Generate a preview image for the current theme.

        Args:
            sample_text: Sample text to display

        Returns:
            PIL Image preview
        """
        return self.render_single_slide(
            text=sample_text,
            slide_number=1,
            total_slides=5,
            highlights=["Sample", "Hook"]
        )

    def get_image_bytes(self, img: Image.Image) -> bytes:
        """Convert PIL Image to bytes for Streamlit display."""
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer.getvalue()

    def generate_meme_slide(
        self,
        slide_data: dict,
        output_path: str = None
    ) -> Optional[Image.Image]:
        """
        Generate a slide where meme is the dominant element.

        Args:
            slide_data: Dict with meme content:
                - slide_type: "meme_template" or "meme_reaction"
                - meme: filename of meme to use
                - panels: dict of panel texts (for template memes)
                - caption: caption text (for reaction memes)
                - setup_text: optional text above meme
                - slide_number: current slide number
                - total_slides: total number of slides

        Returns:
            PIL Image of the rendered slide or None on error
        """
        slide_type = slide_data.get("slide_type", "meme_reaction")
        meme_filename = slide_data.get("meme", "")

        if not meme_filename:
            return None

        # Build content dict for meme renderer
        content = {
            "slide_number": slide_data.get("slide_number", 1),
            "total_slides": slide_data.get("total_slides", 1),
        }

        if slide_type == "meme_template":
            # Template meme - text fills into panels
            content["panels"] = slide_data.get("panels", {})
        else:
            # Reaction meme - setup text + caption
            content["setup_text"] = slide_data.get("setup_text", "")
            content["caption"] = slide_data.get("caption", "")

        # Get theme colors
        theme = self._get_theme_colors()

        # Generate the meme slide
        try:
            result_path = self.meme_renderer.create_meme_slide(
                meme_filename=meme_filename,
                content=content,
                theme=theme,
                output_path=output_path
            )

            if result_path:
                img = Image.open(result_path)
                return img.copy()
        except Exception as e:
            print(f"Error generating meme slide: {e}")

        return None

    def _get_theme_colors(self) -> dict:
        """Get theme colors for meme rendering."""
        # Default dark theme colors
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

    def generate_carousel_with_meme_slides(
        self,
        slides_data: List[dict],
        output_dir: Optional[Path] = None,
        project_name: str = "carousel"
    ) -> Tuple[List[Image.Image], List[Path]]:
        """
        Generate carousel with mixed text and meme-dominant slides.

        Args:
            slides_data: List of slide data dicts. Each can be:
                - Regular text slide: {"text": "...", "highlights": [...]}
                - Meme slide: {"slide_type": "meme_template/reaction", "meme": "...", ...}
            output_dir: Output directory
            project_name: Name for this carousel project

        Returns:
            Tuple of (list of PIL Images, list of saved file paths)
        """
        output_dir = output_dir or Config.OUTPUT_DIR
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create project subfolder with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = output_dir / f"{project_name}_{timestamp}"
        project_dir.mkdir(exist_ok=True)

        images = []
        path_objects = []
        total_slides = len(slides_data)

        for i, slide_data in enumerate(slides_data):
            slide_num = i + 1
            output_path = project_dir / f"slide_{slide_num:02d}.png"

            # Add slide number info
            slide_data["slide_number"] = slide_num
            slide_data["total_slides"] = total_slides

            # Check if this is a meme slide
            if slide_data.get("slide_type") in ["meme_template", "meme_reaction"]:
                img = self.generate_meme_slide(slide_data, str(output_path))
            else:
                # Regular text slide
                text = slide_data.get("text", "")
                highlights = slide_data.get("highlights", [])
                meme_path = slide_data.get("meme_path")

                img = self.render_single_slide(
                    text=text,
                    slide_number=slide_num,
                    total_slides=total_slides,
                    highlights=highlights,
                    meme_path=meme_path,
                    output_path=str(output_path)
                )

            if img:
                images.append(img)
                path_objects.append(output_path)
            else:
                # Create placeholder on error
                placeholder = Image.new('RGB', (1080, 1350), (50, 50, 50))
                placeholder.save(output_path)
                images.append(placeholder)
                path_objects.append(output_path)

        return images, path_objects


# Convenience function for simple usage
def generate_carousel_simple(
    slides: List[str],
    theme: str = "dark_mode",
    output_dir: str = "output",
    highlights: List[List[str]] = None
) -> List[str]:
    """
    Simple function to generate carousel PNGs.

    Args:
        slides: List of slide texts
        theme: Theme name
        output_dir: Output directory
        highlights: Optional list of highlight words per slide

    Returns:
        List of output PNG paths
    """
    # Build highlight data format
    highlight_data = None
    if highlights:
        highlight_data = []
        for i, h_list in enumerate(highlights):
            slide_highlights = []
            text = slides[i] if i < len(slides) else ""
            for word in h_list:
                start = text.lower().find(word.lower())
                if start >= 0:
                    slide_highlights.append({
                        "text": word,
                        "start": start,
                        "end": start + len(word)
                    })
            highlight_data.append({
                "slide_num": i + 1,
                "highlights": slide_highlights
            })

    generator = SlideGenerator(theme=theme)
    _, paths = generator.generate_carousel(
        slides=slides,
        highlight_data=highlight_data,
        output_dir=Path(output_dir)
    )

    return [str(p) for p in paths]
