#!/usr/bin/env python3
"""
Quick setup script for SQL Agent environment configuration
"""

import os
import secrets
import subprocess
import sys
from pathlib import Path

def get_user_input(prompt, default=""):
    """Get user input with a default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def create_env_file():
    """Create .env file with user input."""
    print("🔧 SQL Agent Environment Configuration")
    print("=" * 50)
    
    # Check if .env already exists
    if Path(".env").exists():
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("❌ Setup cancelled")
            return False
    
    # Database configuration
    print("\n📊 Database Configuration:")
    db_host = get_user_input("Database host", "localhost")
    db_port = get_user_input("Database port", "5432")
    db_name = get_user_input("Database name", "sql_agent_db")
    db_user = get_user_input("Database username", "postgres")
    db_password = get_user_input("Database password", "")
    
    if not db_password:
        print("❌ Database password is required")
        return False
    
    # JWT configuration
    print("\n🔐 JWT Configuration:")
    secret_key = secrets.token_urlsafe(32)
    print(f"Generated secret key: {secret_key}")
    use_generated = get_user_input("Use generated secret key? (Y/n)", "Y").strip().lower()
    
    if use_generated != 'n':
        jwt_secret = secret_key
    else:
        jwt_secret = get_user_input("Enter your secret key", "")
        if not jwt_secret:
            print("❌ JWT secret key is required")
            return False
    
    # OpenAI configuration
    print("\n🤖 OpenAI Configuration:")
    openai_key = get_user_input("OpenAI API Key", "")
    if not openai_key:
        print("⚠️  Warning: OpenAI API key is required for LangGraph functionality")
        continue_anyway = get_user_input("Continue without OpenAI key? (y/N)", "N").strip().lower()
        if continue_anyway != 'y':
            return False
    
    # Application configuration
    print("\n⚙️  Application Configuration:")
    debug_mode = get_user_input("Debug mode (True/False)", "True")
    host = get_user_input("Host", "0.0.0.0")
    port = get_user_input("Port", "8000")
    
    # Create .env content
    env_content = f"""# Database Configuration
DATABASE_URL=postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}

# JWT Configuration
SECRET_KEY={jwt_secret}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY={openai_key}

# Application Configuration
DEBUG={debug_mode}
HOST={host}
PORT={port}
"""
    
    # Write .env file
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    print("\n🔍 Testing database connection...")
    try:
        from app.config import settings
        from app.database import engine
        
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def initialize_database():
    """Initialize database with sample data."""
    print("\n🗄️  Initializing database...")
    try:
        subprocess.run([sys.executable, "init_db.py"], check=True, capture_output=True)
        print("✅ Database initialized successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 SQL Agent Quick Setup")
    print("=" * 50)
    
    # Step 1: Create .env file
    if not create_env_file():
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Step 3: Test database connection
    if not test_database_connection():
        print("❌ Setup failed at database connection test")
        print("Please check your database configuration and try again")
        return
    
    # Step 4: Initialize database
    if not initialize_database():
        print("❌ Setup failed at database initialization")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the application:")
    print("   python run.py")
    print("\n2. Test the API:")
    print("   curl http://localhost:8000/health")
    print("\n3. Access API documentation:")
    print("   http://localhost:8000/docs")
    print("\n4. Test with Postman:")
    print("   - Import SQL_Agent_API.postman_collection.json")
    print("   - Set up environment variables")
    print("   - Start testing endpoints")
    print("\n📚 For more information, see README.md and CONFIGURATION_GUIDE.md")

if __name__ == "__main__":
    main() 