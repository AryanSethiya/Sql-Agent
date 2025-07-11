#!/usr/bin/env python3
"""
Setup script for SQL Agent with LangGraph
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def create_env_file():
    """Create .env file from template."""
    env_template = Path("env_example.txt")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists, skipping creation")
        return True
    
    if not env_template.exists():
        print("❌ env_example.txt not found")
        return False
    
    try:
        with open(env_template, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created from template")
        print("📝 Please edit .env file with your configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up SQL Agent with LangGraph")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to create environment file")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration:")
    print("   - Set DATABASE_URL for your PostgreSQL database")
    print("   - Set SECRET_KEY for JWT authentication")
    print("   - Set OPENAI_API_KEY for LangGraph functionality")
    print("\n2. Initialize the database:")
    print("   python init_db.py")
    print("\n3. Run the application:")
    print("   python run.py")
    print("\n4. Test with Postman:")
    print("   - Import SQL_Agent_API.postman_collection.json")
    print("   - Set up environment variables")
    print("   - Start testing endpoints")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 