from fastapi import APIRouter, HTTPException
from joblib import load
from ...services.recommendation_service import RecommendationService

router = APIRouter()
service = RecommendationService()

@router.get("/recommend/{customer_id}")
async def get_recommendations(customer_id: str, top_n: int = 5):
    try:
        recommendations = service.generate_recommendations(customer_id, top_n)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))