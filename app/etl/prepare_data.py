import pandas as pd
from app.core.config import settings

df = pd.read_parquet(settings.raw_events_parquet_path)

EVENT_WEIGHTS = {"view": 1, "add_to_cart": 4, "purchase": 15}

df["weight"] = df["event"].apply(lambda x: EVENT_WEIGHTS.get(x, 1))

mask = df["quantity"].notna()
df.loc[mask, "weight"] *= df.loc[mask, "quantity"]

df.drop("quantity", axis=1, inplace=True)

df = df.groupby(["user_id", "item_id"])["weight"].sum().reset_index()

df.to_parquet(settings.events_parquet_path, index=False)

print(f"{settings.events_parquet_path} created")

df.to_csv(settings.events_csv_path, index=False)

print(f"{settings.events_csv_path} created")

df.sort_values(by="weight", ascending=False)[["item_id", "weight"]].to_csv(
    settings.popular_items_path, index=False
)

print(f"{settings.popular_items_path} created")
