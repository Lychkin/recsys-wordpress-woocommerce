import pandas as pd

# Загрузили данные, полученные из fetch_wc.py
df = pd.read_csv("raw_events.csv")

# Веса (простая имплиситная схема)
EVENT_WEIGHTS = {"view": 1, "add_to_cart": 3, "purchase": 5}

df["weight"] = df["event"].apply(lambda x: EVENT_WEIGHTS.get(x, 1))

df = df[["user_id", "item_id", "event", "weight", "timestamp"]]

CSV_PATH = "data/events.csv"

df.to_csv(CSV_PATH, index=False)

print(f"{CSV_PATH} created")
