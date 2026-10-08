from fastapi import APIRouter
from models.crop_recommender import recommender

router = APIRouter()

@router.post("/recommend-crop")
def recommend_crop(data: dict):
    return recommender.predict(data)