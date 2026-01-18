import pandas as pd
from scipy.sparse import coo_matrix
import implicit
import pickle
import config


def build_sparse_matrix(events_df):
    df = events_df.copy()

    user_ids = df["user_id"].unique()
    item_ids = df["item_id"].unique()

    user_map = {u: i for i, u in enumerate(user_ids)}
    item_map = {p: i for i, p in enumerate(item_ids)}

    df["user_idx"] = df["user_id"].map(user_map)
    df["item_idx"] = df["item_id"].map(item_map)

    matrix = coo_matrix((df["weight"], (df["user_idx"], df["item_idx"])))
    return matrix, user_map, item_map


if __name__ == "__main__":
    events = pd.read_csv(config.EVENTS_PATH)

    matrix, user_map, item_map = build_sparse_matrix(events)

    user_item_matrix = matrix.tocsr()

    model = implicit.als.AlternatingLeastSquares(
        factors=64, regularization=0.01, iterations=15
    )

    model.fit(user_item_matrix)

    with open(config.MODEL_PATH, "wb") as f:
        pickle.dump((model, user_map, item_map, user_item_matrix), f)

    print(f"{config.MODEL_PATH} saved")
