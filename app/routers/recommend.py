from fastapi import APIRouter, Depends

from app.services.recommendation_service import RecommendationService
from app.auth import verify_api_key

router = APIRouter(
    prefix="/recommend",
    tags=["recommendations"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/user/{user_id}")
def recommend_for_user(user_id: int, k: int = 10):
    return RecommendationService().recommend_for_user(user_id, k)


@router.get("/item/{item_id}")
def recommend_item(item_id: int, k: int = 10):
    return RecommendationService().recommend_item(item_id, k)
