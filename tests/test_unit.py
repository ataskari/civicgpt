#!/usr/bin/env python3
"""
Unit tests for CivicGPT components.
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestTextProcessor(unittest.TestCase):
    """Test text processing utilities."""
    
    def setUp(self):
        from utils.text_processor import text_processor
        self.processor = text_processor
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        # Test basic cleaning
        dirty_text = "  This   is   a   test   post  "
        cleaned = self.processor.clean_text(dirty_text)
        self.assertEqual(cleaned, "This is a test post")
        
        # Test unicode normalization
        unicode_text = "café résumé naïve"
        cleaned = self.processor.clean_text(unicode_text)
        self.assertIn("cafe", cleaned.lower())
    
    def test_validate_post(self):
        """Test post validation."""
        # Valid post
        valid_text = "This is a valid post"
        is_valid, errors = self.processor.validate_post(valid_text)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Empty post
        empty_text = ""
        is_valid, errors = self.processor.validate_post(empty_text)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Too long post
        long_text = "This is a very long post. " * 50
        is_valid, errors = self.processor.validate_post(long_text)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_extract_hashtags(self):
        """Test hashtag extraction."""
        text = "This is a #test post with #hashtags #python"
        hashtags = self.processor.extract_hashtags(text)
        self.assertIn("test", hashtags)
        self.assertIn("hashtags", hashtags)
        self.assertIn("python", hashtags)
        self.assertEqual(len(hashtags), 3)
    
    def test_extract_mentions(self):
        """Test mention extraction."""
        text = "This is a test post with @user1 and @user2"
        mentions = self.processor.extract_mentions(text)
        self.assertIn("user1", mentions)
        self.assertIn("user2", mentions)
        self.assertEqual(len(mentions), 2)

class TestSentimentAnalyzer(unittest.TestCase):
    """Test sentiment analysis functionality."""
    
    def setUp(self):
        from services.sentiment_analyzer import SentimentAnalyzer
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection."""
        text = "I love this amazing product! It's fantastic!"
        result = self.analyzer.analyze_sentiment(text)
        
        self.assertIn("sentiment", result)
        self.assertIn("confidence", result)
        self.assertIn("score", result)
        self.assertIn("explanation", result)
        
        # Should be positive
        self.assertEqual(result["sentiment"], "positive")
        self.assertGreater(result["confidence"], 0.5)
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection."""
        text = "This is terrible and I hate it."
        result = self.analyzer.analyze_sentiment(text)
        
        self.assertEqual(result["sentiment"], "negative")
        self.assertGreater(result["confidence"], 0.5)
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection."""
        text = "The weather is cloudy today."
        result = self.analyzer.analyze_sentiment(text)
        
        self.assertEqual(result["sentiment"], "neutral")
    
    def test_fallback_sentiment(self):
        """Test fallback when analysis fails."""
        with patch('textblob.TextBlob') as mock_blob:
            mock_blob.side_effect = Exception("Test error")
            
            result = self.analyzer.analyze_sentiment("test")
            
            self.assertEqual(result["sentiment"], "neutral")
            self.assertEqual(result["confidence"], 0.5)

class TestPromptTemplates(unittest.TestCase):
    """Test prompt template system."""
    
    def setUp(self):
        from services.prompting.templates import PromptTemplates
        self.templates = PromptTemplates
    
    def test_system_prompt(self):
        """Test system prompt generation."""
        prompt = self.templates.get_system_prompt()
        
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 100)
        self.assertIn("CivicGPT", prompt)
    
    def test_comprehensive_analysis_prompt(self):
        """Test comprehensive analysis prompt."""
        text = "This is a test post"
        prompt = self.templates.get_comprehensive_analysis_prompt(text)
        
        self.assertIsInstance(prompt, str)
        self.assertIn(text, prompt)
        self.assertIn("JSON", prompt)
    
    def test_platform_rules(self):
        """Test platform-specific rules."""
        twitter_rules = self.templates._get_platform_rules("twitter")
        linkedin_rules = self.templates._get_platform_rules("linkedin")
        
        self.assertIsInstance(twitter_rules, str)
        self.assertIsInstance(linkedin_rules, str)
        self.assertGreater(len(twitter_rules), 50)
        self.assertGreater(len(linkedin_rules), 50)
    
    def test_prompt_by_type(self):
        """Test prompt selection by type."""
        from services.prompting.templates import AnalysisType
        
        text = "Test post"
        
        # Test comprehensive prompt
        comprehensive = self.templates.get_prompt_by_type(
            AnalysisType.COMPREHENSIVE, text
        )
        self.assertIn(text, comprehensive)
        
        # Test sentiment prompt
        sentiment = self.templates.get_prompt_by_type(
            AnalysisType.SENTIMENT, text
        )
        self.assertIn(text, sentiment)

class TestAPIModels(unittest.TestCase):
    """Test API models and validation."""
    
    def test_post_analysis_request(self):
        """Test post analysis request model."""
        from api.models import PostAnalysisRequest
        
        # Valid request
        request_data = {
            "text": "This is a test post",
            "platform": "twitter"
        }
        request = PostAnalysisRequest(**request_data)
        
        self.assertEqual(request.text, "This is a test post")
        self.assertEqual(request.platform, "twitter")
    
    def test_analysis_result(self):
        """Test analysis result model."""
        from api.models import AnalysisResult, SentimentAnalysis, ToxicityAnalysis, TextStatistics
        
        # Create sample data
        sentiment = SentimentAnalysis(
            sentiment="positive",
            confidence=0.8,
            score=0.6,
            explanation="Positive sentiment detected"
        )
        
        toxicity = ToxicityAnalysis(
            is_toxic=False,
            confidence=0.9,
            categories={},
            explanation="Content appears safe"
        )
        
        stats = TextStatistics(
            char_count=50,
            word_count=10,
            hashtag_count=2,
            mention_count=1
        )
        
        result = AnalysisResult(
            post_id="test-123",
            original_text="Test post",
            cleaned_text="Test post",
            platform="twitter",
            analysis_time=1.5,
            timestamp=1234567890.0,
            sentiment=sentiment,
            toxicity=toxicity,
            policy_violations=[],
            ethical_risks=[],
            suggestions=[],
            statistics=stats,
            overall_risk="low",
            summary="Test analysis",
            recommendations=[]
        )
        
        self.assertEqual(result.post_id, "test-123")
        self.assertEqual(result.original_text, "Test post")
        self.assertEqual(result.sentiment.sentiment, "positive")

class TestOpenAIClient(unittest.TestCase):
    """Test OpenAI client functionality."""
    
    def setUp(self):
        from services.openai_client import OpenAIClient
        self.client = OpenAIClient()
    
    def test_system_prompt(self):
        """Test system prompt generation."""
        prompt = self.client._get_system_prompt()
        
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 100)
        self.assertIn("CivicGPT", prompt)
    
    def test_analysis_prompt_creation(self):
        """Test analysis prompt creation."""
        text = "This is a test post"
        prompt = self.client._create_analysis_prompt(text, "comprehensive")
        
        self.assertIsInstance(prompt, str)
        self.assertIn(text, prompt)
        self.assertIn("JSON", prompt)
    
    def test_fallback_parse(self):
        """Test fallback parsing."""
        fallback = self.client._fallback_parse("Invalid JSON")
        
        self.assertIn("sentiment", fallback)
        self.assertIn("toxicity", fallback)
        self.assertEqual(fallback["sentiment"]["classification"], "neutral")
        self.assertEqual(fallback["toxicity"]["is_toxic"], False)

class TestFrontendComponents(unittest.TestCase):
    """Test frontend component functions."""
    
    def test_api_health_check(self):
        """Test API health check function."""
        from frontend.app import check_api_health
        
        # Mock the requests.get call
        with patch('requests.get') as mock_get:
            # Test successful health check
            mock_get.return_value.status_code = 200
            result = check_api_health()
            self.assertTrue(result)
            
            # Test failed health check
            mock_get.return_value.status_code = 500
            result = check_api_health()
            self.assertFalse(result)
    
    def test_analyze_post(self):
        """Test post analysis function."""
        from frontend.app import analyze_post
        
        # Mock the requests.post call
        with patch('requests.post') as mock_post:
            # Test successful analysis
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "sentiment": {"sentiment": "positive"},
                "toxicity": {"is_toxic": False}
            }
            mock_post.return_value = mock_response
            
            result = analyze_post("Test post", "twitter")
            self.assertIsNotNone(result)
            self.assertIn("sentiment", result)
    
    def test_display_functions(self):
        """Test display function imports."""
        from frontend.app import (
            display_sentiment_analysis,
            display_toxicity_analysis,
            display_risk_assessment,
            display_statistics
        )
        
        # Test that functions can be called (they don't return anything)
        sample_data = {
            "sentiment": "positive",
            "confidence": 0.8,
            "score": 0.6,
            "explanation": "Test explanation"
        }
        
        # These functions should not raise exceptions
        try:
            display_sentiment_analysis(sample_data)
            display_toxicity_analysis(sample_data)
            display_risk_assessment("low", "Test summary")
            display_statistics(sample_data)
        except Exception as e:
            self.fail(f"Display functions failed: {e}")

def run_tests():
    """Run all unit tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestTextProcessor,
        TestSentimentAnalyzer,
        TestPromptTemplates,
        TestAPIModels,
        TestOpenAIClient,
        TestFrontendComponents
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 