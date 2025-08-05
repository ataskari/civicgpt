"""
CivicGPT Frontend - Streamlit Application
"""
import streamlit as st
import requests
import json
import time
from typing import Dict, Any, Optional
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="CivicGPT - Social Media Post Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .risk-low {
        color: #28a745;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .risk-high {
        color: #dc3545;
        font-weight: bold;
    }
    .sentiment-positive {
        color: #28a745;
    }
    .sentiment-negative {
        color: #dc3545;
    }
    .sentiment-neutral {
        color: #6c757d;
    }
    .toxicity-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .suggestion-card {
        background-color: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000"

def check_api_health() -> bool:
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def analyze_post(text: str, platform: str = "twitter") -> Optional[Dict[str, Any]]:
    """Send post for analysis to the API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json={"text": text, "platform": platform},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def display_sentiment_analysis(sentiment: Dict[str, Any]):
    """Display sentiment analysis results."""
    st.subheader("🎭 Sentiment Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sentiment_class = sentiment.get("sentiment", "neutral")
        confidence = sentiment.get("confidence", 0.0)
        
        # Color coding for sentiment
        sentiment_color = {
            "positive": "sentiment-positive",
            "negative": "sentiment-negative", 
            "neutral": "sentiment-neutral"
        }.get(sentiment_class, "sentiment-neutral")
        
        st.metric(
            label="Sentiment",
            value=sentiment_class.title(),
            delta=f"{confidence:.1%} confidence"
        )
    
    with col2:
        score = sentiment.get("score", 0.0)
        st.metric(
            label="Sentiment Score",
            value=f"{score:.2f}",
            delta="(-1 to 1 scale)"
        )
    
    with col3:
        st.metric(
            label="Analysis Time",
            value=f"{sentiment.get('analysis_time', 0):.2f}s"
        )
    
    # Explanation
    explanation = sentiment.get("explanation", "No explanation available.")
    st.info(f"💡 **Explanation:** {explanation}")

def display_toxicity_analysis(toxicity: Dict[str, Any]):
    """Display toxicity analysis results."""
    st.subheader("⚠️ Toxicity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        is_toxic = toxicity.get("is_toxic", False)
        confidence = toxicity.get("confidence", 0.0)
        
        if is_toxic:
            st.error(f"🚨 **TOXIC CONTENT DETECTED** ({confidence:.1%} confidence)")
        else:
            st.success(f"✅ **Content appears safe** ({confidence:.1%} confidence)")
    
    with col2:
        categories = toxicity.get("categories", {})
        if categories:
            st.write("**Toxicity Categories:**")
            for category, score in categories.items():
                if score > 0.3:  # Only show significant scores
                    st.write(f"- {category.title()}: {score:.2f}")
    
    # Explanation
    explanation = toxicity.get("explanation", "No explanation available.")
    if is_toxic:
        st.warning(f"⚠️ **Warning:** {explanation}")
    else:
        st.info(f"💡 **Analysis:** {explanation}")

def display_risk_assessment(overall_risk: str, summary: str):
    """Display overall risk assessment."""
    st.subheader("🎯 Overall Risk Assessment")
    
    risk_colors = {
        "low": "risk-low",
        "medium": "risk-medium", 
        "high": "risk-high"
    }
    
    risk_class = risk_colors.get(overall_risk.lower(), "risk-medium")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Risk Level</h3>
            <p class="{risk_class}">{overall_risk.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write("**Summary:**")
        st.write(summary)

def display_statistics(statistics: Dict[str, Any]):
    """Display text statistics."""
    st.subheader("📊 Text Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Characters", statistics.get("char_count", 0))
    
    with col2:
        st.metric("Words", statistics.get("word_count", 0))
    
    with col3:
        st.metric("Hashtags", statistics.get("hashtag_count", 0))
    
    with col4:
        st.metric("Mentions", statistics.get("mention_count", 0))

def display_suggestions(suggestions: list):
    """Display improvement suggestions."""
    if not suggestions:
        return
    
    st.subheader("💡 Improvement Suggestions")
    
    for i, suggestion in enumerate(suggestions, 1):
        suggestion_type = suggestion.get("type", "general")
        original = suggestion.get("original", "")
        improved = suggestion.get("improved", "")
        reasoning = suggestion.get("reasoning", "")
        
        with st.expander(f"💡 Suggestion {i}: {suggestion_type.title()}"):
            st.write("**Original:**")
            st.code(original)
            st.write("**Improved:**")
            st.code(improved)
            st.write("**Why this helps:**")
            st.write(reasoning)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 CivicGPT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Social Media Post Reviewer</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Platform selection
        platform = st.selectbox(
            "Target Platform",
            ["twitter", "linkedin", "instagram"],
            help="Select the platform you're posting to for platform-specific analysis"
        )
        
        # API health check
        api_healthy = check_api_health()
        if api_healthy:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Not Available")
            st.info("Make sure the backend server is running on port 8000")
        
        st.markdown("---")
        st.markdown("### 📈 Features")
        st.markdown("- 🎭 Sentiment Analysis")
        st.markdown("- ⚠️ Toxicity Detection")
        st.markdown("- 📋 Policy Compliance")
        st.markdown("- 💡 Improvement Suggestions")
        st.markdown("- 📊 Text Statistics")
    
    # Main content
    if not api_healthy:
        st.error("""
        ## 🔌 Backend Not Available
        
        Please start the CivicGPT backend server:
        
        ```bash
        cd civicgpt
        python start_dev.py
        ```
        
        Then select "Start Backend Server" from the menu.
        """)
        return
    
    # Post input
    st.header("📝 Post Analysis")
    
    # Text input
    post_text = st.text_area(
        "Enter your social media post:",
        height=150,
        placeholder="Type or paste your post here...",
        help="Enter the text you want to analyze before posting"
    )
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🔍 Analyze Post",
            type="primary",
            use_container_width=True
        )
    
    # Analysis results
    if analyze_button and post_text.strip():
        with st.spinner("🤖 Analyzing your post..."):
            # Perform analysis
            result = analyze_post(post_text, platform)
            
            if result:
                st.success("✅ Analysis Complete!")
                
                # Display results in tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 Overview", 
                    "🎭 Sentiment", 
                    "⚠️ Toxicity", 
                    "📈 Statistics"
                ])
                
                with tab1:
                    # Overall assessment
                    display_risk_assessment(
                        result.get("overall_risk", "low"),
                        result.get("summary", "Analysis completed.")
                    )
                    
                    # Quick metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        sentiment = result.get("sentiment", {})
                        st.metric(
                            "Sentiment",
                            sentiment.get("sentiment", "neutral").title()
                        )
                    
                    with col2:
                        toxicity = result.get("toxicity", {})
                        is_toxic = toxicity.get("is_toxic", False)
                        st.metric(
                            "Toxicity",
                            "🚨 Toxic" if is_toxic else "✅ Safe"
                        )
                    
                    with col3:
                        analysis_time = result.get("analysis_time", 0)
                        st.metric(
                            "Analysis Time",
                            f"{analysis_time:.2f}s"
                        )
                    
                    # Suggestions
                    suggestions = result.get("suggestions", [])
                    if suggestions:
                        display_suggestions(suggestions)
                
                with tab2:
                    sentiment = result.get("sentiment", {})
                    display_sentiment_analysis(sentiment)
                
                with tab3:
                    toxicity = result.get("toxicity", {})
                    display_toxicity_analysis(toxicity)
                
                with tab4:
                    statistics = result.get("statistics", {})
                    display_statistics(statistics)
    
    elif analyze_button and not post_text.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        <p>🤖 CivicGPT - Your AI-powered social media safety net</p>
        <p>Built with ❤️ using FastAPI, Streamlit, and OpenAI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 