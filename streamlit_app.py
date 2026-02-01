import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sentence_transformers import SentenceTransformer
from emailProcessor import EmailProcessor

# Importar módulos de estilos y componentes
from styles import COLORS, apply_custom_styles
from components import metric_card, result_card_html, hero_banner, sidebar_info

# ───────────────── CONFIG ─────────────────
st.set_page_config(
    page_title="SpamSense AI",
    page_icon="📧",
    layout="wide"
)

# Aplicar estilos personalizados
apply_custom_styles()

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
    st.markdown("## 📊 Forensic Analysis Dashboard")
    st.markdown("---")

    # KPIs
    total = len(batch_df)
    spam = (batch_df["label"] == "SPAM").sum()
    ham = total - spam
    avg_conf = batch_df["confidence"].mean()
    spam_rate = (spam / total * 100) if total > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_card("Total Emails", total, COLORS["PRIMARY"], "📧")
    with col2:
        metric_card("Spam Detected", spam, COLORS["SPAM"], "⚠️")
    with col3:
        metric_card("Legitimate", ham, COLORS["HAM"], "✅")
    with col4:
        metric_card("Spam Rate", f"{spam_rate:.1f}%", COLORS["ACCENT"], "📈")
    with col5:
        metric_card("Avg Confidence", f"{avg_conf:.1%}", COLORS["SECONDARY"], "🎯")

    st.markdown("---")

    # Visualizaciones principales
    col1, col2 = st.columns([1, 1])

    with col1:
        # Pie chart mejorado
        fig = go.Figure(data=[go.Pie(
            labels=batch_df['label'].value_counts().index,
            values=batch_df['label'].value_counts().values,
            hole=0.6,
            marker=dict(colors=[COLORS["HAM"], COLORS["SPAM"]]),
            textinfo='label+percent',
            textfont=dict(size=14, color='white', family='Inter'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(
                text="<b>Email Classification Distribution</b>",
                font=dict(size=18, color='#1E293B', family='Inter')
            ),
            showlegend=True,
            legend=dict(font=dict(size=13, color='#1E293B')),
            height=350,
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Histograma de confianza
        fig = go.Figure()
        
        spam_data = batch_df[batch_df['label'] == 'SPAM']['confidence']
        ham_data = batch_df[batch_df['label'] == 'HAM']['confidence']
        
        fig.add_trace(go.Histogram(
            x=spam_data,
            name='SPAM',
            marker_color=COLORS["SPAM"],
            opacity=0.7,
            nbinsx=20
        ))
        
        fig.add_trace(go.Histogram(
            x=ham_data,
            name='HAM',
            marker_color=COLORS["HAM"],
            opacity=0.7,
            nbinsx=20
        ))
        
        fig.update_layout(
            title=dict(
                text="<b>Confidence Score Distribution</b>",
                font=dict(size=18, color='#1E293B', family='Inter')
            ),
            xaxis=dict(
                title=dict(text="<b>Confidence Score</b>", font=dict(size=14, color='#1E293B')),
                tickfont=dict(size=12, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            yaxis=dict(
                title=dict(text="<b>Count</b>", font=dict(size=14, color='#1E293B')),
                tickfont=dict(size=12, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            barmode='overlay',
            height=350,
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend=dict(font=dict(size=13, color='#1E293B'))
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Tabla de resultados mejorada
    st.markdown("### 📋 Detailed Results")
    
    display_df = batch_df.copy()
    display_df['confidence'] = (display_df['confidence'] * 100).round(1).astype(str) + '%'
    display_df = display_df.rename(columns={
        'name': 'Email File',
        'label': 'Classification',
        'confidence': 'Confidence',
        'subject_length': 'Subject Length'
    })
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Classification": st.column_config.TextColumn(
                "Classification",
                help="Email classification result"
            ),
            "Confidence": st.column_config.TextColumn(
                "Confidence",
                help="Model confidence score"
            )
        }
    )

    st.markdown("---")

    # Análisis avanzado
    col1, col2 = st.columns(2)

    with col1:
        # Scatter plot mejorado
        fig = px.scatter(
            batch_df,
            x='subject_length',
            y='confidence',
            color='label',
            color_discrete_map={"SPAM": COLORS["SPAM"], "HAM": COLORS["HAM"]},
            size=[10]*len(batch_df),
            title="<b>Subject Length vs Confidence</b>"
        )
        
        fig.update_layout(
            title=dict(font=dict(size=18, color='#1E293B', family='Inter')),
            xaxis=dict(
                title=dict(text="<b>Subject Length (characters)</b>", font=dict(size=14, color='#1E293B')),
                tickfont=dict(size=12, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            yaxis=dict(
                title=dict(text="<b>Confidence Score</b>", font=dict(size=14, color='#1E293B')),
                tickfont=dict(size=12, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend=dict(
                title=dict(text="<b>Classification</b>", font=dict(size=13, color='#1E293B')),
                font=dict(size=12, color='#1E293B')
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Box plot de confianza por categoría
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=batch_df[batch_df['label'] == 'SPAM']['confidence'],
            name='SPAM',
            marker_color=COLORS["SPAM"],
            boxmean='sd'
        ))
        
        fig.add_trace(go.Box(
            y=batch_df[batch_df['label'] == 'HAM']['confidence'],
            name='HAM',
            marker_color=COLORS["HAM"],
            boxmean='sd'
        ))
        
        fig.update_layout(
            title=dict(
                text="<b>Confidence Distribution by Category</b>",
                font=dict(size=18, color='#1E293B', family='Inter')
            ),
            xaxis=dict(
                tickfont=dict(size=12, color='#334155'),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text="<b>Confidence Score</b>", font=dict(size=14, color='#1E293B')),
                tickfont=dict(size=12, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend=dict(font=dict(size=12, color='#1E293B'))
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Análisis de características técnicas
    st.markdown("### 🔍 Technical Feature Analysis")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        # Anomalías de headers
        anomaly_data = {
            'Return-Path Mismatch': features_df['from_returnpath_match'].mean(),
            'Reply-To Differs': features_df['reply_to_differs_from_from'].mean(),
            'Missing Message-ID': features_df['message_id_missing'].mean(),
            'Random Message-ID': features_df['message_id_is_random'].mean()
        }
        
        fig = go.Figure(data=[go.Bar(
            x=list(anomaly_data.values()),
            y=list(anomaly_data.keys()),
            orientation='h',
            marker=dict(color=COLORS["ACCENT"]),
            text=[f'{v:.2%}' for v in anomaly_data.values()],
            textposition='outside',
            textfont=dict(size=11, color='#1E293B')
        )])
        
        fig.update_layout(
            title=dict(
                text="<b>Header Anomalies</b>",
                font=dict(size=16, color='#1E293B', family='Inter')
            ),
            xaxis=dict(
                title=dict(text="<b>Detection Rate</b>", font=dict(size=13, color='#1E293B')),
                tickfont=dict(size=11, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            yaxis=dict(
                tickfont=dict(size=11, color='#334155'),
                showgrid=False
            ),
            height=300,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Routing signals
        routing_data = pd.DataFrame({
            'Metric': ['Avg Received Headers', 'Private IP Rate'],
            'Value': [
                features_df['num_received_headers'].mean(),
                features_df['received_first_ip_is_private'].mean()
            ]
        })
        
        fig = go.Figure(data=[go.Bar(
            x=routing_data['Metric'],
            y=routing_data['Value'],
            marker=dict(color=COLORS["SECONDARY"]),
            text=[f'{v:.2f}' for v in routing_data['Value']],
            textposition='outside',
            textfont=dict(size=11, color='#1E293B')
        )])
        
        fig.update_layout(
            title=dict(
                text="<b>Routing Indicators</b>",
                font=dict(size=16, color='#1E293B', family='Inter')
            ),
            xaxis=dict(
                tickfont=dict(size=11, color='#334155'),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text="<b>Average Value</b>", font=dict(size=13, color='#1E293B')),
                tickfont=dict(size=11, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            height=300,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        # Content structure
        content_data = pd.DataFrame({
            'Type': ['HTML Content', 'Multipart Content'],
            'Percentage': [
                features_df['is_html'].mean() * 100,
                features_df['is_multipart'].mean() * 100
            ]
        })
        
        fig = go.Figure(data=[go.Bar(
            x=content_data['Type'],
            y=content_data['Percentage'],
            marker=dict(color=COLORS["PRIMARY"]),
            text=[f'{v:.1f}%' for v in content_data['Percentage']],
            textposition='outside',
            textfont=dict(size=11, color='#1E293B')
        )])
        
        fig.update_layout(
            title=dict(
                text="<b>Content Structure</b>",
                font=dict(size=16, color='#1E293B', family='Inter')
            ),
            xaxis=dict(
                tickfont=dict(size=11, color='#334155'),
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text="<b>Usage Rate (%)</b>", font=dict(size=13, color='#1E293B')),
                tickfont=dict(size=11, color='#334155'),
                gridcolor='#E2E8F0',
                showgrid=True
            ),
            height=300,
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

# ───────────────── UI ─────────────────
# Sidebar
with st.sidebar:
    sidebar_info()

# Hero Banner con imagen
hero_banner()

# Tabs principales
tab1, tab2 = st.tabs(["🔍 Single Email Analysis", "📊 Batch Analysis"])

# ── SINGLE EMAIL ───────────────────────
with tab1:
    st.markdown("### Analyze Individual Email")
    st.markdown("Paste the complete RFC 822 raw source of the email below:")

    raw = st.text_area(
        "Email Raw Source",
        height=300,
        placeholder="Paste email headers and body here...",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        analyze_btn = st.button("🔍 Analyze Email", use_container_width=True, type="primary")

    if analyze_btn:
        if not raw.strip():
            st.warning("⚠️ Please paste email content before analyzing.")
        else:
            with st.spinner("🔄 Analyzing email..."):
                try:
                    df = processor.transform_raw_email(raw)
                    pred = spam_model.predict(df)[0]
                    prob = spam_model.predict_proba(df)[0][pred]

                    label = "SPAM" if pred == 1 else "HAM"
                    color = COLORS["SPAM"] if pred == 1 else COLORS["HAM"]
                    
                    st.markdown("---")
                    st.markdown(result_card_html(label, prob, color), unsafe_allow_html=True)
                    
                    with st.expander("📋 View Technical Details"):
                        st.dataframe(df.T, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"❌ Error analyzing email: {str(e)}")

# ── BATCH ANALYSIS ─────────────────────
with tab2:
    st.markdown("### Batch Email Analysis")
    st.markdown("Upload multiple .eml or .txt files for comprehensive analysis:")

    uploaded = st.file_uploader(
        "Upload Email Files",
        accept_multiple_files=True,
        type=['eml', 'txt'],
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        process_btn = st.button("📊 Generate Report", use_container_width=True, type="primary", disabled=not uploaded)

    if process_btn and uploaded:
        results = []
        all_features = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, f in enumerate(uploaded):
            status_text.text(f"Processing {idx + 1}/{len(uploaded)}: {f.name}")
            progress_bar.progress((idx + 1) / len(uploaded))

            try:
                content = f.getvalue().decode("utf-8", errors="replace").replace("\r\n", "\n")
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
            except Exception as e:
                st.warning(f"⚠️ Error processing {f.name}: {str(e)}")

        progress_bar.empty()
        status_text.empty()

        if results:
            st.success(f"✅ Successfully processed {len(results)} emails!")
            st.markdown("---")
            render_dashboard(
                pd.DataFrame(results),
                pd.concat(all_features, ignore_index=True)
            )
        else:
            st.error("❌ No emails were successfully processed.")
