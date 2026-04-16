# 🚀 AI Customer Support Hub (RAG System)

AI-Powered Intelligent Customer Support System is a Retrieval-Augmented Generation (RAG) based solution that leverages Large Language Models (LLMs) to provide accurate, context-aware responses to user queries. The system processes company documents (PDFs, FAQs, manuals), retrieves relevant information using a vector database, and generates intelligent answers through an LLM. It is built with a scalable FastAPI backend, integrates semantic search, and follows MLOps practices for deployment, monitoring, and continuous improvement.
---

## 🔥 Key Features

- **Blazing Fast Inferences**: Generates answers in milliseconds using **Groq** (`llama-3.1-8b-instant`).
- **Cost-Efficient Local Embeddings**: Employs Hugging Face's `all-MiniLM-L6-v2` to vectorize and embed documents entirely locally for free.
- **Robust Semantic Search**: Local persistence using **FAISS** vector database to reliably retrieve the most prominent context passages.
- **Strict Grounding (No Hallucinations)**: The LLM pipeline explicitly restricts answers to *only* what is covered in your documents.
- **Premium Glassmorphic UI**: Entirely native HTML/Vanilla JS frontend with beautiful dark space gradients natively mounted through FastAPI `StaticFiles`.
- **Production-Ready Endpoints**: Modular REST API design leveraging `FastAPI`.
- **Containerized Integration**: One-command reliable deployment setup via `docker-compose`.

## 🛠 Extensive Tech Stack

**Frontend Interfaces**
- **Streamlit**: Dedicated Python-based chat dashboard (`app.py`).
- **Vanilla HTML/CSS/JS**: A custom, lightweight, glassmorphic UI hosted natively.

**Backend & Server**
- **FastAPI**: Core Python RESTful routing and API service.
- **Uvicorn**: High-performance ASGI web server.

**AI & RAG Engine**
- **LangChain**: AI orchestration and document processing.
- **Groq**: Extremely fast generative inference engine running Meta's `llama-3.1-8b-instant`.
- **Sentence-Transformers**: Open-source HuggingFace models for dense vector embeddings.
- **FAISS**: Facebook AI Similarity Search architecture for local, efficient nearest neighbor search.
- **PyPDF**: Automated document extraction and parsing.

**DevOps & Infrastructure**
- **Docker & Docker Compose**: Complete environment containerization.
- **GitHub Actions**: Continuous Integration pipeline for code validation.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.10+
- [Git](https://git-scm.com/)
- API Key from [Groq Console](https://console.groq.com/keys)

### 2. Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-customer-support.git
   cd ai-customer-support
   ```
2. Create and activate a Virtual Environment (Recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows
   ```
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Environment Variables
Create a `.env` file at the root of your project containing your authentication token:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run Locally
Execute the backend:
```bash
python -m uvicorn app.main:app --port 8000
```
Open **[http://localhost:8000/](http://localhost:8000/)** precisely in your browser to experience the beautiful interface. Swagger UI sandbox is available at `/docs`.

### 5. Running with Docker (Alternative)
To instantly spool the service in an isolated environment without Python dependencies:
```bash
docker-compose up --build
```

---

## 🏗 System Architecture

The workflow consists of two primary endpoints:

1. **Ingestion Layer [`POST /api/upload`]**  
   Accepts raw PDFs/Text arrays and passes them through a PyPDF extraction phase. Langchain's Text Splitter fragments the data into ~500-token chunks with 100-token overlaps. The sentence-transformer binds them mathematically and saves the FAISS index cleanly into persistent local storage.

2. **RAG Pipeline [`POST /api/chat`]**  
   Takes an end-user query, mathematically computes its semantic proximity using the local FAISS index, retrieves the top top-matching segments, strings them cleanly inside an aggressive system prompt, and relays it into Groq API for deterministic contextualization.

---

*Developed by Sumara kanwal*
