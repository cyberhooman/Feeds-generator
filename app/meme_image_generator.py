"""
Meme Image Generator - Renders AI Meme Scripts to Images

This module takes MemeScript objects from the MemeAuthorAgent and renders them
into clean, modern meme images. Instead of using pre-existing templates, it creates
original visual compositions based on the SETUP/REACTION format.

Rendering approaches:
1. Split Panel - Setup on top, reaction below (classic meme format)
2. Full Image with Overlay - Background image with text overlay
3. Minimal Text Card - Clean typography-focused design
4. Reaction Type Visual - Abstract/illustrated representation
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import logging

try:
    from .meme_author_agent import MemeScript
    from .config import Config
except ImportError:
    from meme_author_agent import MemeScript
    from config import Config

logger = logging.getLogger(__name__)


# ============================================================================
# VISUAL STYLE CONFIGURATIONS
# ============================================================================

@dataclass
class MemeStyle:
    """Visual style configuration for meme rendering."""
    name: str
    background_color: str
    text_primary: str
    text_secondary: str
    accent_color: str
    font_setup_size: int
    font_reaction_size: int
    padding: int
    border_radius: int
    use_gradient: bool = False
    gradient_colors: Tuple[str, str] = ("#000000", "#1a1a1a")


# Predefined styles that match the carousel themes
MEME_STYLES = {
    "dark_minimal": MemeStyle(
        name="Dark Minimal",
        background_color="#0a0a0a",
        text_primary="#FFFFFF",
        text_secondary="#888888",
        accent_color="#FFD93D",
        font_setup_size=64,
        font_reaction_size=72,
        padding=80,
        border_radius=30
    ),
    "light_clean": MemeStyle(
        name="Light Clean",
        background_color="#FAFAFA",
        text_primary="#1a1a1a",
        text_secondary="#666666",
        accent_color="#FF6B6B",
        font_setup_size=64,
        font_reaction_size=72,
        padding=80,
        border_radius=30
    ),
    "gradient_vibrant": MemeStyle(
        name="Gradient Vibrant",
        background_color="#1a1a2e",
        text_primary="#FFFFFF",
        text_secondary="#a0a0a0",
        accent_color="#00D9FF",
        font_setup_size=60,
        font_reaction_size=68,
        padding=80,
        border_radius=30,
        use_gradient=True,
        gradient_colors=("#1a1a2e", "#16213e")
    ),
    "warm_earth": MemeStyle(
        name="Warm Earth",
        background_color="#2D2A2A",
        text_primary="#F5E6D3",
        text_secondary="#A89583",
        accent_color="#E07A5F",
        font_setup_size=64,
        font_reaction_size=72,
        padding=80,
        border_radius=30
    ),
    "neon_dark": MemeStyle(
        name="Neon Dark",
        background_color="#0D0D0D",
        text_primary="#FFFFFF",
        text_secondary="#666666",
        accent_color="#39FF14",
        font_setup_size=64,
        font_reaction_size=72,
        padding=80,
        border_radius=30
    )
}

# Map intent to visual treatment
INTENT_VISUALS = {
    "smug superiority": {
        "setup_weight": "light",
        "reaction_weight": "bold",
        "reaction_style": "uppercase",
        "divider": "—"
    },
    "delayed regret": {
        "setup_weight": "normal",
        "reaction_weight": "bold",
        "reaction_style": "italic_feel",
        "divider": "..."
    },
    "fake optimism": {
        "setup_weight": "bold",
        "reaction_weight": "light",
        "reaction_style": "normal",
        "divider": ":)"
    },
    "painful self-awareness": {
        "setup_weight": "normal",
        "reaction_weight": "bold",
        "reaction_style": "lowercase",
        "divider": "→"
    },
    "quiet disappointment": {
        "setup_weight": "light",
        "reaction_weight": "normal",
        "reaction_style": "lowercase",
        "divider": "."
    },
    "ironic confidence": {
        "setup_weight": "bold",
        "reaction_weight": "bold",
        "reaction_style": "uppercase",
        "divider": "✓"
    },
    "sudden realization": {
        "setup_weight": "normal",
        "reaction_weight": "bold",
        "reaction_style": "uppercase",
        "divider": "!"
    }
}


# ============================================================================
# MEME IMAGE GENERATOR
# ============================================================================

class MemeImageGenerator:
    """
    Generates meme images from MemeScript objects.

    Creates visually appealing meme images using the SETUP/REACTION format
    without relying on pre-existing meme templates.
    """

    # Instagram carousel dimensions
    SLIDE_WIDTH = 1080
    SLIDE_HEIGHT = 1350

    def __init__(self, fonts_path: str = None, output_dir: str = None):
        """
        Initialize the meme image generator.

        Args:
            fonts_path: Path to fonts directory
            output_dir: Directory to save generated images
        """
        if fonts_path is None:
            fonts_path = Config.BASE_DIR / "assets" / "fonts"
        if output_dir is None:
            output_dir = Config.OUTPUT_DIR / "ai_memes"

        self.fonts_path = Path(fonts_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Font cache
        self._font_cache = {}

        logger.info("MemeImageGenerator initialized")

    def _get_font(self, size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
        """Get a font at specific size, with caching."""
        cache_key = (size, bold, italic)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        # Try to find appropriate font
        font_names = []
        if bold and italic:
            font_names = ["arialbi.ttf", "Arial-BoldItalic.ttf", "DejaVuSans-BoldOblique.ttf"]
        elif bold:
            font_names = ["arialbd.ttf", "Arial-Bold.ttf", "Impact.ttf", "DejaVuSans-Bold.ttf"]
        elif italic:
            font_names = ["ariali.ttf", "Arial-Italic.ttf", "DejaVuSans-Oblique.ttf"]
        else:
            font_names = ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf"]

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
            font = ImageFont.load_default()

        self._font_cache[cache_key] = font
        return font

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _create_gradient_background(
        self,
        size: Tuple[int, int],
        color1: str,
        color2: str,
        direction: str = "vertical"
    ) -> Image.Image:
        """Create a gradient background image."""
        width, height = size
        img = Image.new("RGB", size)

        rgb1 = self._hex_to_rgb(color1)
        rgb2 = self._hex_to_rgb(color2)

        for y in range(height):
            ratio = y / height if direction == "vertical" else 0
            r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
            g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
            b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)

            for x in range(width):
                img.putpixel((x, y), (r, g, b))

        return img

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = " ".join(current_line)
            bbox = font.getbbox(test_line)
            if bbox[2] > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def _draw_text_centered(
        self,
        draw: ImageDraw.Draw,
        text: str,
        y: int,
        font: ImageFont.FreeTypeFont,
        color: str,
        max_width: int,
        center_x: int
    ) -> int:
        """Draw centered text, returns the height used."""
        lines = self._wrap_text(text, font, max_width)
        line_height = font.getbbox("Ay")[3] + 15

        total_height = len(lines) * line_height
        current_y = y

        for line in lines:
            bbox = font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            x = center_x - text_width // 2
            draw.text((x, current_y), line, font=font, fill=color)
            current_y += line_height

        return total_height

    def generate_split_panel_meme(
        self,
        meme: MemeScript,
        style: MemeStyle = None,
        output_path: str = None
    ) -> str:
        """
        Generate a split-panel meme with setup on top, reaction below.

        This is the classic meme format: text on top, punchline below,
        separated by a visual divider.
        """
        if style is None:
            style = MEME_STYLES["dark_minimal"]

        # Create canvas
        if style.use_gradient:
            img = self._create_gradient_background(
                (self.SLIDE_WIDTH, self.SLIDE_HEIGHT),
                style.gradient_colors[0],
                style.gradient_colors[1]
            )
        else:
            img = Image.new("RGB", (self.SLIDE_WIDTH, self.SLIDE_HEIGHT), style.background_color)

        draw = ImageDraw.Draw(img)

        # Get fonts
        font_setup = self._get_font(style.font_setup_size, bold=False)
        font_reaction = self._get_font(style.font_reaction_size, bold=True)
        font_divider = self._get_font(48, bold=False)

        # Get intent-specific styling
        intent_style = INTENT_VISUALS.get(meme.intent.lower(), INTENT_VISUALS["sudden realization"])

        # Apply text transformations
        setup_text = meme.setup
        reaction_text = meme.reaction

        if intent_style["reaction_style"] == "uppercase":
            reaction_text = reaction_text.upper()
        elif intent_style["reaction_style"] == "lowercase":
            reaction_text = reaction_text.lower()

        # Calculate layout
        padding = style.padding
        max_text_width = self.SLIDE_WIDTH - (padding * 2)
        center_x = self.SLIDE_WIDTH // 2
        divider = intent_style["divider"]

        # Draw setup text (upper third)
        setup_y = self.SLIDE_HEIGHT // 4
        setup_height = self._draw_text_centered(
            draw, setup_text, setup_y, font_setup,
            style.text_secondary, max_text_width, center_x
        )

        # Draw divider (center)
        divider_y = self.SLIDE_HEIGHT // 2
        divider_bbox = font_divider.getbbox(divider)
        divider_width = divider_bbox[2] - divider_bbox[0]
        draw.text(
            (center_x - divider_width // 2, divider_y - 20),
            divider,
            font=font_divider,
            fill=style.accent_color
        )

        # Draw reaction text (lower third)
        reaction_y = self.SLIDE_HEIGHT * 2 // 3
        self._draw_text_centered(
            draw, reaction_text, reaction_y, font_reaction,
            style.text_primary, max_text_width, center_x
        )

        # Add subtle reaction type indicator at bottom
        font_small = self._get_font(20)
        reaction_type_text = f"[ {meme.image_reaction_type} ]"
        draw.text(
            (center_x, self.SLIDE_HEIGHT - 60),
            reaction_type_text,
            font=font_small,
            fill=style.text_secondary,
            anchor="mm"
        )

        # Save
        if not output_path:
            output_path = str(self.output_dir / f"meme_{id(meme)}.png")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path, "PNG")

        return output_path

    def generate_minimal_text_card(
        self,
        meme: MemeScript,
        style: MemeStyle = None,
        output_path: str = None
    ) -> str:
        """
        Generate a minimal typography-focused meme card.

        Clean design with emphasis on the text and whitespace.
        """
        if style is None:
            style = MEME_STYLES["light_clean"]

        img = Image.new("RGB", (self.SLIDE_WIDTH, self.SLIDE_HEIGHT), style.background_color)
        draw = ImageDraw.Draw(img)

        # Fonts
        font_setup = self._get_font(56, bold=False)
        font_reaction = self._get_font(72, bold=True)

        padding = 120
        max_width = self.SLIDE_WIDTH - (padding * 2)
        center_x = self.SLIDE_WIDTH // 2

        # Setup text (smaller, secondary color)
        setup_y = self.SLIDE_HEIGHT // 3
        self._draw_text_centered(
            draw, meme.setup, setup_y, font_setup,
            style.text_secondary, max_width, center_x
        )

        # Accent line
        line_y = self.SLIDE_HEIGHT // 2
        line_width = 100
        draw.line(
            [(center_x - line_width, line_y), (center_x + line_width, line_y)],
            fill=style.accent_color,
            width=4
        )

        # Reaction text (larger, primary color)
        reaction_y = self.SLIDE_HEIGHT * 2 // 3 - 40
        self._draw_text_centered(
            draw, meme.reaction, reaction_y, font_reaction,
            style.text_primary, max_width, center_x
        )

        # Save
        if not output_path:
            output_path = str(self.output_dir / f"meme_minimal_{id(meme)}.png")

        img.save(output_path, "PNG")
        return output_path

    def generate_quote_style_meme(
        self,
        meme: MemeScript,
        style: MemeStyle = None,
        output_path: str = None
    ) -> str:
        """
        Generate a quote-style meme with decorative elements.

        Features quotation marks and decorative accents.
        """
        if style is None:
            style = MEME_STYLES["warm_earth"]

        img = Image.new("RGB", (self.SLIDE_WIDTH, self.SLIDE_HEIGHT), style.background_color)
        draw = ImageDraw.Draw(img)

        # Large decorative quote mark
        font_quote = self._get_font(200, bold=True)
        draw.text(
            (80, 150),
            "\u201C",  # Unicode LEFT DOUBLE QUOTATION MARK
            font=font_quote,
            fill=style.accent_color
        )

        # Main fonts
        font_setup = self._get_font(52, bold=False)
        font_reaction = self._get_font(64, bold=True)

        padding = 100
        max_width = self.SLIDE_WIDTH - (padding * 2)
        center_x = self.SLIDE_WIDTH // 2

        # Setup as the "quote"
        setup_y = 400
        self._draw_text_centered(
            draw, meme.setup, setup_y, font_setup,
            style.text_primary, max_width, center_x
        )

        # Reaction as the "attribution"
        reaction_y = self.SLIDE_HEIGHT - 400
        reaction_text = f"— {meme.reaction}"
        self._draw_text_centered(
            draw, reaction_text, reaction_y, font_reaction,
            style.accent_color, max_width, center_x
        )

        # Intent label at bottom
        font_small = self._get_font(18)
        draw.text(
            (center_x, self.SLIDE_HEIGHT - 80),
            meme.intent.upper(),
            font=font_small,
            fill=style.text_secondary,
            anchor="mm"
        )

        # Save
        if not output_path:
            output_path = str(self.output_dir / f"meme_quote_{id(meme)}.png")

        img.save(output_path, "PNG")
        return output_path

    def generate_meme_image(
        self,
        meme: MemeScript,
        style_name: str = "dark_minimal",
        layout: str = "split_panel",
        output_path: str = None
    ) -> Optional[str]:
        """
        Main entry point - generate a meme image from a MemeScript.

        Args:
            meme: The MemeScript to render
            style_name: Name of style from MEME_STYLES
            layout: "split_panel", "minimal", or "quote"
            output_path: Where to save the image

        Returns:
            Path to saved image or None if failed
        """
        if not meme.is_valid:
            logger.warning(f"Cannot render invalid meme: {meme.abort_reason}")
            return None

        style = MEME_STYLES.get(style_name, MEME_STYLES["dark_minimal"])

        if layout == "split_panel":
            return self.generate_split_panel_meme(meme, style, output_path)
        elif layout == "minimal":
            return self.generate_minimal_text_card(meme, style, output_path)
        elif layout == "quote":
            return self.generate_quote_style_meme(meme, style, output_path)
        else:
            logger.warning(f"Unknown layout: {layout}, using split_panel")
            return self.generate_split_panel_meme(meme, style, output_path)

    def generate_memes_for_carousel(
        self,
        memes: Dict[int, MemeScript],
        style_name: str = "dark_minimal",
        layout: str = "split_panel"
    ) -> Dict[int, str]:
        """
        Generate meme images for all slides in a carousel.

        Args:
            memes: Dict mapping slide numbers to MemeScripts
            style_name: Style to use for all memes
            layout: Layout to use for all memes

        Returns:
            Dict mapping slide numbers to image file paths
        """
        paths = {}

        for slide_num, meme in memes.items():
            output_path = str(self.output_dir / f"carousel_meme_slide_{slide_num}.png")
            result = self.generate_meme_image(meme, style_name, layout, output_path)
            if result:
                paths[slide_num] = result
                logger.info(f"Generated meme for slide {slide_num}")

        return paths


# ============================================================================
# INTEGRATION WITH SLIDE GENERATOR
# ============================================================================

def generate_ai_meme_for_slide(
    meme: MemeScript,
    slide_number: int,
    total_slides: int,
    theme: str = "dark_minimal"
) -> Optional[str]:
    """
    Generate an AI meme image formatted for carousel integration.

    Args:
        meme: The MemeScript to render
        slide_number: Current slide number
        total_slides: Total slides in carousel
        theme: Theme name to use

    Returns:
        Path to generated image or None
    """
    generator = MemeImageGenerator()

    # Map carousel themes to meme styles
    theme_map = {
        "dark_mode": "dark_minimal",
        "minimal_light": "light_clean",
        "ocean_gradient": "gradient_vibrant",
        "sunset_warm": "warm_earth",
        "neon_night": "neon_dark",
    }

    style_name = theme_map.get(theme, "dark_minimal")

    output_path = generator.output_dir / f"slide_{slide_number}_of_{total_slides}.png"
    return generator.generate_meme_image(meme, style_name, "split_panel", str(output_path))


# ============================================================================
# TEST / DEMO
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Testing MemeImageGenerator...")
    print("=" * 60)

    # Create test MemeScript objects
    test_memes = [
        MemeScript(
            intent="smug superiority",
            setup="Me explaining crypto to my parents",
            reaction="They bought at ATH",
            image_reaction_type="smug knowing look",
            is_valid=True
        ),
        MemeScript(
            intent="delayed regret",
            setup="Just one more episode",
            reaction="4am. Again.",
            image_reaction_type="exhausted acceptance",
            is_valid=True
        ),
        MemeScript(
            intent="painful self-awareness",
            setup="I'll start the diet Monday",
            reaction="me, every Sunday",
            image_reaction_type="dead inside smile",
            is_valid=True
        ),
        MemeScript(
            intent="sudden realization",
            setup="When you realize the meeting",
            reaction="COULD HAVE BEEN AN EMAIL",
            image_reaction_type="moment of clarity",
            is_valid=True
        )
    ]

    generator = MemeImageGenerator()

    # Test different layouts
    layouts = ["split_panel", "minimal", "quote"]
    styles = list(MEME_STYLES.keys())

    print("\nGenerating test memes...")

    for i, meme in enumerate(test_memes):
        layout = layouts[i % len(layouts)]
        style = styles[i % len(styles)]

        print(f"\nMeme {i+1}:")
        print(f"  Intent: {meme.intent}")
        print(f"  Setup: {meme.setup}")
        print(f"  Reaction: {meme.reaction}")
        print(f"  Layout: {layout}")
        print(f"  Style: {style}")

        output_path = generator.generate_meme_image(meme, style, layout)
        print(f"  Output: {output_path}")

    # Test carousel generation
    print("\n" + "=" * 60)
    print("Testing carousel meme generation...")

    carousel_memes = {
        2: test_memes[0],
        3: test_memes[1],
        4: test_memes[2]
    }

    paths = generator.generate_memes_for_carousel(carousel_memes, "neon_dark", "split_panel")
    print(f"\nGenerated {len(paths)} carousel memes:")
    for slide_num, path in paths.items():
        print(f"  Slide {slide_num}: {path}")

    print("\n" + "=" * 60)
    print("Testing complete!")
