# Deployment Guide

This guide explains how to deploy both the backend and frontend of the **Health Live Chat** application on Render. I was unable to obtain access for bedrock or apprunner through the provided aws account. I kept getting permission errors. So as a fallback I used Render for deployment and an OpenAI model.

---

## Backend (FastAPI)

### Overview
The backend is a FastAPI server that handles:
- `/ask` (text queries)
- `/ask_image` (image + text queries)
- Content moderation
- PII redaction
- OpenAI model integration

### Deployment Steps

1. **Repository Setup**
   - Push your backend code to a GitHub repository.

2. **Create New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com).
   - Click **"New Web Service"** > **"From GitHub"**.
   - Connect your repository.

3. **Set Build and Start Commands**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`

4. **Environment Variables**
   Set the following in the **Environment** tab:
   - `API_KEY`: Your internal key 
   - `OPENAI_API_KEY`: Your OpenAI key
   - `USE_BEDROCK`: `false`
   - *(Optional)* `AWS_REGION`, `S3_BUCKET` if using S3

---

## Frontend (React)

### Overview
The frontend is a single-page React app that allows users to:
- Submit symptoms as text and/or image
- View friendly and medically-guided responses from the assistant

### Deployment Steps

1. **Repository Setup**
   - Push your backend code to a GitHub repository.

2. **Create New Static Site on Render**
   - Go to [Render Dashboard](https://dashboard.render.com).
   - Click **"New Static Site"** > **"From GitHub"**.
   - Connect your repository.

1. **Set Build Command**
   From your React frontend folder:
   - **Build Command:** `npm install && npm run build`
