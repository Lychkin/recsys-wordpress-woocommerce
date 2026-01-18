import pandas as pd
import config


df = pd.read_csv(config.RAW_EVENTS_PATH)

EVENT_WEIGHTS = {"view": 1, "add_to_cart": 3, "purchase": 5}

df["weight"] = df["event"].apply(lambda x: EVENT_WEIGHTS.get(x, 1))

mask = df["quantity"].notna()
df.loc[mask, "weight"] *= df.loc[mask, "quantity"]

df = df.drop("quantity", axis=1)

agg = df.groupby(["user_id", "item_id"])["weight"].sum().reset_index()

agg.to_csv(config.EVENTS_PATH, index=False)

print(f"{config.EVENTS_PATH} created")

agg.sort_values(by="weight", ascending=False)[["item_id", "weight"]].to_csv(
    config.POPULAR_ITEMS_PATH, index=False
)

print(f"{config.POPULAR_ITEMS_PATH} created")
