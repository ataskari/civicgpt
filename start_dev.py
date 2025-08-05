#!/usr/bin/env python3
"""
Development startup script for CivicGPT.
"""
import os
import sys
import subprocess
import time

def check_python():
    """Check if Python is available."""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python found: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python not found: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        "fastapi", "uvicorn", "pydantic", "loguru"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists."""
    if os.path.exists(".env"):
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("📝 Copy env.example to .env and add your OpenAI API key")
        return False

def start_backend():
    """Start the FastAPI backend server."""
    print("\n🚀 Starting CivicGPT Backend...")
    print("=" * 50)
    
    try:
        # Start uvicorn server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        print("\n📡 API will be available at: http://localhost:8000")
        print("📚 API docs at: http://localhost:8000/docs")
        print("🔍 Health check at: http://localhost:8000/api/health")
        print("\n⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main development startup function."""
    print("🎯 CivicGPT Development Startup")
    print("=" * 50)
    
    # Check prerequisites
    checks = [
        ("Python", check_python),
        ("Dependencies", check_dependencies),
        ("Environment", check_env_file)
    ]
    
    all_good = True
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            all_good = False
    
    if not all_good:
        print("\n❌ Some checks failed. Please fix the issues above.")
        print("💡 Try running: pip install -r requirements.txt")
        return
    
    print("\n✅ All checks passed!")
    
    # Ask user what to do
    print("\n🎮 What would you like to do?")
    print("1. Start backend server")
    print("2. Run tests")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                start_backend()
                break
            elif choice == "2":
                print("\n🧪 Running tests...")
                subprocess.run([sys.executable, "tests/test_backend.py"])
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 