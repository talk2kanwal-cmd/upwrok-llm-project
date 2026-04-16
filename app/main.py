import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"
import time
import logging
from fastapi import FastAPI, Request
from app.core.config import settings
from app.api.endpoints import router as api_router

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - completed in {process_time:.4f}s - status {response.status_code}")
    return response

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

from fastapi.staticfiles import StaticFiles
from pathlib import Path
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
