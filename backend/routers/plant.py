from fastapi import APIRouter, UploadFile, File, HTTPException
from core.schemas import PlantHealthResponse
from models.plant_health import health_model

router = APIRouter()


@router.post("/plant-health", response_model=PlantHealthResponse, summary="Plant Health & Disease Detection")
async def plant_health(file: UploadFile = File(..., description="Leaf/canopy image (JPEG/PNG)")):
    """
    Analyse a leaf or canopy image using MobileNetV2.
    Returns health label, confidence score, and bounding box coordinates.
    Gracefully falls back to heuristic mock if TensorFlow is not installed.
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (JPEG/PNG).")

    try:
        image_bytes = await file.read()
        result = health_model.predict_from_bytes(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plant health analysis failed: {str(e)}")
