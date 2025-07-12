# 🚀 SQL Agent Deployment Guide

This guide provides step-by-step instructions for deploying your SQL Agent application to various cloud platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- A GitHub repository with your code
- Environment variables ready (see `.env` file)
- PostgreSQL database (or use cloud database)

## 🎯 Quick Deploy Options

### Option 1: Railway (Recommended)

**Railway** is the easiest option with built-in PostgreSQL support.

#### Steps:
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub repository**
3. **Create a new project** from your repository
4. **Add PostgreSQL plugin**:
   - Go to your project
   - Click "New" → "Database" → "PostgreSQL"
5. **Set environment variables**:
   ```
   DATABASE_URL=postgresql://... (from Railway PostgreSQL)
   SECRET_KEY=your-secret-key
   OPENAI_API_KEY=your-openai-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
6. **Deploy** - Railway will automatically detect and deploy your FastAPI app

**✅ Pros**: Free tier, automatic PostgreSQL, easy setup
**❌ Cons**: Limited free tier usage

---

### Option 2: Render

**Render** offers free hosting with PostgreSQL.

#### Steps:
1. **Sign up** at [render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. **Add PostgreSQL database**:
   - Create a new PostgreSQL service
   - Copy the connection string
6. **Set environment variables** (same as Railway)
7. **Deploy**

**✅ Pros**: Free tier, good documentation
**❌ Cons**: Slower cold starts

---

### Option 3: Heroku

**Heroku** is a classic choice with good PostgreSQL support.

#### Steps:
1. **Install Heroku CLI**
2. **Login to Heroku**:
   ```bash
   heroku login
   ```
3. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```
4. **Add PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
5. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set OPENAI_API_KEY=your-openai-key
   heroku config:set ALGORITHM=HS256
   heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
6. **Deploy**:
   ```bash
   git push heroku main
   ```

**✅ Pros**: Reliable, good PostgreSQL integration
**❌ Cons**: No free tier anymore

---

## 🎨 Frontend Deployment

### Deploy React Frontend to Vercel

1. **Sign up** at [vercel.com](https://vercel.com)
2. **Import your repository**
3. **Configure build settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
4. **Set environment variables**:
   ```
   VITE_API_URL=https://your-backend-url.com
   ```
5. **Deploy**

---

## 🔧 Environment Variables

Set these environment variables in your deployment platform:

```env
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Application
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

---

## 🗄️ Database Setup

### Option 1: Cloud Database
- **Railway PostgreSQL**: Automatically provisioned
- **Render PostgreSQL**: Free tier available
- **Heroku Postgres**: Reliable but paid

### Option 2: External Database
- **Supabase**: Free PostgreSQL hosting
- **Neon**: Serverless PostgreSQL
- **PlanetScale**: MySQL alternative

---

## 🔍 Post-Deployment Checklist

After deployment, verify:

- [ ] **Health check endpoint** works: `https://your-app.com/health`
- [ ] **Database connection** is working
- [ ] **Authentication** endpoints are accessible
- [ ] **SQL queries** can be executed
- [ ] **Frontend** can connect to backend
- [ ] **Environment variables** are set correctly

---

## 🚨 Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Check `DATABASE_URL` format
   - Ensure database is accessible from deployment region

2. **Import Errors**
   - Verify all dependencies in `requirements.txt`
   - Check Python version compatibility

3. **Environment Variables**
   - Ensure all required variables are set
   - Check for typos in variable names

4. **Port Issues**
   - Use `$PORT` environment variable
   - Don't hardcode port numbers

---

## 📊 Monitoring

### Railway
- Built-in monitoring dashboard
- Logs available in real-time

### Render
- Service logs in dashboard
- Health check monitoring

### Heroku
- `heroku logs --tail` for real-time logs
- Built-in monitoring tools

---

## 🔄 Continuous Deployment

All platforms support automatic deployment:
- **Railway**: Automatic on git push
- **Render**: Automatic on git push
- **Heroku**: Automatic on git push to heroku remote

---

## 💰 Cost Comparison

| Platform | Free Tier | Database | Frontend | Total Cost |
|----------|-----------|----------|----------|------------|
| Railway | ✅ | ✅ | ❌ | $5-20/month |
| Render | ✅ | ✅ | ✅ | $7-25/month |
| Heroku | ❌ | ✅ | ✅ | $7-25/month |
| Vercel + Railway | ✅ | ✅ | ✅ | $5-20/month |

---

## 🎯 Recommended Setup

**For beginners**: Railway (easiest setup)
**For production**: Render (good free tier)
**For enterprise**: Heroku (most reliable)

---

## 📞 Support

If you encounter issues:
1. Check the platform's documentation
2. Review logs in the deployment dashboard
3. Verify environment variables
4. Test locally before deploying

---

**Happy Deploying! 🚀** 