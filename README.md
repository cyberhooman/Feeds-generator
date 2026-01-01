# Meme Content Studio v2.0

**AI-powered Instagram carousel generator that creates ready-to-post, viral content.**

Built with DeepSeek AI | HTML/CSS Templates | Playwright Rendering | 7 Professional Themes

---

## What's New (v2.0)

- **HTML/CSS Template System** - Professional layouts with Jinja2 templates
- **Playwright Rendering** - High-quality PNG output using headless Chromium
- **7 Beautiful Themes** - Dark Mode, Minimal Light, Ocean Gradient, Sunset Gradient, Neon Nights, Warm Cream, Dark Gradient
- **AI Keyword Highlighting** - Auto-highlight important words with accent-colored backgrounds
- **Proper Typography** - Google Fonts (Plus Jakarta Sans, Inter), perfect text rendering
- **Asset Pipeline** - Automatic meme management and caching
- **No More Raw Markdown** - Text properly formatted with bold, highlights, clean layouts

---

## Features

- **Ready-to-Post Slides** - Export 1080x1350 PNG images directly to Instagram
- **7 Professional Themes** - Dark Mode, Minimal Light, Ocean Gradient, Sunset Gradient, Dark Gradient, Warm Cream, Neon Nights
- **HTML/CSS Rendering** - Clean text, proper typography, no markdown artifacts
- **AI Keyword Highlighting** - Automatically highlights key numbers, emotions, and concepts
- **Meme Integration** - Local meme library with auto-matching
- **Viral Content Generation** - 6 proven hook types with psychological triggers
- **100% Human-Sounding** - AI pattern detection & humanization (0-100 scoring)
- **Auto Meme Matching** - AI agent finds perfect memes for each slide
- **Multi-Language** - Bahasa Indonesia, English, Mixed
- **Multiple Tones** - Casual (santai_gaul), Professional, Economics-edgy
- **Algorithm Optimized** - Slide 2 backup hooks, engagement maximization
- **Web UI + CLI** - Streamlit interface or command-line

---

## Quick Start

### Prerequisites
- Python 3.8+
- DeepSeek API key ([Get one here](https://platform.deepseek.com/))

### Installation

```bash
# Clone/download the project
cd "Instagram feeds generator"

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Create .env file
copy .env.example .env
```

### Set Up API Keys

Edit `.env` and add your API keys:

```bash
# Required
DEEPSEEK_API_KEY=sk-your-api-key-here

# Optional - for contextual stock photos
PEXELS_API_KEY=your-pexels-api-key-here
```

### Run the App

```bash
# Start Streamlit Web UI
python -m streamlit run streamlit_app.py
```

Open http://localhost:8501 in your browser.

---

## Available Themes

| Theme | Style | Best For |
|-------|-------|----------|
| **Dark Mode** | Black background, yellow accents, noise texture | Finance, serious content |
| **Minimal Light** | White, clean, black highlights | Premium, professional |
| **Ocean Gradient** | Blue-purple gradient, white highlights | Modern, trendy |
| **Sunset Gradient** | Pink-red warm gradient | Lifestyle, vibrant |
| **Dark Gradient** | Deep blue-purple, cyan accents | Sophisticated, tech |
| **Warm Cream** | Beige, soft aesthetic | Lifestyle, wellness |
| **Neon Nights** | Black with neon green glow | Bold, attention-grabbing |

---

## Usage

### Web UI (Recommended)

1. **Select a Preset** (sidebar):
   - **The Economic Influence** - Dark theme, edgy economics content
   - **Casual Story** - Personal storytelling with sunset gradient
   - **Professional** - Minimal light theme, business content
   - **Custom** - Manual tone/angle/theme selection

2. **Choose Visual Theme**:
   - Select from 7 professional themes
   - Preview shows colors and highlight style

3. **Configure Options**:
   - AI Keyword Highlighting (on/off)
   - Contextual Images (requires Pexels API key)
   - Content versions (1-3)
   - Humanization check

4. **Enter Your Idea**:
   ```
   Example: Kenapa gaji kita stuck tapi harga rumah naik terus?
   Ini breakdown-nya yang jarang orang tau...
   ```

5. **Click Generate** - Get:
   - Ready-to-post PNG slide images
   - AI-highlighted keywords
   - Meme recommendations
   - Instagram captions + hashtags
   - Download all as ZIP

### CLI Commands

```bash
# Generate carousel
python -m app.main create \
  --content "Your rough idea here" \
  --tone santai_gaul \
  --lang bahasa \
  --angle story_personal

# Check human score
python -m app.main check "Your text to analyze"

# List available tones
python -m app.main list-tones

# List content angles
python -m app.main list-angles

# List meme library
python -m app.main list-memes
```

---

## Architecture

### Template System

```
templates/
├── base.html              # Common styles, layout, fonts
├── slides/
│   ├── hook_text.html     # Slide 1 - Large centered hook
│   ├── body_text.html     # Content slides - body text
│   ├── body_with_meme.html # Split layout with meme
│   ├── meme_full.html     # Full meme background
│   ├── meme_reaction.html # Text + meme reaction
│   └── cta_slide.html     # Final CTA slide
└── themes/
    ├── dark_mode.css
    ├── minimal_light.css
    ├── ocean_gradient.css
    ├── sunset_gradient.css
    ├── neon_nights.css
    ├── warm_cream.css
    └── dark_gradient.css
```

### Render Pipeline

1. **ContentRewriter** - Transforms rough idea into slide content
2. **Humanizer** - Detects/removes AI patterns
3. **MemeSearchAgent** - Matches memes to emotional beats
4. **SlideGenerator** - Orchestrates rendering
5. **RenderEngine** - Playwright HTML-to-PNG conversion
6. **AssetPipeline** - Manages meme files and caching

---

## Core Features

### 1. Professional Slide Generation

Creates Instagram-ready images with:
- **1080x1350** dimensions (Instagram carousel standard)
- **HTML/CSS templates** - Clean, professional layouts
- **Google Fonts** - Plus Jakarta Sans, Inter
- **Theme CSS** - Gradient backgrounds, accent colors, glow effects
- **Swipe indicators** and slide numbers
- **CTA slides** with engagement prompts (Save, Share, Comment icons)

### 2. AI Keyword Highlighting

Automatically identifies and highlights:
- **Numbers & statistics** (87%, Rp 50 juta, 3x)
- **Emotional words** (stuck, gagal, sukses, breakthrough)
- **Key concepts** (inflasi, investasi, productivity)

Highlights appear with accent-colored backgrounds for visual emphasis.

### 3. Template Selection

Automatic template selection based on:
- **Slide position** (hook, body, CTA)
- **Text length** (short vs long content)
- **Meme presence** (with/without meme)
- **Meme position** (top, bottom, left, right, full)

### 4. Viral Framework

Built-in psychology for maximum engagement:

| Hook Type | Trigger | Example |
|-----------|---------|---------|
| Question | Brain completion | "Are you doing [X] wrong?" |
| Shock/Data | Disbelief | "87% fail at [X]. Here's why." |
| Promise | Transformation | "How I [achieved X] in [time]" |
| Mistake/Myth | Fear | "Stop doing [X]. Here's why." |
| Curiosity | FOMO | "Nobody talks about this, but..." |
| Unpopular Opinion | Tribal instinct | "Hot take: [controversial view]" |

**Algorithm Optimization:**
- Slide 2 works as backup hook (Instagram re-shows it first)
- 70%+ completion = 3-5x more non-follower reach
- Explicit CTAs for saves/shares/comments

### 5. Humanizer

Detects and removes AI patterns:

```
Human Score: 85/100 PASSES

Issues Found:
- Sentence length too uniform (fixed)
- AI phrase detected: "Let's dive in" (removed)
```

**What it catches:**
- Structural patterns (perfect parallelism, over-bulleting)
- AI phrases ("In today's world...", "Mari kita bahas...")
- Stylistic tells (emoji overload, perfect grammar)

### 6. Meme Search Agent

Automatically matches memes to content:

```
Slide 1: shock/curiosity -> shocked_pikachu.jpg
Slide 3: financial pain -> crying_cat.jpg
Slide 5: system criticism -> clown_makeup.jpg
```

**Features:**
- Analyzes emotional beats per slide
- Checks your meme library
- Suggests downloads for missing memes
- Auto-generates metadata for new memes

---

## Project Structure

```
Instagram feeds generator/
├── app/
│   ├── ai_client.py          # DeepSeek API integration
│   ├── config.py             # Configuration management
│   ├── rewriter.py           # Content transformation + highlighting
│   ├── humanizer.py          # Anti-AI detection
│   ├── meme_matcher.py       # Meme matching logic
│   ├── meme_search_agent.py  # Auto meme discovery
│   ├── caption_generator.py  # Instagram captions
│   ├── slide_generator.py    # Main orchestration
│   ├── render_engine.py      # Playwright HTML-to-PNG
│   ├── asset_pipeline.py     # Meme file management
│   └── main.py               # CLI interface
├── templates/
│   ├── base.html             # Common HTML structure
│   ├── slides/               # Slide templates
│   └── themes/               # Theme CSS files
├── prompts/
│   ├── content_creator.txt   # Main generation prompt
│   ├── viral_framework.txt   # Viral psychology rules
│   └── caption_writer.txt    # Caption optimization
├── tones/
│   ├── bahasa/               # Indonesian tones
│   ├── english/              # English tones
│   └── mixed/                # Mixed language tones
├── angles/                   # Content structure templates
├── assets/memes/             # Permanent meme library
├── cache/memes/              # Downloaded meme cache
├── output/                   # Generated carousels
├── streamlit_app.py          # Web UI
├── requirements.txt          # Dependencies
└── .env.example              # Environment template
```

---

## Configuration

### Environment Variables (.env)

```bash
# Required
DEEPSEEK_API_KEY=sk-your-key-here

# Optional - Contextual Images
PEXELS_API_KEY=your-pexels-key-here

# Optional - Model
DEEPSEEK_MODEL=deepseek-chat

# Optional - Defaults
DEFAULT_TONE=santai_gaul
DEFAULT_LANGUAGE=bahasa
DEFAULT_ANGLE=story_personal

# Optional - Quality
MIN_HUMAN_SCORE=75
```

---

## Customization

### Add Custom Theme

Create `templates/themes/my_theme.css`:

```css
:root {
    --bg-primary: #000000;
    --bg-gradient: linear-gradient(135deg, #000000, #333333);

    --text-primary: #ffffff;
    --text-secondary: #cccccc;

    --accent: #FFD93D;
    --accent-secondary: #FF6B6B;

    --highlight-bg: #FFD93D;
    --highlight-text: #000000;
}

.slide-container {
    background: var(--bg-gradient);
}

.highlight {
    background: var(--highlight-bg);
    color: var(--highlight-text);
    padding: 6px 16px;
    border-radius: 6px;
}
```

Then add the theme name to `SlideGenerator.AVAILABLE_THEMES` in `slide_generator.py`.

### Add Memes to Library

1. Save meme images to `assets/memes/`
2. Click **"Sync Library"** in UI sidebar
3. AI auto-generates metadata

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| AI | DeepSeek API (OpenAI-compatible) |
| Web UI | Streamlit |
| CLI | Typer + Rich |
| Rendering | Playwright + Chromium |
| Templates | Jinja2 + HTML/CSS |
| Images | Pillow (post-processing) |
| Config | python-dotenv |

---

## Output

Generated content saved to `output/[project-name]_[timestamp]/`:

```
output/carousel_20241228_143052/
├── slide_01.png    # Hook slide (1080x1350)
├── slide_02.png    # Body slide with highlights
├── slide_03.png    # Body slide with meme
├── slide_04.png    # Body slide
└── slide_05.png    # CTA slide
```

Download all slides + captions as a single ZIP file from the UI.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Playwright not installed" | Run `pip install playwright && playwright install chromium` |
| "API key not found" | Check `.env` file exists with correct key |
| "Module not found" | Run `pip install -r requirements.txt` |
| Content sounds AI | Use santai_gaul tone, don't skip humanizer |
| No meme matches | Add more memes to `assets/memes/`, click Sync |
| Slides not rendering | Ensure Playwright + Chromium installed |

---

## License

MIT License - Use freely for personal and commercial projects.

---

**Built for content creators who want viral reach with professional design.**
