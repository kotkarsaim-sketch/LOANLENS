"""
config.py - Application configuration, design themes, and styling constants
Features light background with navy-blue accents and subtle teal highlights.
"""

APP_NAME = "LoanLens"
APP_TAGLINE = "Smart Loan Comparison & Financial Intelligence Platform"
APP_VERSION = "v1.0 (Academic Edition)"

# Color Palette
COLORS = {
    "navy_primary": "#0F2744",      # Deep Navy
    "navy_secondary": "#1E3A8A",    # Rich Royal Navy
    "navy_dark": "#0A192F",         # Darkest Navy
    "teal_primary": "#0D9488",      # Vibrant Teal
    "teal_light": "#14B8A6",        # Light Teal
    "teal_accent": "#06B6D4",       # Electric Cyan/Teal
    "teal_bg": "#F0FDFA",           # Very soft teal tint
    "bg_light": "#F8FAFC",          # Slate Light Neutral
    "card_bg": "#FFFFFF",           # Crisp White
    "card_border": "#E2E8F0",       # Clean subtle border
    "text_main": "#0F172A",         # Slate 900
    "text_muted": "#64748B",        # Slate 500
    "success": "#10B981",           # Emerald Green
    "warning": "#F59E0B",           # Amber
    "danger": "#EF4444",            # Crimson / Red
    "chart_palette": ["#0D9488", "#1E3A8A", "#F59E0B", "#8B5CF6", "#EC4899", "#10B981"]
}

CUSTOM_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
        background-color: #F8FAFC;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1280px;
    }

    /* Top App Header Banner */
    .app-header {
        background: linear-gradient(135deg, #0A192F 0%, #0F2744 60%, #0D9488 100%);
        padding: 1.75rem 2rem;
        border-radius: 16px;
        color: #FFFFFF;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 39, 68, 0.15), 0 8px 10px -6px rgba(15, 39, 68, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .app-header h1 {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
        color: #FFFFFF;
    }

    .app-header p {
        margin: 0.35rem 0 0 0;
        color: #94A3B8;
        font-size: 0.95rem;
    }

    .app-badge {
        background: rgba(13, 148, 136, 0.25);
        border: 1px solid rgba(20, 184, 166, 0.4);
        color: #5EEAD4;
        padding: 0.4rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Metric Card Styling */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.07);
    }

    .metric-card .label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.35rem;
    }

    .metric-card .value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0F2744;
        font-family: 'Plus Jakarta Sans', sans-serif;
        line-height: 1.2;
    }

    .metric-card .subtext {
        font-size: 0.82rem;
        color: #0D9488;
        font-weight: 600;
        margin-top: 0.35rem;
    }

    /* Winner Banner Card */
    .winner-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #F0FDFA 100%);
        border: 1.5px solid #10B981;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.08);
    }

    .winner-tag {
        display: inline-flex;
        align-items: center;
        background: #10B981;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    /* Standard Card Container */
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F2744;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .card-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1rem;
    }

    /* Comparison Head-to-Head Table */
    .fin-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }

    .fin-table th {
        background-color: #0F2744;
        color: #FFFFFF;
        text-align: left;
        padding: 0.75rem 1rem;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .fin-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #E2E8F0;
        color: #1E293B;
    }

    .fin-table tr:hover {
        background-color: #F1F5F9;
    }

    .fin-table .highlight {
        font-weight: 700;
        color: #0D9488;
    }

    /* Streamlit Widget Customization */
    div[data-testid="stSidebar"] {
        background-color: #0A192F;
        border-right: 1px solid #1E293B;
    }

    div[data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    div[data-testid="stSidebar"] .stSelectbox label,
    div[data-testid="stSidebar"] .stRadio label,
    div[data-testid="stSidebar"] .stSlider label {
        color: #94A3B8 !important;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0F2744;
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 0.55rem 1.25rem;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #0D9488;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25);
    }

    /* Info Callouts */
    .info-callout {
        background-color: #F0FDFA;
        border-left: 4px solid #0D9488;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
        font-size: 0.875rem;
        color: #0F766E;
    }

    .info-callout strong {
        color: #115E59;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 0.9rem;
        color: #64748B;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #F8FAFC !important;
        color: #0F2744 !important;
        border-bottom: 3px solid #0D9488 !important;
    }
</style>
"""
