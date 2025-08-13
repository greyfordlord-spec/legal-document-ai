#!/usr/bin/env python3
"""
Setup script for Legal Document AI Assistant
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print("✅ Python version is compatible.")

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install them manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("🔧 Creating .env file...")
        env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Customize OpenAI settings
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7

# Application Settings
DEFAULT_LANGUAGE=EN
MAX_CONVERSATION_LENGTH=50

# Document Export Settings
DEFAULT_EXPORT_FORMAT=docx
EXPORT_FOLDER=exports
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created. Please add your OpenAI API key.")
    else:
        print("✅ .env file already exists.")

def create_directories():
    """Create necessary directories."""
    directories = ["exports", "templates/document_templates", "templates/prompts"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created.")

def main():
    """Main setup function."""
    print("🚀 Setting up Legal Document AI Assistant...")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    create_env_file()
    create_directories()
    
    print("=" * 50)
    print("✅ Setup completed!")
    print("\n📋 Next steps:")
    print("1. Add your OpenAI API key to the .env file")
    print("2. Run the application: streamlit run app.py")
    print("3. Open your browser to http://localhost:8501")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
