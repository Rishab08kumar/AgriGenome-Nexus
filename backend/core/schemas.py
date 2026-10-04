from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SensorReading(BaseModel):
    soil_moisture: float
    humidity: float
    temperature: float
    light_intensity: float
    nitrogen: float
    phosphorus: float
    potassium: float
    ec: float
    ph: Optional[float] = None
    weight: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CropRecommendationInput(BaseModel):
    latitude: float
    longitude: float
    soil_moisture: float
    humidity: float
    temperature: float
    light_intensity: float
    nitrogen: float
    phosphorus: float
    potassium: float
    ec: float
    ph: Optional[float] = None

class DosingDecisionInput(BaseModel):
    soil_moisture: float
    humidity: float
    temperature: float
    light_intensity: float
    nitrogen: float
    phosphorus: float
    potassium: float
    ec: float
    ph: Optional[float] = None
    crop_variety: str

class HarvestReadinessInput(BaseModel):
    days_since_planting: int
    cumulative_temperature: float
    cumulative_light: float
    soil_moisture: float
    crop_variety: str

class MarketPriceInput(BaseModel):
    crop_variety: str
    region: str
    season: str
    yield_grade: str
    date: str

class CropRecommendationResponse(BaseModel):
    crop_variety: str
    genomic_strain: str
    confidence: float

class DosingDecisionResponse(BaseModel):
    pump_on: bool
    valve_open: bool
    nutrient_dose_ml: float
    reasons: List[str]

class PlantHealthResponse(BaseModel):
    label: str
    confidence: float
    bounding_boxes: List[dict]

class HarvestReadinessResponse(BaseModel):
    maturity_score: float
    days_to_harvest: int
    alert: bool
    message: str

class MarketPriceResponse(BaseModel):
    predicted_price: float
    price_range_low: float
    price_range_high: float
    currency: str = "INR"
    unit: str = "per quintal"
