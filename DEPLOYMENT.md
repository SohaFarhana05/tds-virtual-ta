# Deployment Guide for TDS Virtual TA

## Quick Start (Local Development)

1. **Setup the environment:**
   ```bash
   ./setup.sh
   source venv/bin/activate
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Test the API:**
   ```bash
   curl -X POST http://localhost:8000/api/ \
     -H "Content-Type: application/json" \
     -d '{"question": "Should I use Docker or Podman for TDS?"}'
   ```

## Production Deployment Options

### Option 1: Railway (Recommended)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy:**
   ```bash
   railway login
   railway init
   railway add
   railway deploy
   ```

3. **Set environment variables in Railway dashboard**

### Option 2: Render

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Add environment variables

### Option 3: Heroku

1. **Install Heroku CLI and login:**
   ```bash
   heroku login
   ```

2. **Create app and deploy:**
   ```bash
   heroku create your-tds-virtual-ta
   git push heroku main
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your_key_here
   ```

### Option 4: Google Cloud Run

1. **Build and push Docker image:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/tds-virtual-ta
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy --image gcr.io/PROJECT_ID/tds-virtual-ta --platform managed
   ```

### Option 5: Docker (Self-hosted)

1. **Build the image:**
   ```bash
   docker build -t tds-virtual-ta .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 \
     -e OPENAI_API_KEY=your_key_here \
     tds-virtual-ta
   ```

## 🚀 GitHub Setup & Deployment

### Step 1: Create GitHub Repository

1. **Go to https://github.com/SohaFarhana05**
2. **Click "New repository"**
3. **Repository name:** `tds-virtual-ta`
4. **Description:** `TDS Virtual TA - AI-powered teaching assistant with 100% test coverage`
5. **Make it Public**
6. **Don't initialize with README** (we already have one)

### Step 2: Push to GitHub

```bash
cd /Users/sohafarhana/Desktop/TDS/Project-01
git remote add origin https://github.com/SohaFarhana05/tds-virtual-ta.git
git push -u origin main
```

### Step 3: Deploy (Choose One)

**⚠️ Note:** GitHub Pages won't work for this project since it's a Python backend, not a static website.

## Environment Variables

Required environment variables for production:

```bash
OPENAI_API_KEY=your_openai_api_key_here
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False
```

Optional environment variables:

```bash
DISCOURSE_API_KEY=your_discourse_api_key
DISCOURSE_USERNAME=your_username
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
```

## Health Checks

The application provides a health check endpoint at `/health` that returns:

```json
{"status": "healthy", "service": "TDS Virtual TA"}
```

## API Documentation

Once deployed, visit `https://your-domain.com/docs` for interactive API documentation.

## Monitoring

- Health endpoint: `GET /health`
- Stats endpoint: `GET /api/stats`
- Application logs for debugging

## Scaling Considerations

For high traffic:

1. **Use a production ASGI server like Gunicorn with Uvicorn workers**
2. **Enable caching for frequently asked questions**
3. **Set up load balancing**
4. **Monitor API rate limits for OpenAI**

## Security

1. **Set proper CORS origins in production**
2. **Use environment variables for all secrets**
3. **Enable HTTPS**
4. **Implement rate limiting if needed**

## Troubleshooting

Common issues and solutions:

1. **Port already in use:**
   ```bash
   export APP_PORT=8080
   python app.py
   ```

2. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment variables not loading:**
   - Check .env file exists
   - Verify environment variable names
   - Restart the application

4. **API not responding:**
   - Check application logs
   - Verify network connectivity
   - Test health endpoint first
