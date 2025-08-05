"""
Text processing utilities for CivicGPT.
"""
import re
import unicodedata
from typing import Dict, List, Optional, Tuple
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class TextProcessor:
    """Text processing utilities for social media posts."""
    
    def __init__(self):
        self.max_length = settings.max_post_length
        
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text input.
        
        Args:
            text: Raw text input
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove common problematic characters
        text = re.sub(r'[^\w\s@#.,!?;:()\-_\'"]', '', text)
        
        return text
    
    def validate_post(self, text: str) -> Tuple[bool, List[str]]:
        """
        Validate a social media post.
        
        Args:
            text: Post text to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if text is empty
        if not text or not text.strip():
            errors.append("Post cannot be empty")
            return False, errors
        
        # Check length
        if len(text) > self.max_length:
            errors.append(f"Post exceeds maximum length of {self.max_length} characters")
        
        # Check for minimum length
        if len(text.strip()) < 3:
            errors.append("Post must be at least 3 characters long")
        
        # Check for excessive repetition
        if self._has_excessive_repetition(text):
            errors.append("Post contains excessive repetition")
        
        # Check for spam-like patterns
        if self._is_spam_like(text):
            errors.append("Post appears to be spam-like")
        
        return len(errors) == 0, errors
    
    def _has_excessive_repetition(self, text: str) -> bool:
        """Check for excessive character repetition."""
        # Check for 4+ repeated characters
        if re.search(r'(.)\1{3,}', text):
            return True
        
        # Check for 3+ repeated words
        words = text.split()
        for i in range(len(words) - 2):
            if words[i] == words[i+1] == words[i+2]:
                return True
        
        return False
    
    def _is_spam_like(self, text: str) -> bool:
        """Check for spam-like patterns."""
        # Check for excessive capitalization
        if len(re.findall(r'[A-Z]', text)) > len(text) * 0.7:
            return True
        
        # Check for excessive punctuation
        if len(re.findall(r'[!?]', text)) > len(text) * 0.1:
            return True
        
        # Check for excessive hashtags
        if len(re.findall(r'#\w+', text)) > 10:
            return True
        
        return False
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text."""
        hashtags = re.findall(r'#(\w+)', text)
        return list(set(hashtags))  # Remove duplicates
    
    def extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text."""
        mentions = re.findall(r'@(\w+)', text)
        return list(set(mentions))  # Remove duplicates
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        return list(set(urls))  # Remove duplicates
    
    def get_text_stats(self, text: str) -> Dict[str, any]:
        """Get statistics about the text."""
        cleaned_text = self.clean_text(text)
        
        return {
            "original_length": len(text),
            "cleaned_length": len(cleaned_text),
            "word_count": len(cleaned_text.split()),
            "character_count": len(cleaned_text),
            "hashtag_count": len(self.extract_hashtags(text)),
            "mention_count": len(self.extract_mentions(text)),
            "url_count": len(self.extract_urls(text)),
            "hashtags": self.extract_hashtags(text),
            "mentions": self.extract_mentions(text),
            "urls": self.extract_urls(text)
        }
    
    def truncate_text(self, text: str, max_length: Optional[int] = None) -> str:
        """Truncate text to specified length."""
        if max_length is None:
            max_length = self.max_length
        
        if len(text) <= max_length:
            return text
        
        # Try to truncate at word boundary
        truncated = text[:max_length-3] + "..."
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # If we can break at word
            truncated = truncated[:last_space] + "..."
        
        return truncated


# Global text processor instance
text_processor = TextProcessor()


def clean_and_validate_post(text: str) -> Tuple[str, bool, List[str]]:
    """
    Clean and validate a post in one step.
    
    Args:
        text: Raw post text
        
    Returns:
        Tuple of (cleaned_text, is_valid, errors)
    """
    cleaned_text = text_processor.clean_text(text)
    is_valid, errors = text_processor.validate_post(cleaned_text)
    
    return cleaned_text, is_valid, errors


def get_post_statistics(text: str) -> Dict[str, any]:
    """
    Get comprehensive statistics about a post.
    
    Args:
        text: Post text
        
    Returns:
        Dictionary with post statistics
    """
    return text_processor.get_text_stats(text) 