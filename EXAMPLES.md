# Usage Examples

Real-world examples of using Meme Content Studio.

---

## Example 1: Personal Career Story (Bahasa - Casual)

### Input

```bash
python -m app.main create \
  -c "3 tahun lalu gua almost quit my first job karena bosen. Tapi mentor gua bilang: jangan quit dulu, coba create your own opportunities dari dalam. Game changer banget. Sekarang gua lead 3 projects dan career path gua totally different." \
  -t santai_gaul \
  -l bahasa \
  -a story_personal \
  -o career_story
```

### What You Get

**Slide 1 (Hook):**
```
3 tahun lalu gua almost quit my first job.

Best decision I never made.
```

**Slide 2:**
```
Fresh graduate. First job. Excited banget.

Bulan pertama? Amazing.
Bulan ketiga? Mulai bosen.
Bulan keenam? Literally counting days to resign.
```

**Slide 3:**
```
Gua ngerasa stuck. Gak belajar apa-apa.

Cuma ngerjain task yang gitu-gitu aja.

Udah draft resignation letter segala.
```

... (and more)

**Caption:**
```
Real talk: Bosen di kerjaan itu normal.

Tapi resign bukan selalu solusinya.

Swipe buat tau apa yang gua lakuin instead →

Siapa disini yang pernah ngerasa stuck di kerjaan? Drop di comment 👇

#karierindonesia #tipskerjacerdas #youngprofessional
```

---

## Example 2: Hot Take on Productivity (English)

### Input

```bash
python -m app.main create \
  -c "Unpopular opinion: waking up at 5am is overrated. Not everyone is a morning person. I'm most productive 9pm-1am. Stop forcing yourself into someone else's routine." \
  -t casual_friendly \
  -l english \
  -a hot_take \
  -v 2 \
  -o productivity_hot_take
```

### What You Get

**Version 1 - Slide 1:**
```
Unpopular opinion:

The 5am club is overrated.
```

**Version 1 - Slide 2:**
```
I know. Everyone says it.

"Wake up at 5am!"
"Win the morning, win the day!"

Sounds great. Also? Not for everyone.
```

**Version 1 - Slide 3:**
```
Here's what they don't tell you:

Your brain has a natural peak performance window.

For some, it's 6am.
For others, it's 9pm.

Forcing yourself against your biology? Recipe for burnout.
```

... (continues)

**Caption Version 1:**
```
Tried the 5am routine for 90 days.

Result? Exhausted and less productive than before.

Here's what actually works (swipe) →

When's YOUR peak productivity window? Morning or night? Let me know 👇

#productivitytips #morningroutine #worksmart
```

**Caption Version 2:** (Alternative approach)
```
Plot twist: Being productive isn't about waking up early.

It's about knowing when YOUR brain works best.

Full breakdown in the slides →

Drop 🔥 if you're team night owl

#productivitymyths #worklifebalance #realproductivity
```

---

## Example 3: Tips Listicle (Professional Bahasa)

### Input

```bash
python -m app.main create \
  -c "5 hal yang saya pelajari dari managing remote team selama 2 tahun: clear communication beats long meetings, async work is powerful, trust your team, over-document everything, celebrate small wins" \
  -t profesional \
  -l bahasa \
  -a tips_listicle \
  -o remote_leadership
```

### What You Get

**Slide 1:**
```
5 lessons dari 2 tahun memimpin remote team.

Learned these the hard way.
```

**Slide 2:**
```
1. Clear Communication > Long Meetings

Rapat 2 jam jarang menyelesaikan masalah.

Brief tertulis yang jelas? Much more effective.

How: 15-minute sync maksimal. Sisanya async written updates.
```

**Slide 3:**
```
2. Embrace Asynchronous Work

Tidak semua harus real-time.

Why? Respects different time zones and working styles.

How: Use Notion/Slack threads. Give 24-hour response windows.
```

... (continues with tips 3-5)

**Caption:**
```
2 tahun managing remote team taught me these 5 critical lessons.

Tidak ada yang fancy. Semua bisa Anda terapkan mulai besok.

Swipe untuk detail setiap lesson →

Mana yang paling resonate dengan pengalaman Anda? Comment dengan angkanya.

#remotework #leadership #teammanagement #workfromhome
```

---

## Example 4: Quick Text-Only Carousel

### Input

```bash
python -m app.main create \
  -c "Signs you're ready for a career pivot: 1) You dread Mondays not because of work but because of the type of work, 2) You keep learning about a different field on weekends, 3) Your passion projects are in a different domain, 4) You feel stuck, not challenged" \
  -t casual_friendly \
  -l english \
  -a tips_listicle \
  --skip-humanizer \
  -o career_pivot_signs
```

*Note: `--skip-humanizer` makes it faster when you're confident in the output*

### What You Get

Clean text slides with no memes, ready in under 60 seconds.

---

## Example 5: Mixed Language (Code-Switching)

### Input

```bash
python -m app.main create \
  -c "Real talk: mindset itu overrated. Everyone bilang 'ubah mindset lu' tapi gak ada yang explain HOW. Action beats thinking. Start small, build momentum, mindset follows." \
  -t indo_english_mix \
  -l mixed \
  -a hot_take \
  -o mindset_hot_take
```

### What You Get

Natural code-switching between Bahasa and English:

**Slide Example:**
```
Unpopular opinion: mindset advice is overrated.

"Change your mindset dulu baru bisa succeed."

Okay, cool. Tapi HOW?

Most people stuck di endless thinking mode.
Meanwhile, the ones winning? They're doing.
```

---

## Example 6: Checking Human Score

### Input

```bash
python -m app.main check "In today's fast-paced world, it's important to note that productivity is essential. Let's dive into 5 tips that will help you become more efficient."
```

### Output

```
HUMAN SCORE: 35/100 ✗ NEEDS WORK

Score Breakdown:
  ✗ sentence_variety: -5
  ✗ ai_phrases: -30
  ✗ personal_voice: -10
  ✗ conversational: 0
  ✗ natural_flow: 0

Detected Issues:
  • AI phrase detected: In today's fast-paced world
  • AI phrase detected: it's important to note that
  • AI phrase detected: Let's dive into
  • No personal pronouns - feels impersonal
  • Sentence lengths too uniform
```

---

## Example 7: Listing Available Resources

### Check Available Tones

```bash
python -m app.main list-tones
```

**Output:**
```
Available Tones

BAHASA:
  • santai_gaul
  • profesional

ENGLISH:
  • casual_friendly

MIXED:
  • indo_english_mix
```

### Check Available Angles

```bash
python -m app.main list-angles
```

**Output:**
```
Available Content Angles

  • story_personal
  • hot_take
  • tips_listicle
```

### Check Meme Library

```bash
python -m app.main list-memes
```

**Output:**
```
Meme Library (8 memes)

┌─────────────────────────────┬────────┬──────────────────────┬────────┐
│ Filename                    │ Exists │ Emotions             │ Energy │
├─────────────────────────────┼────────┼──────────────────────┼────────┤
│ example_success.jpg         │   ✓    │ celebration, winning │ high   │
│ example_thinking.jpg        │   ✓    │ thinking, curious    │ medium │
│ example_realization.jpg     │   ✓    │ realization, aha     │ medium │
└─────────────────────────────┴────────┴──────────────────────┴────────┘
```

---

## Example 8: Multiple Versions for A/B Testing

### Input

```bash
python -m app.main create \
  -c "Why most people fail at networking: they focus on quantity over quality. Better to have 5 real connections than 500 strangers." \
  -t casual_friendly \
  -l english \
  -a hot_take \
  -v 3 \
  -o networking_versions
```

### What You Get

3 different versions of the same content:
- Version 1: Bold/direct approach
- Version 2: Story-led approach
- Version 3: Data/evidence-led approach

Pick the one that fits your brand or test all three!

---

## Example 9: Custom Output Name

### Input

```bash
python -m app.main create \
  -c "Your idea" \
  -t santai_gaul \
  -l bahasa \
  -a story_personal \
  -o "2024-01-15_career_advice"
```

### Output Location

```
output/2024-01-15_career_advice/
├── slide_01.png
├── slide_02.png
├── slide_03.png
└── project_summary.json
```

Organized by date and topic!

---

## Example 10: Full Workflow with Memes

### Step 1: Add meme to library

```bash
# Copy your meme
cp ~/Downloads/office_cringe.gif meme_library/images/
```

### Step 2: Update metadata

Edit `meme_library/metadata.json`:

```json
{
  "office_cringe.gif": {
    "emotions": ["cringe", "awkward", "embarrassed"],
    "context": ["mistake", "fail", "relatable"],
    "energy": "medium",
    "source": "The Office",
    "best_for": ["relatable content", "mistakes", "funny moments"],
    "language_fit": ["indo", "english"],
    "caption_vibe": "when you realize you messed up"
  }
}
```

### Step 3: Create content

```bash
python -m app.main create \
  -c "That moment when you reply all to a company-wide email by accident. We've all been there. Here's what I learned about email etiquette the hard way." \
  -t casual_friendly \
  -l english \
  -a story_personal \
  -o email_fail_story
```

### Step 4: AI automatically matches your meme

The system will:
1. Analyze the "cringe/embarrassment" emotion in your content
2. Find `office_cringe.gif` in your library
3. Recommend it for the slide about the awkward moment
4. Generate the slide with meme + text

---

## Pro Tips

### Tip 1: Iterate on Tone

Try same content with different tones:

```bash
# Casual version
python -m app.main create -c "idea" -t santai_gaul -o v1_casual

# Professional version
python -m app.main create -c "idea" -t profesional -o v2_professional
```

Pick the one that feels more "you".

### Tip 2: Start Generic, Then Customize

1. Generate basic version
2. Look at output in `output/[name]/project_summary.json`
3. Edit slides manually
4. Use edited version as template for future content

### Tip 3: Build Content Library

Create a folder of successful carousels:

```
my_content_library/
├── hooks_that_worked.txt
├── best_meme_matches.txt
└── high_performing_angles.txt
```

Reference these when creating new content.

### Tip 4: Batch Creation

Create a script:

```bash
#!/bin/bash

IDEAS=(
  "Idea 1 here"
  "Idea 2 here"
  "Idea 3 here"
)

for i in "${!IDEAS[@]}"; do
  python -m app.main create \
    -c "${IDEAS[$i]}" \
    -t santai_gaul \
    -l bahasa \
    -o "carousel_$i"
done
```

Generate multiple carousels at once!

---

## Common Patterns

### Pattern 1: Quick Daily Content

```bash
python -m app.main create \
  -c "[Today's insight]" \
  -t [your default tone] \
  -l [your language] \
  -a story_personal \
  --skip-humanizer
```

### Pattern 2: Important Campaign Content

```bash
python -m app.main create \
  -c "[Campaign message]" \
  -t [appropriate tone] \
  -l [language] \
  -a [best angle] \
  -v 3
```

Test multiple versions for important content.

### Pattern 3: Repurposing Content

Already have content? Check its human score:

```bash
python -m app.main check "Your existing content here"
```

If score is low, rewrite with the tool.

---

## Output Structure

Every carousel creates:

```
output/[your-project-name]/
├── slide_01.png              # Ready to upload
├── slide_02.png
├── slide_03.png
├── ...
└── project_summary.json      # Full project data
```

**project_summary.json** contains:
- Your input
- Generated slides (text)
- Captions (all versions)
- Settings used
- Image paths

You can edit this JSON and regenerate if needed!

---

**Experiment. Iterate. Find your voice.**

The tool gets better the more you use it and customize it.
