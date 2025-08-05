"""
Sentiment analysis module for CivicGPT.
"""
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Any, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


class SentimentAnalyzer:
    """Sentiment analysis using TextBlob and VADER."""
    
    def __init__(self):
        """Initialize sentiment analyzers."""
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using multiple methods.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        try:
            # TextBlob analysis
            blob = TextBlob(text)
            textblob_sentiment = blob.sentiment.polarity
            textblob_subjectivity = blob.sentiment.subjectivity
            
            # VADER analysis
            vader_scores = self.vader_analyzer.polarity_scores(text)
            
            # Combine results
            combined_sentiment = self._combine_sentiment_scores(
                textblob_sentiment, vader_scores
            )
            
            # Classify sentiment
            classification, confidence = self._classify_sentiment(combined_sentiment)
            
            return {
                "sentiment": classification,
                "confidence": confidence,
                "score": combined_sentiment,
                "explanation": self._generate_sentiment_explanation(
                    classification, combined_sentiment, textblob_subjectivity
                ),
                "details": {
                    "textblob": {
                        "polarity": textblob_sentiment,
                        "subjectivity": textblob_subjectivity
                    },
                    "vader": vader_scores,
                    "combined": combined_sentiment
                }
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            return self._get_fallback_sentiment()
    
    def _combine_sentiment_scores(self, textblob_score: float, vader_scores: Dict[str, float]) -> float:
        """
        Combine TextBlob and VADER scores.
        
        Args:
            textblob_score: TextBlob polarity score (-1 to 1)
            vader_scores: VADER sentiment scores
            
        Returns:
            Combined sentiment score (-1 to 1)
        """
        # VADER compound score is already normalized to -1 to 1
        vader_score = vader_scores['compound']
        
        # Weighted average (VADER is generally more reliable for social media)
        combined = (0.3 * textblob_score) + (0.7 * vader_score)
        
        # Ensure score is within bounds
        return max(-1.0, min(1.0, combined))
    
    def _classify_sentiment(self, score: float) -> Tuple[str, float]:
        """
        Classify sentiment based on score.
        
        Args:
            score: Sentiment score (-1 to 1)
            
        Returns:
            Tuple of (classification, confidence)
        """
        # Define thresholds
        positive_threshold = 0.1
        negative_threshold = -0.1
        
        if score > positive_threshold:
            classification = "positive"
            confidence = min(1.0, (score - positive_threshold) / (1.0 - positive_threshold))
        elif score < negative_threshold:
            classification = "negative"
            confidence = min(1.0, (negative_threshold - score) / (negative_threshold + 1.0))
        else:
            classification = "neutral"
            confidence = 1.0 - abs(score)  # Higher confidence for scores closer to 0
        
        return classification, confidence
    
    def _generate_sentiment_explanation(self, classification: str, score: float, subjectivity: float) -> str:
        """
        Generate explanation for sentiment analysis.
        
        Args:
            classification: Sentiment classification
            score: Combined sentiment score
            subjectivity: TextBlob subjectivity score
            
        Returns:
            Explanation string
        """
        explanations = {
            "positive": [
                "The post has a positive tone that could engage your audience well.",
                "This content conveys optimism and positivity.",
                "The language suggests a constructive and upbeat message."
            ],
            "negative": [
                "The post may come across as negative or critical.",
                "This tone could potentially alienate some readers.",
                "Consider softening the language to be more constructive."
            ],
            "neutral": [
                "The post has a balanced, neutral tone.",
                "This content is factual and objective.",
                "The tone is professional and measured."
            ]
        }
        
        base_explanation = explanations[classification][0]
        
        # Add subjectivity note
        if subjectivity > 0.7:
            base_explanation += " The content is quite subjective and personal."
        elif subjectivity < 0.3:
            base_explanation += " The content is objective and factual."
        
        # Add intensity note
        if abs(score) > 0.7:
            base_explanation += " The sentiment is strongly expressed."
        elif abs(score) < 0.2:
            base_explanation += " The sentiment is subtle and understated."
        
        return base_explanation
    
    def _get_fallback_sentiment(self) -> Dict[str, Any]:
        """Get fallback sentiment when analysis fails."""
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "score": 0.0,
            "explanation": "Sentiment analysis was unable to process this text.",
            "details": {
                "textblob": {"polarity": 0.0, "subjectivity": 0.5},
                "vader": {"compound": 0.0, "pos": 0.0, "neg": 0.0, "neu": 1.0},
                "combined": 0.0
            }
        }
    
    def analyze_sentiment_batch(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment analysis results
        """
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
        return results


# Global sentiment analyzer instance
sentiment_analyzer = SentimentAnalyzer()


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get the global sentiment analyzer instance."""
    return sentiment_analyzer


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment for a single text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Sentiment analysis results
    """
    return sentiment_analyzer.analyze_sentiment(text) 