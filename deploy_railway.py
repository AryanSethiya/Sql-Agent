#!/usr/bin/env python3
"""
Railway Deployment Helper Script
This script helps set up your SQL Agent for Railway deployment.
"""

import os
import secrets
import subprocess
import sys

def generate_secret_key():
    """Generate a secure secret key for JWT."""
    return secrets.token_urlsafe(32)

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        'requirements.txt',
        'app/main.py',
        'Procfile',
        'railway.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found!")
    return True

def create_env_template():
    """Create a .env template for Railway."""
    env_template = f"""# Railway Deployment Environment Variables
# Copy these to your Railway environment variables

# Database (Railway will provide this)
DATABASE_URL=postgresql://username:password@host:port/database

# JWT Authentication
SECRET_KEY={generate_secret_key()}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Application Configuration
DEBUG=False
HOST=0.0.0.0
PORT=8000
"""
    
    with open('railway.env.template', 'w') as f:
        f.write(env_template)
    
    print("✅ Created railway.env.template")
    print("📝 Copy the variables from railway.env.template to your Railway environment")

def check_git_status():
    """Check if the repository is ready for deployment."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  You have uncommitted changes:")
            print(result.stdout)
            print("💡 Consider committing changes before deploying")
        else:
            print("✅ Repository is clean and ready for deployment")
    except FileNotFoundError:
        print("⚠️  Git not found. Make sure your code is in a git repository")

def main():
    """Main deployment setup function."""
    print("🚀 Railway Deployment Setup for SQL Agent")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix the missing files before deploying")
        sys.exit(1)
    
    # Check git status
    check_git_status()
    
    # Create environment template
    create_env_template()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Sign up at https://railway.app")
    print("2. Connect your GitHub repository")
    print("3. Create a new project from your repository")
    print("4. Add PostgreSQL plugin to your project")
    print("5. Copy environment variables from railway.env.template")
    print("6. Deploy!")
    print("\n📖 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main() 