import os
from typing import Dict, List

from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_client import LLMClient
from local_llm_client import LocalLLMClient


class RAGEngine:
    def __init__(self, data_dir: str = "data"):
        self.doc_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
        self.local_llm_client = None  # Lazy‑loaded
        self.data_dir = data_dir

    def initialize(self):
        """Process all documents in the data directory and ingest them into the vector store."""
        if os.path.exists(self.data_dir) and os.path.isdir(self.data_dir):
            chunks = self.doc_processor.process_directory(self.data_dir)
            if chunks:
                self.vector_store.add_documents(chunks)

    async def answer_question(self, question: str) -> Dict:
        """
        Retrieve relevant context from the vector store and generate an answer
        strictly based only on that context (closed‑book RAG).
        """
        # Step 1: Retrieve top‑k relevant chunks
        relevant_chunks = self.vector_store.search(question)
        if not relevant_chunks:
            return {
                "response": "I cannot answer this question because the required information is not in the provided documents.",
                "chunks": [],
            }

        # Step 2: Build concise context (optional: limit tokens if needed)
        context_parts = []
        for chunk in relevant_chunks:
            content = chunk["content"].strip()
            if content:
                context_parts.append(content)
        context = "\n\n".join(context_parts)

        # Step 3: Generate answer using LLM, constrained to the context
        prompt = f"""
You are an assistant that answers questions using only the provided context.
If the answer is not in the context, respond with:
"I cannot answer this question based on the documents provided."

Context:
{context}

Question:
{question}

Answer:
""".strip()

        try:
            # Try cloud LLM first
            response = await self.llm_client.generate_response(
                prompt=prompt,
                context=context,  # if your LLMClient uses this explicitly
            )
        except Exception as e:
            print(f"Cloud LLM failed: {e}. Falling back to local model...")
            if self.local_llm_client is None:
                self.local_llm_client = LocalLLMClient()
            response = await self.local_llm_client.generate_response(prompt=prompt, context=context)

        return {
            "response": response,
            "chunks": relevant_chunks,
        }
