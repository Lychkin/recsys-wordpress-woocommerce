import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

WC_URL = os.getenv("WC_URL")
CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")
EVENTS_API_URL = os.getenv("EVENTS_API_URL")


def fetch_orders(page=1):
    respone = requests.get(
        f"{WC_URL}/orders",
        params={"per_page": 100, "page": page},
        auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),
    )
    respone.raise_for_status()
    return respone.json()


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
    all_events = []
    page = 1
    while True:
        r = requests.get(EVENTS_API_URL, params={"page": page, "per_page": 500})
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        all_events.extend(data)
        page += 1

    df = pd.DataFrame(all_events)
    if df["timestamp"].dtype == "int64" and df["timestamp"].max() > 1e12:
        df["timestamp"] = (df["timestamp"] / 1000).astype(int)
    return df


if __name__ == "__main__":
    all_orders = []
    for p in range(1, 5):  # увеличь диапазон по необходимости
        data = fetch_orders(p)
        if not data:
            break
        all_orders.extend(data)

    purchase_events = orders_to_events(all_orders)

    other_events = fetch_additional_events()

    all_events_df = pd.concat(
        [purchase_events, other_events], ignore_index=True
    )

    all_events_df.to_csv("events.csv", index=False)
    print("events.csv saved, total events:", len(all_events_df))
