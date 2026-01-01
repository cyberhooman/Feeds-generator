"""
Configuration management for Meme Content Studio
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # API Configuration (DeepSeek)
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    PROMPTS_DIR = BASE_DIR / "prompts"
    TONES_DIR = BASE_DIR / "tones"
    ANGLES_DIR = BASE_DIR / "angles"
    ASSETS_DIR = BASE_DIR / "assets"
    MEME_LIBRARY_DIR = BASE_DIR / "meme_library"
    OUTPUT_DIR = BASE_DIR / "output"

    # Meme library
    MEME_IMAGES_DIR = MEME_LIBRARY_DIR / "images"
    MEME_METADATA_PATH = MEME_LIBRARY_DIR / "metadata.json"

    # Fonts
    FONTS_DIR = ASSETS_DIR / "fonts"

    # Default settings
    DEFAULT_TONE = os.getenv("DEFAULT_TONE", "santai_gaul")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "bahasa")
    DEFAULT_ANGLE = os.getenv("DEFAULT_ANGLE", "story_personal")

    # Slide generation settings
    SLIDE_WIDTH = int(os.getenv("SLIDE_WIDTH", 1080))
    SLIDE_HEIGHT = int(os.getenv("SLIDE_HEIGHT", 1920))
    FONT_SIZE_TITLE = int(os.getenv("FONT_SIZE_TITLE", 72))
    FONT_SIZE_BODY = int(os.getenv("FONT_SIZE_BODY", 48))
    BACKGROUND_COLOR = os.getenv("BACKGROUND_COLOR", "#FFFFFF")
    TEXT_COLOR = os.getenv("TEXT_COLOR", "#000000")

    # Human score threshold
    MIN_HUMAN_SCORE = int(os.getenv("MIN_HUMAN_SCORE", 75))

    # Prompt file paths
    CONTENT_CREATOR_PROMPT = PROMPTS_DIR / "content_creator.txt"
    HUMANIZER_PROMPT = PROMPTS_DIR / "humanizer.txt"
    MEME_ANALYZER_PROMPT = PROMPTS_DIR / "meme_analyzer.txt"
    CAPTION_WRITER_PROMPT = PROMPTS_DIR / "caption_writer.txt"

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.OUTPUT_DIR,
            cls.MEME_IMAGES_DIR,
            cls.FONTS_DIR,
            cls.PROMPTS_DIR,
            cls.TONES_DIR,
            cls.ANGLES_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError(
                "DEEPSEEK_API_KEY not found in environment variables. "
                "Please set it in .env file or environment."
            )

        cls.ensure_directories()

    @classmethod
    def ensure_directories_only(cls):
        """Create directories without API validation (for UI startup)"""
        cls.ensure_directories()
