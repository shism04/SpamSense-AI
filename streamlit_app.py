import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from sentence_transformers import SentenceTransformer
from emailProcessor import EmailProcessor

# ───────────────── CONFIG ─────────────────
st.set_page_config(
    page_title="SpamSense AI",
    page_icon="📧",
    layout="wide"
)

COLORS = {
    "SPAM": "#FF3860",
    "HAM": "#23D160",
    "PRIMARY": "#3475B3"
}

# ───────────────── STYLES ─────────────────
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border-left: 6px solid var(--accent);
}
.kpi-label {
    font-size: 0.9rem;
    color: #6b7280;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #111827;
}
.center-table {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

def kpi_card(label, value, accent):
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{accent}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ───────────────── MODELS ─────────────────
@st.cache_resource
def load_assets():
    spam_model = joblib.load("model/spam_model.pkl")
    emb_model = SentenceTransformer(
        "all-mpnet-base-v2",
        cache_folder="./model_cache"
    )
    return spam_model, emb_model

spam_model, emb_model = load_assets()
processor = EmailProcessor(emb_model)

# ───────────────── DASHBOARD ─────────────────
def render_dashboard(batch_df, features_df):
    st.markdown(
        "<h2 style='margin-bottom: 30px;'>Overview</h2>",
        unsafe_allow_html=True
    )

    total = len(batch_df)
    spam = (batch_df["label"] == "SPAM").sum()
    ham = total - spam
    avg_conf = batch_df["confidence"].mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Emails Analyzed", total, COLORS["PRIMARY"])
    with c2: kpi_card("Spam Detected", spam, COLORS["SPAM"])
    with c3: kpi_card("Legitimate Emails", ham, COLORS["HAM"])
    with c4: kpi_card("Avg Model Confidence", f"{avg_conf:.1f}%", COLORS["PRIMARY"])

    st.divider()

    # ── Distribution ─────────────────────────
    c1, c2 = st.columns([1, 2])

    with c1:
        fig = px.pie(
            batch_df,
            names="label",
            hole=0.55,
            color="label",
            color_discrete_map=COLORS,
            title="Spam vs Legitimate Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### Email Classification Results")

        table_df = batch_df.copy()
        table_df["confidence"] = (table_df["confidence"] * 100).round(2).astype(str) + "%"

        st.markdown("<div class='center-table'>", unsafe_allow_html=True)
        st.dataframe(table_df, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ── Header Anomaly Indicators & Subject length vs Model confidence ─────────────
    c1, c2 = st.columns([1, 2])
    with c1:
        anomaly_cols = [
            "from_returnpath_match",
            "reply_to_differs_from_from",
            "message_id_missing",
            "message_id_is_random"
        ]

        anomaly_df = features_df[anomaly_cols].mean().reset_index()
        anomaly_df.columns = ["Indicator", "Activation Rate"]

        fig = px.bar(
            anomaly_df,
            x="Activation Rate",
            y="Indicator",
            orientation="h",
            title="Header Anomaly Indicators",
            color_discrete_sequence=[COLORS["PRIMARY"]]
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.scatter(
            batch_df,
            x="subject_length",
            y="confidence",
            color="label",
            color_discrete_map=COLORS,
            title="Subject Length vs Model Confidence"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()

    # ── Routing & Content ─────────────────────
    c1, c2 = st.columns(2)

    with c1:
        routing_df = features_df[
            ["num_received_headers", "received_first_ip_is_private"]
        ].mean().reset_index()
        routing_df.columns = ["Signal", "Average"]

        fig = px.bar(
            routing_df,
            x="Average",
            y="Signal",
            orientation="h",
            title="Routing Suspicion Signals",
            color_discrete_sequence=[COLORS["PRIMARY"]]
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        content_df = features_df[["is_html", "is_multipart"]].mean().reset_index()
        content_df.columns = ["Content Type", "Usage Rate"]

        fig = px.bar(
            content_df,
            x="Content Type",
            y="Usage Rate",
            title="Content Structure Usage",
            color_discrete_sequence=[COLORS["PRIMARY"]]
        )
        st.plotly_chart(fig, use_container_width=True)

# ───────────────── UI ─────────────────
# _____________SIDEBAR INSTRUCTIONS______________
with st.sidebar:
    st.header("Instructions")
    st.info("""
    **How to get Raw Source:**
    1. Open email in Gmail/Outlook.
    2. Click 'More' (three dots).
    3. Select 'Show Original' or 'View Message Source'.
    4. Copy the entire text or download the .eml file.
    """)

# ───────── HERO SECTION ─────────
c1, c2 = st.columns(2)

with c1:
    st.markdown(
        """
        <div style="justify-content:center; text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 3rem; font-weight: 700; color:white;">SpamSense AI 📧</h1>
            <p style="font-size: 1.2rem; color:#4b5563; max-width:700px; margin:auto;">
                SpamSense AI is an intelligent email forensic tool that detects SPAM and analyzes emails in detail.
                It uses advanced machine learning and semantic embeddings to identify suspicious patterns in headers and content.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.image("images/spamsense_ai_2.png", width="content")

tab1, tab2 = st.tabs(["Single Email", "Batch Analysis"])

# ── SINGLE EMAIL ───────────────────────
with tab1:
    st.markdown("### Manual Email Inspection")

    raw = st.text_area(
        "Paste full RFC 822 raw source:",
        height=280
    )

    if st.button("Analyze Email"):
        if not raw.strip():
            st.warning("Please paste email content.")
        else:
            with st.spinner("Analyzing email…"):
                df = processor.transform_raw_email(raw)
                pred = spam_model.predict(df)[0]
                prob = spam_model.predict_proba(df)[0][pred]

            st.divider()
            if pred == 1:
                st.error(f"SPAM DETECTED — Confidence {prob:.2%}")
            else:
                st.success(f"LEGITIMATE EMAIL — Confidence {prob:.2%}")

# ── BATCH ANALYSIS ─────────────────────
with tab2:
    uploaded = st.file_uploader(
        "Upload raw email files",
        accept_multiple_files=True
    )

    if st.button("Generate Forensic Report") and uploaded:
        results = []
        all_features = []

        with st.spinner("Processing batch…"):
            for f in uploaded:
                content = f.getvalue().decode(
                    "utf-8",
                    errors="replace"
                ).replace("\r\n", "\n")

                f_df = processor.transform_raw_email(content)
                pred = spam_model.predict(f_df)[0]
                prob = spam_model.predict_proba(f_df)[0][pred]

                results.append({
                    "name": f.name,
                    "label": "SPAM" if pred else "HAM",
                    "confidence": prob,
                    "subject_length": f_df["subject_length"].iloc[0]
                })

                all_features.append(f_df)

        render_dashboard(
            pd.DataFrame(results),
            pd.concat(all_features, ignore_index=True)
        )
