#!/usr/bin/env python3
"""
Test script for CivicGPT AI engine components.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all AI engine modules can be imported."""
    try:
        # Test core imports
        from config.settings import settings
        from utils.logger import get_logger
        from utils.text_processor import text_processor
        
        # Test AI engine imports
        from services.openai_client import OpenAIClient
        from services.sentiment_analyzer import SentimentAnalyzer
        from services.prompting.templates import PromptTemplates, AnalysisType
        
        print("✅ All AI engine modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_sentiment_analyzer():
    """Test sentiment analysis functionality."""
    try:
        from services.sentiment_analyzer import analyze_sentiment
        
        # Test sentiment analysis
        test_text = "I love this amazing product! It's fantastic!"
        result = analyze_sentiment(test_text)
        
        print(f"✅ Sentiment analysis works: {result['sentiment']} (confidence: {result['confidence']:.2f})")
        return True
    except Exception as e:
        print(f"❌ Sentiment analysis test failed: {e}")
        return False


def test_prompt_templates():
    """Test prompt template system."""
    try:
        from services.prompting.templates import PromptTemplates, AnalysisType
        
        # Test prompt generation
        test_text = "This is a test post"
        prompt = PromptTemplates.get_comprehensive_analysis_prompt(test_text)
        
        print(f"✅ Prompt templates work: Generated {len(prompt)} character prompt")
        return True
    except Exception as e:
        print(f"❌ Prompt templates test failed: {e}")
        return False


def test_openai_client():
    """Test OpenAI client structure."""
    try:
        from services.openai_client import OpenAIClient
        
        # Test client initialization
        client = OpenAIClient()
        
        print(f"✅ OpenAI client initialized with model: {client.model}")
        return True
    except Exception as e:
        print(f"❌ OpenAI client test failed: {e}")
        return False


def main():
    """Run all AI engine tests."""
    print("🧪 Testing CivicGPT AI Engine")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Sentiment Analyzer Test", test_sentiment_analyzer),
        ("Prompt Templates Test", test_prompt_templates),
        ("OpenAI Client Test", test_openai_client)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All AI engine tests passed!")
        print("\n🚀 Ready for Stage 4: Frontend Development")
        return True
    else:
        print("⚠️  Some tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 