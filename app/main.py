import os
import shutil
import uuid
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline import run_pipeline

app = FastAPI()

# Load API key
API_KEY = os.getenv("API_KEY")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path in ["/ask", "/ask_image"]:
        auth_header = request.headers.get("x-api-key")
        if not auth_header or auth_header != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API key.")
    return await call_next(request)

class QueryRequest(BaseModel):
    query: str

# text
@app.post("/ask")
def ask(request: QueryRequest):
    response = run_pipeline(request.query)
    return {"response": response}

# multi-model
@app.post("/ask_image")
async def ask_image(query: str = Form(...), image: UploadFile = File(None)):
    temp_path = None
    try:
        if image:
            temp_id = str(uuid.uuid4())
            temp_path = f"/tmp/{temp_id}_{image.filename}"
            with open(temp_path, "wb") as f:
                shutil.copyfileobj(image.file, f)
        response = run_pipeline(query, image_path=temp_path)
        return {"response": response}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
