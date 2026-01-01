"""
Render Engine Module

Uses Playwright and Jinja2 to render HTML templates to PNG images.
Creates professional, Instagram-ready carousel slides.

Uses subprocess to call Playwright CLI directly for Python 3.14 compatibility.
"""

import re
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dataclasses import dataclass

# Check if playwright CLI is available
PLAYWRIGHT_AVAILABLE = False
PLAYWRIGHT_PATH = None

def _find_playwright():
    """Find the playwright CLI executable."""
    global PLAYWRIGHT_AVAILABLE, PLAYWRIGHT_PATH

    # Try to find playwright in PATH
    playwright_cmd = shutil.which("playwright")
    if playwright_cmd:
        PLAYWRIGHT_AVAILABLE = True
        PLAYWRIGHT_PATH = playwright_cmd
        return

    # Try common Windows locations
    import sys
    possible_paths = [
        Path(sys.executable).parent / "Scripts" / "playwright.exe",
        Path.home() / "AppData" / "Roaming" / "Python" / f"Python{sys.version_info.major}{sys.version_info.minor}" / "Scripts" / "playwright.exe",
        Path.home() / "AppData" / "Local" / "Programs" / "Python" / f"Python{sys.version_info.major}{sys.version_info.minor}" / "Scripts" / "playwright.exe",
    ]

    for p in possible_paths:
        if p.exists():
            PLAYWRIGHT_AVAILABLE = True
            PLAYWRIGHT_PATH = str(p)
            return

    # Check if playwright module is installed (for import-based check)
    try:
        import playwright
        # If module exists, playwright CLI should be available
        PLAYWRIGHT_AVAILABLE = True
    except ImportError:
        pass

_find_playwright()


@dataclass
class SlideContent:
    """Structured content for a slide."""
    slide_number: int
    template: str
    text: str
    highlights: List[str] = None
    meme_path: Optional[str] = None
    meme_position: Optional[str] = None  # "top", "bottom", "left", "right", "full"

    def __post_init__(self):
        if self.highlights is None:
            self.highlights = []


@dataclass
class RenderOptions:
    """Options for rendering."""
    theme: str = "dark_mode"
    show_logo: bool = False
    logo_path: Optional[str] = None
    logo_position: str = "top-left"
    show_slide_indicator: bool = False
    show_swipe: bool = True
    total_slides: int = 1


class TextFormatter:
    """Formats text for HTML rendering with highlights and markdown."""

    @staticmethod
    def format_text(text: str, highlights: List[str] = None) -> str:
        """
        Convert text with markdown and highlights to HTML.

        Args:
            text: Raw text (may contain **bold** markers)
            highlights: List of words/phrases to highlight

        Returns:
            HTML-formatted text
        """
        if not text:
            return ""

        # Remove debug markers like [SLIDE 1], [FINAL SLIDE], [ENGAGEMENT OPTIMIZATION], etc.
        text = re.sub(r'\[(?:SLIDE \d+|FINAL SLIDE|HOOK|CTA|ENGAGEMENT OPTIMIZATION)\].*?(?=\n\n|\Z)', '', text, flags=re.DOTALL)
        text = re.sub(r'\[(?:SLIDE \d+|FINAL SLIDE|HOOK|CTA)\]\s*', '', text)

        # Remove any remaining bracketed debug content
        text = re.sub(r'\[(?:Primary target|Hook type|Psychological triggers|Why it will perform)[^\]]*\].*?(?=\n|$)', '', text, flags=re.IGNORECASE)

        # Remove lines starting with dashes that look like analysis
        text = re.sub(r'^-\s*(Primary target|Hook type|Psychological triggers|Why it will perform).*$', '', text, flags=re.MULTILINE | re.IGNORECASE)

        # Convert markdown bold (**text**) to HTML
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

        # Convert markdown italic (*text*) to HTML - but not if already part of bold
        text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)

        # Apply highlights
        if highlights:
            for highlight in highlights:
                if highlight and highlight.strip():
                    # Escape special regex characters
                    escaped = re.escape(highlight.strip())
                    # Case-insensitive replacement with highlight span
                    pattern = rf'(?<![<>/])({escaped})(?![<>/])'
                    replacement = r'<span class="highlight">\1</span>'
                    text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Convert newlines to <br> for multi-line text
        text = text.replace('\n', '<br>')

        return text

    @staticmethod
    def calculate_text_size_class(text: str) -> str:
        """
        Determine font size class based on text length.

        Returns: "", "long", or "very-long"
        """
        # Remove HTML tags for length calculation
        clean_text = re.sub(r'<[^>]+>', '', text)
        length = len(clean_text)

        if length > 200:
            return "very-long"
        elif length > 120:
            return "long"
        return ""


class TemplateSelector:
    """Selects the appropriate template for each slide."""

    @staticmethod
    def select_template(
        slide_number: int,
        total_slides: int,
        has_meme: bool,
        meme_position: Optional[str],
        text_length: int
    ) -> str:
        """
        Select the best template for a slide.

        Args:
            slide_number: Current slide number (1-indexed)
            total_slides: Total number of slides
            has_meme: Whether this slide has a meme
            meme_position: Position of meme if present
            text_length: Character count of text

        Returns:
            Template name (without .html extension)
        """
        # First slide is always hook
        if slide_number == 1:
            if has_meme and meme_position == "full":
                return "meme_full"
            return "hook_text"

        # Last slide is CTA
        if slide_number == total_slides:
            return "cta_slide"

        # Middle slides with memes
        if has_meme:
            if meme_position == "full":
                return "meme_full"
            elif text_length < 80:
                return "meme_reaction"  # Short text + meme reaction
            else:
                return "body_with_meme"  # Split layout

        # Default body slide
        return "body_text"


class SlideRenderer:
    """
    Renders HTML templates to PNG images using Playwright via subprocess.
    This approach bypasses Python 3.14 asyncio compatibility issues.
    """

    SLIDE_WIDTH = 1080
    SLIDE_HEIGHT = 1350

    def __init__(self, templates_path: str = None):
        """
        Initialize the renderer.

        Args:
            templates_path: Path to templates directory
        """
        if templates_path is None:
            templates_path = Path(__file__).parent.parent / "templates"

        self.templates_path = Path(templates_path)
        self.themes_path = self.templates_path / "themes"

        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_path)),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self.text_formatter = TextFormatter()
        self.template_selector = TemplateSelector()

    def _load_theme_css(self, theme: str) -> str:
        """Load CSS for a theme."""
        css_file = self.themes_path / f"{theme}.css"
        if css_file.exists():
            return css_file.read_text(encoding='utf-8')

        # Fallback to dark_mode
        fallback = self.themes_path / "dark_mode.css"
        if fallback.exists():
            return fallback.read_text(encoding='utf-8')

        return ""

    def _get_template_path(self, template_name: str) -> str:
        """Get the full template path."""
        return f"slides/{template_name}.html"

    def _render_html_to_png_subprocess(self, html_path: str, output_path: str) -> bool:
        """
        Render HTML to PNG using a Node.js script with Playwright.
        This bypasses Python asyncio issues entirely.
        """
        # Create a simple Node.js script to do the rendering
        node_script = f'''
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const page = await browser.newPage();
    await page.setViewportSize({{ width: {self.SLIDE_WIDTH}, height: {self.SLIDE_HEIGHT} }});
    await page.goto('file:///{html_path.replace(chr(92), "/")}', {{ waitUntil: 'networkidle' }});
    await page.waitForTimeout(500);
    await page.screenshot({{ path: '{output_path.replace(chr(92), "/")}', type: 'png' }});
    await browser.close();
}})();
'''

        # Try using Node.js directly if available
        node_path = shutil.which("node")
        if node_path:
            try:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
                    f.write(node_script)
                    script_path = f.name

                result = subprocess.run(
                    [node_path, script_path],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(Path.home() / "AppData" / "Local" / "ms-playwright")
                )

                Path(script_path).unlink(missing_ok=True)

                if result.returncode == 0 and Path(output_path).exists():
                    return True
            except Exception as e:
                print(f"Node.js rendering failed: {e}")

        return False

    def _render_html_to_png_python(self, html_content: str, output_path: str) -> bool:
        """
        Render HTML to PNG using Python subprocess with a separate script.
        Runs in a completely separate process to avoid asyncio conflicts.

        Uses page.goto() with file:// URL instead of set_content() to allow
        loading of local file:// resources (images, memes, logos).
        """
        # Create a standalone Python script that does the rendering
        render_script = '''
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    html_file = sys.argv[1]
    output_file = sys.argv[2]
    width = int(sys.argv[3])
    height = int(sys.argv[4])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": width, "height": height})

        # Use goto with file:// URL to allow loading of local resources
        # This is critical for meme/logo images to load correctly
        html_path = Path(html_file).absolute()
        file_url = html_path.as_uri()

        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=output_file, type="png")
        browser.close()

if __name__ == "__main__":
    main()
'''

        try:
            # Write HTML to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                html_path = f.name

            # Write render script to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(render_script)
                script_path = f.name

            # Run in separate process
            import sys
            result = subprocess.run(
                [sys.executable, script_path, html_path, output_path,
                 str(self.SLIDE_WIDTH), str(self.SLIDE_HEIGHT)],
                capture_output=True,
                text=True,
                timeout=120,
                # Use CREATE_NO_WINDOW on Windows to avoid console popup
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )

            # Cleanup temp files
            Path(html_path).unlink(missing_ok=True)
            Path(script_path).unlink(missing_ok=True)

            if result.returncode == 0 and Path(output_path).exists():
                return True
            else:
                print(f"Render script error: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("Rendering timed out")
            return False
        except Exception as e:
            print(f"Rendering error: {e}")
            return False

    def render_slide(
        self,
        content: SlideContent,
        options: RenderOptions,
        output_path: str
    ) -> str:
        """
        Render a single slide to PNG.

        Args:
            content: Slide content
            options: Render options
            output_path: Where to save the PNG

        Returns:
            Path to saved PNG
        """
        # Determine template
        text_length = len(content.text)
        has_meme = bool(content.meme_path)

        template_name = content.template or self.template_selector.select_template(
            slide_number=content.slide_number,
            total_slides=options.total_slides,
            has_meme=has_meme,
            meme_position=content.meme_position,
            text_length=text_length
        )

        # Load template
        template = self.jinja_env.get_template(self._get_template_path(template_name))

        # Format text with highlights
        formatted_text = self.text_formatter.format_text(content.text, content.highlights)
        text_size_class = self.text_formatter.calculate_text_size_class(content.text)

        # Load theme CSS
        theme_css = self._load_theme_css(options.theme)

        # Check if theme uses gradient
        has_gradient = "bg-gradient" in theme_css and "linear-gradient" in theme_css

        # Convert file paths to file:// URLs for browser
        meme_url = None
        if content.meme_path:
            meme_path = Path(content.meme_path)
            if meme_path.exists():
                # Convert to file:// URL format
                meme_url = meme_path.absolute().as_uri()

        logo_url = None
        if options.logo_path:
            logo_path = Path(options.logo_path)
            if logo_path.exists():
                logo_url = logo_path.absolute().as_uri()

        # Prepare template context
        context = {
            # Content
            "formatted_text": formatted_text,
            "text_size_class": text_size_class,
            "meme_path": meme_url,
            "meme_position": content.meme_position or "bottom",

            # Theme
            "theme_css": theme_css,
            "has_gradient": has_gradient,

            # Slide metadata
            "slide_number": content.slide_number,
            "total_slides": options.total_slides,

            # Display options
            "show_logo": options.show_logo and logo_url is not None,
            "logo_path": logo_url,
            "logo_position": options.logo_position,
            "show_slide_indicator": options.show_slide_indicator,
            "show_swipe": options.show_swipe and content.slide_number < options.total_slides,
            "show_slide_badge": content.slide_number > 1,

            # CTA-specific
            "engagement_prompt": "SAVE & SHARE",
            "show_action_buttons": False,
        }

        # Render HTML
        html_content = template.render(**context)

        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Render to PNG using subprocess
        success = self._render_html_to_png_python(html_content, str(output_path))

        if not success:
            raise RuntimeError(f"Failed to render slide to {output_path}")

        return str(output_path)

    def render_carousel(
        self,
        slides: List[SlideContent],
        options: RenderOptions,
        output_dir: str
    ) -> List[str]:
        """
        Render all slides in a carousel.

        Args:
            slides: List of slide contents
            options: Render options
            output_dir: Directory to save slides

        Returns:
            List of paths to saved PNG files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Update total slides in options
        options.total_slides = len(slides)

        paths = []
        for i, slide in enumerate(slides):
            slide.slide_number = i + 1
            output_path = output_dir / f"slide_{i + 1:02d}.png"
            path = self.render_slide(slide, options, str(output_path))
            paths.append(path)

        return paths

    def close(self):
        """Cleanup (no-op for subprocess-based renderer)."""
        pass


class SyncSlideRenderer:
    """
    Wrapper for SlideRenderer that handles lifecycle.
    """

    def __init__(self, templates_path: str = None):
        self.templates_path = templates_path

    def render_slide(
        self,
        content: SlideContent,
        options: RenderOptions,
        output_path: str
    ) -> str:
        """Render a single slide."""
        renderer = SlideRenderer(self.templates_path)
        return renderer.render_slide(content, options, output_path)

    def render_carousel(
        self,
        slides: List[SlideContent],
        options: RenderOptions,
        output_dir: str
    ) -> List[str]:
        """Render all slides."""
        renderer = SlideRenderer(self.templates_path)
        return renderer.render_carousel(slides, options, output_dir)


# Convenience function for simple usage
def render_carousel_sync(
    slides_data: List[Dict],
    theme: str = "dark_mode",
    output_dir: str = "output"
) -> List[str]:
    """
    Simple synchronous function to render a carousel.

    Args:
        slides_data: List of dicts with 'text', 'highlights', 'meme_path', 'meme_position'
        theme: Theme name
        output_dir: Output directory

    Returns:
        List of PNG file paths
    """
    slides = []
    for i, data in enumerate(slides_data):
        slides.append(SlideContent(
            slide_number=i + 1,
            template=data.get('template'),
            text=data.get('text', ''),
            highlights=data.get('highlights', []),
            meme_path=data.get('meme_path'),
            meme_position=data.get('meme_position'),
        ))

    options = RenderOptions(
        theme=theme,
        total_slides=len(slides)
    )

    renderer = SyncSlideRenderer()
    return renderer.render_carousel(slides, options, output_dir)
