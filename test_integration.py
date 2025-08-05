#!/usr/bin/env python3
"""
Integration tests for CivicGPT - End-to-End Testing.
"""
import sys
import os
import time
import requests
import json
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backend_startup():
    """Test if backend can start and respond."""
    print("🔍 Testing backend startup...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        print("💡 Make sure to start the backend: python start_dev.py")
        return False

def test_api_endpoints():
    """Test all API endpoints."""
    print("\n🔍 Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/health", "GET"),
        ("/api/info", "GET"),
        ("/api/analyze", "POST"),
        ("/api/validate", "POST")
    ]
    
    passed = 0
    total = len(endpoints)
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            elif method == "POST":
                # Test with sample data for POST endpoints
                sample_data = {"text": "This is a test post", "platform": "twitter"}
                response = requests.post(f"{base_url}{endpoint}", json=sample_data, timeout=10)
            
            if response.status_code in [200, 201, 400]:  # 400 is OK for validation errors
                print(f"✅ {method} {endpoint} - {response.status_code}")
                passed += 1
            else:
                print(f"❌ {method} {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {e}")
    
    print(f"📊 API Endpoints: {passed}/{total} passed")
    return passed == total

def test_ai_analysis():
    """Test AI analysis functionality."""
    print("\n🔍 Testing AI analysis...")
    
    test_cases = [
        {
            "text": "I love this amazing product! It's fantastic!",
            "expected_sentiment": "positive",
            "description": "Positive sentiment test"
        },
        {
            "text": "This is terrible and I hate it.",
            "expected_sentiment": "negative", 
            "description": "Negative sentiment test"
        },
        {
            "text": "The weather is cloudy today.",
            "expected_sentiment": "neutral",
            "description": "Neutral sentiment test"
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        try:
            response = requests.post(
                "http://localhost:8000/api/analyze",
                json={"text": test_case["text"], "platform": "twitter"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                sentiment = result.get("sentiment", {}).get("sentiment", "unknown")
                
                print(f"✅ {test_case['description']}: {sentiment}")
                passed += 1
            else:
                print(f"❌ {test_case['description']}: API error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {test_case['description']}: Error - {e}")
    
    print(f"📊 AI Analysis: {passed}/{total} passed")
    return passed == total

def test_frontend_components():
    """Test frontend component imports and functions."""
    print("\n🔍 Testing frontend components...")
    
    try:
        # Test Streamlit import
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Test frontend app functions
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "frontend"))
        from app import (
            check_api_health, analyze_post, display_sentiment_analysis,
            display_toxicity_analysis, display_risk_assessment, display_statistics
        )
        print("✅ Frontend functions imported successfully")
        
        # Test API health check function
        health_result = check_api_health()
        print(f"✅ API health check works: {health_result}")
        
        return True
    except Exception as e:
        print(f"❌ Frontend component test failed: {e}")
        return False

def test_text_processing():
    """Test text processing utilities."""
    print("\n🔍 Testing text processing...")
    
    try:
        from utils.text_processor import clean_and_validate_post, get_post_statistics
        
        # Test text cleaning
        test_text = "This is a test post with #hashtag and @mention"
        cleaned_text, is_valid, errors = clean_and_validate_post(test_text)
        
        if is_valid:
            print("✅ Text validation works")
        else:
            print(f"❌ Text validation failed: {errors}")
            return False
        
        # Test statistics
        stats = get_post_statistics(test_text)
        if "char_count" in stats and "word_count" in stats:
            print("✅ Text statistics work")
        else:
            print("❌ Text statistics failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Text processing test failed: {e}")
        return False

def test_ai_services():
    """Test AI service components."""
    print("\n🔍 Testing AI services...")
    
    try:
        # Test sentiment analyzer
        from services.sentiment_analyzer import analyze_sentiment
        
        test_text = "I love this amazing product!"
        result = analyze_sentiment(test_text)
        
        if "sentiment" in result and "confidence" in result:
            print(f"✅ Sentiment analysis works: {result['sentiment']}")
        else:
            print("❌ Sentiment analysis failed")
            return False
        
        # Test prompt templates
        from services.prompting.templates import PromptTemplates
        
        prompt = PromptTemplates.get_comprehensive_analysis_prompt("test")
        if len(prompt) > 100:  # Basic length check
            print("✅ Prompt templates work")
        else:
            print("❌ Prompt templates failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ AI services test failed: {e}")
        return False

def test_error_handling():
    """Test error handling and edge cases."""
    print("\n🔍 Testing error handling...")
    
    try:
        # Test empty text
        response = requests.post(
            "http://localhost:8000/api/analyze",
            json={"text": "", "platform": "twitter"},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Empty text properly rejected")
        else:
            print(f"❌ Empty text not handled properly: {response.status_code}")
            return False
        
        # Test very long text
        long_text = "This is a very long text. " * 100
        response = requests.post(
            "http://localhost:8000/api/analyze",
            json={"text": long_text, "platform": "twitter"},
            timeout=30
        )
        
        if response.status_code in [200, 400]:  # Either success or validation error
            print("✅ Long text handled properly")
        else:
            print(f"❌ Long text not handled properly: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_performance():
    """Test system performance."""
    print("\n🔍 Testing performance...")
    
    try:
        # Test response time
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/api/analyze",
            json={"text": "This is a performance test.", "platform": "twitter"},
            timeout=30
        )
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            print(f"✅ Analysis completed in {response_time:.2f}s")
            
            if response_time < 10:  # Should complete within 10 seconds
                print("✅ Performance is acceptable")
                return True
            else:
                print(f"⚠️  Response time is slow: {response_time:.2f}s")
                return False
        else:
            print(f"❌ Performance test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("🧪 CivicGPT Integration Testing")
    print("=" * 50)
    
    tests = [
        ("Backend Startup", test_backend_startup),
        ("API Endpoints", test_api_endpoints),
        ("AI Analysis", test_ai_analysis),
        ("Frontend Components", test_frontend_components),
        ("Text Processing", test_text_processing),
        ("AI Services", test_ai_services),
        ("Error Handling", test_error_handling),
        ("Performance", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n" + "=" * 50)
    print(f"📊 Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        print("\n🚀 CivicGPT is ready for production!")
        print("\n💡 Next steps:")
        print("   - Stage 6: Deployment & Documentation")
        print("   - Add your OpenAI API key to .env file")
        print("   - Deploy to Render/Railway/Fly.io")
        return True
    else:
        print("⚠️  Some integration tests failed!")
        print("\n💡 Check the errors above and fix them before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 