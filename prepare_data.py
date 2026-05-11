import pandas as pd
from core.config import settings

df = pd.read_csv(settings.raw_events_path)

EVENT_WEIGHTS = {"view": 1, "add_to_cart": 3, "purchase": 5}

df["weight"] = df["event"].apply(lambda x: EVENT_WEIGHTS.get(x, 1))

mask = df["quantity"].notna()
df.loc[mask, "weight"] *= df.loc[mask, "quantity"]

df = df.drop("quantity", axis=1)

agg = df.groupby(["user_id", "item_id"])["weight"].sum().reset_index()

agg.to_csv(settings.events_path, index=False)

print(f"{settings.events_path} created")

agg.sort_values(by="weight", ascending=False)[["item_id", "weight"]].to_csv(
    settings.popular_items_path, index=False
)

print(f"{settings.popular_items_path} created")
