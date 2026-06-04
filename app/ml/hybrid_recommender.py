from dataclasses import dataclass
import pickle

from app.ml.loader import ModelManager


@dataclass
class HybridFilter:

    als_weight: float = 0.7
    content_weight: float = 0.3

    def fit(
        self,
        collaborative_filter,
        content_filter,
        interactions_df,
        popularity_df,
    ):

        self.cf = collaborative_filter
        self.cb = content_filter

        self.interactions_df = interactions_df

        self.popularity = popularity_df.rename(
            columns={"weight": "score"}
        ).to_dict(orient="records")

    def _normalize(self, items):
        print("HybridFilter:_normalize")
        if not items:
            return {}

        if isinstance(items[0], dict):
            scores = [item_score["score"] for item_score in items]
            mn = min(scores)
            mx = max(scores)
            if mx == mn:
                return {item_score["item_id"]: 1.0 for item_score in items}
            return {
                item_score["item_id"]: (item_score["score"] - mn) / (mx - mn)
                for item_score in items
            }
        elif isinstance(items[0], tuple):
            scores = [x[1] for x in items]
            mn = min(scores)
            mx = max(scores)
            if mx == mn:
                return {pid: 1.0 for pid, _ in items}

            return {pid: (s - mn) / (mx - mn) for pid, s in items}
        else:
            raise TypeError("Wrong items data structure")

    def recommend(self, user_id=None, top_k=20):
        model = ModelManager.get_model()
        print("HybridFilter:recommend")
        if user_id is None:
            return model.popularity[:top_k]

        user_history = model.interactions_df[
            model.interactions_df.user_id == user_id
        ]

        if len(user_history) == 0:
            return model.popularity[:top_k]

        als = model.cf.recommend(user_id, n=200)

        content = model.cb.recommend(user_history, top_k=200)

        als_scores = self._normalize(als)
        content_scores = self._normalize(content)

        candidates = set(als_scores.keys()) | set(content_scores.keys())

        result = []

        for pid in candidates:

            score = self.als_weight * als_scores.get(
                pid, 0
            ) + self.content_weight * content_scores.get(pid, 0)

            result.append((pid, score))

        result.sort(key=lambda x: x[1], reverse=True)

        return [
            {"item_id": int(item_id), "score": score}
            for item_id, score in result[:top_k]
        ]

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)
