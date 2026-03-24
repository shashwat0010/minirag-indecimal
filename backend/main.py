from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Force transformers to use PyTorch
os.environ["USE_TORCH"] = "1"
os.environ["USE_TF"] = "0"

from rag_engine import RAGEngine

app = FastAPI()

# CORS configuration
allowed_origins = [
    os.getenv("FRONTEND_URL", "http://localhost:5173"),
    "https://*.vercel.app",  # Allow Vercel preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if os.getenv("ENVIRONMENT") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = RAGEngine()

@app.on_event("startup")
async def startup_event():
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Initialize in a separate thread to avoid blocking uvicorn startup
    # This allows Render health check to pass immediately
    import threading
    threading.Thread(target=rag_engine.initialize, daemon=True).start()
    print("Initialization started in background.")

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    try:
        result = await rag_engine.answer_question(query.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "RAG API is running"}
