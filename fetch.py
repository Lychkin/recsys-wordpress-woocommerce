import os
import requests
import pandas as pd
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

load_dotenv()

WC_URL = os.getenv("WC_URL")
CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")
EVENTS_API_URL = os.getenv("EVENTS_API_URL")
DATA_DIR = "data"
RAW_EVENTS_PATH = f"./{DATA_DIR}/raw_events.csv"

auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET)


def fetch_orders(page=1):
    orders = []
    page = 1
    while True:
        print(f"Fetching page {page} of ORDERS...")
        response = requests.get(
            f"{WC_URL}/orders",
            params={"per_page": 100, "page": page},
            auth=auth,
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


if __name__ == "__main__":
    all_orders = fetch_orders()

    purchase_events = orders_to_events(all_orders)

    purchase_events.to_csv(RAW_EVENTS_PATH, index=False)

    print(f"{RAW_EVENTS_PATH} saved, total events:", len(purchase_events))
