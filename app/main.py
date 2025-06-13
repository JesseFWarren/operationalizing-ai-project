import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline import run_pipeline

app = FastAPI()

# Load API key
API_KEY = os.getenv("API_KEY")

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# check api key
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path == "/ask":
        auth_header = request.headers.get("x-api-key")
        if not auth_header or auth_header != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API key.")
    return await call_next(request)

# input
class QueryRequest(BaseModel):
    query: str

# chatbot endpoint
@app.post("/ask")
def ask(request: QueryRequest):
    """Handles incoming chatbot queries using the modular pipeline."""
    response = run_pipeline(request.query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
