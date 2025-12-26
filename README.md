# 🛡️ Universal Play Store Trend Analyzer

**Live Demo:** [https://play-store-review-trend-analysis-project.onrender.com/]

## 📌 Overview
This is a professional-grade Data Analysis tool that performs real-time trend tracking for any application on the Google Play Store. By scraping live user reviews, the app identifies recurring technical issues, feature requests, and user sentiment patterns to help product teams make data-driven decisions.

## ✨ Key Features
- **Universal Search**: Analyze any app by simply entering its Play Store Package ID.
- **Live Data Scraping**: Fetches the latest reviews directly from Google Play via the `google-play-scraper` API.
- **Automated Trend Detection**: Uses RegEx-based pattern matching to categorize reviews into topics like "App Crashing," "Payment Issues," or "UI/UX Feedback."
- **Interactive Dashboard**: A sleek, dark-themed Streamlit interface featuring dynamic time-series line charts and data tables.
- **Exportable Reports**: Generate and download CSV/Excel reports for offline stakeholder review.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Python-based Web Framework)
- **Data Processing**: Pandas, NumPy
- **Scraping**: Google-Play-Scraper
- **Deployment**: Render

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/RexY8877/Play_Store_Review_Trend_Analysis_Project]

📊 Business Logic
The core engine (trend_orchestrator.py) processes raw review text using an accumulation logic. It calculates the frequency of specific "Seed Topics" over a rolling window (default 14-30 days), allowing developers to see if a bug is getting worse or if a recent update fixed a common complaint.