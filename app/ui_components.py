"""
Production-Grade UI Components - Distinctive Design System
Bold, minimalist interface with sophisticated typography and interactions.
"""

import streamlit as st


def inject_custom_css():
    """Inject production-grade CSS with distinctive aesthetics."""
    st.markdown("""
    <style>
    /* ===== TYPOGRAPHY - Distinctive Choices ===== */
    /* Using Space Grotesk (startup/modern) + Fira Code (technical) */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Fira+Code:wght@400;500;600&family=Fraunces:wght@300;400;600;700;900&display=swap');

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

        /* Accent Colors - Distinctive Palette (Emerald & Amber - High Contrast) */
        --accent-primary: #10B981;
        --accent-secondary: #F59E0B;
        --accent-tertiary: #EC4899;
        --accent-gradient: linear-gradient(135deg, #10B981 0%, #059669 100%);
        --accent-glow: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);

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

        /* Typography Scale - Distinctive Fonts */
        --font-display: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-heading: 'Fraunces', Georgia, serif;
        --font-mono: 'Fira Code', 'Courier New', monospace;

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
    /* Use system fonts as base to prevent rendering issues */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Only apply custom fonts to specific elements */
    .studio-header h1,
    .studio-header p {
        font-family: var(--font-heading) !important;
    }

    .main .block-container {
        padding: var(--space-8) var(--space-6);
        max-width: 1440px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background:
            radial-gradient(circle at 20% 80%, rgba(16, 185, 129, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(245, 158, 11, 0.02) 0%, transparent 50%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2310B981' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"),
            #FAFAFA;
        background-attachment: fixed;
    }

    /* ===== SIDEBAR TOGGLE - Emerald Accent ===== */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: var(--pure-white) !important;
        border: 1px solid #10B981 !important;
        border-left: none !important;
        border-radius: 0 8px 8px 0 !important;
        padding: var(--space-4) var(--space-3) !important;
        position: fixed !important;
        top: 50% !important;
        left: 0 !important;
        transform: translateY(-50%) !important;
        z-index: 999999 !important;
        cursor: pointer !important;
        transition: all var(--transition-base) !important;
        box-shadow:
            0 4px 12px rgba(16, 185, 129, 0.3),
            0 1px 3px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="collapsedControl"]:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        transform: translateY(-50%) translateX(4px) !important;
        box-shadow:
            0 6px 20px rgba(16, 185, 129, 0.4),
            0 2px 6px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="collapsedControl"]:active {
        transform: translateY(-50%) translateX(2px) !important;
    }

    [data-testid="collapsedControl"] svg {
        color: var(--pure-white) !important;
        width: 1.125rem !important;
        height: 1.125rem !important;
    }

    /* ===== TYPOGRAPHY SYSTEM - Only main headers ===== */
    /* Don't override all headers - causes sidebar issues */
    .main h1, .main h2 {
        font-family: var(--font-heading) !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.2 !important;
    }

    .main h1 {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.05em !important;
    }

    .main h2 {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }

    .main h3 {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
    }

    /* Remove aggressive global font-size to prevent overlap issues */
    p, label {
        color: var(--text-primary) !important;
        line-height: 1.5 !important;
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

    /* ===== SIDEBAR - Modern Glass Morphism Design ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.06) !important;
        padding: 0 !important;
        position: relative;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1rem 1rem 2rem 1rem !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 0 !important;
    }

    /* Modern Section Cards */
    .sidebar-section {
        background: var(--pure-white);
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    .sidebar-section:hover {
        border-color: rgba(16, 185, 129, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }

    .sidebar-section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.04);
    }

    .sidebar-section-icon {
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .sidebar-section-icon svg {
        width: 14px;
        height: 14px;
        color: white;
    }

    .sidebar-section-title {
        font-size: 0.8125rem !important;
        font-weight: 600 !important;
        color: #1E293B !important;
        margin: 0 !important;
        letter-spacing: -0.01em !important;
    }

    /* Quick Action Pills */
    .quick-action-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .quick-action-pill {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 0.75rem 0.5rem;
        background: #F8FAFC;
        border: 1px solid transparent;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.15s ease;
        text-align: center;
    }

    .quick-action-pill:hover {
        background: #F1F5F9;
        border-color: rgba(16, 185, 129, 0.2);
        transform: translateY(-1px);
    }

    .quick-action-pill.active {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-color: #10B981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }

    .quick-action-pill .pill-icon {
        font-size: 1.25rem;
        margin-bottom: 0.25rem;
    }

    .quick-action-pill .pill-label {
        font-size: 0.6875rem;
        font-weight: 500;
        color: #64748B;
    }

    .quick-action-pill.active .pill-label {
        color: #059669;
        font-weight: 600;
    }

    /* Theme Selector Grid */
    .theme-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem;
    }

    .theme-chip {
        aspect-ratio: 1;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.15s ease;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }

    .theme-chip:hover {
        transform: scale(1.05);
    }

    .theme-chip.active {
        border-color: #10B981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    }

    .theme-chip.active::after {
        content: '';
        position: absolute;
        bottom: 4px;
        right: 4px;
        width: 14px;
        height: 14px;
        background: #10B981;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Sidebar headings - Modern style */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 0.6875rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin: 1rem 0 0.5rem 0 !important;
        line-height: 1.4 !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: var(--text-primary) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 0.8125rem !important;
        line-height: 1.5 !important;
    }

    /* Use system fonts in sidebar */
    [data-testid="stSidebar"] * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Modern Input Fields */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 10px !important;
        color: var(--gray-900) !important;
        font-size: 0.8125rem !important;
        transition: all 0.15s ease !important;
        min-height: 40px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"]:hover > div {
        border-color: rgba(16, 185, 129, 0.3) !important;
        background-color: var(--pure-white) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"]:focus-within > div {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }

    /* Sidebar select text visibility */
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: var(--gray-900) !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] div {
        color: var(--gray-900) !important;
    }

    /* Status Indicator Dots */
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.5rem;
    }

    .status-dot.online {
        background: #10B981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    }

    .status-dot.offline {
        background: #EF4444;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
    }

    /* Compact Toggle Switch Style */
    .toggle-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.04);
    }

    .toggle-row:last-child {
        border-bottom: none;
    }

    .toggle-label {
        font-size: 0.8125rem;
        color: #334155;
        font-weight: 500;
    }

    .toggle-desc {
        font-size: 0.6875rem;
        color: #94A3B8;
        margin-top: 0.125rem;
    }

    /* Dropdown menu popover - WHITE BACKGROUND WITH DARK TEXT */
    [data-baseweb="popover"] {
        background-color: var(--pure-white) !important;
    }

    [data-baseweb="menu"] {
        background-color: var(--pure-white) !important;
    }

    [data-baseweb="menu"] li {
        background-color: var(--pure-white) !important;
        color: var(--gray-900) !important;
    }

    [data-baseweb="menu"] li:hover {
        background-color: var(--gray-100) !important;
        color: var(--gray-900) !important;
    }

    /* Select dropdown options */
    [role="option"] {
        background-color: var(--pure-white) !important;
        color: var(--gray-900) !important;
    }

    [role="option"]:hover {
        background-color: var(--gray-100) !important;
        color: var(--gray-900) !important;
    }

    [aria-selected="true"][role="option"] {
        background-color: var(--gray-200) !important;
        color: var(--gray-900) !important;
    }

    /* Sidebar captions - better spacing */
    [data-testid="stSidebar"] .stCaption {
        margin-top: 0.25rem !important;
        margin-bottom: 1rem !important;
        font-size: 0.6875rem !important;
        color: var(--text-secondary) !important;
        line-height: 1.4 !important;
        display: block !important;
    }

    /* Fix overlapping text in sidebar */
    [data-testid="stSidebar"] > div > div {
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }

    /* Fix dropdown arrow overlapping with text */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        position: relative !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        padding-right: 2.5rem !important; /* Extra space for arrow */
    }

    /* Position dropdown arrow properly */
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        position: absolute !important;
        right: 0.75rem !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        pointer-events: none !important;
    }

    /* Ensure text doesn't overlap with arrow */
    [data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="select-value"] {
        max-width: calc(100% - 2rem) !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
    }

    /* Sidebar text elements - prevent overlap */
    [data-testid="stSidebar"] label {
        display: block !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.4 !important;
    }

    /* Sidebar form elements spacing */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        margin-bottom: 1rem !important;
    }

    /* ===== HEADER - Distinctive Dark Hero with Emerald Accents ===== */
    .studio-header {
        background:
            radial-gradient(circle at top right, rgba(16, 185, 129, 0.15) 0%, transparent 50%),
            radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.08) 0%, transparent 50%),
            linear-gradient(135deg, #0A0A0A 0%, #18181B 50%, #27272A 100%);
        border-radius: 12px;
        padding: 4rem 3rem;
        margin-bottom: var(--space-8);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .studio-header::before {
        content: '';
        position: absolute;
        top: -100px;
        right: -100px;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 60%);
        pointer-events: none;
        animation: float 8s ease-in-out infinite;
    }

    .studio-header::after {
        content: '';
        position: absolute;
        bottom: -80px;
        left: -80px;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.12) 0%, transparent 60%);
        pointer-events: none;
        animation: float 10s ease-in-out infinite reverse;
    }

    @keyframes float {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(30px, 30px) scale(1.1); }
    }

    .studio-header h1 {
        font-size: 4rem !important;
        font-weight: 900 !important;
        margin: 0 0 1rem 0 !important;
        letter-spacing: -0.05em !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
        animation: fadeSlideUp 0.8s ease-out;
    }

    .studio-header p {
        font-size: 1.125rem !important;
        color: rgba(255, 255, 255, 0.7) !important;
        margin: 0 !important;
        font-weight: 400 !important;
        position: relative;
        z-index: 1;
        animation: fadeSlideUp 0.8s ease-out 0.1s backwards;
    }

    @keyframes fadeSlideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-2);
        background: rgba(16, 185, 129, 0.1);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: var(--radius-full);
        font-size: var(--text-xs);
        font-weight: 600;
        margin-top: var(--space-4);
        color: #10B981 !important;
        border: 1px solid rgba(16, 185, 129, 0.3);
        position: relative;
        z-index: 1;
        animation: fadeSlideUp 0.8s ease-out 0.2s backwards;
        transition: all 0.3s ease;
    }

    .header-badge:hover {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.5);
        transform: translateY(-2px);
    }

    /* ===== BUTTONS - Precise Interactions ===== */
    .stButton > button {
        border-radius: var(--radius-md);
        font-weight: 500;
        font-size: var(--text-sm);
        padding: var(--space-3) var(--space-4);
        transition: var(--transition-fast);
        border: 1px solid var(--border-default);
        background: var(--surface-primary);
        color: var(--text-primary);
        box-shadow: var(--shadow-xs);
        position: relative;
        min-height: 38px;
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

    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: var(--surface-primary);
        border: 1.5px solid var(--border-default);
        color: var(--text-primary);
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: var(--pure-black);
        background: var(--gray-50);
    }

    /* Primary Button - Emerald Gradient with Glow */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border: 1.5px solid #10B981;
        color: var(--pure-white);
        box-shadow:
            0 4px 12px rgba(16, 185, 129, 0.3),
            0 1px 3px rgba(0, 0, 0, 0.2);
        font-weight: 600;
        position: relative;
        overflow: hidden;
    }

    .stButton > button[kind="primary"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }

    .stButton > button[kind="primary"]:hover::before {
        left: 100%;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        border-color: #059669;
        box-shadow:
            0 6px 20px rgba(16, 185, 129, 0.4),
            0 2px 6px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0);
        box-shadow:
            0 2px 8px rgba(16, 185, 129, 0.3),
            0 1px 3px rgba(0, 0, 0, 0.2);
    }

    /* Sidebar preset buttons - Modern icon style */
    [data-testid="stSidebar"] .stButton > button {
        padding: 0.625rem;
        font-size: 1.25rem;
        min-height: 48px;
        aspect-ratio: 1;
        border-radius: 12px;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border: 2px solid #10B981;
        transform: scale(1.05);
    }

    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: #F8FAFC;
        border: 1px solid rgba(0, 0, 0, 0.08);
        color: #64748B;
    }

    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background: #F1F5F9;
        border-color: rgba(16, 185, 129, 0.2);
    }

    /* Modern Toggle Switches - Fix vertical text issue */
    [data-testid="stSidebar"] .stCheckbox,
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        background: transparent;
        padding: 0;
    }

    /* Toggle label text - ensure horizontal display */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label,
    [data-testid="stSidebar"] .stCheckbox label {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 0.5rem !important;
        white-space: nowrap !important;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] label span,
    [data-testid="stSidebar"] .stCheckbox label span {
        writing-mode: horizontal-tb !important;
        text-orientation: mixed !important;
    }

    /* Generate button - Full width with emphasis */
    div[data-testid="stButton"] > button[kind="primary"]:not([data-testid="stSidebar"] *) {
        width: 100%;
        padding: var(--space-4) var(--space-6);
        font-size: var(--text-base);
        font-weight: 600;
        letter-spacing: -0.01em;
        min-height: 48px;
    }

    /* ===== INPUTS - Clean & Functional ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border-default) !important;
        background-color: var(--pure-white) !important;
        color: var(--gray-900) !important;
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

    /* ALL SELECTBOX TEXT - FORCE DARK COLOR */
    .stSelectbox {
        color: var(--gray-900) !important;
    }

    .stSelectbox > div > div {
        color: var(--gray-900) !important;
        background-color: var(--pure-white) !important;
    }

    .stSelectbox span,
    .stSelectbox div {
        color: var(--gray-900) !important;
    }

    /* Selectbox SVG icons */
    .stSelectbox svg {
        fill: var(--gray-900) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #10B981 !important;
        box-shadow:
            0 0 0 3px rgba(16, 185, 129, 0.1) !important,
            0 1px 3px rgba(0, 0, 0, 0.1) !important;
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

    /* Sidebar checkboxes - ensure visibility and proper layout */
    [data-testid="stSidebar"] .stCheckbox {
        margin-bottom: 1rem !important;
    }

    [data-testid="stSidebar"] .stCheckbox label {
        color: var(--text-primary) !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        line-height: 1.5 !important;
    }

    [data-testid="stSidebar"] .stCheckbox label > span {
        color: var(--text-primary) !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    [data-testid="stSidebar"] .stCheckbox label > div {
        flex-shrink: 0 !important;
    }

    /* Radio button group - Segmented control style */
    .stRadio [role="radiogroup"] {
        background: var(--gray-100);
        padding: var(--space-1);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-subtle);
        display: flex;
        gap: var(--space-1);
    }

    .stRadio label {
        padding: var(--space-2) var(--space-3) !important;
        border-radius: var(--radius-sm) !important;
        transition: var(--transition-fast) !important;
        cursor: pointer !important;
        margin: 0 !important;
        background: transparent !important;
        flex: 1;
        text-align: center;
    }

    .stRadio label:hover {
        background: var(--surface-overlay) !important;
    }

    /* Selected radio button */
    .stRadio label[data-selected="true"],
    .stRadio label:has(input:checked) {
        background: var(--pure-white) !important;
        box-shadow: var(--shadow-xs) !important;
        font-weight: 500 !important;
    }

    /* Sidebar radio buttons - proper spacing and layout */
    [data-testid="stSidebar"] .stRadio {
        margin-bottom: 1rem !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: var(--text-primary) !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    [data-testid="stSidebar"] .stRadio label span {
        color: var(--text-primary) !important;
        font-size: var(--text-sm) !important;
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
        font-size: 0.875rem !important;
        color: var(--text-primary) !important;
        background-color: var(--gray-50) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        transition: var(--transition-fast) !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Fix expander text overlap - target the inner span/p */
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span,
    .streamlit-expanderHeader div {
        font-size: 0.875rem !important;
        line-height: 1.4 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: var(--gray-100) !important;
        border-color: var(--border-default) !important;
    }

    .streamlit-expanderContent {
        background-color: var(--surface-primary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }

    /* Sidebar expander - Modern minimal style */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        margin-bottom: 0.25rem !important;
        padding: 0.625rem 0.875rem !important;
        background: #F8FAFC !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 10px !important;
        font-size: 0.8125rem !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: #F1F5F9 !important;
        border-color: rgba(16, 185, 129, 0.2) !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderContent {
        margin-bottom: 0.75rem !important;
        padding: 0.75rem !important;
        background: transparent !important;
        border: none !important;
    }

    /* Radio buttons in sidebar - segmented control style */
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        background: #F8FAFC;
        padding: 0.25rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 0, 0, 0.06);
        gap: 0.25rem;
    }

    [data-testid="stSidebar"] .stRadio label {
        padding: 0.375rem 0.75rem !important;
        border-radius: 8px !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: white !important;
        color: #10B981 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }

    /* Expander content elements spacing */
    .streamlit-expanderContent > div > div {
        margin-bottom: 0.75rem !important;
    }

    .streamlit-expanderContent > div > div:last-child {
        margin-bottom: 0 !important;
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

    /* ===== SLIDER - Modern Track & Thumb ===== */
    .stSlider {
        padding: var(--space-2) 0;
    }

    .stSlider > div > div > div > div {
        background-color: var(--gray-200) !important;
        height: 4px !important;
        border-radius: var(--radius-full);
    }

    .stSlider > div > div > div > div > div {
        background: linear-gradient(90deg, #10B981, #059669) !important;
        height: 4px !important;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.3) !important;
    }

    .stSlider > div > div > div > div > div > div {
        background: linear-gradient(135deg, #10B981, #059669) !important;
        border: 2px solid var(--pure-white) !important;
        box-shadow:
            0 2px 6px rgba(16, 185, 129, 0.3),
            0 1px 3px rgba(0, 0, 0, 0.2) !important;
        width: 20px !important;
        height: 20px !important;
        top: -8px !important;
        transition: all var(--transition-fast) !important;
    }

    .stSlider > div > div > div > div > div > div:hover {
        transform: scale(1.2);
        box-shadow:
            0 4px 12px rgba(16, 185, 129, 0.4),
            0 2px 6px rgba(0, 0, 0, 0.2) !important;
    }

    /* Slider labels */
    .stSlider label {
        color: var(--text-primary) !important;
        font-size: var(--text-sm) !important;
        font-weight: 500 !important;
        margin-bottom: var(--space-2) !important;
    }

    /* ===== PROGRESS & LOADING - Emerald Theme ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10B981, #059669) !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important;
    }

    .stSpinner > div {
        border-color: var(--border-subtle) var(--border-subtle) #10B981 #10B981 !important;
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

    /* Card Component - Enhanced with Glow */
    .studio-card {
        background: var(--surface-primary);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: var(--space-6);
        margin-bottom: var(--space-4);
        transition: all var(--transition-base);
        box-shadow: var(--shadow-xs);
        position: relative;
        overflow: hidden;
    }

    .studio-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10B981, #F59E0B, #EC4899);
        opacity: 0;
        transition: opacity var(--transition-base);
    }

    .studio-card:hover {
        border-color: rgba(16, 185, 129, 0.3);
        box-shadow:
            var(--shadow-md),
            0 0 0 1px rgba(16, 185, 129, 0.1);
        transform: translateY(-2px);
    }

    .studio-card:hover::before {
        opacity: 1;
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

    /* ===== MICRO-INTERACTIONS - Staggered Page Load ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }

    .fade-in {
        animation: fadeIn var(--transition-base) ease-out;
    }

    /* Disable staggered animation - can cause layout issues */
    /* .main .block-container > div {
        animation: fadeIn 0.6s ease-out backwards;
    } */

    /* Hover lift effect for cards */
    .lift-on-hover {
        transition: transform var(--transition-base), box-shadow var(--transition-base);
    }

    .lift-on-hover:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    /* Pulse effect for loading states */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* ===== ICON UTILITIES ===== */
    .icon-sm { width: 0.875rem; height: 0.875rem; }
    .icon-md { width: 1.125rem; height: 1.125rem; }
    .icon-lg { width: 1.5rem; height: 1.5rem; }
    .icon-xl { width: 2rem; height: 2rem; }

    /* ===== CRITICAL DROPDOWN FIX - MAXIMUM SPECIFICITY ===== */
    /* Force white background and dark text on ALL dropdown elements */

    /* Dropdown container */
    ul[role="listbox"],
    [data-baseweb="menu"] ul,
    [data-baseweb="popover"] > div,
    div[role="listbox"] {
        background-color: var(--pure-white) !important;
        border: 1px solid var(--border-default) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }

    /* Dropdown options - all variations */
    ul[role="listbox"] li,
    [data-baseweb="menu"] li,
    li[role="option"],
    div[role="option"],
    [data-baseweb="list-item"] {
        background-color: var(--pure-white) !important;
        color: var(--gray-900) !important;
        padding: 0.5rem 1rem !important;
    }

    /* Dropdown hover state */
    ul[role="listbox"] li:hover,
    [data-baseweb="menu"] li:hover,
    li[role="option"]:hover,
    div[role="option"]:hover,
    [data-baseweb="list-item"]:hover {
        background-color: rgba(16, 185, 129, 0.1) !important;
        color: var(--gray-900) !important;
    }

    /* Selected option */
    ul[role="listbox"] li[aria-selected="true"],
    [data-baseweb="menu"] li[aria-selected="true"],
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background-color: rgba(16, 185, 129, 0.15) !important;
        color: var(--gray-900) !important;
        font-weight: 600 !important;
    }

    /* All text inside options */
    ul[role="listbox"] *,
    [data-baseweb="menu"] *,
    li[role="option"] *,
    div[role="option"] * {
        color: var(--gray-900) !important;
    }

    /* Selectbox input field text color */
    [data-baseweb="select"] input {
        color: var(--gray-900) !important;
    }

    /* Override any inherited dark colors */
    .stSelectbox * {
        color: var(--gray-900) !important;
    }

    [data-baseweb="popover"] * {
        color: var(--gray-900) !important;
    }
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
        "success": '<svg style="width: 14px; height: 14px; display: inline-block; vertical-align: middle;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        "warning": '<svg style="width: 14px; height: 14px; display: inline-block; vertical-align: middle;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>',
        "error": '<svg style="width: 14px; height: 14px; display: inline-block; vertical-align: middle;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>',
        "info": '<svg style="width: 14px; height: 14px; display: inline-block; vertical-align: middle;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>'
    }

    colors = {
        "success": {"bg": "#F0FDF4", "border": "#86EFAC", "text": "#166534"},
        "warning": {"bg": "#FFFBEB", "border": "#FCD34D", "text": "#92400E"},
        "error": {"bg": "#FEF2F2", "border": "#FCA5A5", "text": "#991B1B"},
        "info": {"bg": "#EFF6FF", "border": "#93C5FD", "text": "#1E40AF"}
    }

    color = colors.get(status, colors["info"])
    icon = icons.get(status, "")

    return f'''
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8125rem;
        font-weight: 500;
        border: 1px solid {color['border']};
        background: {color['bg']};
        color: {color['text']};
        margin-bottom: 0.5rem;
        width: 100%;
    ">
        {icon}
        <span>{text}</span>
    </div>
    '''


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
