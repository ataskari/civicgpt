#!/usr/bin/env python3
"""
Health check script for CivicGPT application.
"""
import sys
import time
import requests
from typing import Dict, Any


def check_api_health(api_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Check if the API is healthy.
    
    Args:
        api_url: Base URL of the API
        
    Returns:
        Dictionary with health check results
    """
    try:
        response = requests.get(f"{api_url}/api/health", timeout=5)
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "unhealthy",
            "status_code": None,
            "response_time": None,
            "error": str(e)
        }


def check_frontend_health(frontend_url: str = "http://localhost:8501") -> Dict[str, Any]:
    """
    Check if the frontend is healthy.
    
    Args:
        frontend_url: URL of the frontend
        
    Returns:
        Dictionary with health check results
    """
    try:
        response = requests.get(frontend_url, timeout=5)
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "error": None
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "unhealthy",
            "status_code": None,
            "response_time": None,
            "error": str(e)
        }


def main():
    """Main health check function."""
    print("🔍 CivicGPT Health Check")
    print("=" * 40)
    
    # Check API
    print("\n📡 Checking API...")
    api_health = check_api_health()
    if api_health["status"] == "healthy":
        print(f"✅ API is healthy (Response time: {api_health['response_time']:.3f}s)")
    else:
        print(f"❌ API is unhealthy: {api_health['error']}")
    
    # Check Frontend
    print("\n🖥️  Checking Frontend...")
    frontend_health = check_frontend_health()
    if frontend_health["status"] == "healthy":
        print(f"✅ Frontend is healthy (Response time: {frontend_health['response_time']:.3f}s)")
    else:
        print(f"❌ Frontend is unhealthy: {frontend_health['error']}")
    
    # Overall status
    print("\n" + "=" * 40)
    if api_health["status"] == "healthy" and frontend_health["status"] == "healthy":
        print("🎉 All services are healthy!")
        sys.exit(0)
    else:
        print("⚠️  Some services are unhealthy!")
        sys.exit(1)


if __name__ == "__main__":
    main() 