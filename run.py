#!/usr/bin/env python3
"""
Quick start script for Legal Document AI Assistant
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if all requirements are met."""
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        print("Please run: python setup.py")
        return False
    
    # Check if OPENAI_API_KEY is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
        print("❌ OpenAI API key not configured!")
        print("Please add your OpenAI API key to the .env file")
        return False
    
    return True

def main():
    """Main function to run the application."""
    print("🚀 Starting Legal Document AI Assistant...")
    
    if not check_requirements():
        sys.exit(1)
    
    print("✅ All requirements met. Starting Streamlit app...")
    
    try:
        # Run streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
