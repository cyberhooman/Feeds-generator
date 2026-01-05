# Smart Image Curator - AI-Powered Visual Content Finder

## Overview

The **Smart Image Curator** is an intelligent AI agent that acts like a professional content creator, finding the perfect images for your carousel slides by scraping the web.

Unlike template-based systems, it:
- ✅ **Finds contextually relevant images** (not just mainstream memes)
- ✅ **Searches multiple sources** (Google Images, Bing Images, Imgur)
- ✅ **Uses AI to determine** what kind of visual works best
- ✅ **No paid APIs required** (pure web scraping)
- ✅ **Versatile image types**: memes, reaction images, movie scenes, photos, abstract visuals

## How It Works

### 1. AI Analysis
The curator uses DeepSeek AI to analyze each slide and determine:
- **Image type needed**: meme, photo, scene, or abstract
- **Mood/emotion**: What feeling should the image convey?
- **Search queries**: The best 2-4 word search terms
- **Backup queries**: Alternative searches if first fails
- **Avoid list**: What NOT to include

**Example Analysis:**
```
Text: "When you realize the meeting could have been an email"

AI Output:
{
  "image_type": "meme",
  "mood": "exasperated",
  "search_query": "facepalm meeting meme",
  "backup_queries": [
    "could have been an email meme",
    "wasted time meeting reaction"
  ],
  "avoid": ["happy office workers", "productive meeting"]
}
```

### 2. Web Scraping
Searches multiple sources:
- **Bing Images** (primary - easier to scrape)
- **Google Images** (secondary - more results)
- **Imgur** (for memes and reactions)

### 3. Image Validation
- Downloads images to local cache
- Validates image format and size
- Filters out tiny/broken images
- Returns first valid, relevant image

## Usage in Streamlit App

### Enable Smart Curator:
1. In sidebar → **Slide Settings** → Check "Include Memes"
2. Select **"AI Original"** mode
3. You'll see: *"✨ AI will find perfect images from the web"*

### What Happens:
When you generate a carousel, the Smart Curator:
- Analyzes each slide (skips hook and CTA)
- Searches the web for relevant visuals
- Downloads and caches images
- Integrates them into your slides

## Features

### Intelligent Search
- **Context-aware**: Understands the emotion and situation in your text
- **Professional judgment**: Picks images like a content creator would
- **Diverse sources**: Not limited to meme databases

### Web Scraping (No APIs)
- Uses `requests` and `BeautifulSoup4`
- Respects rate limits (0.5-1s delays)
- Random user agents to avoid blocking
- No paid API keys required

### Caching
- Downloaded images are cached locally
- Reuses images when possible
- Auto-cleanup keeps cache manageable

## Technical Details

### Dependencies
```python
pip install beautifulsoup4 requests pillow
```

### Files
- `app/smart_image_curator.py` - Main curator class
- `output/image_cache/` - Cached downloaded images

### Key Methods

**SmartImageCurator**
- `analyze_content_for_visuals(text, topic)` - AI analysis
- `scrape_bing_images(query, limit)` - Bing scraping
- `scrape_google_images(query, limit)` - Google scraping
- `scrape_imgur_search(query, limit)` - Imgur scraping
- `download_image(url)` - Download and validate
- `find_image_for_content(text, topic)` - Main entry point
- `find_images_for_slides(slides, topic)` - Batch processing

### Data Structures

**ImageResult**
```python
@dataclass
class ImageResult:
    url: str              # Original image URL
    local_path: str       # Cached file path
    source: str           # google, bing, imgur
    relevance_score: float # How relevant (0-1)
    description: str      # Search query used
    image_type: str       # meme, photo, scene, abstract
```

## Examples

### Single Image Search
```python
from app.smart_image_curator import SmartImageCurator

curator = SmartImageCurator()

result = curator.find_image_for_content(
    text="Me trying to explain code to non-technical people",
    topic="tech"
)

if result:
    print(f"Found: {result.description}")
    print(f"Saved to: {result.local_path}")
```

### Carousel Batch Search
```python
slides = [
    "Hook slide",
    "First point about productivity",
    "Second point about time management",
    "Final takeaway",
    "CTA - follow for more"
]

results = curator.find_images_for_slides(slides, topic="work")
# Returns: {2: ImageResult, 3: ImageResult}
# (skips slide 1 and 5)
```

## Advantages Over Template Matching

### Old System (Template Matching)
- ❌ Limited to pre-defined meme templates
- ❌ Same memes used repeatedly
- ❌ Can't adapt to new content types
- ❌ Requires local meme library

### New System (Smart Curator)
- ✅ Finds ANY relevant image from the web
- ✅ Always fresh, never repetitive
- ✅ Adapts to any content topic
- ✅ No local storage needed

## Best Practices

### 1. Clear Slide Text
Better results with specific, clear text:
- ❌ "This is about productivity"
- ✅ "When you check your phone 50 times during a 1-hour meeting"

### 2. Topic Hints
Provide topic hints for better context:
```python
curator.find_images_for_slides(slides, topic="finance")
```

### 3. Rate Limiting
Built-in delays prevent API blocking:
- 0.5s between image downloads
- 1s between slide searches

### 4. Cache Management
Periodically clean cache:
```python
curator.cleanup_cache(keep_recent=100)
```

## Troubleshooting

### No Images Found
**Possible causes:**
1. Network issues (firewall, VPN)
2. Search engines blocking requests
3. Overly specific search queries

**Solutions:**
- Check internet connection
- Try with VPN disabled
- Simplify slide text

### Images Too Generic
**Cause:** AI choosing broad search terms

**Solution:** Make slide text more specific and emotional

### Slow Performance
**Cause:** Web scraping takes time

**Expected:** 3-5 seconds per slide
**Solution:** Use "Template Match" mode for faster generation

## Legal & Ethical Notes

⚠️ **Important Disclaimers:**

1. **Web Scraping Legality**
   - Scraping public search engine results is generally permitted
   - Respect robots.txt and rate limits
   - For educational/personal use

2. **Image Copyright**
   - Downloaded images may have copyright
   - Use only for personal/educational projects
   - For commercial use, verify image licenses
   - Consider using this as proof-of-concept only

3. **Responsible Usage**
   - Don't overwhelm servers (rate limiting is built-in)
   - Cache images to minimize requests
   - Consider alternatives for production (paid APIs, royalty-free sources)

## Future Enhancements

Potential improvements:
- [ ] Add more image sources (Reddit, Pinterest)
- [ ] AI-based image quality scoring
- [ ] Support for video/GIF search
- [ ] Custom image filters (color, orientation)
- [ ] Local AI vision model for relevance validation

## Summary

The Smart Image Curator brings **professional content creator intelligence** to your carousel generation:

🧠 **AI-Powered** - Understands context and emotion
🌐 **Web-Connected** - Finds fresh, relevant visuals
🎯 **Contextual** - Not limited to meme templates
⚡ **No APIs** - Pure web scraping, no costs

Perfect for creating engaging, unique carousels that stand out!
