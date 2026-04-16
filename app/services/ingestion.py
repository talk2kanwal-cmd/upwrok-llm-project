import os
import re
from typing import List, Dict, Any
from io import BytesIO
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentIngestionService:
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 100):
        # User requested: Chunk size: 500-800 tokens, 10-20% overlap.
        # 1 token roughly 4 characters in English text. 600 tokens ≈ 2400 char, 15% overlap ≈ 360 char.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2400,
            chunk_overlap=360,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def clean_text(self, text: str) -> str:
        """Removes excessive whitespace and newline/tab artifacts."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extracts text from a loaded PDF bytes."""
        reader = PdfReader(BytesIO(file_bytes))
        extracted_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)
        return "\n\n".join(extracted_text)

    def process_document(self, file_bytes: bytes, file_name: str) -> List[Dict[str, Any]]:
        """Extracts, cleans, and chunks the document."""
        if file_name.lower().endswith('.pdf'):
            raw_text = self.extract_text_from_pdf(file_bytes)
        elif file_name.lower().endswith('.txt'):
            raw_text = file_bytes.decode('utf-8')
        else:
            raise ValueError("Unsupported file format. Only PDF and TXT are supported for now.")
        
        cleaned_text = self.clean_text(raw_text)
        chunks = self.text_splitter.split_text(cleaned_text)
        
        # Package chunks with metadata
        return [{"text": chunk, "metadata": {"source": file_name, "chunk_index": i}} for i, chunk in enumerate(chunks)]

ingestion_service = DocumentIngestionService()
