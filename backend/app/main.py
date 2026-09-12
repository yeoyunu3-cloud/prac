"""FastAPI main application"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import API router
from app.api import router

# Create FastAPI app
app = FastAPI(
    title="YouTube Lecture Summarizer API",
    description="Summarize YouTube lectures using Claude AI",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
if isinstance(cors_origins, str):
    cors_origins = [cors_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)

# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting YouTube Lecture Summarizer API")
    
    # Check environment variables
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.warning("ANTHROPIC_API_KEY not set - API will not work")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "YouTube Lecture Summarizer API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint at root"""
    return {
        "status": "ok",
        "service": "YouTube Lecture Summarizer API"
    }


if __name__ == "__main__":
    import uvicorn
    
    debug = os.getenv("DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    )
