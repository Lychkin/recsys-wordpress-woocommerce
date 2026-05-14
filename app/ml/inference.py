# import pickle
# import pandas as pd

# from app.core.config import settings
from .exceptions import ItemNotFoundError
from app.ml.loader import ModelManager


class ALSInference:
    def recommend_for_user(self, user_id: int, k):
        (
            model,
            user_items_matrix,
            user_to_idx,
            _,
            idx_to_item,
            popular_items,
        ) = ModelManager.get_model_data()

        if user_id not in user_to_idx:
            return popular_items[:k].to_dict(orient="records")

        uidx = user_to_idx[user_id]

        user_items = user_items_matrix[uidx]

        recommended = model.recommend(uidx, user_items=user_items, N=k)

        result = [
            {"item_id": int(idx_to_item[int(i)]), "score": float(score)}
            for i, score in zip(recommended[0], recommended[1])
        ]
        return result

    def recommend_item(self, item_id: int, k):
        (
            model,
            _,
            _,
            item_to_idx,
            idx_to_item,
            _,
        ) = ModelManager.get_model_data()

        if item_id not in item_to_idx:
            raise ItemNotFoundError("Item {item_id} not found")

        iidx = item_to_idx[item_id]

        similar = model.similar_items(iidx, N=k, filter_items=[iidx])

        result = [
            {"item_id": int(idx_to_item[int(i)]), "score": float(score)}
            for i, score in zip(similar[0], similar[1])
        ]

        return result
