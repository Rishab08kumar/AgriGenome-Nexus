import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


# 1. Define Lifespan Manager First
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load all ML models on startup so first requests are fast."""
    print("🌱 AgriGenome-Nexus API starting up — loading ML models...")
    from models.crop_recommender import recommender
    from models.dosing_engine import engine
    from models.harvest_predictor import predictor
    from models.market_forecaster import forecaster
    from scripts.plant_health import health_model

    print("✅ All models loaded successfully!")
    yield
    print("🛑 AgriGenome-Nexus API shutting down.")


# 2. Initialize FastAPI App
app = FastAPI(
    title="AgriGenome-Nexus API",
    description="AI-powered precision agriculture platform — sensor ingestion, ML crop intelligence, and market forecasting.",
    version="1.0.0",
    lifespan=lifespan,
)

# 3. Configure CORS Origins
allowed_origins = [
    "https://agri-genome-nexus-31pc.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

env_origins = os.getenv("CORS_ORIGINS", "")
if env_origins:
    allowed_origins.extend([origin.strip() for origin in env_origins.split(",") if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Import & Mount Routers
from routers import crop, dosing, harvest, market, plant, sensor

app.include_router(sensor.router, prefix="/api/sensor-data", tags=["Sensor Data"])
app.include_router(crop.router, prefix="/api", tags=["Crop Intelligence"])
app.include_router(dosing.router, prefix="/api", tags=["Dosing Decision"])
app.include_router(plant.router, prefix="/api", tags=["Plant Health"])
app.include_router(harvest.router, prefix="/api", tags=["Harvest Readiness"])
app.include_router(market.router, prefix="/api", tags=["Market Price"])


# 5. Root & Health Check Endpoints
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