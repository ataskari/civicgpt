"""
OpenAI client service for CivicGPT.
"""
import openai
from typing import Dict, Any, Optional, List
import time
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class OpenAIClient:
    """OpenAI client for CivicGPT analysis."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens
        self.temperature = settings.openai_temperature
        
    def analyze_post(self, text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze a social media post using OpenAI.
        
        Args:
            text: Post text to analyze
            analysis_type: Type of analysis (comprehensive, sentiment, toxicity, etc.)
            
        Returns:
            Analysis results
        """
        try:
            start_time = time.time()
            
            # Create prompt based on analysis type
            prompt = self._create_analysis_prompt(text, analysis_type)
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse response
            result = self._parse_analysis_response(response.choices[0].message.content)
            
            # Add metadata
            result["analysis_time"] = time.time() - start_time
            result["model_used"] = self.model
            result["tokens_used"] = response.usage.total_tokens if response.usage else 0
            
            logger.info(f"OpenAI analysis completed in {result['analysis_time']:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI analysis failed: {str(e)}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for CivicGPT."""
        return """You are CivicGPT, an AI assistant that analyzes social media posts for safety, tone, and compliance. 

Your role is to:
1. Analyze posts for sentiment (positive, negative, neutral)
2. Detect potential toxicity or harmful content
3. Check for platform policy violations (Twitter/X)
4. Identify ethical and legal risks
5. Provide constructive improvement suggestions

Be helpful, accurate, and constructive in your analysis."""
    
    def _create_analysis_prompt(self, text: str, analysis_type: str) -> str:
        """Create analysis prompt based on type."""
        base_prompt = f"""Please analyze this social media post:

POST: "{text}"

Please provide a comprehensive analysis including:
1. Sentiment analysis (positive/negative/neutral with confidence)
2. Toxicity assessment (is it potentially harmful?)
3. Platform policy compliance (Twitter/X rules)
4. Ethical and legal risks
5. Specific improvement suggestions

Format your response as JSON with these fields:
{{
    "sentiment": {{
        "classification": "positive/negative/neutral",
        "confidence": 0.0-1.0,
        "explanation": "brief explanation"
    }},
    "toxicity": {{
        "is_toxic": true/false,
        "confidence": 0.0-1.0,
        "categories": {{"hate": 0.0, "harassment": 0.0, "violence": 0.0}},
        "explanation": "brief explanation"
    }},
    "policy_violations": [
        {{
            "rule": "rule name",
            "severity": "low/medium/high",
            "description": "explanation",
            "suggestion": "how to fix"
        }}
    ],
    "ethical_risks": [
        {{
            "type": "risk type",
            "severity": "low/medium/high",
            "description": "explanation",
            "suggestion": "how to address"
        }}
    ],
    "suggestions": [
        {{
            "type": "tone/clarity/safety",
            "original": "original text",
            "improved": "suggested text",
            "reasoning": "why this helps"
        }}
    ],
    "overall_risk": "low/medium/high",
    "summary": "brief overall assessment"
}}"""
        
        return base_prompt
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse OpenAI response into structured format."""
        try:
            import json
            # Try to extract JSON from response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            parsed = json.loads(response)
            return parsed
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            # Fallback to basic parsing
            return self._fallback_parse(response)
    
    def _fallback_parse(self, response: str) -> Dict[str, Any]:
        """Fallback parsing for non-JSON responses."""
        return {
            "sentiment": {
                "classification": "neutral",
                "confidence": 0.5,
                "explanation": "Analysis completed but response format unclear"
            },
            "toxicity": {
                "is_toxic": False,
                "confidence": 0.5,
                "categories": {},
                "explanation": "Analysis completed but response format unclear"
            },
            "policy_violations": [],
            "ethical_risks": [],
            "suggestions": [],
            "overall_risk": "low",
            "summary": "Analysis completed. Please review the original response for details."
        }


# Global OpenAI client instance
openai_client = OpenAIClient()


def get_openai_client() -> OpenAIClient:
    """Get the global OpenAI client instance."""
    return openai_client 