"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import router


app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "InterleaveLab API",
        "version": settings.api_version,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    print("🚀 InterleaveLab API started")
    print(f"📖 API Docs available at /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    print("🛑 InterleaveLab API shutting down")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
