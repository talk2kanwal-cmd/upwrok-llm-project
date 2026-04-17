import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.middleware import setup_security_middleware, limiter
from app.api.endpoints import router as api_router
from app.core.security import security

# Configure production logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log") if settings.ENVIRONMENT == "production" else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app with production settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Customer Support System with RAG",
    version="2.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None
)

# Setup security middleware
setup_security_middleware(app)

# Rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

app.include_router(api_router, prefix="/api")

@app.get("/health")
@limiter.limit("100/minute")
def health_check():
    """Enhanced health check with system status."""
    try:
        # Test API key availability
        api_key_status = "valid" if settings.GROQ_API_KEY else "missing"
        
        return {
            "status": "ok",
            "project": settings.PROJECT_NAME,
            "environment": settings.ENVIRONMENT,
            "api_key_status": api_key_status,
            "version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.post("/setup-api-key")
def setup_api_key(api_key: str):
    """Securely store API key (for development/setup only)."""
    if settings.ENVIRONMENT == "production":
        raise HTTPException(status_code=403, detail="API key setup not allowed in production")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required")
    
    try:
        security.store_api_key(api_key)
        return {"status": "success", "message": "API key stored securely"}
    except Exception as e:
        logger.error(f"Failed to store API key: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to store API key")

# Static files (mount after all API routes)
from fastapi.staticfiles import StaticFiles
from pathlib import Path
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
