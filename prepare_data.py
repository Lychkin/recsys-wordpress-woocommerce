import pandas as pd


DATA_DIR = "data"
RAW_EVENTS_PATH = f"./{DATA_DIR}/raw_events.csv"
EVENTS_PATH = f"./{DATA_DIR}/events.csv"


df = pd.read_csv(RAW_EVENTS_PATH)

# Веса (простая имплиситная схема)
EVENT_WEIGHTS = {"view": 1, "add_to_cart": 3, "purchase": 5}

df["weight"] = df["event"].apply(lambda x: EVENT_WEIGHTS.get(x, 1))

df = df[["user_id", "item_id", "event", "weight", "timestamp"]]

df.to_csv(EVENTS_PATH, index=False)

print(f"{EVENTS_PATH} created")
