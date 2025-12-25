import pandas as pd
from scipy.sparse import coo_matrix
import implicit
import pickle

DATA_DIR = "data"
EVENTS_PATH = f"./{DATA_DIR}/events.csv"
MODEL_PATH = f"./{DATA_DIR}/als_model.pkl"


def build_sparse_matrix(events_df):
    users = events_df["user_id"].astype("category")
    items = events_df["item_id"].astype("category")

    user_idx = users.cat.codes.values
    item_idx = items.cat.codes.values

    data = events_df["weight"].values

    data = events_df["weight"].values
    mat = coo_matrix(
        (data, (user_idx, item_idx)),
        shape=(users.cat.categories.size, items.cat.categories.size),
    )
    return mat.tocsr(), users.cat.categories, items.cat.categories


if __name__ == "__main__":
    events = pd.read_csv(EVENTS_PATH)
    events["user_id"] = events["user_id"].astype(str)

    sparse_matrix, user_map, item_map = build_sparse_matrix(events)

    # implicit ожидает item-user matrix
    item_user = sparse_matrix.T.tocsr()

    model = implicit.als.AlternatingLeastSquares(
        factors=64, regularization=0.01, iterations=15
    )

    model.fit(item_user)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((model, user_map, item_map, sparse_matrix), f)

    print(f"{MODEL_PATH} saved")
