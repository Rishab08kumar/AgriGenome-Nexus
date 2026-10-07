from fastapi import APIRouter
from core.schemas import SensorReading
from core.firebase import push_sensor_data, get_latest_sensor_data
from datetime import datetime

router = APIRouter()

sensor_history = []
latest_reading = {}

@router.post("/", response_model=dict)
def post_sensor_data(data: SensorReading):
    global latest_reading

    reading = data.dict()
    reading["soil_moisture"] = data.soil_percent or 0.0
    reading["light_intensity"] = data.lux or 0.0
    reading["timestamp"] = datetime.utcnow().isoformat()

    alerts = []
    if data.temperature and data.temperature > 35:
        alerts.append("Heat stress detected!")
    if data.soil_percent and data.soil_percent < 30:
        alerts.append("Soil dry - pump activated!")
    if data.humidity and data.humidity < 40:
        alerts.append("Low humidity!")
    reading["alerts"] = alerts

    latest_reading = reading
    sensor_history.append(reading)
    if len(sensor_history) > 100:
        sensor_history.pop(0)

    push_sensor_data(reading)

    print(f"Received: Temp={data.temperature}C Humidity={data.humidity}% Soil={data.soil_percent}%")
    return {"status": "success", "message": "Data saved", "data": reading}

@router.get("/latest", response_model=dict)
def get_latest_data():
    if latest_reading:
        return latest_reading
    data = get_latest_sensor_data()
    if data:
        return data
    return {"message": "No data yet - waiting for ESP32"}

@router.get("/history", response_model=list)
def get_history():
    return sensor_history