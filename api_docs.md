# API Documentation

This document outlines the available API endpoints for the **HealthLiveChat** system, which includes a FastAPI backend for handling both text and image-based health queries.  

---

## Base URL

- **Production (Render)**: https://healthlivechatbackend.onrender.com

---

## Endpoints

### 1. POST /ask

Handles text-only health questions

- `Content-Type: application/json`
- `x-api-key: YOUR_API_KEY`

#### Request Example

```json
{
  "query": "What are the symptoms of dehydration?"
}
```
#### Response Example
```json
{
  "response": "Some common symptoms of dehydration include dry mouth, fatigue, dizziness, and dark-colored urine."
}
```

## 2. POST /ask_image

Handles health questions that include an image 

### Headers

- `Content-Type: multipart/form-data`
- `x-api-key: YOUR_API_KEY`

### Form Fields

- `query`: *(string)* The user's question  
- `image`: *(file, optional)* An image file (.jpg, .png, etc.)

### Curl Example

```bash
curl -X POST https://healthlivechatbackend.onrender.com/ask_image \
  -H "x-api-key: YOUR_API_KEY" \
  -F "query=Does this look infected?" \
  -F "image=@rash.jpg"
```

### Response Example

```json
{
  "response": "The image shows signs that may indicate an infection. Please consult a healthcare provider."
}
```

## Authorization

All endpoints require an API key.  

Pass your API key in the request header: 'x-api-key: YOUR_API_KEY'  
If your request does not include a valid API key, the server will respond with:

```json
{
  "detail": "Unauthorized: Invalid or missing API key."
}
```

## Additional Notes
If no image is included in /ask_image, it behaves the same as /ask.  
Ensure your API key is securely stored and passed from the frontend or testing tool.  