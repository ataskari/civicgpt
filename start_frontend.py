#!/usr/bin/env python3
"""
Startup script for CivicGPT Frontend.
"""
import os
import sys
import subprocess
import time
import requests

def check_streamlit():
    """Check if Streamlit is available."""
    try:
        import streamlit
        print("✅ Streamlit is available")
        return True
    except ImportError:
        print("❌ Streamlit not found")
        return False

def check_backend():
    """Check if backend is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print("❌ Backend responded with error")
            return False
    except requests.exceptions.RequestException:
        print("❌ Backend is not running")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "requests"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend."""
    print("🚀 Starting CivicGPT Frontend...")
    
    # Change to the frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    os.chdir(frontend_dir)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped by user")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    """Main startup function."""
    print("🤖 CivicGPT Frontend Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("frontend/app.py"):
        print("❌ Please run this script from the civicgpt directory")
        return
    
    # Check dependencies
    if not check_streamlit():
        print("📦 Installing Streamlit...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return
    
    # Check backend
    print("\n🔍 Checking backend status...")
    backend_running = check_backend()
    
    if not backend_running:
        print("\n⚠️  Backend is not running!")
        print("Please start the backend first:")
        print("  python start_dev.py")
        print("\nOr start both together:")
        print("  python start_dev.py")
        print("  # In another terminal:")
        print("  python start_frontend.py")
        
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Start frontend
    print("\n🎯 Starting frontend...")
    print("📱 Frontend will be available at: http://localhost:8501")
    print("🔌 Backend should be running at: http://localhost:8000")
    print("\nPress Ctrl+C to stop the frontend")
    
    start_frontend()

if __name__ == "__main__":
    main() 