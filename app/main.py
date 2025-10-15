from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.core.config import settings
from app.api.recipes import router as recipes_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A RESTful API for managing and searching recipes",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include API routers
app.include_router(recipes_router, prefix=settings.API_V1_STR, tags=["recipes"])


@app.get("/")
async def root():
    """Root endpoint - serves index.html if available, otherwise returns API info"""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))

    return {
        "message": "Welcome to Recipe API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
