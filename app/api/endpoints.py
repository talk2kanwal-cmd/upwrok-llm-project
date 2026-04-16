from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

from app.services.ingestion import ingestion_service
from app.services.vector_store import vector_store_service
from app.services.llm_service import rag_service

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    query: str
    response: str
    context_sources: List[str]

@router.post("/upload", tags=["Ingestion"])
async def upload_document(file: UploadFile = File(...)):
    """Uploads a PDF or text document, chunks it, and adds it to the vector database."""
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    
    try:
        contents = await file.read()
        
        # Phase 2: Ingest, clean, and chunk
        chunks = ingestion_service.process_document(contents, file.filename)
        
        if not chunks:
            return {"status": "warning", "message": "No text could be extracted from the document."}
        
        # Phase 3 & 4: Create embeddings and store in FAISS
        vector_store_service.store_documents(chunks)
        
        return {
            "status": "success",
            "message": f"Successfully processed '{file.filename}'",
            "chunks_created": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/chat", response_model=ChatResponse, tags=["Retrieval & Generation"])
async def chat_with_bot(request: ChatRequest):
    """Processes a user query by retrieving context and calling the LLM."""
    try:
        # Phase 5: Semantic Retrieval from FAISS
        docs = vector_store_service.retrieve_context(request.query)
        
        # Phase 6: Language Model generation with strict prompt
        response_text = rag_service.generate_response(request.query, docs)
        
        # Extract unique sources for transparency
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
        
        return ChatResponse(
            query=request.query,
            response=response_text,
            context_sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
