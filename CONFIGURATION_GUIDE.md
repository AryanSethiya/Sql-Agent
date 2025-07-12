# Environment Configuration Guide

This guide will help you configure your SQL Agent environment step by step.

## Step 1: Create Environment File

First, create a `.env` file in your project root:

```bash
# Copy the template
cp env_example.txt .env
```

## Step 2: Configure Database Connection

Edit your `.env` file and update the `DATABASE_URL`:

### For Local PostgreSQL:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/sql_agent_db
```

### For PostgreSQL with Docker:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/sql_agent_db
```

### For Cloud PostgreSQL (e.g., AWS RDS):
```env
DATABASE_URL=postgresql://username:password@your-db-host:5432/database_name
```

### Database Setup Instructions:

#### Option A: Local PostgreSQL Installation
1. **Install PostgreSQL:**
   - **Windows:** Download from https://www.postgresql.org/download/windows/
   - **macOS:** `brew install postgresql`
   - **Ubuntu/Debian:** `sudo apt-get install postgresql postgresql-contrib`

2. **Create Database:**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   
   # Create database
   CREATE DATABASE sql_agent_db;
   
   # Create user (optional)
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sql_agent_db TO your_username;
   ```

#### Option B: Docker PostgreSQL
```bash
# Run PostgreSQL in Docker
docker run --name sql-agent-postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=sql_agent_db \
  -p 5432:5432 \
  -d postgres:15
```

## Step 3: Configure JWT Secret Key

Generate a secure secret key for JWT authentication:

### Option A: Generate with Python
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Option B: Use Online Generator
Visit: https://generate-secret.vercel.app/32

### Update .env file:
```env
SECRET_KEY=your-generated-secret-key-here
```

## Step 4: Get OpenAI API Key

1. **Sign up for OpenAI:**
   - Go to https://platform.openai.com/
   - Create an account or sign in

2. **Get API Key:**
   - Navigate to API Keys section
   - Create a new API key
   - Copy the key

3. **Update .env file:**
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

## Step 5: Complete Environment Configuration

Your final `.env` file should look like this:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/sql_agent_db

# JWT Configuration
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 7: Initialize Database

```bash
python init_db.py
```

## Step 8: Run the Application

```bash
python run.py
```

## Step 9: Test the Setup

1. **Check Health Endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Access API Documentation:**
   - Open browser: http://localhost:8000/docs
   - Interactive API documentation

## Troubleshooting

### Database Connection Issues

**Error: "connection refused"**
- Check if PostgreSQL is running
- Verify port 5432 is accessible
- Check firewall settings

**Error: "authentication failed"**
- Verify username/password in DATABASE_URL
- Check PostgreSQL user permissions

### OpenAI API Issues

**Error: "Invalid API key"**
- Verify your OpenAI API key is correct
- Check if you have sufficient credits
- Ensure the key is active

### JWT Issues

**Error: "Invalid token"**
- Verify SECRET_KEY is set correctly
- Check token expiration time
- Ensure token format is correct

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/db` |
| `SECRET_KEY` | JWT signing key | `your-secret-key-here` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `DEBUG` | Debug mode | `True` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## Security Best Practices

1. **Never commit .env file:**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use strong passwords:**
   - Database passwords should be complex
   - JWT secret keys should be random

3. **Limit API access:**
   - Use environment-specific API keys
   - Monitor API usage

4. **Database security:**
   - Use dedicated database users
   - Limit database permissions
   - Enable SSL for remote connections

## Next Steps

After configuration:

1. **Test with Postman:**
   - Import `SQL_Agent_API.postman_collection.json`
   - Set up environment variables in Postman
   - Test authentication and endpoints

2. **Explore the API:**
   - Visit http://localhost:8000/docs
   - Try different endpoints
   - Test CRUD operations

3. **Monitor logs:**
   - Check application logs for errors
   - Monitor database connections
   - Track API usage

## Support

If you encounter issues:

1. Check the logs for error messages
2. Verify all environment variables are set
3. Test database connectivity separately
4. Review the README.md for additional information 

## 🚨 **Current Error:**
```
FATAL: database "sql_agent_db" does not exist
```

## 🔍 **Root Cause:**
Your `.env` file has:
```env
DATABASE_URL=postgresql://postgres:Aryan@mp14@localhost:5432/sql_agent_db
```

But the database `sql_agent_db` hasn't been created in PostgreSQL yet.

## 🔧 **How to Fix:**

### **Step 1: Create the Database**

**Option A - Using psql command line:**
```bash
# Connect to PostgreSQL
psql -U postgres -h localhost

# In the psql prompt, create the database:
CREATE DATABASE sql_agent_db;

# Exit psql
\q
```

**Option B - Using Docker (recommended):**
```bash
# Stop any existing container
docker stop sql-agent-postgres 2>/dev/null || true
docker rm sql-agent-postgres 2>/dev/null || true

# Start fresh PostgreSQL container
docker run --name sql-agent-postgres \
  -e POSTGRES_PASSWORD=Aryan@mp14 \
  -e POSTGRES_DB=sql_agent_db \
  -p 5432:5432 \
  -d postgres:15
```

### **Step 2: Initialize Database**
```bash
python init_db.py
```

### **Step 3: Run Application**
```bash
python run.py
```

## 🎯 **Quick Test:**
After creating the database, test if PostgreSQL is accessible:
```bash
psql -U postgres -h localhost -d sql_agent_db -c "SELECT 1;"
```

