from fastapi import APIRouter, HTTPException
from core.schemas import DosingDecisionInput, DosingDecisionResponse
from models.dosing_engine import engine

router = APIRouter()


@router.post("/dosing-decision", response_model=DosingDecisionResponse, summary="Irrigation & Nutrient Dosing Decision")
def dosing_decision(data: DosingDecisionInput):
    """
    Evaluate real-time sensor readings against crop-specific physiological thresholds.
    Returns pump/valve control signals and nutrient dose recommendation.
    """
    try:
        result = engine.decide(data.model_dump(), data.crop_variety)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosing decision failed: {str(e)}")
