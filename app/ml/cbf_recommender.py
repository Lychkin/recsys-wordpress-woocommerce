from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class ContentBasedRecommender:

    def build_text(self, row):
        print("ContentBasedRecommender:build_text")
        fields = [
            str(row["name"]),
            str(row["category"]),
            str(row["brand"]),
            str(row["color"]),
            str(row["material"]),
        ]
        tags = row["tags"]
        bullet_points = row["description"]
        fields.extend(tags if isinstance(tags, list) else "")
        fields.extend(bullet_points if isinstance(bullet_points, list) else "")

        return " ".join(fields)

    def fit(self, products_df):
        products_df = products_df.copy()

        text = products_df.apply(self.build_text, axis=1)

        self.product_ids = products_df["product_id"].tolist()

        self.product_id_to_idx = {
            int(product): idx for idx, product in enumerate(self.product_ids)
        }

        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words=None)

        self.product_vectors = self.vectorizer.fit_transform(text)

    def build_user_profile(self, user_interactions):
        print("ContentBasedRecommender:build_user_profile")
        vectors = []
        weights = []

        for _, row in user_interactions.iterrows():

            pid = row["item_id"]

            if pid not in self.product_id_to_idx:
                continue

            idx = self.product_id_to_idx[pid]

            vectors.append(self.product_vectors[idx].toarray()[0])

            weights.append(row["weight"])

        if not vectors:
            return None

        vectors = np.array(vectors)
        weights = np.array(weights)

        profile = np.average(vectors, axis=0, weights=weights)

        return profile.reshape(1, -1)

    def recommend(self, user_interactions, top_k=100):
        print("ContentBasedRecommender:recommend")
        profile = self.build_user_profile(user_interactions)

        if profile is None:
            return []

        scores = cosine_similarity(profile, self.product_vectors)[0]

        seen = set(user_interactions["item_id"])

        result = []

        for idx in np.argsort(-scores):
            pid = self.product_ids[idx]

            if pid in seen:
                continue

            result.append((pid, float(scores[idx])))

            if len(result) >= top_k:
                break

        return result
