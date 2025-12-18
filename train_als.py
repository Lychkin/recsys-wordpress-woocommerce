import pandas as pd
from scipy.sparse import coo_matrix
import implicit
import pickle


def build_sparse_matrix(events_df):
    users = events_df["user_id"].astype("category")
    items = events_df["item_id"].astype("category")

    user_idx = users.cat.codes.values
    item_idx = items.cat.codes.values

    data = events_df["weight"].values

    matrix = coo_matrix(
        (data, (user_idx, item_idx)),
        shape=(len(users.cat.categories), len(items.cat.categories)),
    ).tocsr()

    return matrix, users.cat.categories, items.cat.categories


if __name__ == "__main__":
    CSV_PATH = "data/events.csv"

    events = pd.read_csv(CSV_PATH)

    sparse_matrix, user_map, item_map = build_sparse_matrix(events)

    # implicit ожидает item-user matrix
    item_user = sparse_matrix.T.tocsr()

    model = implicit.als.AlternatingLeastSquares(
        factors=64, regularization=0.01, iterations=15
    )

    model.fit(item_user)

    with open("als_model.pkl", "wb") as f:
        pickle.dump((model, user_map, item_map), f)

    print("als_model.pkl saved")
