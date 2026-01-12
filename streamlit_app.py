"""
Content Studio - Professional SaaS UI
Create viral Instagram carousels powered by AI

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

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="Content Studio",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Import UI components
from app.ui_components import (
    inject_custom_css,
    render_header,
    render_status_badge,
    render_empty_state,
    render_metric_card
)

# Inject custom CSS
inject_custom_css()

# Ensure directories exist without API validation
from app.config import Config
Config.ensure_directories_only()

# Check if Playwright is available
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass

# Import slide generator
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
        for i, img in enumerate(images):
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            zip_file.writestr(f"slide_{i+1:02d}.png", img_buffer.getvalue())

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
            "description": "Classic dark with yellow accents - Perfect for finance content",
            "colors": {"bg": "#121212", "text": "#FFFFFF", "accent": "#FFD93D"}
        },
        "minimal_light": {
            "label": "Minimal Light",
            "description": "Clean white with black highlights - Professional & clean",
            "colors": {"bg": "#FFFFFF", "text": "#1A1A1A", "accent": "#1A1A1A"}
        },
        "ocean_gradient": {
            "label": "Ocean Gradient",
            "description": "Blue-purple gradient - Modern & trendy",
            "colors": {"bg": "#1a2980", "text": "#FFFFFF", "accent": "#FFFFFF"}
        },
        "sunset_gradient": {
            "label": "Sunset Gradient",
            "description": "Warm pink-red gradient - Energetic & warm",
            "colors": {"bg": "#ee9ca7", "text": "#FFFFFF", "accent": "#FFFFFF"}
        },
        "neon_nights": {
            "label": "Neon Nights",
            "description": "Black with neon green glow - Bold & attention-grabbing",
            "colors": {"bg": "#0a0a0a", "text": "#FFFFFF", "accent": "#39FF14"}
        },
        "warm_cream": {
            "label": "Warm Cream",
            "description": "Soft beige aesthetic - Lifestyle & wellness",
            "colors": {"bg": "#FDF6E3", "text": "#2D2D2D", "accent": "#D4A574"}
        },
        "dark_gradient": {
            "label": "Dark Gradient",
            "description": "Deep blue-purple with cyan - Tech & professional",
            "colors": {"bg": "#0f0c29", "text": "#FFFFFF", "accent": "#00D9FF"}
        },
    }


def render_sidebar():
    """Render the professional sidebar."""
    with st.sidebar:
        # Logo/Brand
        st.markdown("""
        <div style="padding: 1.5rem 0; border-bottom: 1px solid var(--border-subtle); margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: var(--pure-black); border-radius: 4px; display: flex; align-items: center; justify-content: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="18" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/></svg>
                </div>
                <div>
                    <div style="font-weight: 700; font-size: 1rem; color: var(--text-primary); letter-spacing: -0.02em;">Content Studio</div>
                    <div style="font-size: 0.6875rem; color: var(--text-tertiary); font-family: var(--font-mono);">v2.0</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Presets
        st.markdown('<h3 style="color: #71717A; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin: 1.5rem 0 0.75rem 0;">Style Preset</h3>', unsafe_allow_html=True)

        preset_options = {
            "custom": {"name": "Custom", "desc": "Configure your own settings", "icon": "⚙️"},
            "economic": {"name": "Economic Influence", "desc": "Dark, edgy economics content", "icon": "📊"},
            "casual": {"name": "Casual Story", "desc": "Warm, personal storytelling", "icon": "✨"},
            "professional": {"name": "Professional", "desc": "Clean, business content", "icon": "💼"}
        }

        # Initialize session state for preset
        if 'selected_preset' not in st.session_state:
            st.session_state.selected_preset = 'custom'

        # Render preset buttons in 2x2 grid
        cols = st.columns(2)
        preset_keys = list(preset_options.keys())

        for idx, key in enumerate(preset_keys):
            with cols[idx % 2]:
                option = preset_options[key]
                is_selected = st.session_state.selected_preset == key

                # Use Streamlit button with custom styling
                button_label = f"{option['icon']} {option['name']}"

                if st.button(
                    button_label,
                    key=f"preset_{key}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_preset = key
                    st.rerun()

                # Show description below button
                st.caption(option['desc'])

        preset = st.session_state.selected_preset

        # Apply preset settings
        if preset == "economic":
            language = "bahasa"
            tone = "ekonomi_edgy"
            angle = "ekonomi_explainer"
            default_theme = "dark_mode"
        elif preset == "casual":
            language = "bahasa"
            tone = "santai_gaul"
            angle = "story_personal"
            default_theme = "sunset_gradient"
        elif preset == "professional":
            language = "bahasa"
            tone = "profesional"
            angle = "story_personal"
            default_theme = "minimal_light"
        else:
            default_theme = "dark_mode"
            language = None
            tone = None
            angle = None

        # Custom settings expander
        if preset == "custom":
            with st.expander("Language & Tone", expanded=True):
                language = st.selectbox(
                    "Language",
                    ["bahasa", "english", "mixed"],
                    index=0
                )

                # Tone selection with manual input option
                st.markdown("**Tone**")
                tone_mode = st.radio(
                    "Tone Input Mode",
                    ["Select from presets", "Write custom tone"],
                    index=0,
                    label_visibility="collapsed",
                    horizontal=True,
                    key="tone_mode"
                )

                if tone_mode == "Select from presets":
                    all_tones = get_available_tones()
                    available_tones = all_tones.get(language, [])
                    if available_tones:
                        default_idx = available_tones.index("santai_gaul") if "santai_gaul" in available_tones else 0
                        tone = st.selectbox(
                            "Select Tone",
                            available_tones,
                            index=default_idx,
                            label_visibility="collapsed"
                        )
                    else:
                        tone = "santai_gaul"
                        st.caption("⚠️ No preset tones found")
                else:
                    tone = st.text_input(
                        "Custom Tone",
                        value="professional, friendly, informative",
                        placeholder="e.g., casual, witty, educational",
                        help="Describe the tone/voice you want (e.g., 'sarcastic but helpful', 'warm and empathetic')",
                        label_visibility="collapsed"
                    )

                st.markdown("---")

                # Content Angle selection with manual input option
                st.markdown("**Content Angle**")
                angle_mode = st.radio(
                    "Angle Input Mode",
                    ["Select from presets", "Write custom angle"],
                    index=0,
                    label_visibility="collapsed",
                    horizontal=True,
                    key="angle_mode"
                )

                if angle_mode == "Select from presets":
                    available_angles = get_available_angles()
                    if available_angles:
                        default_idx = available_angles.index("story_personal") if "story_personal" in available_angles else 0
                        angle = st.selectbox(
                            "Select Angle",
                            available_angles,
                            index=default_idx,
                            label_visibility="collapsed"
                        )
                    else:
                        angle = "story_personal"
                        st.caption("⚠️ No preset angles found")
                else:
                    angle = st.text_area(
                        "Custom Content Angle",
                        value="Tell a personal story with lessons learned",
                        placeholder="e.g., 'Start with a mistake, then show the solution', 'Controversial take with data backing'",
                        help="Describe the content structure/approach you want",
                        height=80,
                        label_visibility="collapsed"
                    )

        st.markdown('<hr style="border: none; border-top: 1px solid #E2E8F0; margin: 1.5rem 0;">', unsafe_allow_html=True)

        # Theme Selection
        st.markdown('<h3 style="color: #71717A; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin: 1.5rem 0 0.75rem 0;">Visual Theme</h3>', unsafe_allow_html=True)

        theme_info = get_theme_info()
        theme_names = list(theme_info.keys())

        default_theme_idx = theme_names.index(default_theme) if default_theme in theme_names else 0

        theme = st.selectbox(
            "Choose Theme",
            theme_names,
            index=default_theme_idx,
            format_func=lambda x: theme_info[x]["label"],
            label_visibility="collapsed"
        )

        # Theme preview - improved with clear spacing
        colors = theme_info[theme]["colors"]
        is_gradient = "gradient" in theme

        if is_gradient:
            gradient_map = {
                "ocean_gradient": "linear-gradient(135deg, #1a2980, #26d0ce)",
                "sunset_gradient": "linear-gradient(135deg, #ee9ca7, #ffdde1)",
                "dark_gradient": "linear-gradient(135deg, #0f0c29, #302b63)"
            }
            bg_style = gradient_map.get(theme, f"background-color: {colors['bg']}")
        else:
            bg_style = f"background-color: {colors['bg']}"

        # Smart text color based on background
        if theme in ['dark_mode', 'neon_nights', 'dark_gradient', 'ocean_gradient']:
            preview_text_color = '#FFFFFF'
            preview_bg = colors['bg']
        else:
            preview_text_color = '#18181B'
            preview_bg = colors['bg']

        st.markdown(f"""
        <div style="{bg_style}; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.75rem 0 0.5rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.1);">
            <div style="color: {preview_text_color}; font-weight: 700; font-size: 1.5rem; margin-bottom: 0.75rem; letter-spacing: -0.02em;">Aa Bb Cc</div>
            <div style="background: {colors['accent']}; color: {preview_bg}; padding: 6px 14px; border-radius: 6px; display: inline-block; font-size: 0.8125rem; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">Highlight Text</div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(theme_info[theme]["description"])

        st.markdown('<hr style="border: none; border-top: 1px solid #E2E8F0; margin: 1.5rem 0;">', unsafe_allow_html=True)

        # Generation Options
        st.markdown('<h3 style="color: #64748B; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 1.5rem 0 0.75rem 0;">Generation</h3>', unsafe_allow_html=True)

        with st.expander("Output Options", expanded=False):
            versions = st.slider("Content Versions", 1, 3, 1)

            use_highlighting = st.checkbox(
                "AI Keyword Highlighting",
                value=True,
                help="Automatically highlight important words"
            )

            skip_humanizer = st.checkbox("Skip humanization", value=False)
            output_name = st.text_input("Output folder", value="carousel")

        st.markdown('<hr style="border: none; border-top: 1px solid #E2E8F0; margin: 1.5rem 0;">', unsafe_allow_html=True)

        # Display Options
        st.markdown('<h3 style="color: #64748B; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin: 1.5rem 0 0.75rem 0;">Display</h3>', unsafe_allow_html=True)

        with st.expander("Slide Settings", expanded=False):
            show_logo = st.checkbox("Show Logo", value=False)
            logo_path = None
            if show_logo:
                default_logo = Path("assets/logo.png")
                if default_logo.exists():
                    st.caption("Using: assets/logo.png")
                    logo_path = str(default_logo)
                else:
                    st.caption("Add logo.png to assets/")
                    show_logo = False

            show_slide_indicator = st.checkbox("Slide Indicators", value=False)

            # AI-Powered Visual Selection (simplified)
            use_memes = st.checkbox(
                "🤖 AI Visual Selection",
                value=True,  # DEFAULT: AI automatically chooses best images
                help="AI intelligently chooses the best cartoon/movie/meme for each slide"
            )

            if use_memes:
                st.success("🎯 AI Mode: Automatically selects cartoons, movies, or memes based on content")
                st.caption("✨ AI analyzes each slide and picks the perfect visual (Spongebob, anime, movie scenes, memes, etc.)")

                # Always use AI with blend mode (intelligent mix)
                use_ai_memes = True
                content_type_override = "blend"  # AI freely chooses from all types
                meme_style = "dark_minimal"
                meme_language = "en"

            else:
                use_ai_memes = False
                content_type_override = None
                meme_style = "dark_minimal"
                meme_language = "en"
                st.info("✨ Text-only mode - Clean, professional look!")

        st.markdown('<hr style="border: none; border-top: 1px solid #E2E8F0; margin: 1.5rem 0;">', unsafe_allow_html=True)

        # System Status
        st.markdown('<h3 style="color: #71717A; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin: 1.5rem 0 0.75rem 0;">System Status</h3>', unsafe_allow_html=True)

        # Renderer status
        if PLAYWRIGHT_AVAILABLE:
            st.markdown(render_status_badge("success", "Renderer"), unsafe_allow_html=True)
        else:
            st.markdown(render_status_badge("error", "Renderer"), unsafe_allow_html=True)

        st.markdown('<div style="height: 0.5rem;"></div>', unsafe_allow_html=True)

        # API Key status
        if check_api_key():
            st.markdown(render_status_badge("success", "API Key"), unsafe_allow_html=True)
        else:
            st.markdown(render_status_badge("error", "API Key"), unsafe_allow_html=True)

        # Draft History Section
        st.markdown('<hr style="border: none; border-top: 1px solid #E2E8F0; margin: 1.5rem 0;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #71717A; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin: 1.5rem 0 0.75rem 0;">Draft History</h3>', unsafe_allow_html=True)

        # Initialize draft history in session state
        if 'draft_history' not in st.session_state:
            st.session_state.draft_history = []

        # Show save current draft button
        if st.session_state.get('content_draft', '').strip():
            if st.button("💾 Save Current Draft", use_container_width=True, help="Save draft to history"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                preview = st.session_state.content_draft[:50] + "..." if len(st.session_state.content_draft) > 50 else st.session_state.content_draft
                st.session_state.draft_history.insert(0, {
                    'content': st.session_state.content_draft,
                    'timestamp': timestamp,
                    'preview': preview
                })
                # Keep only last 5 drafts
                st.session_state.draft_history = st.session_state.draft_history[:5]
                st.success("Draft saved!")
                st.rerun()

        # Display saved drafts
        if st.session_state.draft_history:
            for idx, draft in enumerate(st.session_state.draft_history):
                with st.expander(f"📝 {draft['timestamp']}", expanded=False):
                    st.caption(draft['preview'])
                    col_load, col_del = st.columns([3, 1])
                    with col_load:
                        if st.button("Load", key=f"load_draft_{idx}", use_container_width=True):
                            st.session_state.content_draft = draft['content']
                            st.success("Draft loaded!")
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_draft_{idx}", help="Delete this draft"):
                            st.session_state.draft_history.pop(idx)
                            st.rerun()
        else:
            st.caption("No saved drafts yet")

        # Footer
        st.markdown("""
        <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #E2E8F0; text-align: center;">
            <div style="font-size: 0.75rem; color: #94A3B8;">Powered by DeepSeek AI</div>
        </div>
        """, unsafe_allow_html=True)

    return {
        "preset": preset,
        "language": language,
        "tone": tone,
        "angle": angle,
        "theme": theme,
        "versions": versions if preset == "custom" else 1,
        "use_highlighting": use_highlighting if preset == "custom" else True,
        "skip_humanizer": skip_humanizer if preset == "custom" else False,
        "output_name": output_name if preset == "custom" else "carousel",
        "show_logo": show_logo if preset == "custom" else False,
        "logo_path": logo_path if preset == "custom" else None,
        "show_slide_indicator": show_slide_indicator if preset == "custom" else False,
        "use_memes": use_memes,  # Always respect user's checkbox regardless of preset
        "use_ai_memes": use_ai_memes if use_memes else False,
        "content_type_override": content_type_override if use_memes else None,
        "meme_style": meme_style if use_memes else "dark_minimal",
        "meme_language": meme_language if use_memes else "en",
    }


def main():
    # Check API key first
    if not check_api_key():
        render_header()
        st.error("DeepSeek API key not found!")

        st.markdown("""
        <div class="card" style="max-width: 500px; margin: 2rem auto;">
            <h3 style="margin-bottom: 1rem;">Setup Required</h3>
            <p style="color: var(--text-secondary); margin-bottom: 1rem;">To use Content Studio, you need a DeepSeek API key.</p>
            <ol style="color: var(--text-secondary); padding-left: 1.5rem;">
                <li>Create a <code>.env</code> file in the project root</li>
                <li>Add: <code>DEEPSEEK_API_KEY=your_key_here</code></li>
                <li>Get your key from <a href="https://platform.deepseek.com/" target="_blank">platform.deepseek.com</a></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        api_key = st.text_input("Or enter your API key here:", type="password")
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            st.success("API key set for this session!")
            st.rerun()
        return

    # Render sidebar and get settings
    settings = render_sidebar()

    # Main content area
    render_header()

    # Show Playwright warning if needed
    if not PLAYWRIGHT_AVAILABLE:
        st.warning("""
        **Playwright not installed!** Install with:
        ```bash
        pip install playwright && playwright install chromium
        ```
        """)

    # Two-column layout
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        # Input Card
        st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <span style="font-size: 1.125rem; font-weight: 600; color: #1E293B;">Content Input</span>
        </div>
        """, unsafe_allow_html=True)

        # Auto-save: Initialize draft from session state
        if 'content_draft' not in st.session_state:
            st.session_state.content_draft = ""

        # Dynamic placeholder
        if settings["preset"] == "economic":
            placeholder = "Example: Kenapa gaji kita stuck tapi harga rumah naik terus? Ini breakdown-nya yang jarang orang tau..."
        else:
            placeholder = "Example: I used to wake up at 5am thinking it made me productive. It just made me tired. Here's what actually worked..."

        content = st.text_area(
            "Your content idea",
            value=st.session_state.content_draft,
            height=180,
            placeholder=placeholder,
            help="Be specific! Include personal details for best results. ✨ Auto-saved!",
            label_visibility="collapsed",
            key="content_input"
        )

        # Auto-save: Update session state when content changes
        if content != st.session_state.content_draft:
            st.session_state.content_draft = content

        # Auto-save indicator & Clear button
        if content.strip():
            col_save, col_clear = st.columns([3, 1])
            with col_save:
                st.markdown("""
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                        <circle cx="6" cy="6" r="5" fill="#10B981"/>
                        <path d="M3.5 6L5.5 8L8.5 4" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span style="font-size: 0.75rem; color: #10B981; font-weight: 500;">Draft auto-saved</span>
                </div>
                """, unsafe_allow_html=True)
            with col_clear:
                if st.button("🗑️ Clear", key="clear_draft", help="Clear your draft"):
                    st.session_state.content_draft = ""
                    st.rerun()

        # Tips Section
        with st.expander("Tips for better results"):
            if settings["preset"] == "economic":
                st.markdown("""
                **Hook Ideas:**
                - Shocking data: "10 orang Indonesia = 50 juta rakyat termiskin"
                - Relatable pain: "Gaji naik 5%, inflasi 6%. Congrats, lu makin miskin."

                **Style:**
                - Mix Bahasa + English naturally
                - Include data/statistics
                - Be sarcastic but substantive
                """)
            else:
                st.markdown("""
                **Be specific:**
                - Bad: "content about productivity"
                - Good: "I used to wake up at 5am thinking it made me productive..."

                **Match your audience:**
                - Casual → `santai_gaul`
                - Professional → `profesional`
                """)

        # Generate Button
        generate_button = st.button(
            "Generate Carousel",
            type="primary",
            disabled=not content.strip(),
            use_container_width=True
        )

        # Current settings display
        # Determine picture status text
        if settings['use_memes']:
            if settings['use_ai_memes']:
                picture_status = "AI Search"
            else:
                picture_status = "Stock/Templates"
        else:
            picture_status = "Text Only"

        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
            <div style="font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Current Settings</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-bottom: 0.25rem;">Theme</div>
                    <div style="font-size: 0.875rem; color: #1E293B; font-weight: 500;">{settings['theme'].replace('_', ' ').title()}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-bottom: 0.25rem;">Language</div>
                    <div style="font-size: 0.875rem; color: #1E293B; font-weight: 500;">{settings['language'] or 'Auto'}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-bottom: 0.25rem;">Pictures</div>
                    <div style="font-size: 0.875rem; color: #1E293B; font-weight: 500;">{picture_status}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Output Preview
        st.markdown("""
        <div style="margin-bottom: 0.5rem;">
            <span style="font-size: 1.125rem; font-weight: 600; color: #1E293B;">Output Preview</span>
        </div>
        """, unsafe_allow_html=True)

        if generate_button and content.strip():
            try:
                # Import modules
                from app.rewriter import ContentRewriter
                from app.humanizer import Humanizer
                from app.caption_generator import CaptionGenerator
                from app.slide_generator import SlideGenerator

                # Progress container
                progress_container = st.container()

                with progress_container:
                    with st.status("Creating your carousel...", expanded=True) as status:
                        # Step 1: Rewrite
                        st.write("Writing content with AI copywriter...")
                        rewriter = ContentRewriter()
                        content_versions = rewriter.rewrite_content(
                            rough_idea=content,
                            tone=settings["tone"] or "santai_gaul",
                            language=settings["language"] or "bahasa",
                            angle=settings["angle"] or "story_personal",
                            versions=settings["versions"]
                        )
                        st.write(f"✓ Generated {len(content_versions)} version(s)")

                        selected_version = content_versions[0]
                        slides = selected_version['slides']

                        # Step 2: Humanization
                        if not settings["skip_humanizer"]:
                            st.write("Checking authenticity...")
                            humanizer = Humanizer()
                            needs_improvement = []
                            for i, slide in enumerate(slides):
                                score = humanizer.calculate_human_score(slide)
                                if not score["passes_threshold"]:
                                    needs_improvement.append((i, slide, score))

                            if needs_improvement:
                                st.write(f"Humanizing {len(needs_improvement)} slide(s)...")
                                humanized_results = humanizer.batch_humanize_slides(slides)
                                slides = [result["humanized"] for result in humanized_results]
                            st.write("✓ Content sounds human")

                        # Step 3: Meme settings
                        meme_results = None
                        if settings["use_memes"]:
                            if settings["use_ai_memes"]:
                                st.write("Smart Image Curator - AI searching the web for perfect visuals...")
                            else:
                                st.write("Preparing meme template matching...")
                            meme_results = {"use_dynamic": True}
                        else:
                            st.write("Text-only mode")

                        # Step 4: Images (removed - using AI meme agent instead)
                        image_assignments = None

                        # Step 5: Highlights
                        highlight_data = None
                        if settings["use_highlighting"]:
                            st.write("Identifying keywords...")
                            try:
                                highlight_data = rewriter.get_slides_with_highlights(slides)
                                total_highlights = sum(len(h.get('highlights', [])) for h in highlight_data)
                                st.write(f"✓ Found {total_highlights} keywords")
                            except Exception as e:
                                st.write(f"Warning: Highlights skipped: {e}")

                        # Step 6: Caption
                        st.write("Generating captions...")
                        caption_gen = CaptionGenerator()
                        captions = caption_gen.generate_caption(
                            slides=slides,
                            tone=settings["tone"] or "santai_gaul",
                            language=settings["language"] or "bahasa",
                            versions=2
                        )
                        st.write(f"✓ Generated {len(captions)} caption(s)")

                        # Step 7: Render slides
                        st.write(f"Rendering slides ({settings['theme']})...")
                        slide_gen = SlideGenerator(theme=settings["theme"])

                        topic_hint = None
                        if settings["tone"] in ["ekonomi_edgy", "profesional"] or settings["preset"] == "economic":
                            topic_hint = "finance"

                        images, saved_paths = slide_gen.generate_carousel(
                            slides=slides,
                            meme_recommendations=meme_results,
                            image_assignments=image_assignments,
                            highlight_data=highlight_data,
                            project_name=settings["output_name"],
                            show_logo=settings["show_logo"],
                            logo_path=settings["logo_path"],
                            show_slide_indicator=settings["show_slide_indicator"],
                            use_dynamic_memes=settings["use_memes"] and not settings["use_ai_memes"],
                            topic_hint=topic_hint,
                            use_ai_meme_agent=settings["use_memes"] and settings["use_ai_memes"],
                            content_type_override=settings["content_type_override"],
                            meme_style=settings["meme_style"],
                            meme_language=settings["meme_language"]
                        )
                        st.write(f"✓ Created {len(images)} slides")

                        status.update(label="✓ Carousel ready!", state="complete", expanded=False)

                # Store results
                st.session_state['generated_images'] = images
                st.session_state['saved_paths'] = saved_paths
                st.session_state['captions'] = captions
                st.session_state['slides'] = slides
                st.session_state['selected_version'] = selected_version
                st.session_state['slide_gen'] = slide_gen
                st.session_state['meme_results'] = meme_results

                # Success message
                st.success("Your carousel is ready!")

                # Download button
                zip_data = create_zip_download(images, captions)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                st.download_button(
                    label="Download All (ZIP)",
                    data=zip_data,
                    file_name=f"{settings['output_name']}_{timestamp}.zip",
                    mime="application/zip",
                    use_container_width=True
                )

                # Engagement metrics
                if selected_version.get('engagement_optimization'):
                    eng_opt = selected_version['engagement_optimization']
                    st.markdown("#### Viral Optimization")

                    metric_cols = st.columns(3)
                    with metric_cols[0]:
                        st.metric("Target", eng_opt.get('primary_target', 'N/A'))
                    with metric_cols[1]:
                        st.metric("Hook", eng_opt.get('hook_type', 'N/A'))
                    with metric_cols[2]:
                        st.metric("Triggers", len(eng_opt.get('triggers', [])))

                # Slide tabs
                st.markdown("#### Slides")
                slide_tabs = st.tabs([f"#{i+1}" for i in range(len(images))])

                for i, (tab, img) in enumerate(zip(slide_tabs, images)):
                    with tab:
                        st.image(img, use_container_width=True)

                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            with st.expander("View text"):
                                st.text(slides[i])
                        with col_b:
                            img_bytes = slide_gen.get_image_bytes(img)
                            st.download_button(
                                label="Download",
                                data=img_bytes,
                                file_name=f"slide_{i+1:02d}.png",
                                mime="image/png",
                                key=f"dl_{i}"
                            )

                # Captions
                st.markdown("#### Captions")
                for idx, cap_data in enumerate(captions):
                    strategy = cap_data.get("strategy", f"Version {idx+1}")
                    caption = cap_data.get("caption", "")
                    hashtags = cap_data.get("hashtags", [])

                    with st.expander(f"{strategy}", expanded=(idx == 0)):
                        st.text_area(
                            "Caption",
                            value=caption,
                            height=120,
                            key=f"cap_{idx}",
                            label_visibility="collapsed"
                        )
                        if hashtags:
                            st.caption(" ".join(hashtags))

                # Store result
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
            st.info("Previous result shown. Enter new content to regenerate.")

            if 'images' in result and result['images']:
                images = result['images']
                slide_tabs = st.tabs([f"#{i+1}" for i in range(len(images))])
                for i, (tab, img) in enumerate(zip(slide_tabs, images)):
                    with tab:
                        st.image(img, use_container_width=True)
        else:
            # Empty state
            render_empty_state()

            # Theme previews
            st.markdown("#### Available Themes")
            theme_info = get_theme_info()
            theme_cols = st.columns(4)

            for i, (theme_key, theme_data) in enumerate(list(theme_info.items())[:4]):
                with theme_cols[i]:
                    colors = theme_data["colors"]
                    is_gradient = "gradient" in theme_key

                    if is_gradient:
                        gradient_map = {
                            "ocean_gradient": "linear-gradient(135deg, #1a2980, #26d0ce)",
                            "sunset_gradient": "linear-gradient(135deg, #ee9ca7, #ffdde1)",
                            "dark_gradient": "linear-gradient(135deg, #0f0c29, #302b63)"
                        }
                        bg_style = gradient_map.get(theme_key, f"background-color: {colors['bg']}")
                    else:
                        bg_style = f"background-color: {colors['bg']}"

                    st.markdown(f"""
                    <div style="{bg_style}; padding: 1.5rem; border-radius: 8px; text-align: center; margin-bottom: 0.5rem;">
                        <span style="color: {colors['text']}; font-weight: 600;">Aa</span>
                    </div>
                    <div style="font-size: 0.75rem; text-align: center; color: #64748B;">{theme_data['label']}</div>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
