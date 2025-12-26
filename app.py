import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from trend_orchestrator import TrendAnalysisOrchestrator
from mock_data import MockDataGenerator
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
    with st.spinner("🔄 Generating data and analyzing trends..."):
        # 1. Initialize your components
        orchestrator = TrendAnalysisOrchestrator()
        data_generator = MockDataGenerator()
        
        target_date = datetime.now()
        start_date = target_date - timedelta(days=days)
        
        # 2. Process reviews day-by-day (matching your assignment logic)
        current_date = start_date
        while current_date <= target_date:
            reviews = data_generator.generate_daily_reviews(current_date, 50)
            orchestrator.process_daily_batch(reviews, current_date)
            current_date += timedelta(days=1)
        
        # 3. Generate the final report
        report = orchestrator.generate_trend_report(target_date)
        
        if report is not None and not report.empty:
            st.success("Analysis Complete!")
            
            # 4. Main Metrics (Corrected Logic)
            col1, col2 = st.columns(2)
            
            # In your code, topics are the Index. We sum across columns (dates)
            total_mentions_per_topic = report.sum(axis=1)
            top_issue = total_mentions_per_topic.idxmax() # Finds topic with highest sum
            total_mentions = total_mentions_per_topic.sum()

            col1.metric("Top Issue Tracked", top_issue)
            col2.metric("Total Mentions Found", int(total_mentions))

            # 5. The Graph (Aesthetic Blue Trendline)
            st.subheader("📈 Issue Frequency Over Time")
            # We transpose (.T) so Dates are on the bottom and Topics are in the legend
            st.line_chart(report.T)

            # 6. Detailed Data Table
            st.subheader("📝 Detailed Data Breakdown")
            st.dataframe(report, use_container_width=True)
            
            # 7. Download Option
            csv = report.to_csv().encode('utf-8')
            st.download_button("Download Full Report (CSV)", csv, "trend_report.csv", "text/csv")
        else:
            st.error("No data found to generate a report.")