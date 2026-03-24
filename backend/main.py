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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_engine = RAGEngine()

@app.on_event("startup")
async def startup_event():
    # Ensure data directory exists and process PDFs
    if not os.path.exists("data"):
        os.makedirs("data")
    rag_engine.initialize()

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
