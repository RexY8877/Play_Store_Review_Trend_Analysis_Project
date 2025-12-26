import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from trend_orchestrator import TrendAnalysisOrchestrator
from config import Config

# App Header
st.set_page_config(page_title="Review Trend Analyzer", layout="wide")
st.title("📊 Play Store Review Trend Analysis")
st.markdown("---")

# Sidebar Configuration
st.sidebar.header("Settings")
app_id = st.sidebar.text_input("App ID", value=Config.APP_ID)
days = st.sidebar.slider("Analysis Period (Days)", 7, 30, 14)

# Analysis Trigger
if st.sidebar.button("Run Live Analysis"):
    with st.spinner("🔄 Fetching and analyzing reviews..."):
        orchestrator = TrendAnalysisOrchestrator()
        target_date = datetime.now()
        
        # We simulate the batch process using your existing logic
        report = orchestrator.generate_trend_report(target_date)
        
        if report is not None and not report.empty:
            # 1. Main Metrics
            col1, col2 = st.columns(2)
            top_issue = report.groupby('topic')['frequency'].sum().idxmax()
            col1.metric("Top Issue", top_issue)
            col2.metric("Total Reviews Processed", report['frequency'].sum())

            # 2. The Graph (Aesthetic Blue Trendline)
            st.subheader("📈 Issue Frequency Over Time")
            # Pivot data for the chart
            chart_data = report.pivot(index='date', columns='topic', values='frequency').fillna(0)
            st.line_chart(chart_data)

            # 3. Data Table
            st.subheader("📝 Detailed Breakdown")
            st.dataframe(report, use_container_width=True)
            
            # 4. Download Option
            csv = report.to_csv(index=False).encode('utf-8')
            st.download_button("Download Report (CSV)", csv, "trend_report.csv", "text/csv")
        else:
            st.error("No data found to generate a report.")