from fastapi import APIRouter, File, UploadFile
from models.plant_health import predict_plant_health

router = APIRouter()

@router.post("/plant-health")
async def analyze_plant_health(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = predict_plant_health(image_bytes)
    return {
        "filename": file.filename,
        "analysis": result
    }