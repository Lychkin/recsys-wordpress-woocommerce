import pickle
import pandas as pd

from app.core.config import settings


class ModelManager:
    model = None

    @classmethod
    def load_model(cls):
        print("Loading model from file...")
        with open(settings.rec_model_path, "rb") as f:
            cls.model, cls.user_map, cls.item_map, cls.user_items_matrix = (
                pickle.load(f)
            )

            cls.user_to_idx = {u: i for i, u in enumerate(cls.user_map)}
            cls.item_to_idx = {i: j for j, i in enumerate(cls.item_map)}
            cls.idx_to_item = {v: k for k, v in cls.item_to_idx.items()}
            cls.popular_items = pd.read_csv(settings.popular_items_path)

    @classmethod
    def get_model_data(cls):
        return (
            cls.model,
            cls.user_items_matrix,
            cls.user_to_idx,
            cls.item_to_idx,
            cls.idx_to_item,
            cls.popular_items,
        )
