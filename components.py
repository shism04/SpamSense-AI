"""
Componentes visuales para SpamSense AI
Funciones reutilizables para elementos de la UI
"""

import streamlit as st
from styles import COLORS


def metric_card(label, value, accent_color, icon="📊"):
    """
    Renderiza una tarjeta de métrica moderna
    
    Args:
        label: Etiqueta de la métrica
        value: Valor a mostrar
        accent_color: Color de acento
        icon: Emoji o ícono
    """
    st.markdown(
        f"""
        <div class="metric-card" style="--accent-color: {accent_color}">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def result_card_html(label, confidence, color):
    """
    Genera HTML para la tarjeta de resultado de análisis
    
    Args:
        label: SPAM o HAM
        confidence: Score de confianza (0-1)
        color: Color del borde
        
    Returns:
        String HTML del componente
    """
    badge_color = COLORS["SPAM"] if label == "SPAM" else COLORS["HAM"]
    badge_shadow = "rgba(220, 38, 38, 0.3)" if label == "SPAM" else "rgba(5, 150, 105, 0.3)"
    status_text = "⚠️ SPAM DETECTED" if label == "SPAM" else "✅ LEGITIMATE EMAIL"
    
    return f"""
    <div class="result-card" style="--result-color: {color}">
        <h3 style="margin: 0 0 1.5rem 0; color: #1E293B;">🔍 Analysis Result</h3>
        <div style="margin-bottom: 1rem;">
            <span class="result-badge" style="--badge-color: {badge_color}; --badge-shadow: {badge_shadow}">
                {status_text}
            </span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1.5rem; padding: 1.5rem; background: #F8FAFC; border-radius: 12px;">
            <div>
                <div style="font-size: 0.875rem; color: #64748B; font-weight: 600; margin-bottom: 0.5rem;">CLASSIFICATION</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {badge_color};">{label}</div>
            </div>
            <div>
                <div style="font-size: 0.875rem; color: #64748B; font-weight: 600; margin-bottom: 0.5rem;">CONFIDENCE SCORE</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1E293B;">{confidence:.1%}</div>
            </div>
        </div>
        <div class="confidence-bar-container">
            <div class="confidence-bar-fill" style="width: {confidence*100}%; --bar-color: {badge_color};"></div>
        </div>
    </div>
    """


def hero_section():
    """Renderiza la sección hero del dashboard"""
    st.markdown("""
    <div class="hero-gradient">
        <div class="hero-title">🛡️ SpamSense AI</div>
        <div class="hero-subtitle">
            Advanced Email Forensic Intelligence Platform<br/>
            Powered by Machine Learning & Semantic Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)


def hero_banner():
    """Renderiza el banner hero con imagen"""
    import streamlit as st
    try:
        # Contenedor centrado para la imagen
        col1, col2, col3 = st.columns([0.5, 4, 0.5])
        with col2:
            st.image("images/spamsense_banner.jpg", use_container_width=True)
    except:
        # Fallback si no existe la imagen
        st.markdown("""
        <div class="hero-gradient">
            <div class="hero-title">🛡️ SpamSense AI</div>
            <div class="hero-subtitle">
                Advanced Email Forensic Intelligence Platform<br/>
                Powered by Machine Learning & Semantic Analysis
            </div>
        </div>
        """, unsafe_allow_html=True)


def sidebar_info():
    """Renderiza información en el sidebar"""
    with st.sidebar:
        # Instructions Section
        st.markdown(
            """
            <h3 style="color: #FFFFFF;">📖 Instructions</h3>
            <div class="info-card">
                <strong>How to get Raw Email Source:</strong><br><br>
                1. Open email in Gmail/Outlook<br>
                2. Click 'More' (⋮) menu<br>
                3. Select 'Show Original' or 'View Source'<br>
                4. Copy entire text or download .eml<br>
                5. Paste here or upload file
            </div>
            """,
            unsafe_allow_html=True
        )

        # About Section
        st.markdown(
            """
            <h3 style="color: #FFFFFF;">ℹ️ About</h3>
            <div class="info-card">
                <strong>SpamSense AI</strong> uses advanced machine learning and semantic analysis to detect spam with high precision.<br><br>
                <strong>Features:</strong>
                <ul style="margin-left: -20px;">
                    <li>RFC 822 header analysis</li>
                    <li>Semantic evaluation</li>
                    <li>Routing anomaly detection</li>
                    <li>Confidence scoring</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
