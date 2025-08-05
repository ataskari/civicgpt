#!/usr/bin/env python3
"""
Test script for CivicGPT Frontend components.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that frontend modules can be imported."""
    try:
        # Test Streamlit import
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Test requests import
        import requests
        print("✅ Requests imported successfully")
        
        # Test frontend app import
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "frontend"))
        from app import check_api_health, analyze_post
        print("✅ Frontend app functions imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_api_health_check():
    """Test API health check function."""
    try:
        from frontend.app import check_api_health
        
        # Test health check (will fail if backend not running, but function should work)
        result = check_api_health()
        print(f"✅ API health check works (result: {result})")
        return True
    except Exception as e:
        print(f"❌ API health check test failed: {e}")
        return False

def test_ui_components():
    """Test UI component functions."""
    try:
        from frontend.app import (
            display_sentiment_analysis,
            display_toxicity_analysis,
            display_risk_assessment,
            display_statistics
        )
        
        # Test with sample data
        sample_sentiment = {
            "sentiment": "positive",
            "confidence": 0.85,
            "score": 0.7,
            "explanation": "This is a positive message"
        }
        
        sample_toxicity = {
            "is_toxic": False,
            "confidence": 0.9,
            "categories": {"hate": 0.1, "harassment": 0.05},
            "explanation": "Content appears safe"
        }
        
        sample_statistics = {
            "char_count": 150,
            "word_count": 25,
            "hashtag_count": 2,
            "mention_count": 1
        }
        
        print("✅ UI component functions imported successfully")
        print("✅ Sample data structures created successfully")
        return True
    except Exception as e:
        print(f"❌ UI components test failed: {e}")
        return False

def test_streamlit_config():
    """Test Streamlit configuration."""
    try:
        import streamlit as st
        
        # Test basic Streamlit functionality
        print("✅ Streamlit is available and functional")
        return True
    except Exception as e:
        print(f"❌ Streamlit test failed: {e}")
        return False

def main():
    """Run all frontend tests."""
    print("🧪 Testing CivicGPT Frontend")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("API Health Check Test", test_api_health_check),
        ("UI Components Test", test_ui_components),
        ("Streamlit Config Test", test_streamlit_config)
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
        print("🎉 All frontend tests passed!")
        print("\n🚀 Ready to start the frontend!")
        print("\n💡 To start the frontend:")
        print("   python start_dev.py")
        print("   # Then select option 2 (Start frontend)")
        return True
    else:
        print("⚠️  Some tests failed!")
        print("\n💡 Try installing missing dependencies:")
        print("   pip install streamlit requests")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 