import numpy as np
import pandas as pd

from app.core.config import settings


def main():
    now = pd.Timestamp.now()

    events_df = pd.read_csv(settings.raw_events_csv_path)

    BASE_WEIGHT = {"view": 1, "add_to_cart": 4, "purchase": 15}
    HALF_LIFE = {"view": 7, "add_to_cart": 14, "purchase": 90}

    events_df["base_weight"] = events_df["event"].map(BASE_WEIGHT)
    events_df["half_life"] = events_df["event"].map(HALF_LIFE)
    events_df["age_days"] = (
        now - pd.to_datetime(events_df["timestamp"])
    ).dt.days
    events_df["decay"] = 0.5 ** (events_df["age_days"] / events_df["half_life"])
    events_df["quantity_factor"] = np.log1p(events_df["quantity"])

    events_df["weight"] = (
        events_df["base_weight"]
        * events_df["quantity_factor"]
        * events_df["decay"]
    )

    needless_columns = [
        "base_weight",
        "half_life",
        "age_days",
        "decay",
        "quantity_factor",
        "quantity",
    ]
    events_df.drop(labels=needless_columns, axis=1, inplace=True)

    events_df = (
        events_df.groupby(["user_id", "item_id"])["weight"].sum().reset_index()
    )

    events_df.info()
    print(events_df.head(10))
    exit()

    events_df.to_parquet(settings.events_parquet_path, index=False)
    print(f"{settings.events_parquet_path} created")
    events_df.to_csv(settings.events_csv_path, index=False)
    print(f"{settings.events_csv_path} created")

    events_df.sort_values(by="weight", ascending=False)[
        ["item_id", "weight"]
    ].to_csv(settings.popular_items_path, index=False)

    print(f"{settings.popular_items_path} created")


if __name__ == "__main__":
    main()
