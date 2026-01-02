# Text-Only Mode Guide

## Overview

Text-only mode allows you to generate Instagram carousel slides with **pure text content**, without any meme images. This is perfect for professional content, educational carousels, or when you want a clean, minimalist aesthetic.

## How to Enable Text-Only Mode

### In the Streamlit UI

1. Start the app: `python -m streamlit run streamlit_app.py`
2. Open the sidebar (left panel)
3. Look for the **"Include Memes"** checkbox under "Slide Display Options"
4. **Uncheck** the "Include Memes" box
5. You'll see: "ℹ️ Text-only mode enabled - No memes will be added to slides"
6. The meme library section will automatically hide

### Visual Indicator

When text-only mode is active:
- ✅ Blue info box appears: "Text-only mode enabled - No memes will be added to slides"
- ✅ Meme library section is hidden (no clutter)
- ✅ During generation, you'll see: "⏭️ Memes disabled - creating text-only slides"

## What Happens in Text-Only Mode

### Generation Process

1. **Content Analysis**: AI still analyzes your topic and creates engaging slides
2. **Slide Creation**: Text slides are generated with the selected theme
3. **Meme Detection Skipped**: No meme matching or emotion detection runs
4. **Clean Output**: Pure text slides rendered at 1080x1350px

### Features Still Available

✅ **All themes**: Dark, minimal, gradients, neon, cream, etc.
✅ **AI highlighting**: Keywords still get emphasized
✅ **Humanization**: Anti-AI detection still runs
✅ **Contextual images**: Stock photos from Pexels (if enabled)
✅ **Caption generation**: Instagram captions with hashtags
✅ **Multiple versions**: Generate 1-3 variations

### Features Disabled

❌ **Meme matching**: No emotion detection or meme selection
❌ **Meme rendering**: No Drake format, Shocked Pikachu, etc.
❌ **Meme library**: Management section hidden from UI

## Use Cases for Text-Only Mode

### 1. Professional Content
- Business tips
- Industry insights
- Educational content
- How-to guides
- Case studies

### 2. Minimalist Aesthetics
- Quotes
- Statistics
- Tips and tricks
- List-based content
- Clean infographics

### 3. Brand Guidelines
- Corporate accounts with strict visual standards
- Professional services (law, finance, consulting)
- Academic institutions
- News and journalism

### 4. Quick Content
- When you don't have time to review meme selections
- Rapid content creation workflows
- Batch content generation

## Comparison: With Memes vs Text-Only

| Feature | With Memes | Text-Only |
|---------|-----------|-----------|
| **Visual Style** | Dynamic, humorous | Clean, professional |
| **Generation Time** | ~30-60 seconds | ~20-40 seconds (faster) |
| **Engagement** | High (memes boost virality) | Moderate (depends on copy) |
| **Use Case** | Viral content, Gen-Z | Professional, educational |
| **Themes** | All 7 themes work | All 7 themes work |
| **Best For** | Finance/trading humor | Tips, guides, insights |

## Examples

### With Memes (Default)
```
Slide 1: Hook text
Slide 2: Body text + Drake format meme
Slide 3: Body text + Shocked Pikachu
Slide 4: Body text + Clown makeup progression
Slide 5: CTA text
```

### Text-Only Mode
```
Slide 1: Hook text with AI-highlighted keywords
Slide 2: Body text with emphasized points
Slide 3: Body text with bullet points
Slide 4: Body text with key takeaways
Slide 5: CTA text with swipe indicator
```

## Tips for Best Results

### 1. Choose the Right Theme
- **Dark Mode**: Best for serious, professional content
- **Minimal Light**: Clean, airy feel for tips and guides
- **Ocean Gradient**: Calming, trustworthy for education
- **Neon Nights**: Modern, tech-focused content

### 2. Enable AI Highlighting
- Keep "AI Keyword Highlighting" checked
- Makes text-only slides more visually interesting
- Draws attention to key points

### 3. Use Strong Copy
- Since there are no memes, your writing must be stronger
- Start with a powerful hook
- Use numbers and specific data
- End with a clear CTA

### 4. Consider Contextual Images
- Enable "Contextual Images" (requires Pexels API)
- Adds stock photos to slides instead of memes
- More professional look than memes

### 5. Test Different Slide Counts
- Text-only works best with 5-7 slides
- Too many slides without visuals can feel monotonous
- Break up long content with highlighted quotes

## Switching Between Modes

You can easily toggle between modes:

1. **During Setup**: Check/uncheck "Include Memes" before generating
2. **After Generation**: Change the checkbox and regenerate
3. **No Data Loss**: Your content idea and settings are preserved

## Technical Details

### Code Flow

When `use_memes=False`:
```python
# streamlit_app.py line 597
meme_results = None
if use_memes:
    # Meme matching runs
else:
    st.write("⏭️ Memes disabled - creating text-only slides")

# slide_generator.py line 215
meme_paths = {}  # Empty dict when meme_recommendations is None
```

### Template Selection

Text-only slides use these templates:
- `templates/slides/body.html` - Standard text slide
- `templates/slides/hook.html` - Opening slide
- `templates/slides/cta.html` - Call-to-action slide

Meme slides would use:
- `templates/slides/body_with_meme.html` - Text + meme split layout

## Troubleshooting

### Problem: Text-only checkbox not visible
**Solution**: Scroll down in the sidebar to "Slide Display Options" section

### Problem: Memes still appearing after unchecking
**Solution**: Make sure to click "Generate Carousel" again after changing settings

### Problem: Slides look too plain
**Solutions**:
- Enable "AI Keyword Highlighting"
- Try a more colorful theme (Neon Nights, Ocean Gradient)
- Enable "Contextual Images" for stock photos
- Use stronger, punchier copy with emojis

### Problem: Want memes on some slides only
**Current Limitation**: It's all or nothing - either all slides get memes or none do
**Workaround**: Generate two carousels and manually combine in Photoshop/Canva

## Future Enhancements

Potential improvements:
- [ ] Per-slide meme control (slide 1,3,5 only)
- [ ] Text-only with custom illustrations
- [ ] Icon-based visual elements (instead of memes)
- [ ] Chart/graph integration for data slides
- [ ] Split-layout text formatting options

## Related Features

- **Contextual Images**: Use stock photos instead of memes
- **Themes**: Change visual style without changing content
- **AI Highlighting**: Emphasize keywords automatically
- **Custom Logo**: Add your brand logo to text slides

## Example Workflows

### Professional B2B Content
```
1. Uncheck "Include Memes"
2. Select "Professional" preset
3. Choose "Minimal Light" theme
4. Enable "AI Keyword Highlighting"
5. Enable "Show Logo"
6. Generate with profesional tone
```

### Educational Tips
```
1. Uncheck "Include Memes"
2. Select "Custom" preset
3. Choose "Ocean Gradient" theme
4. Keep highlighting enabled
5. Use "story_personal" angle
6. Generate with casual tone
```

### Quick Viral Text
```
1. Keep "Include Memes" checked (default)
2. Select "The Economic Influence" preset
3. Use "dark_mode" theme
4. Let AI add humorous memes
5. Generate with ekonomi_edgy tone
```

## Summary

**Text-only mode is perfect when you want:**
- ✅ Professional, clean aesthetics
- ✅ Fast generation (no meme processing)
- ✅ Brand-safe content (no meme risks)
- ✅ Educational or informative carousels
- ✅ Full control over visual presentation

**Keep memes enabled when you want:**
- 🎭 Viral, engaging content
- 🎭 Humor and relatability
- 🎭 Gen-Z audience appeal
- 🎭 Finance/trading content
- 🎭 Maximum shareability

The choice is yours - switch modes anytime with a single checkbox!
