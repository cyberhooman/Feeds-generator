# Meme Library

This directory holds your meme/movie scene library for carousel creation.

## Structure

```
meme_library/
├── images/          # Your meme images/GIFs go here
└── metadata.json    # Metadata for meme matching
```

## How to Add Memes

### 1. Add Image Files

Save your meme images to `images/` folder:
- Supported formats: JPG, PNG, GIF
- Recommended size: At least 1080px wide
- Name files descriptively (e.g., `succession_kendall_walk.gif`)

### 2. Add Metadata

Edit `metadata.json` and add an entry for your meme:

```json
{
  "your_meme_filename.jpg": {
    "emotions": ["confident", "power", "unbothered"],
    "context": ["business", "success", "power_move"],
    "energy": "high",
    "source": "Movie/Show Name",
    "best_for": ["confidence content", "success stories"],
    "language_fit": ["indo", "english"],
    "caption_vibe": "describe the vibe this meme gives"
  }
}
```

### Metadata Fields Explained

**emotions** (array): Primary emotions this meme conveys
- Examples: confident, cringe, excited, frustrated, realization, smug, etc.

**context** (array): Situations/contexts where this meme fits
- Examples: success, failure, learning, decision, celebration, etc.

**energy** (string): Energy level
- `"high"`: Celebration, excitement, high energy moments
- `"medium"`: Thinking, processing, moderate emotions
- `"low"`: Reflective, calm, emotional depth

**source** (string): Where the meme is from (movie, show, etc.)

**best_for** (array): Types of content this meme works best with

**language_fit** (array): Which language content this works with
- `"indo"`: Bahasa Indonesia content
- `"english"`: English content
- Both for versatile memes

**caption_vibe** (string): One-line description of the meme's vibe/feeling

## Tips for Building Your Library

### 1. Quality Over Quantity
Start with 20-30 well-tagged memes rather than 100 poorly tagged ones.

### 2. Diverse Emotions
Cover the full emotional spectrum:
- High energy: celebration, excitement, confidence
- Medium: thinking, curious, processing
- Low: emotional, reflective, calm
- Relatable: cringe, awkward, frustrated

### 3. Popular Sources
Use memes from:
- Popular movies (Interstellar, Wolf of Wall Street, etc.)
- Well-known shows (The Office, Succession, etc.)
- Universal meme templates your audience recognizes

### 4. Test and Iterate
Track which memes get the best response and adjust your library accordingly.

### 5. Update Regularly
Add new trending memes, remove ones that feel dated.

## Example Meme Collection Starter

Good memes to start with:

**Success/Confidence:**
- Succession Kendall walk
- Wolf of Wall Street money throw
- Any "main character energy" scene

**Realization:**
- Interstellar crying scene
- Mind blown reactions
- Light bulb moments

**Relatable/Cringe:**
- The Office Michael Scott cringe
- Facepalm reactions
- "Why am I like this" energy

**Thinking/Curious:**
- Confused math lady
- Thinking/pondering faces
- Skeptical looks

**Emotional:**
- Touching movie moments
- Proud/moved reactions
- Deep reflection scenes

## Organizing Tips

You can organize images into subfolders and reference them with paths:

```json
{
  "movies/interstellar_crying.jpg": {
    ...
  },
  "shows/the_office_cringe.gif": {
    ...
  }
}
```

Just make sure the path in `metadata.json` matches the actual file location.

---

**Remember:** The better you tag your memes, the better the AI can match them to your content's emotional beats!
