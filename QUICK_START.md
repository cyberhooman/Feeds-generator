# Quick Start Guide

Get your first Instagram carousel created in 5 minutes.

## Setup (One Time)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file in the project root:

```bash
copy .env.example .env
```

Edit `.env` and add your DeepSeek API key:

```
DEEPSEEK_API_KEY=sk-your-api-key-here
```

Get your API key from: https://platform.deepseek.com/

### 3. (Optional) Add Memes

Add your meme images to `meme_library/images/` and click "Sync Library" in the UI.

---

## Option 1: Web UI (Recommended)

```bash
python -m streamlit run streamlit_app.py
```

Open http://localhost:8501 and:

1. Select a preset (The Economic Influence, Casual Story, Professional)
2. Enter your content idea
3. Click "Generate Carousel"
4. Copy your slides & captions!

---

## Option 2: CLI

### Basic Usage

```bash
python -m app.main create \
  --content "Ide kasar tentang pentingnya networking untuk karir" \
  --tone santai_gaul \
  --lang bahasa \
  --angle story_personal
```

This will:
1. Rewrite your idea with viral hooks
2. Check for AI patterns and humanize
3. Match memes from your library
4. Generate Instagram captions

Output saved to: `output/carousel/`

### More Examples

**Economics Content:**
```bash
python -m app.main create \
  --content "Kenapa gaji stuck tapi harga rumah naik terus" \
  --tone ekonomi_edgy \
  --lang bahasa \
  --angle ekonomi_explainer
```

**English Hot Take:**
```bash
python -m app.main create \
  --content "Why most productivity advice is actually harmful" \
  --tone casual_friendly \
  --lang english \
  --angle hot_take
```

**Multiple Versions:**
```bash
python -m app.main create \
  --content "5 lessons from my first year as a founder" \
  --tone profesional \
  --lang bahasa \
  --angle tips_listicle \
  --versions 2
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `create` | Generate carousel content |
| `check "text"` | Analyze human score (0-100) |
| `list-tones` | Show available tones |
| `list-angles` | Show content angles |
| `list-memes` | Show meme library |

### Create Options

| Option | Description | Default |
|--------|-------------|---------|
| `--content, -c` | Your rough idea | Required |
| `--tone, -t` | Tone to use | santai_gaul |
| `--lang, -l` | Language | bahasa |
| `--angle, -a` | Content angle | story_personal |
| `--versions, -v` | Number of versions | 1 |
| `--output, -o` | Output folder name | carousel |
| `--skip-humanizer` | Skip humanization | False |

---

## Tips for Best Results

### 1. Be Specific

❌ "content about productivity"
✅ "I used to wake up at 5am thinking it made me productive. It just made me tired."

### 2. Match Tone to Audience

- Gen Z / Casual → `santai_gaul`
- Professional / LinkedIn → `profesional`
- Economics / Critical → `ekonomi_edgy`
- International → `casual_friendly`

### 3. Choose the Right Angle

- Personal story → `story_personal`
- Controversial opinion → `hot_take`
- Educational tips → `tips_listicle`
- Data/economics → `ekonomi_explainer`

---

## Troubleshooting

### "DEEPSEEK_API_KEY not found"
1. Make sure `.env` file exists
2. Check your API key is correct
3. No extra spaces in the key

### "Module not found"
```bash
pip install -r requirements.txt
```

### Content sounds too AI
- Use `santai_gaul` tone (most human)
- Don't use `--skip-humanizer`
- Add more personal details to your input

---

## Next Steps

- Check `README.md` for full documentation
- Add custom tones in `tones/custom/`
- Build your meme library for better matching
- Generate multiple versions and A/B test

---

**Your voice + AI efficiency = viral content**
