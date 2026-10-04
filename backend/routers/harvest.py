from fastapi import APIRouter, HTTPException
from core.schemas import HarvestReadinessInput, HarvestReadinessResponse
from models.harvest_predictor import predictor

router = APIRouter()


@router.post("/harvest-readiness", response_model=HarvestReadinessResponse, summary="Harvest Maturity Predictor")
def harvest_readiness(data: HarvestReadinessInput):
    """
    Predict crop maturity % and estimated days remaining to harvest.
    Triggers alert when maturity score exceeds 90%.
    """
    try:
        result = predictor.predict(data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Harvest prediction failed: {str(e)}")
