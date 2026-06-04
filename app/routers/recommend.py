from fastapi import APIRouter, Depends
from typing import Optional
from app.services.recommendation_service import RecommendationService
from app.auth import verify_api_key

router = APIRouter(
    tags=["recommendations"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/recommend")
def recommend_for_user(user_id: Optional[int] = None, k: int = 10):
    result = RecommendationService().recommend_for_user(user_id, k)
    print(result)
    return result
