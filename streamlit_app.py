import streamlit as st
import joblib
import pandas as pd
import email
from sentence_transformers import SentenceTransformer
from emailProcessor import EmailProcessor 

st.set_page_config(page_title="SpamSense AI", page_icon="📧")

@st.cache_resource
def load_assets():
    spam_model = joblib.load('model/spam_model.pkl')
    emb_model = SentenceTransformer(
                "all-mpnet-base-v2",
                cache_folder="./model_cache"
            )
    return spam_model, emb_model


try:
    spam_model, emb_model = load_assets()
except Exception as e:
    st.error("Model file 'spam_model.pkl' not found. Please ensure it is in the app directory.")
    st.stop()

# Initialize the email processor class
processor = EmailProcessor(emb_model)

# --- SIDEBAR INSTRUCTIONS ---
with st.sidebar:
    st.header("Instructions")
    st.info("""
    **How to get Raw Source:**
    1. Open email in Gmail/Outlook.
    2. Click 'More' (three dots).
    3. Select 'Show Original' or 'View Message Source'.
    4. Copy the entire text or download the .eml file.
    """)

# --- MAIN UI ---
st.title("SpanSense AI: Raw Email Classifier")
st.markdown("Analyze email integrity using deep header and body parsing.")

tab1, tab2 = st.tabs(["Paste Raw Text", "Upload .eml File"])

raw_input = ""

with tab1:
    raw_input = st.text_area("Paste the full RFC 822 raw source here:", height=300)
    if st.button("Analyze Email raw text"):
        if raw_input.strip() == "":
            st.warning("Please provide email content first.")
        else:
            with st.spinner("Classifying..."):
                # Process Raw Data
                features_df = processor.transform_raw_email(raw_input)
                
                # Prediction
                prediction = spam_model.predict(features_df)[0]
                
                # Display Results
                st.divider()
                if prediction == 1:
                    st.error("### Result: SPAM DETECTED")
                else:
                    st.success("### Result: LEGITIMATE (HAM)")

with tab2:
    uploaded_files = st.file_uploader("Choose a raw email file", type=['txt', 'eml'], accept_multiple_files="directory")
    if uploaded_files:
        file_raw_input = {uploaded_file.name:uploaded_file.getvalue().decode("utf-8", errors="replace").replace('\r\n', '\n') for uploaded_file in uploaded_files}
        #st.write(file_raw_input)
        
    if st.button("Analyze Email files"):
        for name, raw_input in file_raw_input.items():
            if raw_input.strip() == "":
                st.warning("Please provide email content first.")
            else:
                with st.spinner("Classifying..."):
                    # Process Raw Data
                    features_df = processor.transform_raw_email(raw_input)
                    
                    # Prediction 
                    prediction = spam_model.predict(features_df)[0]
                    
                    # Display Results
                    st.divider()
                    if prediction == 1:
                        st.error(f"{name} is a SPAM")
                    else:
                        st.success(f"{name} is a LEGITIMATE")


