from fastapi import FastAPI, HTTPException
import pickle

app = FastAPI()

DATA_DIR = "data"
MODEL_PATH = f"./{DATA_DIR}/als_model.pkl"


with open(MODEL_PATH, "rb") as f:
    model, user_map, item_map, user_item_matrix = pickle.load(f)

user_to_idx = {u: i for i, u in enumerate(user_map)}
item_to_idx = {i: j for j, i in enumerate(item_map)}
idx_to_item = {v: k for k, v in item_to_idx.items()}


@app.get("/recommend/user/{user_id}")
def recommend_user(user_id: str, k: int = 10):
    if user_id not in user_to_idx:
        raise HTTPException(status_code=404, detail="User not found")

    uidx = user_to_idx[user_id]

    user_items = user_item_matrix[uidx]

    recommended = model.recommend(userid=uidx, user_items=user_items, N=k)

    result = [
        {"item_id": str(item_id), "score": float(score)}
        for item_id, score in zip(recommended[0], recommended[1])
    ]
    return result
