from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
import config

app = FastAPI()


with open(config.MODEL_PATH, "rb") as f:
    model, user_map, item_map, user_items_matrix = pickle.load(f)

user_to_idx = {u: i for i, u in enumerate(user_map)}
item_to_idx = {i: j for j, i in enumerate(item_map)}
idx_to_item = {v: k for k, v in item_to_idx.items()}
popular_items = pd.read_csv(config.POPULAR_ITEMS_PATH)


@app.get("/recommend/user/{user_id}")
def recommend_user(user_id: int, k: int = 10):
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


@app.get("/recommend/item/{item_id}")
def recommend_item(item_id: int, k: int = 10):
    if item_id not in item_to_idx:
        raise HTTPException(status_code=404, detail="Item not found")

    iidx = item_to_idx[item_id]

    similar = model.similar_items(iidx, N=k, filter_items=[iidx])

    result = [
        {"item_id": int(idx_to_item[int(i)]), "score": float(score)}
        for i, score in zip(similar[0], similar[1])
    ]

    return result
