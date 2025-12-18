from fastapi import FastAPI, HTTPException
import pickle

app = FastAPI()

with open("als_model.pkl", "rb") as f:
    model, user_map, item_map = pickle.load(f)

user_to_idx = {u: i for i, u in enumerate(user_map)}
item_to_idx = {i: j for j, i in enumerate(item_map)}
idx_to_item = {v: k for k, v in item_to_idx.items()}


@app.get("/recommend/user/{user_id}")
def recommend_user(user_id: str, k: int = 10):
    if user_id not in user_to_idx:
        raise HTTPException(status_code=404, detail="User not found")

    uidx = user_to_idx[user_id]

    # user_items=None позволяет ALS использовать общую матрицу
    recommended = model.recommend(uidx, user_items=None, N=k)

    return [
        {"item_id": idx_to_item[i], "score": float(s)}
        for i, s in recommended
    ]


@app.get("/recommend/item/{item_id}")
def recommend_item(item_id: str, k: int = 10):
    if item_id not in item_to_idx:
        raise HTTPException(status_code=404, detail="Item not found")

    iidx = item_to_idx[item_id]

    similar = model.similar_items(iidx, N=k)

    return [
        {"item_id": idx_to_item[i], "score": float(s)}
        for i, s in similar
    ]
