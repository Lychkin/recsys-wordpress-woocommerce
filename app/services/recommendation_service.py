from app.ml.inference import ALSInference


class RecommendationService:
    def __init__(self):
        self.model = ALSInference()

    def recommend_for_user(self, user_id: int, k: int):
        return self.model.recommend_for_user(user_id, k)

    def recommend_item(self, item_id: int, k: int):
        return self.model.recommend_item(item_id, k)
