# Meme Scraper - Auto-Download Fresh Memes

## Overview

The meme scraper automatically downloads and maintains a fresh library of meme templates from the internet, ensuring your content always has the latest and most popular meme formats.

## Features

### Automatic Downloads
- **On Startup**: Memes are automatically checked and downloaded when the app starts
- **Smart Updates**: Only downloads missing memes or those older than 30 days
- **Fallback URLs**: Multiple source URLs per meme for reliability
- **Metadata Tracking**: Tracks download dates, source URLs, and file sizes

### Supported Memes (14 templates)
1. Drake Format - Comparison/preference memes
2. Shocked Pikachu - Surprise/obvious outcomes
3. Galaxy Brain / Expanding Brain - Escalating ideas
4. Clown Makeup - Progressive mistakes
5. Distracted Boyfriend - Choosing wrong options
6. This Is Fine - Accepting chaos
7. Crying Cat - Emotional moments
8. Two Buttons - Difficult choices
9. Is This a Pigeon? - Misidentification
10. Woman Yelling at Cat - Conflicting perspectives
11. Success Kid - Small victories
12. UNO Reverse - Plot twists
13. Brain Meme - Intelligence levels
14. Stonks - Finance/investment humor

## Usage

### Automatic Mode (Default)
The scraper runs automatically when you start the Streamlit app:
```bash
python -m streamlit run streamlit_app.py
```

On startup, it will:
- Check for missing memes
- Update memes older than 30 days
- Log results to console

### Manual Refresh via UI
In the Streamlit sidebar:
1. Look for the "🎭 Meme Library" section
2. See the current status (e.g., "13/14 memes available")
3. Click "🔄 Refresh Memes" to manually update
4. Click "📊 View Status" to see detailed list

### Programmatic Usage
```python
from app.meme_scraper import MemeScraper, auto_download_memes_on_startup

# Quick startup function
results = auto_download_memes_on_startup(max_age_days=30)

# Or use the class directly
scraper = MemeScraper()

# Download all templates
scraper.download_all_templates(force_refresh=False)

# Update only old memes
scraper.auto_update_library(max_age_days=30)

# Check what's missing
missing = scraper.check_missing_memes()

# Get detailed status
status = scraper.get_all_memes_status()
```

### Standalone Testing
```bash
cd "d:\code\Instagram feeds generator"
python app/meme_scraper.py
```

## File Locations

### Downloaded Memes
- **Path**: `static/memes/`
- **Format**: JPG images
- **Naming**: Descriptive names (e.g., `drake_format.jpg`)

### Metadata
- **Path**: `static/memes/.meme_metadata.json`
- **Contents**: Download timestamps, source URLs, file sizes
- **Purpose**: Track when memes were last updated

## Configuration

### Update Frequency
By default, memes are updated if they're older than 30 days. Adjust this:

```python
# In streamlit_app.py (line 38)
auto_download_memes_on_startup(max_age_days=30)  # Change 30 to desired days
```

### Adding New Memes
To add new meme templates:

1. Edit `app/meme_scraper.py`
2. Add entry to `MEME_TEMPLATE_URLS` dictionary:
```python
MEME_TEMPLATE_URLS = {
    "new_meme.jpg": [
        "https://i.imgflip.com/xxxxx.jpg",  # Primary URL
        "https://backup-url.com/xxxxx.jpg"   # Fallback URL
    ],
    # ... existing memes
}
```

3. Save the file
4. Restart the app or click "Refresh Memes"

### Finding Meme URLs
Good sources for meme template URLs:
- **Imgflip**: `https://i.imgflip.com/[ID].jpg`
- **Know Your Meme**: Check the image gallery
- **Direct image links**: Must be direct JPG/PNG URLs

## Troubleshooting

### Meme Failed to Download
**Symptom**: "failed" status in download results
**Causes**:
- URL returned 404 (image moved/deleted)
- Network connectivity issues
- Server blocking requests

**Solution**:
1. Check the logs for specific error
2. Find new URL for the meme template
3. Update `MEME_TEMPLATE_URLS` in `meme_scraper.py`

### All Downloads Failing
**Symptom**: All memes show "failed"
**Causes**:
- No internet connection
- Firewall blocking requests
- Imgflip API rate limiting

**Solution**:
1. Check internet connection
2. Wait a few minutes and retry
3. Use VPN if geo-blocked

### Missing Memes in UI
**Symptom**: Memes don't appear in carousel generation
**Cause**: Meme files not in correct directory

**Solution**:
1. Check `static/memes/` directory exists
2. Run scraper manually: `python app/meme_scraper.py`
3. Verify files downloaded successfully

## Technical Details

### Rate Limiting
- 0.5 second delay between downloads
- Polite to source servers
- Prevents IP blocking

### Fallback System
- Each meme has 2+ source URLs
- Tries URLs sequentially until success
- Logs which URL worked

### Metadata Tracking
JSON format:
```json
{
  "drake_format.jpg": {
    "downloaded_at": "2026-01-03T00:17:21.188276",
    "source_url": "https://i.imgflip.com/30b1gx.jpg",
    "size_bytes": 92771
  }
}
```

## Integration Points

### Streamlit App
- **Startup**: Line 36-40 in `streamlit_app.py`
- **UI Controls**: Line 368-402 in `streamlit_app.py`

### Meme Matcher
The scraper works seamlessly with:
- `app/meme_matcher.py` - Emotion-based meme selection
- `app/meme_search_agent.py` - Dynamic meme twist generation
- All carousel generation workflows

## Benefits

1. **Always Fresh**: Automatically updates old memes
2. **Reliable**: Fallback URLs ensure high success rate
3. **Low Maintenance**: Set it and forget it
4. **Trackable**: Metadata shows exactly when/where memes came from
5. **User Friendly**: Simple UI controls for manual management

## Example Workflow

```python
# App starts
auto_download_memes_on_startup(max_age_days=30)
# Output: "Meme library update complete: 2 updated, 0 failed, 12 up-to-date"

# User generates carousel
# Meme matcher selects "drake_format.jpg"
# File exists because scraper downloaded it
# Content generation proceeds smoothly

# 31 days later...
# App starts again
auto_download_memes_on_startup(max_age_days=30)
# Output: "Meme library update complete: 14 updated, 0 failed, 0 up-to-date"
# All memes refreshed with latest versions
```

## Future Enhancements

Potential improvements:
- [ ] Web scraping for trending memes from Reddit/Twitter
- [ ] ML-based meme quality scoring
- [ ] Automatic meme category detection
- [ ] Custom upload endpoint for user memes
- [ ] Cloud storage integration (S3, GCS)
- [ ] CDN caching for faster access

## Support

If you encounter issues:
1. Check logs in console output
2. Run `python app/meme_scraper.py` to test standalone
3. Verify `static/memes/` directory has write permissions
4. Check `.meme_metadata.json` for tracking data
