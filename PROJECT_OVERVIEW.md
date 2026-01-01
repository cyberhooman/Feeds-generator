# Meme Content Studio - Project Overview

## What Is This?

**Meme Content Studio** is a local content creation tool that helps you create Instagram carousel posts that sound 100% human-made, not AI-generated.

### The Problem It Solves

AI-generated content often sounds:
- Too perfect
- Too structured
- Too predictable
- Generic and soulless

This tool thinks like a professional content creator, writes like a seasoned copywriter, and strategizes like a marketer — **but outputs content in YOUR authentic voice.**

### Core Philosophy

> "Konten yang bagus bukan tentang kesempurnaan. Ini tentang koneksi."
>
> "Great content isn't about perfection. It's about connection."

---

## Key Features

### 1. **Professional Content Creator Brain**
- Applies proven copywriting frameworks (AIDA, PAS, etc.)
- Uses hook formulas that stop the scroll
- Structures content for maximum engagement
- Understands marketing psychology

### 2. **Anti-AI Detection System**
- Identifies AI-sounding patterns
- Adds human imperfections strategically
- Varies sentence length naturally
- Includes personality markers
- Calculates "human score" (0-100)

### 3. **Multi-Language Support**
- **Bahasa Indonesia:** Multiple tones (santai gaul, profesional, dll.)
- **English:** Various voices (casual friendly, professional, gen z)
- **Mixed:** Natural code-switching

### 4. **Content Angle Templates**
- Personal stories
- Hot takes
- Tips/listicles
- Myth busters
- Behind-the-scenes
- And more...

### 5. **Smart Meme Matching**
- Analyzes emotional beats of content
- Matches perfect memes from your library
- Considers emotion, energy, and context
- Suggests top recommendations with reasoning

### 6. **Slide Generation**
- Instagram-ready dimensions (1080x1920)
- Text-only or meme+text layouts
- Customizable fonts and colors
- Professional-looking output

### 7. **Caption Generator**
- Engaging hooks
- Strategic hashtags
- Multiple CTA options
- Tone-matched writing

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  USER INPUT (rough idea)                    │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  CONTENT REWRITER (Claude API)              │
│  - Applies copywriting frameworks           │
│  - Matches tone & angle templates           │
│  - Generates multiple versions              │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  HUMANIZER                                  │
│  - Calculates human score                   │
│  - Identifies AI patterns                   │
│  - Adds natural imperfections               │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  MEME MATCHER (Claude API)                  │
│  - Analyzes emotional beats                 │
│  - Searches tagged library                  │
│  - Recommends top matches                   │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  SLIDE GENERATOR (Pillow)                   │
│  - Creates text slides                      │
│  - Composites meme images                   │
│  - Exports PNG files                        │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  CAPTION GENERATOR (Claude API)             │
│  - Writes engaging captions                 │
│  - Suggests strategic hashtags              │
│  - Provides CTA variations                  │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  OUTPUT (ready-to-post carousel)            │
└─────────────────────────────────────────────┘
```

---

## Tech Stack

- **Python 3.9+**
- **Anthropic Claude API** (Sonnet 4.5) - Content generation
- **Pillow (PIL)** - Image manipulation
- **Typer** - CLI framework
- **Rich** - Terminal UI
- **python-dotenv** - Environment management

---

## Project Structure

```
meme-content-studio/
│
├── app/                          # Core application
│   ├── __init__.py
│   ├── main.py                   # CLI entry point
│   ├── config.py                 # Configuration management
│   ├── rewriter.py               # Content rewriter (Claude)
│   ├── humanizer.py              # Anti-AI detection
│   ├── meme_matcher.py           # Meme matching logic
│   ├── slide_generator.py        # Image generation
│   └── caption_generator.py      # Caption writing
│
├── prompts/                      # AI prompt templates
│   ├── content_creator.txt       # Master content creator prompt
│   ├── humanizer.txt             # Humanization prompt
│   ├── meme_analyzer.txt         # Meme matching prompt
│   └── caption_writer.txt        # Caption generation prompt
│
├── tones/                        # Tone definitions
│   ├── bahasa/
│   │   ├── santai_gaul.txt
│   │   └── profesional.txt
│   ├── english/
│   │   └── casual_friendly.txt
│   └── mixed/
│
├── angles/                       # Content angle templates
│   ├── story_personal.txt
│   ├── hot_take.txt
│   └── tips_listicle.txt
│
├── meme_library/                 # Your meme collection
│   ├── images/                   # Meme image files
│   ├── metadata.json             # Meme metadata for matching
│   └── README.md
│
├── assets/                       # Fonts, templates, etc.
│   └── fonts/
│
├── output/                       # Generated carousels
│
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore
├── README.md                     # Main documentation
├── QUICK_START.md                # Quick start guide
├── SETUP_INSTRUCTIONS.md         # Detailed setup
└── PROJECT_OVERVIEW.md           # This file
```

---

## How It Works

### Input → Output Flow

**1. You provide a rough idea:**
```
"Dulu gua mikir networking cuma basa-basi. Ternyata salah besar."
```

**2. Content Rewriter transforms it:**
- Applies storytelling framework
- Adds copywriting hooks
- Structures for carousel flow
- Matches your tone and language

**3. Humanizer checks quality:**
- Scans for AI patterns
- Calculates human score
- Adds natural variations if needed

**4. Meme Matcher finds visuals:**
- Analyzes emotional journey
- Searches your library
- Suggests top 3 matches per slide

**5. Slide Generator creates images:**
- Professional layouts
- Instagram dimensions
- Text + memes combined

**6. Caption Generator writes captions:**
- Engaging hooks
- Strategic hashtags
- Clear CTAs

**7. You get ready-to-post content:**
- Multiple slide images
- Caption options
- Complete project summary

---

## Customization

### Add Your Own Tone

Create `tones/custom/my_tone.txt`:

```
## TONE: My Custom Tone

**Target Audience:** [who]
**Voice Description:** [how it sounds]

## LANGUAGE RULES:
...
```

Use it:
```bash
python -m app.main create -c "idea" -t my_tone -l bahasa
```

### Add Your Own Angle

Create `angles/my_angle.txt`:

```
## CONTENT ANGLE: My Angle

**Framework:** [structure]
**Why It Works:** [reasoning]

## STRUCTURE:
...
```

Use it:
```bash
python -m app.main create -c "idea" -a my_angle
```

### Build Your Meme Library

1. Add images to `meme_library/images/`
2. Tag them in `meme_library/metadata.json`
3. The AI will auto-match based on emotions

---

## Use Cases

### Content Creators
- Batch create carousels faster
- Maintain consistent voice
- A/B test different approaches

### Marketers
- Create engaging educational content
- Test messaging variations
- Build brand voice library

### Solopreneurs
- Professional content without designer
- Save time on copywriting
- Consistent posting schedule

### Agencies
- Scale content production
- Maintain client voice
- Streamline workflow

---

## Limitations

### What This Tool IS:
✅ Content creation accelerator
✅ Voice consistency helper
✅ Copywriting framework applier
✅ Human-sounding output generator

### What This Tool IS NOT:
❌ Full automation (you review/edit)
❌ Strategy replacement (you decide what to post)
❌ Voice creator (it amplifies YOUR voice)
❌ Magic bullet (garbage in = garbage out)

---

## Best Practices

### 1. Specific Input
The more specific your rough idea, the better the output.

❌ "content about productivity"
✅ "I wasted 3 years trying morning routines that didn't fit my lifestyle. Here's what actually worked."

### 2. Review & Edit
Always review output. Add your personal touches.

### 3. Build Your Library
Invest time in:
- Well-tagged meme library
- Custom tone definitions
- Your own angle templates

### 4. Iterate
- Test different tones
- Try various angles
- See what resonates
- Refine your approach

### 5. Keep It Human
Use AI for speed, keep creativity yours.

---

## Roadmap

### Current Version (v0.1.0)
✅ Core rewriting engine
✅ Multi-language support
✅ Tone & angle systems
✅ Meme matching
✅ Humanizer
✅ Caption generation
✅ CLI interface

### Planned Features
- [ ] Streamlit web UI
- [ ] A/B version generator
- [ ] Performance tracking
- [ ] Batch mode
- [ ] Tone marketplace
- [ ] Video carousel support
- [ ] Analytics integration

---

## Philosophy

### Why Human-Sounding Matters

AI content is easy to spot:
- Perfect grammar
- Structured paragraphs
- Generic advice
- No personality

Human content connects:
- Natural imperfections
- Varied rhythm
- Personal stories
- Authentic voice

This tool bridges the gap:
- AI efficiency + Human authenticity = Better content

### The 100% Human Test

Before posting, ask:
1. Would I actually say this?
2. Is there at least one specific detail?
3. Does it sound like ME?
4. Would my friend engage with this?

If all yes → post it.
If any no → edit it.

---

## Contributing

This is designed to be customizable:

**Share if you want:**
- Custom tone definitions
- Angle templates
- Workflow improvements

**Keep private if you prefer:**
- Your meme library
- Your voice adaptations
- Your secret sauce

---

## License

MIT - Do whatever you want with it.

---

## Final Thoughts

This tool won't replace your creativity.

It removes friction from your creative process.

Think of it as:
- Spell check (but for AI patterns)
- Template library (but for voice)
- Design tool (but for copy)

**Your ideas + This tool = Content that actually sounds like you.**

That's the goal.

---

Built for creators who give a damn about authenticity.

🎨 Create human. Create real. Create better.
