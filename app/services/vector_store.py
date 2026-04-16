import os
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class VectorStoreService:
    def __init__(self, persist_dir: str = "./faiss_index"):
        self.persist_dir = persist_dir
        # Initialize HuggingFace embeddings
        # The user requested: sentence-transformers/all-MiniLM-L6-v2
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}, 
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vector_store = None
        self._load_or_create_index()

    def _load_or_create_index(self):
        """Loads an existing FAISS index or creates a placeholder if empty."""
        if os.path.exists(self.persist_dir) and os.listdir(self.persist_dir):
            try:
                # Local development often requires allowing deserialization for FAISS
                self.vector_store = FAISS.load_local(self.persist_dir, self.embeddings, allow_dangerous_deserialization=True)
                print(f"Loaded existing FAISS index from {self.persist_dir}")
            except Exception as e:
                print(f"Error loading FAISS index: {e}. Will create a new one.")
                self.vector_store = None
        else:
            self.vector_store = None
            
    def store_documents(self, chunks: List[Dict[str, Any]]) -> bool:
        """Stores a list of chunked documents into the FAISS index."""
        docs = [Document(page_content=chunk["text"], metadata=chunk["metadata"]) for chunk in chunks]
        
        if self.vector_store is None:
            # Initialize FAISS with the first documents
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
        else:
            self.vector_store.add_documents(docs)
            
        # Persist index
        self._persist_index()
        return True

    def _persist_index(self):
        """Saves the index to disk."""
        if self.vector_store:
            self.vector_store.save_local(self.persist_dir)

    def retrieve_context(self, query: str, top_k: int = 4) -> List[Document]:
        """Retrieves the top_k most similar documents to the query."""
        if not self.vector_store:
            return []
        
        results = self.vector_store.similarity_search(query, k=top_k)
        return results

vector_store_service = VectorStoreService()
