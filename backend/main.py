from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

from routers import sensor, crop, dosing, plant, harvest, market


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load all ML models on startup so first requests are fast."""
    print("🌱 AgriGenome-Nexus API starting up — loading ML models...")
    from models.crop_recommender import recommender
    from models.dosing_engine import engine
    from models.plant_health import health_model
    from models.harvest_predictor import predictor
    from models.market_forecaster import forecaster
    print("✅ All models loaded successfully!")
    yield
    print("🛑 AgriGenome-Nexus API shutting down.")


app = FastAPI(
    title="AgriGenome-Nexus API",
    description="AI-powered precision agriculture platform — sensor ingestion, ML crop intelligence, and market forecasting.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Vite dev server (5173) and CRA (3000)
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers at exact spec-defined paths
app.include_router(sensor.router,  prefix="/api/sensor-data",       tags=["Sensor Data"])
app.include_router(crop.router,    prefix="/api",                   tags=["Crop Intelligence"])
app.include_router(dosing.router,  prefix="/api",                   tags=["Dosing Decision"])
app.include_router(plant.router,   prefix="/api",                   tags=["Plant Health"])
app.include_router(harvest.router, prefix="/api",                   tags=["Harvest Readiness"])
app.include_router(market.router,  prefix="/api",                   tags=["Market Price"])


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "AgriGenome-Nexus",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
