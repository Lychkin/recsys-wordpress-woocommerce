import os
import requests
import pandas as pd
from requests_oauthlib import OAuth1

from app.core.config import settings


def fetch_orders(page=1):
    orders = []
    page = 1
    while True:
        print(f"Fetching page {page} of ORDERS...")
        response = requests.get(
            f"{settings.wc_url}/orders",
            params={"per_page": 100, "page": page},
            auth=OAuth1(settings.wc_consumer_key, settings.wc_consumer_secret),
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        orders.extend(data)
        page += 1

    return orders


def orders_to_events(orders):
    rows = []
    for order in orders:
        user = order.get("customer_id") or f"guest_{order['id']}"
        ts = order["date_completed"] or order["date_created"]

        for item in order["line_items"]:
            rows.append(
                {
                    "user_id": str(user),
                    "item_id": str(item["product_id"]),
                    "event": "purchase",
                    "timestamp": ts,
                    "quantity": int(item.get("quantity", 1)),
                }
            )

    return pd.DataFrame(rows)


def fetch_additional_events():
    events = []
    page = 1
    while True:
        print(f"Fetching page {page} of ADD'EVENTS...")
        response = requests.get(
            settings.events_api_url, params={"page": page, "per_page": 100}
        )
        response.raise_for_status()
        data = response.json()["data"]
        if not data:
            break
        events.extend(data)
        page += 1

    df = pd.DataFrame(events)
    df.drop(columns=["id"], inplace=True)
    if df["timestamp"].dtype == "int64" and df["timestamp"].max() > 1e12:
        df["timestamp"] = (df["timestamp"] / 1000).astype(int)
    return df


if __name__ == "__main__":
    all_orders = fetch_orders()

    purchase_events = orders_to_events(all_orders)

    other_events = fetch_additional_events()

    all_events_df = pd.concat(
        [purchase_events, other_events], ignore_index=True
    )

    os.makedirs(settings.data_dir, exist_ok=True)
    all_events_df.to_csv(settings.raw_events_path, index=False)
    print(
        f"{settings.raw_events_path} saved, total events:", len(all_events_df)
    )
