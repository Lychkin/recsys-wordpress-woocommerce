from dataclasses import dataclass

import implicit
from scipy.sparse import coo_matrix


@dataclass
class CollaborativeRecommender:
    factors: int = 64
    regularization: float = 0.05
    iterations: int = 30

    def build_sparse_matrix(self, events_df):
        print("CollaborativeRecommender:build_sparse_matrix")
        df = events_df.copy()

        user_ids = df["user_id"].unique()
        item_ids = df["item_id"].unique()

        user_to_idx = {u: i for i, u in enumerate(user_ids)}
        item_to_idx = {p: i for i, p in enumerate(item_ids)}

        df["user_idx"] = df["user_id"].map(user_to_idx)
        df["item_idx"] = df["item_id"].map(item_to_idx)

        matrix = coo_matrix((df["weight"], (df["user_idx"], df["item_idx"])))
        return matrix, user_to_idx, item_to_idx

    def fit(self, interactions_df):
        matrix, self.user_map, self.item_map = self.build_sparse_matrix(
            interactions_df
        )

        self.user_item_matrix = matrix.tocsr()

        self.model = implicit.als.AlternatingLeastSquares(
            factors=self.factors,
            regularization=self.regularization,
            iterations=self.iterations,
            random_state=42,
        )

        self.model.fit(self.user_item_matrix)

        self.user_to_idx = {u: i for i, u in enumerate(self.user_map)}
        self.item_to_idx = {i: j for j, i in enumerate(self.item_map)}
        self.idx_to_item = {v: k for k, v in self.item_to_idx.items()}

        return self

    def recommend(self, user_id: int, n):
        print("CollaborativeRecommender:recommend")
        if user_id not in self.user_to_idx:
            return []

        uidx = self.user_to_idx[user_id]

        user_items = self.user_item_matrix[uidx]

        recommended = self.model.recommend(uidx, user_items=user_items, N=n)

        result = [
            {"item_id": int(self.idx_to_item[int(i)]), "score": float(score)}
            for i, score in zip(recommended[0], recommended[1])
        ]
        return result
