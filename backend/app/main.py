"""
FastAPI Backend for EGFR-NSCLC Clinical Decision Support System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="NG-DX Clinical API",
    description="REST API for EGFR-mutant NSCLC clinical data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "NG-DX Clinical API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health():
    """API health check"""
    return {"status": "healthy"}


@app.get("/api/db/status")
async def db_status():
    """Database connection status and statistics"""
    from backend.app.database import test_connection
    return test_connection()


# Router includes
from backend.app.api import patients, timeline, decisions, alerts

app.include_router(patients.router, prefix="/api", tags=["patients"])
app.include_router(timeline.router, prefix="/api", tags=["timeline"])
app.include_router(decisions.router, prefix="/api", tags=["decisions"])
app.include_router(alerts.router, prefix="/api", tags=["alerts"])

# Static file serving for medical images (must be LAST to avoid route conflicts)
from pathlib import Path
import os

# Get absolute path to static directory
STATIC_DIR = Path(__file__).parent.parent / "static"
STATIC_DIR = STATIC_DIR.resolve()  # Convert to absolute path

print(f"[INFO] Mounting static files from: {STATIC_DIR}")
print(f"[INFO] Static directory exists: {STATIC_DIR.exists()}")

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    print(f"[WARNING] Static directory not found at: {STATIC_DIR}")