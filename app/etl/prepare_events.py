import numpy as np
import pandas as pd

from app.core.config import settings


def main():
    now = pd.Timestamp.now()

    events_df = pd.read_parquet(settings.raw_events_parquet_path)

    events_df["quantity"] = events_df["quantity"].fillna(1)

    BASE_WEIGHT = {"view": 1, "add_to_cart": 4, "purchase": 12}
    HALF_LIFE = {"view": 7, "add_to_cart": 14, "purchase": 90}

    # Базовый вес
    events_df["base_weight"] = events_df["event"].map(BASE_WEIGHT)

    # Half-life
    events_df["half_life"] = events_df["event"].map(HALF_LIFE)

    # Возраст события
    events_df["age_days"] = (
        now - pd.to_datetime(events_df["timestamp"])
    ).dt.days

    # Временной коэффициент
    events_df["decay"] = 0.5 ** (events_df["age_days"] / events_df["half_life"])

    # Коэффициент кол-ва товара
    events_df["quantity_factor"] = np.log1p(events_df["quantity"])

    # Итоговый вес
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

    popularity_df = (
        (
            events_df.groupby("item_id")["weight"]
            .sum()
            .sort_values(ascending=False)
        )
        .to_frame()
        .reset_index()
    )

    popularity_df.to_parquet(settings.popularity_parquet_path, index=True)
    print(f"{settings.popularity_parquet_path} created")
    popularity_df.to_csv(settings.popularity_csv_path, index=True)
    print(f"{settings.popularity_csv_path} created")

    events_df.to_parquet(settings.events_parquet_path, index=False)
    print(f"{settings.events_parquet_path} created")
    events_df.to_csv(settings.events_csv_path, index=False)
    print(f"{settings.events_csv_path} created")


if __name__ == "__main__":
    main()
