# Setup Instructions

Complete setup guide for Meme Content Studio.

## Prerequisites

- Python 3.9 or higher
- Anthropic API key (get from https://console.anthropic.com/)
- Windows, macOS, or Linux

## Installation Steps

### 1. Clone or Download the Project

If you haven't already:

```bash
cd "D:\code\Instagram feeds generator"
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client
- `Pillow` - Image generation
- `python-dotenv` - Environment management
- `typer` - CLI framework
- `rich` - Beautiful terminal output

### 4. Configure Environment

**Copy the example environment file:**

```bash
# Windows (Command Prompt)
copy .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env

# macOS/Linux
cp .env.example .env
```

**Edit `.env` and add your API key:**

```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### 5. (Optional) Add Custom Fonts

For better-looking slides, add fonts to `assets/fonts/`:

**Recommended free fonts:**
- Inter (https://fonts.google.com/specimen/Inter)
- Plus Jakarta Sans (https://fonts.google.com/specimen/Plus+Jakarta+Sans)

Download and place `.ttf` files in `assets/fonts/`.

The tool will work with system fonts if custom fonts aren't available.

### 6. Verify Installation

Test that everything works:

```bash
python -m app.main list-tones
```

You should see a list of available tones.

```bash
python -m app.main list-angles
```

You should see available content angles.

## Configuration Options

Edit `.env` to customize:

```bash
# API Configuration
ANTHROPIC_API_KEY=your_key_here
CLAUDE_MODEL=claude-sonnet-4-5-20250929

# Default Settings
DEFAULT_TONE=santai_gaul
DEFAULT_LANGUAGE=bahasa
DEFAULT_ANGLE=story_personal

# Slide Generation
SLIDE_WIDTH=1080
SLIDE_HEIGHT=1920
FONT_SIZE_TITLE=72
FONT_SIZE_BODY=48
BACKGROUND_COLOR=#FFFFFF
TEXT_COLOR=#000000

# Human Score Threshold (0-100)
MIN_HUMAN_SCORE=75
```

## Meme Library Setup (Optional)

The tool works without memes, but adding them makes content better.

### Quick Setup:

1. **Add images** to `meme_library/images/`
   - Use JPG, PNG, or GIF
   - Name descriptively (e.g., `office_cringe.gif`)

2. **Update metadata** in `meme_library/metadata.json`:

```json
{
  "your_meme.jpg": {
    "emotions": ["confident", "powerful"],
    "context": ["success", "achievement"],
    "energy": "high",
    "source": "Movie Name",
    "best_for": ["success content"],
    "language_fit": ["indo", "english"],
    "caption_vibe": "main character energy"
  }
}
```

See `meme_library/README.md` for detailed guide.

## Testing Your Setup

### Test 1: Basic Content Creation

```bash
python -m app.main create \
  -c "Test carousel about productivity" \
  -t santai_gaul \
  -l bahasa \
  -a story_personal \
  -o test_output
```

Check `output/test_output/` for generated slides.

### Test 2: Human Score Check

```bash
python -m app.main check "This is a test sentence to check human score."
```

Should show a score breakdown.

### Test 3: List Commands

```bash
python -m app.main list-tones
python -m app.main list-angles
python -m app.main list-memes
```

All should work without errors.

## Troubleshooting

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'anthropic'`

**Fix:**
```bash
pip install -r requirements.txt
```

Make sure you're in the virtual environment (if you created one).

### API Key Issues

**Error:** `ANTHROPIC_API_KEY not found in environment variables`

**Fix:**
1. Make sure `.env` file exists in project root
2. Check that API key is correctly set: `ANTHROPIC_API_KEY=sk-ant-...`
3. No quotes around the API key
4. No spaces around the `=`

### Font Issues

**Error:** Font-related warnings

**Fix:**
- The tool will use system fonts as fallback
- For better results, add custom fonts to `assets/fonts/`
- On Windows, Arial is used as fallback
- On macOS, Helvetica is used

### Permission Errors

**Error:** Permission denied when creating files

**Fix:**
```bash
# Make sure output directory is writable
mkdir output
chmod 755 output  # macOS/Linux
```

### Python Version

**Error:** Syntax errors or feature not available

**Fix:**
Make sure you're using Python 3.9+:
```bash
python --version
```

If using older version, install Python 3.9+ from python.org.

## Updating

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To pull latest changes (if using git):

```bash
git pull
pip install --upgrade -r requirements.txt
```

## Uninstalling

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Then remove
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Remove All Generated Content

```bash
# Windows
rmdir /s output

# macOS/Linux
rm -rf output
```

## Getting API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new key
5. Copy and paste into `.env`

**Note:** Keep your API key secret. Don't commit `.env` to git!

## Next Steps

Once setup is complete:

1. Read `QUICK_START.md` for usage examples
2. Explore tone files in `tones/`
3. Review angle templates in `angles/`
4. Start creating!

---

**Need help?**
- Check main `README.md` for full documentation
- Review example prompts in `prompts/` folder
- Look at example metadata in `meme_library/metadata.json`

Happy creating! 🎨
