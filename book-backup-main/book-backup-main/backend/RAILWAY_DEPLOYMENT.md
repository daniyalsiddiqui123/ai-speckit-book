# Deploying Backend to Railway.com

This document provides step-by-step instructions to deploy your FastAPI backend to Railway.com.

## Prerequisites

- A Railway.com account (sign up at https://railway.com)
- Your backend code pushed to a GitHub repository (completed)
- Environment variables ready for deployment

## Deployment Steps

### 1. Create a New Project on Railway

1. Log in to your Railway dashboard at https://railway.app
2. Click the "New Project" button
3. Select "Deploy from GitHub repo"
4. Choose your repository (`daniyalsiddiqui123/backend`)

### 2. Configure the Deployment

**Service Configuration:**
- Railway will automatically detect this as a Python application
- The Dockerfile will be used for building the application
- If no Dockerfile is detected, Railway will use its Python buildpack

**Environment Variables:**
After deployment, go to the "Variables" tab and set the following environment variables:
- `ENVIRONMENT`: `production`
- `DATABASE_URL`: Your production database URL (PostgreSQL recommended)
- `SECRET_KEY`: A strong, random secret key
- `CLIENT_ORIGIN_URL`: Your frontend application's URL
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `QDRANT_URL`: Your Qdrant instance URL
- `QDRANT_API_KEY`: Your Qdrant API key
- `REDIS_URL`: Your Redis instance URL (for rate limiting)

### 3. Optional: Set up PostgreSQL Database on Railway

If you don't have a database yet:
1. In your Railway project, click "New" → "Database"
2. Select "PostgreSQL" and choose "Provision from Railway"
3. Railway will create a PostgreSQL database and automatically set environment variables

### 4. Deploy

1. Railway will automatically build and deploy your application
2. Monitor the build logs in the "Deployments" tab
3. Once complete, your application will be accessible via the assigned URL

### 5. Post-Deployment Configuration

After deployment, you may need to:
1. Run database migrations (if you implement them later)
2. Configure custom domains if needed
3. Set up SSL certificates (handled automatically by Railway)
4. Configure health checks if required

## Important Notes

- The application is configured to only recreate database tables in development mode
- In production (when ENVIRONMENT is set to "production" or "prod"), tables will only be created if they don't exist
- Make sure to properly secure your environment variables
- Consider implementing proper database migration tools like Alembic for production use

## Troubleshooting

- If deployment fails, check the build logs in the Railway dashboard
- Ensure all required environment variables are set
- Verify that your `requirements.txt` includes all necessary dependencies
- Check that your `Dockerfile` is properly configured

## Updating Your Deployment

After making changes to your code:
1. Push updates to your GitHub repository
2. Railway will automatically detect the changes and trigger a new deployment
3. Monitor the deployment logs to ensure successful update

## Alternative: Railway CLI Deployment

You can also deploy using the Railway CLI:
1. Install the Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Link your project: `railway init`
4. Set variables: `railway variables set ENVIRONMENT=production`
5. Deploy: `railway up`

## Important Notes for Railway Deployment

- The application will automatically use the PORT environment variable provided by Railway
- The Procfile and Dockerfile are configured to default to port 8000 if PORT is not set
- Make sure to set all required environment variables in the Railway dashboard
- The application uses environment detection to avoid recreating database tables in production