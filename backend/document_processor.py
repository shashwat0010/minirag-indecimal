import os
from pypdf import PdfReader
from typing import List, Dict

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extracts text from a PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def split_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Splits text into chunks more intelligently based on sections/paragraphs."""
        # Try to split by Markdown headers first to preserve semantic sections
        sections = text.split("\n## ")
        chunks = []
        
        for section in sections:
            # If section is too small, combine or handle as is
            if len(section) < self.chunk_size:
                chunks.append({
                    "content": section.strip(),
                    "metadata": metadata or {}
                })
            else:
                # If section is too large, use a sliding window approach
                start = 0
                while start < len(section):
                    end = start + self.chunk_size
                    # Try to find a good breaking point (newline)
                    if end < len(section):
                        last_newline = section.rfind("\n", start, end)
                        if last_newline != -1 and last_newline > start:
                            end = last_newline
                    
                    chunk_text = section[start:end].strip()
                    if chunk_text:
                        chunks.append({
                            "content": chunk_text,
                            "metadata": metadata or {}
                        })
                    start += self.chunk_size - self.chunk_overlap
        return chunks

    def process_directory(self, directory_path: str) -> List[Dict]:
        """Processes all PDF and Markdown files in a directory."""
        all_chunks = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if filename.endswith(".pdf"):
                text = self.extract_text_from_pdf(file_path)
                chunks = self.split_text(text, metadata={"source": filename})
                all_chunks.extend(chunks)
            elif filename.endswith(".md") or filename.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                chunks = self.split_text(text, metadata={"source": filename})
                all_chunks.extend(chunks)
        return all_chunks
