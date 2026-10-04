from fastapi import APIRouter, HTTPException
from core.schemas import CropRecommendationInput, CropRecommendationResponse
from models.crop_recommender import recommender

router = APIRouter()


@router.post("/recommend-crop", response_model=CropRecommendationResponse, summary="AI Crop & Cultivar Recommendation")
def recommend_crop(data: CropRecommendationInput):
    """
    Recommend a crop variety and genomic strain based on location + soil-climate readings.
    ph is optional/nullable — handled via NaN imputation internally.
    """
    try:
        result = recommender.predict(data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop recommendation failed: {str(e)}")
