
from fastapi import APIRouter, Request, HTTPException
from core.schemas import SensorReading
from core.firebase import push_sensor_data, get_latest_sensor_data
from datetime import datetime, timezone

router = APIRouter()

sensor_history = []
latest_reading = {}


@router.post("/", response_model=dict)
async def post_sensor_data(
    data: SensorReading,
    request: Request
):
    global latest_reading

    # Validated sensor fields from the existing schema
    reading = (
        data.model_dump()
        if hasattr(data, "model_dump")
        else data.dict()
    )

    # Original ESP32 JSON, including additional
    # hardware status fields
    raw = await request.json()

    # Preserve ESP32-reported pump state
    pump = raw.get("pump_status")

    if pump is not None and not isinstance(pump, bool):
        raise HTTPException(
            status_code=422,
            detail="pump_status must be true or false"
        )

    reading["pump_status"] = pump

    # Preserve valid device and GPS information
    device_id = raw.get("device_id")
    if isinstance(device_id, str):
        reading["device_id"] = device_id[:100]

    for field in ("latitude", "longitude", "altitude"):
        value = raw.get(field)
        if value is None:
            reading[field] = None
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            reading[field] = float(value)

    # Preserve moisture and light without fake zeros
    reading["soil_moisture"] = data.soil_percent
    reading["light_intensity"] = data.lux

    reading["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    alerts = []

    if data.temperature is not None and data.temperature > 35:
        alerts.append("Heat stress detected!")

    if data.soil_percent is not None and data.soil_percent < 30:
        alerts.append("Soil moisture below threshold")

    if data.humidity is not None and data.humidity < 40:
        alerts.append("Low humidity!")

    if pump is True:
        alerts.append("ESP32 reports pump ON")

    reading["alerts"] = alerts

    # Existing in-memory cache
    latest_reading = reading
    sensor_history.append(reading)

    if len(sensor_history) > 100:
        sensor_history.pop(0)

    # Existing Firebase integration
    try:
        push_sensor_data(reading)
    except Exception as exc:
        print("Firebase storage error:", exc)

    print(
        "ESP32 received:",
        "Soil =", data.soil_percent,
        "Pump =", pump,
        "Temperature =", data.temperature
    )

    return {
        "status": "success",
        "message": "Sensor data received",
        "data": reading
    }


@router.get("/latest", response_model=dict)
def get_latest_data():
    # Query persistent storage first when available
    try:
        stored = get_latest_sensor_data()
        if isinstance(stored, dict) and stored:
            if "timestamp" in stored:
                return stored
    except Exception as exc:
        print("Firebase read error:", exc)

    if latest_reading:
        return latest_reading

    return {
        "message": "No live ESP32 data available",
        "pump_status": None,
        "timestamp": None
    }


@router.get("/history", response_model=list)
def get_history():
    return sensor_history
