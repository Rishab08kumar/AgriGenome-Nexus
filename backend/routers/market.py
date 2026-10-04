from fastapi import APIRouter, HTTPException
from core.schemas import MarketPriceInput, MarketPriceResponse
from models.market_forecaster import forecaster

router = APIRouter()


@router.post("/market-price", response_model=MarketPriceResponse, summary="APMC Fair Market Price Forecaster")
def market_price(data: MarketPriceInput):
    """
    Forecast APMC mandi price (₹/quintal) using XGBoost trained on synthetic Agmarknet-style data.
    Returns predicted price + confidence band (±10%).
    """
    try:
        result = forecaster.predict(data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market price prediction failed: {str(e)}")
