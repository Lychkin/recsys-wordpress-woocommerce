from typing import Optional

from app.ml.hybrid_recommender import HybridFilter


class RecommendationService:
    def __init__(self):
        self.model = HybridFilter()

    def recommend_for_user(self, user_id: Optional[int], k: int):
        return self.model.recommend(user_id, k)
