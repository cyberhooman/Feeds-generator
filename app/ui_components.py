"""
Production-Grade UI Components - Distinctive Design System
Bold, minimalist interface with sophisticated typography and interactions.
"""

import streamlit as st


def inject_custom_css():
    """Inject production-grade CSS with distinctive aesthetics."""
    st.markdown("""
    <style>
    /* ===== TYPOGRAPHY - IBM Plex & JetBrains Mono ===== */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ===== DESIGN TOKENS ===== */
    :root {
        /* Pure Monochrome */
        --pure-black: #000000;
        --pure-white: #FFFFFF;

        /* Grayscale System */
        --gray-50: #FAFAFA;
        --gray-100: #F4F4F5;
        --gray-200: #E4E4E7;
        --gray-300: #D4D4D8;
        --gray-400: #A1A1AA;
        --gray-500: #71717A;
        --gray-600: #52525B;
        --gray-700: #3F3F46;
        --gray-800: #27272A;
        --gray-900: #18181B;

        /* Semantic Colors */
        --surface-primary: var(--pure-white);
        --surface-secondary: var(--gray-50);
        --surface-elevated: var(--pure-white);
        --surface-overlay: rgba(0, 0, 0, 0.02);

        --text-primary: var(--gray-900);
        --text-secondary: var(--gray-600);
        --text-tertiary: var(--gray-400);
        --text-inverse: var(--pure-white);

        --border-subtle: var(--gray-200);
        --border-default: var(--gray-300);
        --border-strong: var(--gray-400);
        --border-accent: var(--pure-black);

        /* Typography Scale */
        --font-display: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'JetBrains Mono', 'Courier New', monospace;

        --text-xs: 0.6875rem;    /* 11px */
        --text-sm: 0.8125rem;    /* 13px */
        --text-base: 0.9375rem;  /* 15px */
        --text-lg: 1.125rem;     /* 18px */
        --text-xl: 1.5rem;       /* 24px */
        --text-2xl: 2rem;        /* 32px */

        /* Spacing Scale */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.25rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        --space-10: 2.5rem;

        /* Layout */
        --radius-sm: 2px;
        --radius-md: 4px;
        --radius-lg: 6px;
        --radius-full: 9999px;

        /* Shadows - Extremely subtle */
        --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.02);
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
        --shadow-md: 0 2px 6px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.08);

        /* Transitions */
        --transition-fast: 120ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ===== GLOBAL RESETS ===== */
    * {
        font-family: var(--font-display) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .main .block-container {
        padding: var(--space-8) var(--space-6);
        max-width: 1440px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background-color: var(--surface-primary);
    }

    /* ===== SIDEBAR TOGGLE - Sophisticated Interaction ===== */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        background: var(--pure-black) !important;
        color: var(--pure-white) !important;
        border: 1px solid var(--pure-black) !important;
        border-left: none !important;
        border-radius: 0 var(--radius-md) var(--radius-md) 0 !important;
        padding: var(--space-4) var(--space-3) !important;
        position: fixed !important;
        top: 50% !important;
        left: 0 !important;
        transform: translateY(-50%) !important;
        z-index: 999999 !important;
        cursor: pointer !important;
        transition: var(--transition-base) !important;
        box-shadow: var(--shadow-md) !important;
    }

    [data-testid="collapsedControl"]:hover {
        background: var(--gray-800) !important;
        transform: translateY(-50%) translateX(3px) !important;
        box-shadow: var(--shadow-lg) !important;
    }

    [data-testid="collapsedControl"]:active {
        transform: translateY(-50%) translateX(1px) !important;
    }

    [data-testid="collapsedControl"] svg {
        color: var(--pure-white) !important;
        width: 1.125rem !important;
        height: 1.125rem !important;
    }

    /* ===== TYPOGRAPHY SYSTEM ===== */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
        line-height: 1.2 !important;
    }

    h1 {
        font-size: var(--text-2xl) !important;
        font-weight: 700 !important;
        letter-spacing: -0.04em !important;
    }

    h2 {font-size: var(--text-xl) !important;}
    h3 {font-size: var(--text-lg) !important;}

    p, span, div, label {
        color: var(--text-primary) !important;
        line-height: 1.5 !important;
        font-size: var(--text-base) !important;
    }

    /* Caption text */
    .stCaption,
    [data-testid="stCaption"] {
        color: var(--text-secondary) !important;
        font-size: var(--text-sm) !important;
        line-height: 1.4 !important;
    }

    /* Code blocks */
    code {
        font-family: var(--font-mono) !important;
        font-size: var(--text-sm) !important;
        background: var(--surface-overlay) !important;
        padding: 0.125rem 0.375rem !important;
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border-subtle) !important;
    }

    /* ===== SIDEBAR - Clean Structure ===== */
    [data-testid="stSidebar"] {
        background-color: var(--surface-secondary);
        border-right: 1px solid var(--border-subtle);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: var(--text-xs);
        font-weight: 600;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: var(--space-6) 0 var(--space-3) 0;
    }

    /* ===== HEADER - Bold Statement ===== */
    .studio-header {
        background: var(--pure-black);
        border-radius: var(--radius-lg);
        padding: var(--space-8) var(--space-10);
        margin-bottom: var(--space-8);
        position: relative;
        overflow: hidden;
    }

    .studio-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        pointer-events: none;
    }

    .studio-header h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 0 var(--space-2) 0 !important;
        letter-spacing: -0.045em !important;
        color: var(--pure-white) !important;
    }

    .studio-header p {
        font-size: var(--text-base) !important;
        color: var(--gray-400) !important;
        margin: 0 !important;
        font-weight: 400 !important;
    }

    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-2);
        background: var(--gray-900);
        padding: var(--space-1) var(--space-3);
        border-radius: var(--radius-full);
        font-size: var(--text-xs);
        font-weight: 500;
        margin-top: var(--space-4);
        color: var(--gray-400) !important;
        border: 1px solid var(--gray-800);
    }

    /* ===== BUTTONS - Precise Interactions ===== */
    .stButton > button {
        border-radius: var(--radius-md);
        font-weight: 500;
        font-size: var(--text-sm);
        padding: var(--space-2) var(--space-4);
        transition: var(--transition-fast);
        border: 1px solid var(--border-default);
        background: var(--surface-primary);
        color: var(--text-primary);
        box-shadow: var(--shadow-xs);
        position: relative;
    }

    .stButton > button:hover {
        background: var(--surface-secondary);
        border-color: var(--border-strong);
        transform: translateY(-1px);
        box-shadow: var(--shadow-sm);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: none;
    }

    /* Primary Button - Bold Black */
    .stButton > button[kind="primary"] {
        background: var(--pure-black);
        border: 1px solid var(--pure-black);
        color: var(--pure-white);
        box-shadow: var(--shadow-md);
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--gray-800);
        border-color: var(--gray-800);
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }

    /* Generate button - Full width with emphasis */
    div[data-testid="stButton"] > button[kind="primary"] {
        width: 100%;
        padding: var(--space-4) var(--space-6);
        font-size: var(--text-base);
        font-weight: 600;
        letter-spacing: -0.01em;
    }

    /* ===== INPUTS - Clean & Functional ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-default) !important;
        background-color: var(--surface-primary) !important;
        color: var(--text-primary) !important;
        font-size: var(--text-sm) !important;
        transition: var(--transition-fast) !important;
        box-shadow: var(--shadow-xs) !important;
    }

    .stTextInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover,
    .stSelectbox > div > div:hover {
        border-color: var(--border-strong) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--border-accent) !important;
        box-shadow: 0 0 0 3px var(--surface-overlay) !important;
        outline: none !important;
    }

    /* Labels */
    .stTextArea label,
    .stTextInput label,
    .stSelectbox label,
    .stNumberInput label {
        color: var(--text-primary) !important;
        font-size: var(--text-sm) !important;
        font-weight: 500 !important;
        margin-bottom: var(--space-2) !important;
    }

    /* Placeholder */
    ::placeholder {
        color: var(--text-tertiary) !important;
        opacity: 1 !important;
    }

    /* ===== CHECKBOX & RADIO - Modern Controls ===== */
    .stCheckbox label,
    .stRadio label {
        color: var(--text-primary) !important;
        font-size: var(--text-sm) !important;
        font-weight: 400 !important;
    }

    /* Radio button group */
    .stRadio > div {
        background: var(--surface-secondary);
        padding: var(--space-1);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-subtle);
        display: flex;
        gap: var(--space-1);
    }

    .stRadio > div > label {
        padding: var(--space-2) var(--space-3);
        border-radius: var(--radius-sm);
        transition: var(--transition-fast);
        cursor: pointer;
        margin: 0 !important;
    }

    .stRadio > div > label:hover {
        background: var(--surface-overlay);
    }

    /* ===== TABS - Segmented Control Style ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-1);
        background: var(--surface-secondary);
        padding: var(--space-1);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-subtle);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: var(--space-2) var(--space-4);
        font-weight: 500;
        font-size: var(--text-sm);
        color: var(--text-secondary);
        background: transparent;
        border: none;
        transition: var(--transition-fast);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--surface-overlay);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background: var(--surface-primary);
        color: var(--text-primary);
        box-shadow: var(--shadow-xs);
    }

    /* ===== EXPANDER - Minimal Disclosure ===== */
    .streamlit-expanderHeader {
        font-weight: 500 !important;
        font-size: var(--text-sm) !important;
        color: var(--text-primary) !important;
        background-color: transparent !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        transition: var(--transition-fast) !important;
        padding: var(--space-3) var(--space-4) !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: var(--surface-secondary) !important;
        border-color: var(--border-default) !important;
    }

    .streamlit-expanderContent {
        background-color: var(--surface-primary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        padding: var(--space-4) !important;
    }

    /* ===== METRICS - Data Display ===== */
    [data-testid="stMetricValue"] {
        font-size: var(--text-xl) !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        font-family: var(--font-mono) !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: var(--text-xs) !important;
        color: var(--text-tertiary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 500 !important;
    }

    /* ===== PROGRESS & LOADING ===== */
    .stProgress > div > div > div {
        background-color: var(--pure-black) !important;
    }

    .stSpinner > div {
        border-color: var(--border-subtle) var(--border-subtle) var(--pure-black) var(--pure-black) !important;
    }

    /* ===== ALERTS ===== */
    .stAlert {
        background-color: var(--surface-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        padding: var(--space-4) !important;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: var(--space-6) 0;
    }

    /* ===== CUSTOM COMPONENTS ===== */

    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-2);
        padding: var(--space-1) var(--space-3);
        border-radius: var(--radius-full);
        font-size: var(--text-xs);
        font-weight: 500;
        border: 1px solid var(--border-default);
        background: var(--surface-primary);
        box-shadow: var(--shadow-xs);
    }

    /* Card Component */
    .studio-card {
        background: var(--surface-primary);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: var(--space-6);
        margin-bottom: var(--space-4);
        transition: var(--transition-base);
        box-shadow: var(--shadow-xs);
    }

    .studio-card:hover {
        border-color: var(--border-default);
        box-shadow: var(--shadow-sm);
    }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: var(--space-10) var(--space-8);
        background: var(--surface-secondary);
        border-radius: var(--radius-lg);
        border: 2px dashed var(--border-default);
    }

    .empty-state-icon {
        margin-bottom: var(--space-4);
        opacity: 0.4;
    }

    .empty-state-title {
        font-size: var(--text-lg);
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--space-2);
    }

    .empty-state-desc {
        color: var(--text-secondary);
        font-size: var(--text-sm);
    }

    /* ===== MICRO-INTERACTIONS ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn var(--transition-base) ease-out;
    }

    /* Hover lift effect for cards */
    .lift-on-hover {
        transition: transform var(--transition-base), box-shadow var(--transition-base);
    }

    .lift-on-hover:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    /* ===== ICON UTILITIES ===== */
    .icon-sm { width: 0.875rem; height: 0.875rem; }
    .icon-md { width: 1.125rem; height: 1.125rem; }
    .icon-lg { width: 1.5rem; height: 1.5rem; }
    .icon-xl { width: 2rem; height: 2rem; }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render distinctive header with bold typography."""
    st.markdown("""
    <div class="studio-header">
        <h1>Content Studio</h1>
        <p>Professional Instagram carousel generator powered by AI</p>
        <div class="header-badge">
            <svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 3 4 8 5-5 5 15H2L8 3z"/></svg>
            <span>Production v2.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_status_badge(status: str, text: str):
    """Render status badge with icon."""
    icons = {
        "success": '<svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        "warning": '<svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>',
        "error": '<svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>',
        "info": '<svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>'
    }
    icon = icons.get(status, "")
    return f'<span class="status-badge">{icon} {text}</span>'


def render_empty_state():
    """Render empty state with icon."""
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">
            <svg class="icon-xl" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="18" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/></svg>
        </div>
        <div class="empty-state-title">Your carousel will appear here</div>
        <div class="empty-state-desc">Enter your content and generate to preview</div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, icon_svg: str):
    """Render metric card."""
    st.markdown(f"""
    <div class="studio-card" style="text-align: center;">
        <div style="margin-bottom: 0.5rem;">{icon_svg}</div>
        <div style="font-size: 1.5rem; font-weight: 700; font-family: var(--font-mono); color: var(--text-primary);">{value}</div>
        <div style="font-size: 0.6875rem; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500;">{label}</div>
    </div>
    """, unsafe_allow_html=True)
