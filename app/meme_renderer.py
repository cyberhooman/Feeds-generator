"""
Meme Renderer Module

Renders text onto meme templates and creates meme images with captions.
Supports two types of memes:
1. Template memes - Text fills into defined panels (Drake, Expanding Brain)
2. Reaction memes - Caption below/on the image (Shocked Pikachu, Crying Cat)
"""

import os
import textwrap
from pathlib import Path
from typing import Dict, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from .meme_categories import get_meme_category, normalize_meme_filename, MEME_CATEGORIES
from .config import Config


class MemeRenderer:
    """Renders text onto meme images."""

    # Default slide dimensions (Instagram carousel)
    SLIDE_WIDTH = 1080
    SLIDE_HEIGHT = 1350

    def __init__(self, meme_library_path: str = None, fonts_path: str = None):
        """
        Initialize the meme renderer.

        Args:
            meme_library_path: Path to meme images directory
            fonts_path: Path to fonts directory
        """
        if meme_library_path is None:
            meme_library_path = Config.BASE_DIR / "cache" / "memes"
        if fonts_path is None:
            fonts_path = Config.BASE_DIR / "assets" / "fonts"

        self.meme_library_path = Path(meme_library_path)
        self.fonts_path = Path(fonts_path)

        # Ensure directories exist
        self.meme_library_path.mkdir(parents=True, exist_ok=True)
        self.fonts_path.mkdir(parents=True, exist_ok=True)

        # Font cache
        self._font_cache = {}

    def _get_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Get a font at specific size, with caching."""
        cache_key = (size, bold)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        font_names = [
            "Impact.ttf",
            "arial.ttf",
            "Arial.ttf",
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        ]

        font = None
        for font_name in font_names:
            try:
                font_path = self.fonts_path / font_name
                if font_path.exists():
                    font = ImageFont.truetype(str(font_path), size)
                    break
                # Try system fonts
                font = ImageFont.truetype(font_name, size)
                break
            except (OSError, IOError):
                continue

        if font is None:
            # Fallback to default
            font = ImageFont.load_default()

        self._font_cache[cache_key] = font
        return font

    def _find_meme_file(self, meme_filename: str) -> Optional[Path]:
        """Find meme file in library or cache."""
        normalized = normalize_meme_filename(meme_filename)

        # Check direct path
        direct_path = self.meme_library_path / normalized
        if direct_path.exists():
            return direct_path

        # Check with different extensions
        base_name = normalized.replace(".jpg", "").replace(".png", "")
        for ext in [".jpg", ".jpeg", ".png", ".gif"]:
            check_path = self.meme_library_path / f"{base_name}{ext}"
            if check_path.exists():
                return check_path

        # Check parent directories
        for parent in [Config.BASE_DIR / "assets" / "memes", Config.MEME_IMAGES_DIR]:
            if parent.exists():
                for ext in [".jpg", ".jpeg", ".png"]:
                    check_path = parent / f"{base_name}{ext}"
                    if check_path.exists():
                        return check_path

        return None

    def _draw_text_with_stroke(
        self,
        draw: ImageDraw.Draw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: str = "#FFFFFF",
        stroke_color: str = "#000000",
        stroke_width: int = 3,
        anchor: str = "mm",
        align: str = "center"
    ):
        """Draw text with outline/stroke for visibility."""
        x, y = position

        # Draw stroke
        for offset_x in range(-stroke_width, stroke_width + 1):
            for offset_y in range(-stroke_width, stroke_width + 1):
                if offset_x != 0 or offset_y != 0:
                    draw.text(
                        (x + offset_x, y + offset_y),
                        text,
                        font=font,
                        fill=stroke_color,
                        anchor=anchor,
                        align=align
                    )

        # Draw main text
        draw.text(
            position,
            text,
            font=font,
            fill=fill_color,
            anchor=anchor,
            align=align
        )

    def render_template_meme(
        self,
        meme_path: Path,
        config: dict,
        panels_content: Dict[str, str],
        output_path: str = None
    ) -> str:
        """
        Render text into meme template panels (Drake, Expanding Brain, etc.)

        Args:
            meme_path: Path to meme image
            config: Meme configuration from MEME_CATEGORIES
            panels_content: Dict of {panel_name: text_content}
            output_path: Where to save rendered meme

        Returns:
            Path to rendered meme image
        """
        img = Image.open(meme_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # Handle panel-based templates (Drake, Expanding Brain, Clown)
        if "panels" in config:
            for panel_config in config["panels"]:
                panel_name = panel_config["name"]
                text = panels_content.get(panel_name, "")

                if not text:
                    continue

                bbox = panel_config["bbox"]
                font_size = panel_config.get("font_size", 36)
                text_color = panel_config.get("text_color", "#000000")
                max_chars = panel_config.get("max_chars", 50)
                bg_color = panel_config.get("bg_color")

                # Get font
                font = self._get_font(font_size, bold=True)

                # Wrap text to fit panel
                wrap_width = max(8, max_chars // 4)
                wrapped = textwrap.fill(text, width=wrap_width)

                # Calculate center of panel
                center_x = bbox["x"] + bbox["w"] // 2
                center_y = bbox["y"] + bbox["h"] // 2

                # Draw background if specified
                if bg_color:
                    draw.rectangle(
                        [bbox["x"], bbox["y"], bbox["x"] + bbox["w"], bbox["y"] + bbox["h"]],
                        fill=bg_color
                    )

                # Draw text
                draw.text(
                    (center_x, center_y),
                    wrapped,
                    font=font,
                    fill=text_color,
                    anchor="mm",
                    align="center"
                )

        # Handle label-based templates (Distracted Boyfriend)
        elif "labels" in config:
            for label_config in config["labels"]:
                label_name = label_config["name"]
                text = panels_content.get(label_name, "")

                if not text:
                    continue

                pos = label_config["position"]
                font_size = label_config.get("font_size", 28)
                text_color = label_config.get("text_color", "#FFFFFF")
                use_stroke = label_config.get("stroke", True)

                font = self._get_font(font_size, bold=True)

                # Wrap short
                wrapped = textwrap.fill(text, width=15)

                if use_stroke:
                    self._draw_text_with_stroke(
                        draw,
                        (pos["x"], pos["y"]),
                        wrapped,
                        font,
                        fill_color=text_color,
                        anchor="mm",
                        align="center"
                    )
                else:
                    draw.text(
                        (pos["x"], pos["y"]),
                        wrapped,
                        font=font,
                        fill=text_color,
                        anchor="mm",
                        align="center"
                    )

        # Save result
        if not output_path:
            base = meme_path.stem
            output_path = str(self.meme_library_path / f"{base}_rendered.png")

        img.save(output_path, "PNG")
        return output_path

    def render_reaction_meme(
        self,
        meme_path: Path,
        config: dict,
        caption: str,
        setup_text: str = "",
        output_path: str = None
    ) -> str:
        """
        Render reaction meme with caption.

        Args:
            meme_path: Path to meme image
            config: Meme configuration from MEME_CATEGORIES
            caption: Caption text for the meme
            setup_text: Optional setup text (shown above meme)
            output_path: Where to save rendered meme

        Returns:
            Path to rendered meme image
        """
        img = Image.open(meme_path).convert("RGBA")
        caption_position = config.get("caption_position", "bottom")

        if not caption:
            # No caption, just return original
            if output_path:
                img.save(output_path, "PNG")
                return output_path
            return str(meme_path)

        # Get image dimensions
        img_width, img_height = img.size

        # Calculate font size based on image width (smaller images = smaller font)
        base_font_size = max(24, min(48, img_width // 10))
        font = self._get_font(base_font_size, bold=True)
        font_small = self._get_font(int(base_font_size * 0.75), bold=True)

        # Calculate wrap width based on image width (chars per line)
        # Roughly 1 char = 0.6 * font_size pixels wide for Impact font
        char_width = base_font_size * 0.55
        wrap_width = max(10, int(img_width / char_width))
        wrapped_caption = textwrap.fill(caption, width=wrap_width)

        if caption_position == "bottom":
            # Add space below image for caption
            caption_lines = wrapped_caption.count('\n') + 1
            line_height = int(base_font_size * 1.3)
            caption_height = 40 + (caption_lines * line_height)
            new_img = Image.new("RGBA", (img_width, img_height + caption_height), (0, 0, 0, 255))
            new_img.paste(img, (0, 0))

            draw = ImageDraw.Draw(new_img)
            caption_y = img_height + caption_height // 2

            # White text - centered properly
            draw.multiline_text(
                (img_width // 2, caption_y),
                wrapped_caption,
                font=font,
                fill="#FFFFFF",
                anchor="mm",
                align="center"
            )
            img = new_img

        elif caption_position == "overlay":
            # Draw caption over image at bottom
            draw = ImageDraw.Draw(img)
            caption_y = img_height - 80

            self._draw_text_with_stroke(
                draw,
                (img_width // 2, caption_y),
                wrapped_caption,
                font,
                fill_color="#FFFFFF",
                stroke_width=4,
                anchor="mm",
                align="center"
            )

        elif caption_position == "top":
            # Add space above image for caption
            caption_lines = wrapped_caption.count('\n') + 1
            caption_height = 60 + (caption_lines * 50)
            new_img = Image.new("RGBA", (img_width, img_height + caption_height), (0, 0, 0, 255))
            new_img.paste(img, (0, caption_height))

            draw = ImageDraw.Draw(new_img)
            caption_y = caption_height // 2

            draw.text(
                (img_width // 2, caption_y),
                wrapped_caption,
                font=font,
                fill="#FFFFFF",
                anchor="mm",
                align="center"
            )
            img = new_img

        elif caption_position == "split":
            # Special handling for Woman Yelling at Cat style
            draw = ImageDraw.Draw(img)
            labels = config.get("split_labels", ["left", "right"])

            # Split caption by newline or use as single caption
            if "\n" in caption:
                parts = caption.split("\n", 1)
            else:
                parts = [caption, ""]

            # Left side (yelling)
            if len(parts) > 0 and parts[0]:
                self._draw_text_with_stroke(
                    draw,
                    (img_width // 4, img_height - 60),
                    textwrap.fill(parts[0], width=15),
                    font_small,
                    fill_color="#FFFFFF",
                    anchor="mm",
                    align="center"
                )

            # Right side (response)
            if len(parts) > 1 and parts[1]:
                self._draw_text_with_stroke(
                    draw,
                    (3 * img_width // 4, img_height - 60),
                    textwrap.fill(parts[1], width=15),
                    font_small,
                    fill_color="#FFFFFF",
                    anchor="mm",
                    align="center"
                )

        # Save result
        if not output_path:
            base = meme_path.stem
            output_path = str(self.meme_library_path / f"{base}_rendered.png")

        img.save(output_path, "PNG")
        return output_path

    def render_meme(
        self,
        meme_filename: str,
        content: dict,
        output_path: str = None
    ) -> Optional[str]:
        """
        Main entry point - renders any meme type with content.

        Args:
            meme_filename: Name of meme file (e.g., "drake_format.jpg")
            content: Dict with either:
                - "panels": {"reject": "text", "approve": "text"} for template memes
                - "caption": "text" for reaction memes
                - "setup_text": "optional setup text above meme"
            output_path: Where to save rendered meme

        Returns:
            Path to rendered meme image or None if meme not found
        """
        # Find the meme file
        meme_path = self._find_meme_file(meme_filename)
        if not meme_path:
            print(f"Meme not found: {meme_filename}")
            return None

        # Get category and config
        category, config = get_meme_category(meme_filename)

        if category == "template":
            panels = content.get("panels", {})
            return self.render_template_meme(meme_path, config, panels, output_path)
        else:
            caption = content.get("caption", "")
            setup_text = content.get("setup_text", "")
            return self.render_reaction_meme(meme_path, config, caption, setup_text, output_path)

    def create_meme_slide(
        self,
        meme_filename: str,
        content: dict,
        slide_size: Tuple[int, int] = None,
        theme: dict = None,
        output_path: str = None
    ) -> Optional[str]:
        """
        Create a complete slide with meme as dominant element.

        Args:
            meme_filename: Meme file to use
            content: {
                "panels": {...} or "caption": "...",
                "setup_text": "Optional text above meme",
                "slide_number": 3,
                "total_slides": 6
            }
            slide_size: Output dimensions (width, height)
            theme: Theme config with colors
            output_path: Where to save

        Returns:
            Path to saved slide or None if failed
        """
        if slide_size is None:
            slide_size = (self.SLIDE_WIDTH, self.SLIDE_HEIGHT)

        # Default theme
        if not theme:
            theme = {
                "background": "#0a0a0a",
                "text_primary": "#FFFFFF",
                "text_secondary": "#666666",
                "accent": "#FFD93D"
            }

        # Create slide canvas
        slide = Image.new("RGBA", slide_size, theme["background"])
        draw = ImageDraw.Draw(slide)

        # Render the meme first
        rendered_meme_path = self.render_meme(meme_filename, content)
        if not rendered_meme_path:
            return None

        meme_img = Image.open(rendered_meme_path).convert("RGBA")

        # Calculate layout
        padding = 50
        available_width = slide_size[0] - (padding * 2)

        setup_text = content.get("setup_text", "")
        setup_height = 0

        # Draw setup text if present
        if setup_text:
            font = self._get_font(42, bold=True)
            wrapped_setup = textwrap.fill(setup_text, width=28)

            # Calculate setup text height
            bbox = draw.textbbox((0, 0), wrapped_setup, font=font)
            setup_height = bbox[3] - bbox[1] + 60

            draw.text(
                (padding, padding + 30),
                wrapped_setup,
                font=font,
                fill=theme["text_primary"]
            )

        # Calculate meme size and position
        meme_top = padding + setup_height + 20
        available_height = slide_size[1] - meme_top - 120  # Leave room for swipe indicator

        # Resize meme to fit (maintain aspect ratio)
        # Target: meme should be 60-80% of available space
        meme_ratio = meme_img.width / meme_img.height

        if meme_img.width / available_width > meme_img.height / available_height:
            # Width constrained
            new_width = int(available_width * 0.95)
            new_height = int(new_width / meme_ratio)
        else:
            # Height constrained
            new_height = int(available_height * 0.9)
            new_width = int(new_height * meme_ratio)

        # Ensure minimum size (meme should dominate)
        min_width = int(available_width * 0.7)
        if new_width < min_width:
            new_width = min_width
            new_height = int(new_width / meme_ratio)

        meme_img = meme_img.resize((new_width, new_height), Image.LANCZOS)

        # Center meme horizontally
        meme_x = (slide_size[0] - new_width) // 2
        meme_y = meme_top + (available_height - new_height) // 2

        # Add rounded corners to meme
        # Create mask for rounded corners
        mask = Image.new("L", (new_width, new_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, new_width, new_height], radius=20, fill=255)

        # Paste meme onto slide with mask
        slide.paste(meme_img, (meme_x, meme_y), mask)

        # Add slide number
        slide_num = content.get("slide_number")
        total_slides = content.get("total_slides")
        if slide_num and total_slides:
            font_small = self._get_font(24, bold=False)
            draw.text(
                (slide_size[0] - padding, padding),
                f"{slide_num}/{total_slides}",
                font=font_small,
                fill=theme["text_secondary"],
                anchor="rt"
            )

        # Add swipe indicator (if not last slide)
        if slide_num and total_slides and slide_num < total_slides:
            font_small = self._get_font(22, bold=False)
            draw.text(
                (slide_size[0] // 2, slide_size[1] - 50),
                "Swipe >",
                font=font_small,
                fill=theme["text_secondary"],
                anchor="mm"
            )

        # Save
        if not output_path:
            output_dir = Config.OUTPUT_DIR / "meme_slides"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / f"meme_slide_{content.get('slide_number', 0)}.png")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        slide.save(output_path, "PNG")

        # Clean up temp rendered meme
        if rendered_meme_path and "_rendered" in rendered_meme_path:
            try:
                os.remove(rendered_meme_path)
            except:
                pass

        return output_path


# Convenience function
def render_meme_slide(
    meme_filename: str,
    content: dict,
    theme: dict = None,
    output_path: str = None
) -> Optional[str]:
    """
    Quick function to render a meme slide.

    Args:
        meme_filename: Meme to use
        content: Content dict with panels/caption
        theme: Optional theme colors
        output_path: Where to save

    Returns:
        Path to saved slide or None
    """
    renderer = MemeRenderer()
    return renderer.create_meme_slide(meme_filename, content, theme=theme, output_path=output_path)
