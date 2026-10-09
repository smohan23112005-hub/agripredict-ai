"""AgriPredict AI - FastAPI Backend Application"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.db import engine, Base, init_db
from app.api import weather, farm, crops, risk, finance, dashboard, reports, health
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    print("[INFO] AgriPredict AI starting up...")
    init_db()
    print("[INFO] Database initialized")

    # Ensure directories exist
    os.makedirs("app/ml/models", exist_ok=True)
    os.makedirs("app/data/cache", exist_ok=True)
    os.makedirs("reports_output", exist_ok=True)

    yield
    # Shutdown
    print("[INFO] AgriPredict AI shutting down...")


app = FastAPI(
    title="AgriPredict AI",
    description="Smart Crop Planning & Financial Risk Prediction System for Indian Farmers",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(farm.router, prefix="/api/farm", tags=["Farm"])
app.include_router(crops.router, prefix="/api/crops", tags=["Crops"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk"])
app.include_router(finance.router, prefix="/api/finance", tags=["Finance"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])


@app.get("/")
async def root():
    return {
        "name": "AgriPredict AI",
        "version": "1.0.0",
        "description": "Smart Crop Planning & Financial Risk Prediction System",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
