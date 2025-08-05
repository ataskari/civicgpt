"""
Analysis endpoints for CivicGPT API.
"""
import uuid
import time
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any

from api.models import (
    PostAnalysisRequest, 
    AnalysisResult, 
    ErrorResponse,
    SentimentAnalysis,
    ToxicityAnalysis,
    TextStatistics,
    RiskLevel,
    SentimentType
)
from utils.text_processor import clean_and_validate_post, get_post_statistics
from utils.logger import get_logger, log_analysis_start, log_analysis_complete
from config.settings import settings

logger = get_logger(__name__)

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_post(request: PostAnalysisRequest):
    """
    Analyze a social media post for sentiment, toxicity, policy compliance, and ethical risks.
    
    Args:
        request: Post analysis request containing text and options
        
    Returns:
        Complete analysis result with all assessments
    """
    start_time = time.time()
    post_id = str(uuid.uuid4())
    
    try:
        # Log analysis start
        log_analysis_start(post_id, request.text)
        
        # Clean and validate input
        cleaned_text, is_valid, errors = clean_and_validate_post(request.text)
        
        if not is_valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid post: {'; '.join(errors)}"
            )
        
        # Get text statistics
        stats = get_post_statistics(request.text)
        text_stats = TextStatistics(**stats)
        
        # TODO: This is a placeholder - we'll implement the actual AI analysis in Stage 3
        # For now, return a basic analysis structure
        
        # Placeholder sentiment analysis
        sentiment = SentimentAnalysis(
            sentiment=SentimentType.NEUTRAL,
            confidence=0.5,
            score=0.0,
            explanation="Sentiment analysis not yet implemented"
        )
        
        # Placeholder toxicity analysis
        toxicity = ToxicityAnalysis(
            is_toxic=False,
            confidence=0.5,
            categories={},
            explanation="Toxicity analysis not yet implemented"
        )
        
        # Calculate analysis time
        analysis_time = time.time() - start_time
        
        # Create analysis result
        result = AnalysisResult(
            post_id=post_id,
            original_text=request.text,
            cleaned_text=cleaned_text,
            platform=request.platform,
            analysis_time=analysis_time,
            timestamp=time.time(),
            sentiment=sentiment,
            toxicity=toxicity,
            policy_violations=[],
            ethical_risks=[],
            suggestions=[],
            statistics=text_stats,
            overall_risk=RiskLevel.LOW,
            summary="Basic analysis completed. AI analysis features coming in next stage.",
            recommendations=["Implement AI analysis services"]
        )
        
        # Log analysis completion
        log_analysis_complete(post_id, analysis_time)
        
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log and return error
        logger.error(f"Analysis failed for post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/validate")
async def validate_post(request: PostAnalysisRequest):
    """
    Validate a social media post without performing full analysis.
    
    Args:
        request: Post validation request
        
    Returns:
        Validation result with errors and warnings
    """
    try:
        # Clean and validate input
        cleaned_text, is_valid, errors = clean_and_validate_post(request.text)
        
        # Get text statistics
        stats = get_post_statistics(request.text)
        text_stats = TextStatistics(**stats)
        
        # Create validation response
        from api.models import ValidationResponse, ValidationError
        
        validation_errors = []
        for error in errors:
            validation_errors.append(
                ValidationError(
                    field="text",
                    message=error,
                    code="VALIDATION_ERROR"
                )
            )
        
        warnings = []
        if text_stats.hashtag_count > 5:
            warnings.append("High number of hashtags detected")
        if text_stats.mention_count > 3:
            warnings.append("High number of mentions detected")
        
        return ValidationResponse(
            is_valid=is_valid,
            errors=validation_errors,
            warnings=warnings,
            statistics=text_stats
        )
        
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )


@router.get("/statistics/{text:path}")
async def get_text_statistics(text: str):
    """
    Get statistics about a text without performing analysis.
    
    Args:
        text: Text to analyze
        
    Returns:
        Text statistics
    """
    try:
        # URL decode the text
        import urllib.parse
        decoded_text = urllib.parse.unquote(text)
        
        # Get statistics
        stats = get_post_statistics(decoded_text)
        text_stats = TextStatistics(**stats)
        
        return text_stats
        
    except Exception as e:
        logger.error(f"Statistics calculation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Statistics calculation failed: {str(e)}"
        ) 