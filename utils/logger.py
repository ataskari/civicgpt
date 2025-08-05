"""
Logging configuration for CivicGPT application.
"""
import logging
import sys
from pathlib import Path
from typing import Optional

from loguru import logger
from config.settings import settings


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    # Use settings if not provided
    if log_level is None:
        log_level = settings.log_level
    
    # Remove default loguru handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        format=settings.log_format,
        level=log_level,
        colorize=True
    )
    
    # Add file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            format=settings.log_format,
            level=log_level,
            rotation="10 MB",
            retention="7 days"
        )
    
    # Add file handler for logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    logger.add(
        logs_dir / "civicgpt.log",
        format=settings.log_format,
        level=log_level,
        rotation="10 MB",
        retention="7 days"
    )


def get_logger(name: str) -> logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


# Initialize logging on module import
setup_logging()


# Convenience function for common logging patterns
def log_analysis_start(post_id: str, user_input: str) -> None:
    """Log the start of a post analysis."""
    logger.info(f"Starting analysis for post {post_id}", extra={
        "post_id": post_id,
        "input_length": len(user_input),
        "action": "analysis_start"
    })


def log_analysis_complete(post_id: str, analysis_time: float) -> None:
    """Log the completion of a post analysis."""
    logger.info(f"Analysis completed for post {post_id} in {analysis_time:.2f}s", extra={
        "post_id": post_id,
        "analysis_time": analysis_time,
        "action": "analysis_complete"
    })


def log_error(error: Exception, context: dict = None) -> None:
    """Log an error with optional context."""
    logger.error(f"Error occurred: {str(error)}", extra={
        "error_type": type(error).__name__,
        "context": context or {}
    })


def log_api_request(method: str, endpoint: str, status_code: int, response_time: float) -> None:
    """Log API request details."""
    logger.info(f"API {method} {endpoint} - {status_code} ({response_time:.3f}s)", extra={
        "method": method,
        "endpoint": endpoint,
        "status_code": status_code,
        "response_time": response_time,
        "action": "api_request"
    }) 