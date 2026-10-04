from fastapi import APIRouter, HTTPException
from core.schemas import SensorReading
from core.firebase import push_sensor_data, get_latest_sensor_data

router = APIRouter()

@router.post("/", response_model=dict)
def post_sensor_data(data: SensorReading):
    success = push_sensor_data(data.model_dump(mode='json'))
    if not success:
        raise HTTPException(status_code=500, detail="Failed to push to Firebase")
    return {"status": "success", "message": "Data saved successfully"}

@router.get("/latest", response_model=SensorReading)
def get_latest_data():
    data = get_latest_sensor_data()
    if not data:
        raise HTTPException(status_code=404, detail="No sensor data found")
    return data
