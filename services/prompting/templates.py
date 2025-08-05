"""
Prompt templates for CivicGPT analysis.
"""
from typing import Dict, Any, List
from enum import Enum


class AnalysisType(str, Enum):
    """Types of analysis available."""
    COMPREHENSIVE = "comprehensive"
    SENTIMENT = "sentiment"
    TOXICITY = "toxicity"
    POLICY = "policy"
    ETHICAL = "ethical"
    SUGGESTIONS = "suggestions"


class PromptTemplates:
    """Prompt templates for different analysis types."""
    
    # Version tracking
    VERSION = "1.0.0"
    
    @staticmethod
    def get_system_prompt() -> str:
        """Get the system prompt for CivicGPT."""
        return """You are CivicGPT, an AI assistant that analyzes social media posts for safety, tone, and compliance. 

Your role is to:
1. Analyze posts for sentiment (positive, negative, neutral)
2. Detect potential toxicity or harmful content
3. Check for platform policy violations (Twitter/X)
4. Identify ethical and legal risks
5. Provide constructive improvement suggestions

Be helpful, accurate, and constructive in your analysis. Focus on being educational and actionable."""

    @staticmethod
    def get_comprehensive_analysis_prompt(text: str, platform: str = "twitter") -> str:
        """Get comprehensive analysis prompt."""
        return f"""Please analyze this social media post for {platform}:

POST: "{text}"

Provide a comprehensive analysis including:
1. Sentiment analysis (positive/negative/neutral with confidence)
2. Toxicity assessment (is it potentially harmful?)
3. Platform policy compliance ({platform} rules)
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

    @staticmethod
    def get_sentiment_analysis_prompt(text: str) -> str:
        """Get sentiment analysis prompt."""
        return f"""Analyze the sentiment of this social media post:

POST: "{text}"

Focus specifically on:
1. Overall sentiment (positive/negative/neutral)
2. Confidence level
3. Key words/phrases that influenced the sentiment
4. Tone and emotional impact

Format as JSON:
{{
    "sentiment": "positive/negative/neutral",
    "confidence": 0.0-1.0,
    "key_factors": ["factor1", "factor2"],
    "tone": "description of tone",
    "emotional_impact": "description of emotional impact"
}}"""

    @staticmethod
    def get_toxicity_analysis_prompt(text: str) -> str:
        """Get toxicity analysis prompt."""
        return f"""Analyze this post for potential toxicity or harmful content:

POST: "{text}"

Check for:
1. Hate speech or discriminatory language
2. Harassment or bullying
3. Violence or threats
4. Misinformation or harmful claims
5. Privacy violations

Format as JSON:
{{
    "is_toxic": true/false,
    "confidence": 0.0-1.0,
    "categories": {{
        "hate": 0.0-1.0,
        "harassment": 0.0-1.0,
        "violence": 0.0-1.0,
        "misinformation": 0.0-1.0
    }},
    "explanation": "detailed explanation",
    "flagged_phrases": ["phrase1", "phrase2"]
}}"""

    @staticmethod
    def get_policy_analysis_prompt(text: str, platform: str = "twitter") -> str:
        """Get platform policy analysis prompt."""
        platform_rules = PromptTemplates._get_platform_rules(platform)
        
        return f"""Analyze this post for {platform} policy compliance:

POST: "{text}"

{platform_rules}

Check for violations and provide specific feedback.

Format as JSON:
{{
    "policy_violations": [
        {{
            "rule": "rule name",
            "severity": "low/medium/high",
            "description": "explanation",
            "suggestion": "how to fix"
        }}
    ],
    "overall_compliance": "compliant/needs_review/violation",
    "risk_level": "low/medium/high"
}}"""

    @staticmethod
    def get_ethical_analysis_prompt(text: str) -> str:
        """Get ethical analysis prompt."""
        return f"""Analyze this post for ethical considerations:

POST: "{text}"

Consider:
1. Potential harm to individuals or groups
2. Privacy and data protection
3. Misinformation or misleading claims
4. Bias or discrimination
5. Professional conduct

Format as JSON:
{{
    "ethical_risks": [
        {{
            "type": "risk type",
            "severity": "low/medium/high",
            "description": "explanation",
            "suggestion": "how to address"
        }}
    ],
    "overall_ethical_score": 0.0-1.0,
    "recommendations": ["rec1", "rec2"]
}}"""

    @staticmethod
    def get_suggestions_prompt(text: str) -> str:
        """Get improvement suggestions prompt."""
        return f"""Provide constructive improvement suggestions for this post:

POST: "{text}"

Focus on:
1. Tone and clarity improvements
2. Safety and compliance enhancements
3. Engagement optimization
4. Professional presentation

Format as JSON:
{{
    "suggestions": [
        {{
            "type": "tone/clarity/safety/engagement",
            "original": "original text",
            "improved": "suggested text",
            "reasoning": "why this helps",
            "priority": 1-5
        }}
    ],
    "overall_improvement_score": 0.0-1.0
}}"""

    @staticmethod
    def _get_platform_rules(platform: str) -> str:
        """Get platform-specific rules."""
        rules = {
            "twitter": """Twitter/X Community Guidelines:
- No hate speech or discriminatory content
- No harassment or bullying
- No violence or threats
- No misinformation about public health/safety
- No impersonation or fake accounts
- No private information without consent
- No spam or manipulation""",
            
            "linkedin": """LinkedIn Professional Standards:
- Maintain professional tone
- No discriminatory content
- No harassment or bullying
- No false or misleading information
- No spam or excessive self-promotion
- Respect intellectual property
- Maintain confidentiality""",
            
            "instagram": """Instagram Community Guidelines:
- No hate speech or discrimination
- No harassment or bullying
- No violence or threats
- No nudity or sexual content
- No spam or fake engagement
- Respect intellectual property
- No private information without consent"""
        }
        
        return rules.get(platform.lower(), rules["twitter"])

    @staticmethod
    def get_prompt_by_type(analysis_type: AnalysisType, text: str, **kwargs) -> str:
        """Get prompt by analysis type."""
        prompts = {
            AnalysisType.COMPREHENSIVE: PromptTemplates.get_comprehensive_analysis_prompt,
            AnalysisType.SENTIMENT: PromptTemplates.get_sentiment_analysis_prompt,
            AnalysisType.TOXICITY: PromptTemplates.get_toxicity_analysis_prompt,
            AnalysisType.POLICY: PromptTemplates.get_policy_analysis_prompt,
            AnalysisType.ETHICAL: PromptTemplates.get_ethical_analysis_prompt,
            AnalysisType.SUGGESTIONS: PromptTemplates.get_suggestions_prompt
        }
        
        prompt_func = prompts.get(analysis_type)
        if prompt_func:
            return prompt_func(text, **kwargs)
        else:
            return PromptTemplates.get_comprehensive_analysis_prompt(text, **kwargs)


# Convenience functions
def get_system_prompt() -> str:
    """Get the system prompt."""
    return PromptTemplates.get_system_prompt()


def get_analysis_prompt(analysis_type: str, text: str, **kwargs) -> str:
    """Get analysis prompt by type."""
    return PromptTemplates.get_prompt_by_type(AnalysisType(analysis_type), text, **kwargs) 