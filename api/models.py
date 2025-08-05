"""
Pydantic models for CivicGPT API.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import time


class SentimentType(str, Enum):
    """Sentiment classification types."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class RiskLevel(str, Enum):
    """Risk level classifications."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisType(str, Enum):
    """Types of analysis performed."""
    SENTIMENT = "sentiment"
    TOXICITY = "toxicity"
    POLICY = "policy"
    ETHICAL = "ethical"
    SUGGESTIONS = "suggestions"


# Request Models
class PostAnalysisRequest(BaseModel):
    """Request model for post analysis."""
    text: str = Field(..., min_length=1, max_length=280, description="Social media post text")
    platform: Optional[str] = Field(default="twitter", description="Target platform (twitter, linkedin, etc.)")
    include_suggestions: bool = Field(default=True, description="Whether to include improvement suggestions")
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Post text cannot be empty")
        return v.strip()


# Response Models
class SentimentAnalysis(BaseModel):
    """Sentiment analysis result."""
    sentiment: SentimentType
    confidence: float = Field(..., ge=0.0, le=1.0)
    score: float = Field(..., description="Raw sentiment score")
    explanation: Optional[str] = None


class ToxicityAnalysis(BaseModel):
    """Toxicity analysis result."""
    is_toxic: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    categories: Dict[str, float] = Field(default_factory=dict)
    explanation: Optional[str] = None


class PolicyViolation(BaseModel):
    """Platform policy violation."""
    rule_name: str
    description: str
    severity: RiskLevel
    confidence: float = Field(..., ge=0.0, le=1.0)
    suggestion: Optional[str] = None


class EthicalRisk(BaseModel):
    """Ethical risk assessment."""
    risk_type: str
    description: str
    severity: RiskLevel
    confidence: float = Field(..., ge=0.0, le=1.0)
    suggestion: Optional[str] = None


class ImprovementSuggestion(BaseModel):
    """Suggestion for improving the post."""
    type: str = Field(..., description="Type of suggestion (tone, clarity, safety, etc.)")
    description: str
    original_text: str
    suggested_text: str
    reasoning: Optional[str] = None
    priority: int = Field(..., ge=1, le=5, description="Priority level (1=low, 5=high)")


class TextStatistics(BaseModel):
    """Text statistics."""
    original_length: int
    cleaned_length: int
    word_count: int
    character_count: int
    hashtag_count: int
    mention_count: int
    url_count: int
    hashtags: List[str] = Field(default_factory=list)
    mentions: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """Complete analysis result."""
    post_id: str
    original_text: str
    cleaned_text: str
    platform: str
    analysis_time: float
    timestamp: float
    
    # Analysis results
    sentiment: SentimentAnalysis
    toxicity: ToxicityAnalysis
    policy_violations: List[PolicyViolation] = Field(default_factory=list)
    ethical_risks: List[EthicalRisk] = Field(default_factory=list)
    suggestions: List[ImprovementSuggestion] = Field(default_factory=list)
    
    # Statistics
    statistics: TextStatistics
    
    # Summary
    overall_risk: RiskLevel
    summary: str
    recommendations: List[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: float
    version: str
    environment: str


class APIInfoResponse(BaseModel):
    """API information response."""
    name: str
    version: str
    environment: str
    openai_model: str
    max_post_length: int


# Validation Models
class ValidationError(BaseModel):
    """Validation error details."""
    field: str
    message: str
    code: str


class ValidationResponse(BaseModel):
    """Validation response."""
    is_valid: bool
    errors: List[ValidationError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    statistics: TextStatistics 