"""
Streamlit Web UI for Meme Content Studio v2.0

A web interface for creating Instagram carousels with DeepSeek AI.
Features:
- Professional HTML/CSS templates rendered with Playwright
- 7 beautiful themes (dark, light, gradients, neon)
- AI-powered keyword highlighting
- Meme integration
- Ready-to-post PNG output
"""

import streamlit as st
import os
import io
import zipfile
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Meme Content Studio v2.0",
    page_icon="🎨",
    layout="wide"
)

# Ensure directories exist without API validation
from app.config import Config
Config.ensure_directories_only()

# Note: Memes are now fetched dynamically from the internet on-demand
# No local meme library is needed - see app/dynamic_meme_engine.py

# Check if Playwright is available
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass

# Import slide generator (has its own theme list)
from app.slide_generator import SlideGenerator


def check_api_key():
    """Check if DeepSeek API key is configured"""
    return bool(os.getenv("DEEPSEEK_API_KEY"))


def check_pexels_api_key():
    """Check if Pexels API key is configured"""
    return bool(os.getenv("PEXELS_API_KEY"))


def get_available_tones():
    """Get list of available tones by language"""
    tones = {"bahasa": [], "english": [], "mixed": []}

    for lang in tones.keys():
        lang_dir = Config.TONES_DIR / lang
        if lang_dir.exists():
            tones[lang] = [f.stem for f in lang_dir.glob("*.txt")]

    return tones


def get_available_angles():
    """Get list of available content angles"""
    if Config.ANGLES_DIR.exists():
        return [f.stem for f in Config.ANGLES_DIR.glob("*.txt")]
    return []


def create_zip_download(images, captions):
    """Create a ZIP file containing all slide images and captions."""
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add images
        for i, img in enumerate(images):
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            zip_file.writestr(f"slide_{i+1:02d}.png", img_buffer.getvalue())

        # Add captions text file
        captions_text = ""
        for idx, cap_data in enumerate(captions):
            strategy = cap_data.get("strategy", f"Version {idx+1}")
            caption = cap_data.get("caption", "")
            hashtags = " ".join(cap_data.get("hashtags", []))
            captions_text += f"=== {strategy} ===\n\n{caption}\n\n{hashtags}\n\n---\n\n"

        zip_file.writestr("captions.txt", captions_text)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def get_theme_info():
    """Get theme display information for the new template system."""
    return {
        "dark_mode": {
            "label": "Dark Mode",
            "description": "Classic dark with yellow accents",
            "colors": {"bg": "#121212", "text": "#FFFFFF", "accent": "#FFD93D"}
        },
        "minimal_light": {
            "label": "Minimal Light",
            "description": "Clean white with black highlights",
            "colors": {"bg": "#FFFFFF", "text": "#1A1A1A", "accent": "#1A1A1A"}
        },
        "ocean_gradient": {
            "label": "Ocean Gradient",
            "description": "Blue-purple gradient with white highlights",
            "colors": {"bg": "#1a2980", "text": "#FFFFFF", "accent": "#FFFFFF"}
        },
        "sunset_gradient": {
            "label": "Sunset Gradient",
            "description": "Warm pink-red gradient",
            "colors": {"bg": "#ee9ca7", "text": "#FFFFFF", "accent": "#FFFFFF"}
        },
        "neon_nights": {
            "label": "Neon Nights",
            "description": "Black with neon green glow",
            "colors": {"bg": "#0a0a0a", "text": "#FFFFFF", "accent": "#39FF14"}
        },
        "warm_cream": {
            "label": "Warm Cream",
            "description": "Soft beige aesthetic",
            "colors": {"bg": "#FDF6E3", "text": "#2D2D2D", "accent": "#D4A574"}
        },
        "dark_gradient": {
            "label": "Dark Gradient",
            "description": "Deep blue-purple with cyan accents",
            "colors": {"bg": "#0f0c29", "text": "#FFFFFF", "accent": "#00D9FF"}
        },
    }


def render_theme_preview(theme_name: str):
    """Render a small preview of the theme."""
    themes = get_theme_info()
    theme = themes.get(theme_name, themes["dark_mode"])
    colors = theme["colors"]

    bg_color = colors["bg"]
    text_color = colors["text"]
    accent_color = colors["accent"]

    # Check if it's a gradient theme
    is_gradient = "gradient" in theme_name

    if is_gradient:
        if theme_name == "ocean_gradient":
            bg_style = "background: linear-gradient(135deg, #1a2980, #26d0ce);"
        elif theme_name == "sunset_gradient":
            bg_style = "background: linear-gradient(135deg, #ee9ca7, #ffdde1);"
        elif theme_name == "dark_gradient":
            bg_style = "background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);"
        else:
            bg_style = f"background-color: {bg_color};"
    else:
        bg_style = f"background-color: {bg_color};"

    html = f"""
    <div style="{bg_style} padding: 15px; border-radius: 8px; text-align: center; margin: 5px 0;">
        <span style="color: {text_color}; font-weight: bold;">Aa</span>
        <span style="background-color: {accent_color}; color: {bg_color}; padding: 2px 6px; border-radius: 3px; margin-left: 8px;">Key</span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def main():
    # Header
    st.title("🎨 Meme Content Studio v2.0")
    st.markdown("Create **ready-to-post** Instagram carousels with AI-powered HTML templates")

    # Show Playwright status
    if not PLAYWRIGHT_AVAILABLE:
        st.warning("""
        **Playwright not installed!** The new rendering system requires Playwright.

        Install with:
        ```bash
        pip install playwright
        playwright install chromium
        ```
        """)

    # Check API key
    if not check_api_key():
        st.error("DeepSeek API key not found!")
        st.markdown("""
        Please set your API key:
        1. Create a `.env` file in the project root
        2. Add: `DEEPSEEK_API_KEY=your_key_here`
        3. Get your key from: https://platform.deepseek.com/
        """)

        api_key = st.text_input("Or enter your DeepSeek API key here:", type="password")
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            st.success("API key set for this session!")
            st.rerun()
        return

    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")

        # Quick Preset Selection
        st.subheader("Quick Presets")
        preset = st.selectbox(
            "Style Preset",
            ["Custom", "The Economic Influence", "Casual Story", "Professional"],
            index=0,
            help="Quick presets for different content styles"
        )

        # Apply preset settings
        if preset == "The Economic Influence":
            language = "bahasa"
            tone = "ekonomi_edgy"
            angle = "ekonomi_explainer"
            default_theme = "dark"
            st.success("Economics style loaded!")
            st.caption("Dark, edgy, meme-integrated economics content")
        elif preset == "Casual Story":
            language = "bahasa"
            tone = "santai_gaul"
            angle = "story_personal"
            default_theme = "gradient_sunset"
        elif preset == "Professional":
            language = "bahasa"
            tone = "profesional"
            angle = "story_personal"
            default_theme = "minimal"
        else:
            # Custom settings
            st.divider()

            # Language selection
            language = st.selectbox(
                "Language",
                ["bahasa", "english", "mixed"],
                index=0,
                help="Choose the output language"
            )

            # Get tones for selected language
            all_tones = get_available_tones()
            available_tones = all_tones.get(language, [])

            if available_tones:
                default_idx = 0
                if "santai_gaul" in available_tones:
                    default_idx = available_tones.index("santai_gaul")
                tone = st.selectbox(
                    "Tone",
                    available_tones,
                    index=default_idx,
                    help="Choose the writing tone"
                )
            else:
                tone = "santai_gaul"
                st.warning(f"No tones found for {language}")

            # Angle selection
            available_angles = get_available_angles()
            if available_angles:
                default_idx = 0
                if "story_personal" in available_angles:
                    default_idx = available_angles.index("story_personal")
                angle = st.selectbox(
                    "Content Angle",
                    available_angles,
                    index=default_idx,
                    help="Choose the content structure"
                )
            else:
                angle = "story_personal"
                st.warning("No angles found")

            default_theme = "dark"

        st.divider()

        # Theme Selection with Previews
        st.subheader("🎨 Visual Theme")

        theme_info = get_theme_info()
        theme_names = list(theme_info.keys())

        # Map old theme names to new ones
        theme_name_map = {
            "dark": "dark_mode",
            "minimal": "minimal_light",
            "gradient_blue": "ocean_gradient",
            "gradient_sunset": "sunset_gradient",
        }
        default_theme = theme_name_map.get(default_theme, default_theme)

        # Find default theme index
        default_theme_idx = 0
        if default_theme in theme_names:
            default_theme_idx = theme_names.index(default_theme)

        theme = st.selectbox(
            "Theme",
            theme_names,
            index=default_theme_idx,
            format_func=lambda x: theme_info.get(x, {}).get("label", x),
            help="Choose the visual style for your slides"
        )

        # Show theme preview
        render_theme_preview(theme)

        # Theme description
        theme_desc = theme_info.get(theme, {}).get("description", "")
        st.caption(theme_desc)

        st.divider()

        # Generation Options
        st.subheader("Generation Options")

        # Number of versions
        versions = st.slider("Content Versions", 1, 3, 1, help="Number of content variations to generate")

        # AI Highlighting
        use_highlighting = st.checkbox(
            "AI Keyword Highlighting",
            value=True,
            help="Automatically highlight important words"
        )

        # Contextual Images
        use_images = st.checkbox(
            "Contextual Images",
            value=check_pexels_api_key(),
            disabled=not check_pexels_api_key(),
            help="Add contextual stock photos (requires Pexels API key)"
        )

        if not check_pexels_api_key():
            st.caption("Add PEXELS_API_KEY to .env for stock photos")

        # Skip humanizer
        skip_humanizer = st.checkbox("Skip humanization check", value=False)

        # Output name
        output_name = st.text_input("Output folder name", value="carousel")

        st.divider()

        # Meme Library Management
        st.subheader("🎭 Meme Library")

        from app.meme_scraper import MemeScraper
        scraper = MemeScraper()
        status = scraper.get_all_memes_status()
        total_memes = len(status)
        available_memes = sum(1 for info in status.values() if info['exists'])

        st.caption(f"{available_memes}/{total_memes} memes available")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Memes", help="Download missing or outdated memes"):
                with st.spinner("Updating meme library..."):
                    results = scraper.auto_update_library(max_age_days=30)
                    updated = sum(1 for s in results.values() if s == "updated")
                    failed = sum(1 for s in results.values() if s == "failed")

                    if updated > 0:
                        st.success(f"Updated {updated} memes!")
                    if failed > 0:
                        st.warning(f"Failed to update {failed} memes")
                    st.rerun()

        with col2:
            if st.button("📊 View Status", help="Show detailed meme library status"):
                st.session_state.show_meme_status = not st.session_state.get('show_meme_status', False)

        if st.session_state.get('show_meme_status', False):
            st.caption("Meme Library Status:")
            for meme_name, info in status.items():
                status_icon = "✅" if info['exists'] else "❌"
                st.caption(f"{status_icon} {meme_name}")

        st.divider()

        # Slide Display Options
        st.subheader("Slide Display")

        # Logo option
        show_logo = st.checkbox(
            "Show Logo",
            value=False,
            help="Add your logo to slides"
        )

        logo_path = None
        if show_logo:
            # Check for default logo
            default_logo = Path("assets/logo.png")
            if default_logo.exists():
                st.caption(f"Using: assets/logo.png")
                logo_path = str(default_logo)
            else:
                st.caption("Add logo.png to assets/ folder")
                show_logo = False

        # Slide indicators
        show_slide_indicator = st.checkbox(
            "Slide Indicator Dots",
            value=False,
            help="Show position dots (● ○ ○)"
        )

        # Meme integration toggle
        use_memes = st.checkbox(
            "Include Memes",
            value=True,
            help="Auto-add memes to slides based on content. Uncheck for text-only slides."
        )

        if not use_memes:
            st.info("ℹ️ Text-only mode enabled - No memes will be added to slides")
        else:
            # Dynamic meme info
            st.caption("🌐 Memes fetched dynamically from internet based on content analysis")

        st.divider()
        st.caption("Powered by DeepSeek AI")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Your Content Idea")

        # Dynamic placeholder based on preset
        if preset == "The Economic Influence":
            placeholder_text = "Example: Kenapa gaji kita stuck tapi harga rumah naik terus? Ini breakdown-nya yang jarang orang tau..."
        else:
            placeholder_text = "Example: I used to wake up at 5am thinking it made me productive. It just made me tired. Here's what actually worked for me..."

        # Content input
        content = st.text_area(
            "Enter your rough idea for the carousel:",
            height=200,
            placeholder=placeholder_text,
            help="Be specific! Include personal details for best results."
        )

        # Tips - dynamic based on preset
        with st.expander("💡 Tips for better results"):
            if preset == "The Economic Influence":
                st.markdown("""
                **Economics Content Tips:**

                **Hook Ideas:**
                - Data yang shocking: "10 orang Indonesia = 50 juta rakyat termiskin"
                - Relatable pain: "Gaji naik 5%, inflasi 6%. Congrats, lu makin miskin."
                - Controversial take: "Subsidi BBM itu regresif. Here's why."

                **Content Pillars:**
                - Macro economics (inflasi, GDP, resesi)
                - Personal finance reality (gaji vs biaya hidup)
                - Wealth inequality (oligarki, wealth gap)
                - Government policy criticism

                **Style:**
                - Mix Bahasa + English naturally
                - Include data/statistics
                - Be sarcastic but substantive
                - Always reveal the "system"
                """)
            else:
                st.markdown("""
                **Be specific in your input:**
                - Bad: "content about productivity"
                - Good: "I used to wake up at 5am thinking it made me productive. It just made me tired."

                **Match tone to audience:**
                - Casual audience → `santai_gaul`
                - Professional audience → `profesional`
                - International audience → `casual_friendly`

                **Choose the right angle:**
                - Personal story → `story_personal`
                - Controversial opinion → `hot_take`
                - Educational value → `tips_listicle`
                """)

        # Generate button
        generate_button = st.button(
            "🚀 Generate Carousel",
            type="primary",
            disabled=not content.strip()
        )

    with col2:
        st.header("🖼️ Output Preview")

        if generate_button and content.strip():
            try:
                # Import modules
                from app.rewriter import ContentRewriter
                from app.humanizer import Humanizer
                from app.caption_generator import CaptionGenerator
                from app.meme_search_agent import MemeSearchAgent
                from app.slide_generator import SlideGenerator

                # Step 1: Rewrite content
                with st.status("Creating your carousel...", expanded=True) as status:
                    st.write("✍️ Rewriting content with professional copywriter brain...")

                    rewriter = ContentRewriter()
                    content_versions = rewriter.rewrite_content(
                        rough_idea=content,
                        tone=tone,
                        language=language,
                        angle=angle,
                        versions=versions
                    )

                    st.write(f"✅ Generated {len(content_versions)} version(s)")

                    # Get slides from first version
                    selected_version = content_versions[0]
                    slides = selected_version['slides']

                    # Step 2: Humanization check
                    if not skip_humanizer:
                        st.write("🔍 Running humanization check...")
                        humanizer = Humanizer()

                        needs_improvement = []
                        for i, slide in enumerate(slides):
                            score = humanizer.calculate_human_score(slide)
                            if not score["passes_threshold"]:
                                needs_improvement.append((i, slide, score))

                        if needs_improvement:
                            st.write(f"⚠️ {len(needs_improvement)} slide(s) need humanization")
                            st.write("🔧 Humanizing content...")

                            humanized_results = humanizer.batch_humanize_slides(slides)
                            slides = [result["humanized"] for result in humanized_results]

                            st.write("✅ Humanization complete")
                        else:
                            st.write("✅ All slides sound human!")

                    # Step 3: Prepare meme settings (dynamic fetching happens during generation)
                    meme_results = None
                    if use_memes:
                        st.write("🎭 Memes enabled - will fetch fresh memes dynamically...")
                        # Just pass a flag dict to trigger dynamic fetching
                        meme_results = {"use_dynamic": True}
                    else:
                        st.write("⏭️ Memes disabled - creating text-only slides")

                    # Step 4: Get contextual images (if enabled)
                    image_assignments = None
                    if use_images and check_pexels_api_key():
                        st.write("🖼️ Finding contextual images...")
                        try:
                            from app.image_search import ContentImageMatcher
                            matcher = ContentImageMatcher()
                            image_assignments = matcher.get_images_for_slides(slides, meme_results)
                            images_found = sum(1 for a in image_assignments if a.get('has_image'))
                            st.write(f"✅ Found {images_found} contextual images")
                        except Exception as e:
                            st.write(f"⚠️ Image search skipped: {e}")

                    # Step 5: Extract highlights (if enabled)
                    highlight_data = None
                    if use_highlighting:
                        st.write("✨ Identifying key words to highlight...")
                        try:
                            highlight_data = rewriter.get_slides_with_highlights(slides)
                            total_highlights = sum(len(h.get('highlights', [])) for h in highlight_data)
                            st.write(f"✅ Found {total_highlights} keywords to highlight")
                        except Exception as e:
                            st.write(f"⚠️ Highlighting skipped: {e}")

                    # Step 6: Generate caption
                    st.write("💬 Generating Instagram caption...")
                    caption_gen = CaptionGenerator()
                    captions = caption_gen.generate_caption(
                        slides=slides,
                        tone=tone,
                        language=language,
                        versions=2
                    )

                    st.write(f"✅ Generated {len(captions)} caption variation(s)")

                    # Step 7: Generate slide images (with dynamic meme fetching)
                    st.write(f"🎨 Generating slide images ({theme} theme)...")
                    if use_memes:
                        st.write("🌐 Fetching fresh memes from internet...")
                    slide_gen = SlideGenerator(theme=theme)

                    # Determine topic hint from preset/tone
                    topic_hint = None
                    if tone in ["ekonomi_edgy", "profesional"]:
                        topic_hint = "finance"
                    elif preset == "The Economic Influence":
                        topic_hint = "finance"

                    images, saved_paths = slide_gen.generate_carousel(
                        slides=slides,
                        meme_recommendations=meme_results,
                        image_assignments=image_assignments,
                        highlight_data=highlight_data,
                        project_name=output_name,
                        show_logo=show_logo,
                        logo_path=logo_path,
                        show_slide_indicator=show_slide_indicator,
                        use_dynamic_memes=use_memes,
                        topic_hint=topic_hint
                    )
                    st.write(f"✅ Created {len(images)} slide images")

                    status.update(label="✅ Carousel created!", state="complete", expanded=False)

                # Store results in session state
                st.session_state['meme_results'] = meme_results
                st.session_state['generated_images'] = images
                st.session_state['saved_paths'] = saved_paths
                st.session_state['captions'] = captions
                st.session_state['slides'] = slides
                st.session_state['selected_version'] = selected_version
                st.session_state['slide_gen'] = slide_gen

                # Display results
                st.success("🎉 Your carousel is ready!")

                # Engagement Optimization Display
                if selected_version.get('engagement_optimization'):
                    eng_opt = selected_version['engagement_optimization']
                    st.subheader("📈 Viral Optimization")

                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        target = eng_opt.get('primary_target', 'N/A')
                        st.metric("Target", target)
                    with col_b:
                        hook = eng_opt.get('hook_type', 'N/A')
                        st.metric("Hook Type", hook)
                    with col_c:
                        triggers = eng_opt.get('triggers', [])
                        st.metric("Triggers", len(triggers))

                    if triggers:
                        st.caption(f"**Psychological Triggers:** {', '.join(triggers)}")
                    if eng_opt.get('performance_reason'):
                        st.info(f"**Why it will perform:** {eng_opt['performance_reason']}")

                # Slide Images Preview
                st.subheader("📱 Slide Images")

                # Download All button
                zip_data = create_zip_download(images, captions)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                st.download_button(
                    label="📥 Download All (ZIP)",
                    data=zip_data,
                    file_name=f"{output_name}_{timestamp}.zip",
                    mime="application/zip"
                )

                # Image tabs
                slide_tabs = st.tabs([f"Slide {i+1}" for i in range(len(images))])

                for i, (tab, img) in enumerate(zip(slide_tabs, images)):
                    with tab:
                        # Display image
                        st.image(img)

                        # Individual download button
                        img_bytes = slide_gen.get_image_bytes(img)
                        st.download_button(
                            label=f"📥 Download Slide {i+1}",
                            data=img_bytes,
                            file_name=f"slide_{i+1:02d}.png",
                            mime="image/png",
                            key=f"download_slide_{i}"
                        )

                        # Show slide text and meme info
                        col_text, col_meme = st.columns([2, 1])
                        with col_text:
                            with st.expander("📝 Slide Text"):
                                st.text(slides[i])
                        with col_meme:
                            # Show meme assignment if any
                            if meme_results and meme_results.get('available_memes'):
                                for meme in meme_results['available_memes']:
                                    if meme.get('slide_num') == i + 1:
                                        st.success(f"🎭 {meme.get('filename', 'meme')}")
                                        break

                # Captions
                st.subheader("💬 Caption Options")
                for idx, cap_data in enumerate(captions):
                    strategy = cap_data.get("strategy", f"Version {idx+1}")
                    caption = cap_data.get("caption", "")
                    hashtags = " ".join(cap_data.get("hashtags", []))

                    with st.expander(f"Caption: {strategy}", expanded=(idx == 0)):
                        st.text_area(
                            "Caption",
                            value=caption,
                            height=150,
                            key=f"caption_{idx}"
                        )
                        if hashtags:
                            st.text_input("Hashtags", value=hashtags, key=f"hashtags_{idx}")

                        # Copy button
                        full_caption = f"{caption}\n\n{hashtags}" if hashtags else caption
                        st.code(full_caption, language=None)

                # Hook alternatives
                if selected_version.get('hook_alternatives'):
                    st.subheader("🎣 Hook Alternatives")
                    for i, alt in enumerate(selected_version['hook_alternatives'][:3]):
                        st.markdown(f"**Option {i+1}:** {alt}")

                # Meme Recommendations Section
                if 'meme_results' in st.session_state and st.session_state['meme_results']:
                    meme_results = st.session_state['meme_results']

                    st.subheader("🎭 Meme Recommendations")

                    # Available memes
                    if meme_results.get('available_memes'):
                        st.markdown("**✅ Available in your library:**")
                        for meme in meme_results['available_memes']:
                            st.success(f"Slide {meme['slide_num']}: `{meme['filename']}` - {meme['reason']}")

                    # Missing memes
                    if meme_results.get('missing_memes'):
                        st.markdown("**📥 Need to download:**")
                        for meme in meme_results['missing_memes']:
                            with st.expander(f"Slide {meme['slide_num']}: {meme['meme_name']}", expanded=False):
                                st.markdown(f"**Save as:** `{meme['suggested_filename']}`")
                                st.markdown(f"**Why:** {meme['reason']}")
                                st.markdown(f"**Search:** {', '.join(meme.get('search_keywords', []))}")

                                # Show suggested metadata
                                if meme.get('suggested_metadata'):
                                    meta = meme['suggested_metadata']
                                    st.markdown(f"**Emotions:** {', '.join(meta.get('emotions', []))}")
                                    st.markdown(f"**Best for:** {', '.join(meta.get('best_for', []))}")

                                st.markdown("---")
                                st.markdown("**Quick download links:**")
                                search_query = meme['meme_name'].replace(' ', '+') + '+meme+template'
                                st.markdown(f"- [Google Images](https://www.google.com/search?tbm=isch&q={search_query})")
                                st.markdown(f"- [Know Your Meme](https://knowyourmeme.com/search?q={search_query})")
                                st.markdown(f"- [Imgflip](https://imgflip.com/memesearch?q={meme['meme_name'].replace(' ', '%20')})")

                    # Show analysis details
                    with st.expander("📊 Full Meme Analysis", expanded=False):
                        for analysis in meme_results.get('analysis', []):
                            slide_num = analysis.get('slide_num', '?')
                            emotion = analysis.get('emotional_beat', 'N/A')
                            needs_meme = analysis.get('needs_meme', False)
                            suggestion = analysis.get('meme_suggestion', 'None')

                            if needs_meme:
                                st.markdown(f"**Slide {slide_num}:** {emotion} → `{suggestion}`")
                            else:
                                st.markdown(f"**Slide {slide_num}:** {emotion} → *Text only recommended*")

                # Store in session state
                st.session_state['last_result'] = {
                    'slides': slides,
                    'captions': captions,
                    'version': selected_version,
                    'images': images
                }

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.exception(e)

        elif 'last_result' in st.session_state:
            # Show previous result
            result = st.session_state['last_result']
            st.info("Showing previous result. Enter new content and click Generate to create a new carousel.")

            # Show previous images if available
            if 'images' in result and result['images']:
                images = result['images']
                slide_tabs = st.tabs([f"Slide {i+1}" for i in range(len(images))])

                for i, (tab, img) in enumerate(zip(slide_tabs, images)):
                    with tab:
                        st.image(img)
            else:
                # Fallback to text-only display
                slides = result['slides']
                slide_tabs = st.tabs([f"Slide {i+1}" for i in range(len(slides))])

                for i, (tab, slide) in enumerate(zip(slide_tabs, slides)):
                    with tab:
                        st.markdown(f"**{'Hook' if i == 0 else f'Slide {i+1}'}**")
                        st.info(slide)
        else:
            st.info("Enter your content idea and click **Generate Carousel** to get started!")

            # Show system status
            if PLAYWRIGHT_AVAILABLE:
                st.success("Playwright rendering ready")
            else:
                st.error("Playwright not installed - rendering unavailable")

            # Show theme previews
            st.subheader("🎨 Available Themes")
            theme_cols = st.columns(3)
            theme_info = get_theme_info()

            for i, (theme_key, theme_data) in enumerate(list(theme_info.items())[:6]):
                with theme_cols[i % 3]:
                    st.caption(theme_data["label"])
                    render_theme_preview(theme_key)


if __name__ == "__main__":
    main()
