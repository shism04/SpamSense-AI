"""
Estilos CSS para SpamSense AI
Módulo dedicado a la gestión de estilos y tema visual
"""

COLORS = {
    "SPAM": "#DC2626",
    "HAM": "#059669",
    "PRIMARY": "#2563EB",
    "SECONDARY": "#7C3AED",
    "ACCENT": "#F59E0B",
    "BACKGROUND": "#F8FAFC",
    "CARD": "#FFFFFF",
    "TEXT": "#1E293B",
    "TEXT_LIGHT": "#64748B"
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main .block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

/* Hero Banner Image */
[data-testid="stImage"] img {
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    margin-bottom: 2rem;
    max-height: 300px;
    object-fit: cover;
    width: 100%;
}

/* Contenedor de imagen centrado */
.hero-image-container {
    max-width: 1200px;
    margin: 0 auto 2rem auto;
}

/* Títulos con mejor contraste */
h1, h2, h3, h4 {
    color: #1E293B !important;
    font-weight: 700 !important;
}

/* Hero Section */
.hero-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: #FFFFFF !important;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #F1F5F9 !important;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Metric Cards */
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    border-left: 4px solid var(--accent-color);
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.metric-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--accent-color);
    line-height: 1;
}

/* Result Card */
.result-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    border-left: 6px solid var(--result-color);
    margin: 1rem 0;
}

.result-badge {
    display: inline-block;
    padding: 0.5rem 1.5rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1rem;
    color: white;
    background: var(--badge-color);
    box-shadow: 0 4px 12px var(--badge-shadow);
}

.confidence-bar-container {
    background: #E2E8F0;
    height: 12px;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 1rem;
}

.confidence-bar-fill {
    height: 100%;
    background: var(--bar-color);
    border-radius: 10px;
    transition: width 0.6s ease;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: white;
    padding: 0.5rem;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    color: #64748B;
    background: transparent;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 2rem !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3) !important;
}

/* File Uploader */
[data-testid="stFileUploadDropzone"] {
    background: white;
    border: 2px dashed #CBD5E1;
    border-radius: 12px;
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: #667eea;
}

/* Text Area */
textarea {
    border-radius: 8px !important;
    border: 2px solid #E2E8F0 !important;
}

textarea:focus {
    border-color: #667eea !important;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Divider */
hr {
    margin: 2rem 0;
    border-color: #E2E8F0;
}
</style>
"""

def apply_custom_styles():
    """Aplica los estilos personalizados a la aplicación"""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
