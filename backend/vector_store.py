import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self.index = None
        self.metadata = []

    @property
    def model(self):
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}...")
            self._model = SentenceTransformer(self.model_name)
            print("Embedding model loaded.")
        return self._model

    def add_documents(self, chunks: List[Dict]):
        """Adds documents to the FAISS index."""
        texts = [chunk["content"] for chunk in chunks]
        embeddings = self.model.encode(texts)
        
        dimension = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)
            
        self.index.add(np.array(embeddings).astype('float32'))
        self.metadata.extend(chunks)

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Searches the index for relevant documents."""
        if self.index is None:
            return []
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.metadata[idx])
        return results
