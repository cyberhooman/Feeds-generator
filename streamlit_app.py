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


# Pexels removed - using AI-powered Smart Image Curator instead


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
    """Render the modern, easy-to-use sidebar."""
    with st.sidebar:
        # Modern Logo/Brand Header
        st.markdown("""
        <div class="sidebar-section" style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border: none; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #10B981 0%, #059669 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="18" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/></svg>
                </div>
                <div>
                    <div style="font-weight: 700; font-size: 1.125rem; color: #FFFFFF; letter-spacing: -0.02em;">Content Studio</div>
                    <div style="font-size: 0.6875rem; color: #10B981; font-weight: 500;">Pro Edition</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Start Presets - Card Section
        st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-header">
                <div class="sidebar-section-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <span class="sidebar-section-title">Quick Start</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        preset_options = {
            "custom": {"name": "Custom", "icon": "⚙️"},
            "economic": {"name": "Finance", "icon": "📊"},
            "casual": {"name": "Story", "icon": "✨"},
            "professional": {"name": "Business", "icon": "💼"}
        }

        # Initialize session state for preset
        if 'selected_preset' not in st.session_state:
            st.session_state.selected_preset = 'custom'

        # Render preset buttons in 2x2 grid with modern styling
        cols = st.columns(4)
        preset_keys = list(preset_options.keys())

        for idx, key in enumerate(preset_keys):
            with cols[idx]:
                option = preset_options[key]
                is_selected = st.session_state.selected_preset == key

                if st.button(
                    f"{option['icon']}",
                    key=f"preset_{key}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                    help=option['name']
                ):
                    st.session_state.selected_preset = key
                    st.rerun()

        # Show current preset name
        current_preset = preset_options[st.session_state.selected_preset]
        st.markdown(f"""
        <div style="text-align: center; margin: 0.5rem 0 1rem 0;">
            <span style="font-size: 0.75rem; color: #64748B; background: #F1F5F9; padding: 0.25rem 0.75rem; border-radius: 20px;">
                {current_preset['icon']} {current_preset['name']} Mode
            </span>
        </div>
        """, unsafe_allow_html=True)

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

        # Custom settings - Modern Card Section
        if preset == "custom":
            st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-section-header">
                    <div class="sidebar-section-icon" style="background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
                    </div>
                    <span class="sidebar-section-title">Language & Style</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            language = st.selectbox(
                "Language",
                ["bahasa", "english", "mixed"],
                index=0
            )

            # Tone selection - simplified
            tone_mode = st.radio(
                "Tone",
                ["Preset", "Custom"],
                index=0,
                horizontal=True,
                key="tone_mode"
            )

            if tone_mode == "Preset":
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
            else:
                tone = st.text_input(
                    "Custom Tone",
                    value="professional, friendly",
                    placeholder="e.g., casual, witty",
                    label_visibility="collapsed"
                )

            # Content Angle - simplified
            angle_mode = st.radio(
                "Content Angle",
                ["Preset", "Custom"],
                index=0,
                horizontal=True,
                key="angle_mode"
            )

            if angle_mode == "Preset":
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
            else:
                angle = st.text_area(
                    "Custom Angle",
                    value="Tell a personal story with lessons learned",
                    height=60,
                    label_visibility="collapsed"
                )

        # Theme Selection - Modern Visual Grid
        st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-header">
                <div class="sidebar-section-icon" style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.555C21.965 6.012 17.461 2 12 2z"/></svg>
                </div>
                <span class="sidebar-section-title">Visual Theme</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

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

        # Compact theme preview
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

        if theme in ['dark_mode', 'neon_nights', 'dark_gradient', 'ocean_gradient']:
            preview_text_color = '#FFFFFF'
        else:
            preview_text_color = '#18181B'

        st.markdown(f"""
        <div style="{bg_style}; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="color: {preview_text_color}; font-weight: 700; font-size: 1.125rem; margin-bottom: 0.5rem;">Aa Bb</div>
            <div style="background: {colors['accent']}; color: {colors['bg']}; padding: 4px 10px; border-radius: 4px; display: inline-block; font-size: 0.75rem; font-weight: 600;">Highlight</div>
        </div>
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 0.6875rem; color: #94A3B8;">{theme_info[theme]["description"]}</span>
        </div>
        """, unsafe_allow_html=True)

        # Content Strategy - Compact Modern Card
        st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-header">
                <div class="sidebar-section-icon" style="background: linear-gradient(135deg, #EC4899 0%, #DB2777 100%);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                </div>
                <span class="sidebar-section-title">Content Strategy</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        content_purpose = st.radio(
            "Purpose",
            options=["Educational", "Motivational", "Storytelling"],
            index=2,
            horizontal=True,
            help="Controls narrative arc"
        )

        visual_role = st.radio(
            "Visuals",
            options=["Amplify", "Evidence", "Minimal"],
            index=0,
            horizontal=True,
            help="How images support text"
        )

        visual_style = st.selectbox(
            "Style",
            options=["Auto (AI)", "Cartoon", "Movie/TV", "Photos", "Diagrams", "Text Only"],
            index=0,
            label_visibility="collapsed"
        )

        # Compact arc summary
        strategy_summary = {
            "Educational": "Problem → Explain → Apply",
            "Motivational": "Pain → Shift → Action",
            "Storytelling": "Hook → Tension → Resolve"
        }
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(236, 72, 153, 0.08) 0%, rgba(219, 39, 119, 0.08) 100%); padding: 0.5rem 0.75rem; border-radius: 8px; margin: 0.5rem 0 1rem 0; border-left: 3px solid #EC4899;">
            <span style="font-size: 0.6875rem; color: #9D174D; font-weight: 500;">{strategy_summary[content_purpose]}</span>
        </div>
        """, unsafe_allow_html=True)

        # AI Visual & Options - Combined Compact Section
        st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-header">
                <div class="sidebar-section-icon" style="background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="m6 20 .7-2.9A1.4 1.4 0 0 1 8.1 16h7.8a1.4 1.4 0 0 1 1.4 1.1l.7 2.9"/></svg>
                </div>
                <span class="sidebar-section-title">Output Settings</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # AI Visual Selection checkbox
        use_memes = st.checkbox("AI Visual Selection", value=True, help="AI picks best images for each slide")

        if use_memes:
            st.markdown("""
            <div style="background: #ECFDF5; padding: 0.5rem 0.75rem; border-radius: 8px; margin-bottom: 0.75rem;">
                <span style="font-size: 0.6875rem; color: #047857;">AI auto-selects cartoons, movies, memes</span>
            </div>
            """, unsafe_allow_html=True)
            use_ai_memes = True
            content_type_override = "blend"
            meme_style = "dark_minimal"
            meme_language = "en"
        else:
            st.markdown("""
            <div style="background: #F1F5F9; padding: 0.5rem 0.75rem; border-radius: 8px; margin-bottom: 0.75rem;">
                <span style="font-size: 0.6875rem; color: #64748B;">Text-only mode</span>
            </div>
            """, unsafe_allow_html=True)
            use_ai_memes = False
            content_type_override = None
            meme_style = "dark_minimal"
            meme_language = "en"

        # Compact toggles - stacked for better readability
        use_highlighting = st.checkbox("AI Keyword Highlighting", value=True, help="Highlight important words")
        show_logo = st.checkbox("Show Logo", value=False, help="Display logo on slides")

        logo_path = None
        if show_logo:
            default_logo = Path("assets/logo.png")
            if default_logo.exists():
                logo_path = str(default_logo)
            else:
                show_logo = False

        show_slide_indicator = st.checkbox("Slide Indicators", value=False, help="Show slide numbers")
        skip_humanizer = st.checkbox("Skip Humanization", value=False, help="Skip AI authenticity check")

        # Advanced options (collapsed)
        with st.expander("More Options", expanded=False):
            versions = st.slider("Content Versions", 1, 3, 1, help="Generate multiple variations")
            st.markdown('<p style="font-size: 0.75rem; color: #64748B; margin-bottom: 0.25rem;">Output Folder</p>', unsafe_allow_html=True)
            output_name = st.text_input("output_folder_hidden", value="carousel", label_visibility="hidden", placeholder="carousel")

        # System Status - Compact inline
        st.markdown("""
        <div class="sidebar-section" style="padding: 0.75rem;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.6875rem; color: #64748B; font-weight: 500;">System Status</span>
                <div style="display: flex; gap: 0.75rem;">
        """, unsafe_allow_html=True)

        renderer_status = "online" if PLAYWRIGHT_AVAILABLE else "offline"
        api_status = "online" if check_api_key() else "offline"

        st.markdown(f"""
                    <div style="display: flex; align-items: center; gap: 0.25rem;">
                        <span class="status-dot {renderer_status}"></span>
                        <span style="font-size: 0.625rem; color: #64748B;">Renderer</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.25rem;">
                        <span class="status-dot {api_status}"></span>
                        <span style="font-size: 0.625rem; color: #64748B;">API</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Draft History - Compact
        if 'draft_history' not in st.session_state:
            st.session_state.draft_history = []

        if st.session_state.get('content_draft', '').strip() or st.session_state.draft_history:
            with st.expander("Drafts", expanded=False):
                if st.session_state.get('content_draft', '').strip():
                    if st.button("Save Current", use_container_width=True, type="secondary"):
                        timestamp = datetime.now().strftime("%m/%d %H:%M")
                        preview = st.session_state.content_draft[:40] + "..." if len(st.session_state.content_draft) > 40 else st.session_state.content_draft
                        st.session_state.draft_history.insert(0, {
                            'content': st.session_state.content_draft,
                            'timestamp': timestamp,
                            'preview': preview
                        })
                        st.session_state.draft_history = st.session_state.draft_history[:5]
                        st.rerun()

                for idx, draft in enumerate(st.session_state.draft_history):
                    col_info, col_load, col_del = st.columns([3, 1, 1])
                    with col_info:
                        st.markdown(f"<span style='font-size: 0.6875rem; color: #64748B;'>{draft['timestamp']}</span>", unsafe_allow_html=True)
                    with col_load:
                        if st.button("Load", key=f"load_{idx}", use_container_width=True):
                            st.session_state.content_draft = draft['content']
                            st.rerun()
                    with col_del:
                        if st.button("X", key=f"del_{idx}"):
                            st.session_state.draft_history.pop(idx)
                            st.rerun()

        # Footer
        st.markdown("""
        <div style="margin-top: 1.5rem; text-align: center;">
            <span style="font-size: 0.625rem; color: #CBD5E1;">Powered by DeepSeek AI</span>
        </div>
        """, unsafe_allow_html=True)

    # Map UI values to internal values
    content_purpose_map = {
        "Educational": "educational",
        "Motivational": "motivational",
        "Storytelling": "storytelling"
    }
    visual_role_map = {
        "Amplify Emotion": "amplify_emotion",
        "Provide Evidence": "provide_evidence",
        "Minimal/None": "minimal"
    }
    visual_style_map = {
        "Auto (AI Decides)": "auto",
        "Cartoon Scenes": "cartoon",
        "Movie/TV Stills": "movie",
        "Professional Photos": "photo",
        "Diagrams/Charts": "diagram",
        "Text Only": "text_only"
    }

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
        # Content Strategy settings - NEW
        "content_purpose": content_purpose_map.get(content_purpose, "storytelling"),
        "visual_role": visual_role_map.get(visual_role, "amplify_emotion"),
        "visual_style": visual_style_map.get(visual_style, "auto"),
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
                        # Step 1: Rewrite with content strategy
                        st.write(f"Writing {settings['content_purpose']} content with AI copywriter...")
                        rewriter = ContentRewriter()
                        content_versions = rewriter.rewrite_content(
                            rough_idea=content,
                            tone=settings["tone"] or "santai_gaul",
                            language=settings["language"] or "bahasa",
                            angle=settings["angle"] or "story_personal",
                            versions=settings["versions"],
                            content_purpose=settings["content_purpose"]  # NEW: Pass content purpose
                        )
                        st.write(f"✓ Generated {len(content_versions)} version(s)")

                        selected_version = content_versions[0]
                        slides = selected_version['slides']
                        narrative_beats = selected_version.get('narrative_beats', {})  # NEW: Get beats

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
                            meme_language=settings["meme_language"],
                            # NEW: Content Strategy parameters
                            content_purpose=settings["content_purpose"],
                            visual_role=settings["visual_role"],
                            visual_style=settings["visual_style"],
                            narrative_beats=narrative_beats
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
