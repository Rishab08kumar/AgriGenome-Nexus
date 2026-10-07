from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SensorReading(BaseModel):
    device_id: Optional[str] = "ESP32-SMART-001"
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    soil_raw: Optional[int] = None
    soil_percent: Optional[float] = None
    soil_dry: Optional[bool] = None
    lux: Optional[float] = None
    ldr_raw: Optional[int] = None
    ads0: Optional[int] = None
    ads1: Optional[int] = None
    latitude: Optional[float] = 0.0
    longitude: Optional[float] = 0.0
    altitude: Optional[float] = 0.0
    pump_status: Optional[bool] = False
    crop: Optional[str] = "tomato"
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    soil_moisture: Optional[float] = None
    light_intensity: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    ec: Optional[float] = None
    ph: Optional[float] = None
    weight: Optional[float] = None

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