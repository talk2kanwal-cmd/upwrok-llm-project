# AI Customer Support Hub (RAG System)

[![CI Pipeline](https://github.com/yourusername/ai-customer-support/actions/workflows/main.yml/badge.svg)](https://github.com/yourusername/ai-customer-support/actions/workflows/main.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-Powered Intelligent Customer Support System is a Retrieval-Augmented Generation (RAG) based solution that leverages Large Language Models (LLMs) to provide accurate, context-aware responses to user queries. The system processes company documents (PDFs, FAQs, manuals), retrieves relevant information using a vector database, and generates intelligent answers through an LLM. It is built with a scalable FastAPI backend, integrates semantic search, and follows MLOps practices for deployment, monitoring, and continuous improvement.

---

## Key Features

- **Blazing Fast Inferences**: Generates answers in milliseconds using **Groq** (`llama-3.1-8b-instant`)
- **Cost-Efficient Local Embeddings**: Employs Hugging Face's `all-MiniLM-L6-v2` to vectorize and embed documents entirely locally for free
- **Robust Semantic Search**: Local persistence using **FAISS** vector database to reliably retrieve the most prominent context passages
- **Strict Grounding (No Hallucinations)**: The LLM pipeline explicitly restricts answers to *only* what is covered in your documents
- **Production-Ready Security**: API key encryption, rate limiting, security headers, and monitoring
- **Dual Frontend Options**: Streamlit chat interface and native HTML/CSS/JS UI
- **Containerized Deployment**: One-command reliable deployment setup via `docker-compose`

---
 Retrieval-Augmented Generation (RAG) system with these key components:

Backend (FastAPI)
FastAPI Server: RESTful API handling requests
Vector Database (FAISS): Stores document embeddings
Embedding Service: Converts text to vectors using HuggingFace
LLM Integration: Groq API for intelligent responses
Security Layer: API key encryption, rate limiting, headers
Frontend (Streamlit)
Web Interface: User-friendly chat and file upload
Real-time Communication: API calls to backend
Document Management: Upload and index files
--
## System Architecture

### High-Level Overview

```
User Interface (Streamlit/Web)
       |
       v
FastAPI Backend
       |
       v
RAG Pipeline
       |
       v
Vector Database (FAISS) + LLM (Groq)
```

### Core Components

#### 1. **Ingestion Layer** [`POST /api/upload`]
- **Document Processing**: Accepts PDFs and text files
- **Text Extraction**: PyPDF handles PDF parsing with encoding detection
- **Chunking**: RecursiveCharacterTextSplitter creates ~600-token chunks with 100-token overlaps
- **Embedding**: Sentence-transformers convert chunks to dense vectors
- **Storage**: FAISS index persists vectors with metadata (filename, chunk index)

#### 2. **Query Pipeline** [`POST /api/chat`]
- **Query Processing**: User questions converted to vectors
- **Semantic Search**: FAISS retrieves top-k similar chunks
- **Context Assembly**: Retrieved chunks formatted with source citations
- **LLM Generation**: Groq receives strict prompt to use only provided context
- **Response Grounding**: Answers returned with source references

#### 3. **Security Layer**
- **API Key Encryption**: Fernet symmetric encryption for secure storage
- **Rate Limiting**: Redis-based limiting (10 uploads/min, 30 chats/min)
- **Security Headers**: XSS, CSRF, HSTS protection
- **CORS Management**: Restricted to allowed origins
- **Production Logging**: Structured logging with monitoring

#### 4. **Frontend Interfaces**
- **Streamlit Dashboard**: Python-based chat interface with file upload
- **Native Web UI**: Glassmorphic design with dark gradients

---

## Technology Stack

### Frontend
- **Streamlit**: Interactive Python web interface
- **HTML/CSS/JavaScript**: Custom lightweight UI
- **Responsive Design**: Mobile-friendly interface

### Backend & API
- **FastAPI**: High-performance async web framework
- **Uvicorn**: ASGI server with production optimizations
- **Pydantic**: Data validation and serialization

### AI & Machine Learning
- **LangChain**: AI orchestration and document processing
- **Groq**: Ultra-fast LLM inference (Meta's Llama 3.1)
- **Sentence-Transformers**: Open-source embedding models
- **FAISS**: Facebook AI Similarity Search for vector operations
- **PyPDF**: Document extraction and parsing

### Security & Infrastructure
- **Cryptography**: Fernet encryption for API keys
- **Redis**: Rate limiting and caching
- **Docker & Docker Compose**: Containerization
- **Nginx**: Reverse proxy with SSL termination
- **GitHub Actions**: CI/CD pipeline

---

## API Endpoints

### Core Endpoints
- `POST /api/upload` - Document ingestion and indexing
- `POST /api/chat` - Query processing and response generation
- `GET /health` - System health check and status
- `POST /setup-api-key` - Secure API key storage (development only)

### Security Features
- **Rate Limiting**: Prevents abuse with Redis-based limits
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Graceful error responses with logging
- **Monitoring**: Production-ready logging and metrics

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- [Git](https://git-scm.com/)
- API Key from [Groq Console](https://console.groq.com/keys)
- Redis (for production rate limiting)

### Quick Start

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/ai-customer-support.git
   cd ai-customer-support
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: `.venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your Groq API key
   ```

5. **Start Backend**
   ```bash
   python -m uvicorn app.main:app --port 8000
   ```

6. **Start Frontend**
   ```bash
   # Option 1: Streamlit
   streamlit run streamlit_app.py
   
   # Option 2: Native UI (automatically served)
   # Visit http://localhost:8000/
   ```

### Environment Variables

```env
# Core Configuration
GROQ_API_KEY=your_groq_api_key_here
ENVIRONMENT=development

# Production Settings
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=http://localhost:8501,https://yourdomain.com

# Logging
LOG_LEVEL=INFO
```

---

## Production Deployment

### Docker Deployment

1. **Development Docker**
   ```bash
   docker-compose up --build
   ```

2. **Production Docker**
   ```bash
   # Create production environment
   cp env.production.example .env.production
   
   # Deploy with SSL and monitoring
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Production Architecture

```
Internet
    |
    v
Nginx (SSL Termination, Rate Limiting)
    |
    v
FastAPI (Multiple Workers)
    |
    v
Redis (Rate Limiting, Caching)
    |
    v
FAISS + Groq API
```

### Security Configuration

- **SSL/TLS**: Automatic certificate management
- **API Key Encryption**: Fernet-based secure storage
- **Rate Limiting**: Prevents DDoS and abuse
- **Security Headers**: XSS, CSRF, HSTS protection
- **CORS**: Restricted to trusted domains
- **Monitoring**: Structured logging and health checks

---

## Usage Guide

### Document Upload
1. Access the Streamlit interface at `http://localhost:8501`
2. Use the sidebar to upload PDF or text files
3. Files are automatically processed and indexed
4. System confirms successful ingestion

### Chat Interaction
1. Type questions in the chat interface
2. System retrieves relevant document chunks
3. LLM generates grounded responses
4. Source citations provided for verification

### API Usage
```python
import requests

# Upload document
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )

# Chat query
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'query': 'What are the key features?'}
)
```

---

## Testing

### Run Test Suite
```bash
# Basic tests
pytest

# With coverage
pytest --cov=app

# Integration tests
pytest tests/test_api.py -v
```

### Test Coverage
- API endpoint functionality
- Document processing pipeline
- Security features
- Error handling

---

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Contributing
1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

See [Contributing Guidelines](CONTRIBUTING.md) for detailed instructions.

---

## Monitoring & Maintenance

### Health Checks
- `GET /health` - System status and metrics
- Automatic health monitoring in production
- Docker health checks for container management

### Logging
- Structured JSON logging in production
- Request/response logging for debugging
- Error tracking and alerting

### Performance
- Vector search optimization with FAISS
- Async processing for concurrent requests
- Connection pooling for external APIs

---

## Troubleshooting

### Common Issues
- **API Key Errors**: Verify Groq API key in `.env`
- **Encoding Issues**: System handles multiple text encodings
- **Memory Issues**: FAISS optimized for large document sets
- **Rate Limiting**: Adjust Redis configuration if needed

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python -m uvicorn app.main:app --reload --port 8000
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For questions and support:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation at `/docs`


---
## API Endpoints
POST /api/upload: Document ingestion
POST /api/chat: Query processing
GET /health: System status
POST /setup-api-key: Secure key storage
Frontend Features
File upload with progress indicators
Real-time chat interface
Source citation display
Error handling and feedback
🚀 Production Deployment
Docker Setup
Multi-stage builds: Optimized production images
Nginx Proxy: SSL termination, load balancing
Redis: Rate limiting and caching
Health Checks: Automatic restarts
--
Security Features
API Key Management
Encryption: Fernet encryption for secure storage
Environment Variables: Cloud deployment support
File Permissions: 0o600 restricted access

Production Security

Rate Limiting: 10 uploads/min, 30 chats/min
Security Headers: XSS, CSRF, HSTS protection
CORS: Restricted to allowed origins
Logging: Production-ready monitoring
---
*Developed by Sumara Kanwal with FastAPI, LangChain, and Groq for enterprise-ready AI customer support*
