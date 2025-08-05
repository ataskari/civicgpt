"""
Basic tests for CivicGPT backend.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported."""
    try:
        # Test core imports
        from config.settings import settings
        from utils.logger import get_logger
        from utils.text_processor import TextProcessor
        from api.models import PostAnalysisRequest, AnalysisResult
        print("✅ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_text_processor():
    """Test text processing functionality."""
    try:
        from utils.text_processor import text_processor, clean_and_validate_post
        
        # Test basic text cleaning
        test_text = "  Hello   World!  "
        cleaned = text_processor.clean_text(test_text)
        assert cleaned == "Hello World!"
        print("✅ Text cleaning works")
        
        # Test validation
        is_valid, errors = text_processor.validate_post("Valid post")
        assert is_valid
        assert len(errors) == 0
        print("✅ Text validation works")
        
        # Test statistics
        stats = text_processor.get_text_stats("Hello #world @user")
        assert stats["hashtag_count"] == 1
        assert stats["mention_count"] == 1
        print("✅ Text statistics work")
        
        return True
    except Exception as e:
        print(f"❌ Text processor test failed: {e}")
        return False


def test_models():
    """Test Pydantic models."""
    try:
        from api.models import PostAnalysisRequest, SentimentType, RiskLevel
        
        # Test request model
        request = PostAnalysisRequest(
            text="Test post",
            platform="twitter",
            include_suggestions=True
        )
        assert request.text == "Test post"
        assert request.platform == "twitter"
        print("✅ Request models work")
        
        # Test enums
        assert SentimentType.POSITIVE == "positive"
        assert RiskLevel.HIGH == "high"
        print("✅ Enums work")
        
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Running CivicGPT Backend Tests")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Text Processor Test", test_text_processor),
        ("Models Test", test_models)
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
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 