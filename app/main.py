from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline import run_pipeline

app = FastAPI()

# CORS config 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# route to call run pipeline
@app.post("/ask")
def ask(request: QueryRequest):
    """Handles incoming chatbot queries using the modular pipeline."""
    response = run_pipeline(request.query)
    return {"response": response}

# run config
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
