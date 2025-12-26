"""
Configuration settings for Play Store Trend Analyzer
"""
import os

class Config:
    """Configuration settings"""
    
    # App settings
    APP_ID = "in.swiggy.android"
    COUNTRY = "in"
    LANGUAGE = "en"
    
    # Processing settings
    LOOKBACK_DAYS = 30
    MAX_REVIEWS_PER_DAY = 50
    MIN_TOPIC_FREQUENCY = 2
    
    # Topic settings
    SEED_TOPICS = [
        
        "App crashing", "Slow performance", "Login issue", 
        "Battery drain", "User interface", "Account hacked",
        "Payment failure", "Update bug", "Notification issue",
        "Customer support", "Feature request", "Ads annoying"
    ]
    
    
    # Output settings
    OUTPUT_DIR = "./output"
    REPORTS_DIR = "./output/reports"
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories"""
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        os.makedirs("./data", exist_ok=True)