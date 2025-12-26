import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from google_play_scraper import app, reviews, Sort
from trend_orchestrator import TrendAnalysisOrchestrator
from config import Config

# --- UI Setup ---
st.set_page_config(page_title="App Insights Pro", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    stMetric { background-color: #1f2937; border-radius: 10px; padding: 15px; }
    </style>
    """, unsafe_allow_index=True)

st.title("🛡️ Universal Play Store Trend Analyzer")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("🔍 Analysis Target")
    target_app_id = st.text_input("Enter Play Store ID (e.g., com.whatsapp)", value="in.swiggy.android")
    lookback = st.slider("Days to Analyze", 7, 30, 14)
    run_btn = st.button("Start Live Analysis", use_container_width=True)

if run_btn:
    try:
        # 1. Fetch App Metadata (Makes it look pro!)
        info = app(target_app_id)
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(info['icon'], width=100)
        with col2:
            st.subheader(info['title'])
            st.write(f"⭐ {info['score']:.1f} | 🏢 {info['developer']}")

        # 2. Live Scraping
        with st.spinner(f"Scraping real reviews for {info['title']}..."):
            # We fetch more than we need to ensure we cover the date range
            result, _ = reviews(
                target_app_id,
                lang='en',
                country='in',
                sort=Sort.NEWEST,
                count=500 
            )
            
            # Convert to DataFrame and fix dates
            df_real = pd.DataFrame(result)
            df_real['at'] = pd.to_datetime(df_real['at'])
            
            # Filter for the selected lookback period
            cutoff_date = datetime.now() - timedelta(days=lookback)
            df_filtered = df_real[df_real['at'] >= cutoff_date]

            # 3. Analyze using your existing Orchestrator logic
            orchestrator = TrendAnalysisOrchestrator()
            
            # Map real reviews to your orchestrator's expected format
            for _, row in df_filtered.iterrows():
                review_obj = {
                    'content': row['content'],
                    'score': row['score'],
                    'at': row['at']
                }
                orchestrator.process_daily_batch([review_obj], row['at'])

            report = orchestrator.generate_trend_report(datetime.now())

            # 4. Visualization (Aesthetic Blue)
            if not report.empty:
                st.markdown("---")
                m1, m2 = st.columns(2)
                m1.metric("Volume Analyzed", len(df_filtered))
                m2.metric("Top Trending Issue", report.sum(axis=1).idxmax())

                st.subheader("📈 Trend Visualization")
                st.line_chart(report.T) # Beautiful blue lines

                st.subheader("📂 Raw Analysis Table")
                st.dataframe(report.style.highlight_max(axis=0, color='#1f2937'))
            else:
                st.warning("No trend patterns found in recent reviews.")

    except Exception as e:
        st.error(f"Error fetching data: {e}. Please check the App ID.")