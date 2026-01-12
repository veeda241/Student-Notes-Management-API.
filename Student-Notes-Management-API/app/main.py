"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routes import notes_router
from .database import engine, SessionLocal
from .models.note import Base
from .database.seeder import seed_database

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed database
try:
    db = SessionLocal()
    seed_database(db)
finally:
    db.close()

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Notes",
            "description": "Operations for managing student notes - Create, Read, Update, Delete"
        },
        {
            "name": "Health",
            "description": "Health check and status endpoints"
        }
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root endpoint serves frontend
@app.get("/", include_in_schema=False)
async def read_root():
    return FileResponse('app/static/index.html')


# Health check endpoint
@app.get("/health", tags=["Health"], summary="Health check")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status information
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# API Information endpoint
@app.get("/info", tags=["Health"], summary="API Information")
async def api_info():
    """
    Get detailed API information.
    
    Returns:
        dict: API details and available endpoints
    """
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "endpoints": {
            "documentation": "/docs",
            "alternative_docs": "/redoc",
            "openapi_schema": "/openapi.json",
            "health": "/health",
            "notes": f"{settings.API_V1_PREFIX}/notes"
        }
    }


# Include routers
app.include_router(notes_router, prefix=settings.API_V1_PREFIX)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} is starting...")
    print(f"📚 Documentation available at: http://{settings.HOST}:{settings.PORT}/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    print(f"👋 {settings.APP_NAME} is shutting down...")
