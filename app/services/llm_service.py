import os
from pydantic import BaseModel
from groq import Groq
from app.core.config import settings

class RAGQueryService:
    def __init__(self):
        api_key = settings.GROQ_API_KEY
        if api_key == "your_groq_api_key_here" or not api_key:
            print("WARNING: Groq API Key is not set or using the default placeholder.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant" # Fast, cost-efficient open weights model

    def generate_response(self, query: str, context_documents: list) -> str:
        """Generates a response using OpenAI, strictly bounded by the retrieved context."""
        
        # Combine retrieved contexts
        context_text = "\n\n".join([doc.page_content for doc in context_documents])
        
        system_prompt = (
            "You are a helpful and intelligent customer support assistant.\n"
            "You must answer the user's question STRICTLY using the provided context below.\n"
            "If the answer is not contained in the context, you must reply identically: "
            "'I do not have enough information to answer that question based on the provided documents.'\n"
            "Do not hallucinate, make up facts, or rely on outside knowledge.\n\n"
            "### Context ###\n"
            f"{context_text}"
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.0 # Lowest temperature to enforce strict determinism
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error connecting to LLM service: {str(e)}"

rag_service = RAGQueryService()
