import os
import re
from html import unescape

import requests
import pandas as pd
from requests_oauthlib import OAuth1

from app.core.config import settings


def fetch_products(page=1):
    products = []
    page = 1
    fields = [
        "id",
        "name",
        "categories",
        "brands",
        "price",
        "tags",
        "description",
        "attributes",
    ].join(",")

    while True:
        print(f"Fetching page {page} of PRODUCTS...")
        response = requests.get(
            f"{settings.wc_url}/products",
            params={
                "per_page": 100,
                "page": page,
                "_fields": fields,
            },
            auth=OAuth1(settings.wc_consumer_key, settings.wc_consumer_secret),
        )
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        products.extend(data)
        page += 1

    return products


def html_to_list(html: str) -> list[str]:
    html = re.sub(r"</?p>", "", html)
    items = re.split(r"<br\s*/?>", html)

    result = []

    for item in items:
        item = item.replace("&bull;", "").strip()
        item = unescape(item)

        if item:
            result.append(item)

    return result


def process_products(products):
    rows = []
    for product in products:
        tags_field = product.get("tags")
        attrs = product.get("attributes")
        color = attrs[0]["options"][0]
        material = attrs[1]["options"][0]

        rows.append(
            {
                "product_id": str(product.get("id")),
                "name": product.get("name"),
                "category": product.get("categories")[0]["name"],
                "brand": product.get("brands")[0]["name"],
                "price": int(product.get("price")),
                "tags": (
                    tags_field[0]["name"].split(", ") if tags_field else None
                ),
                "description": html_to_list(product.get("description")),
                "color": color,
                "material": material,
            }
        )

    return pd.DataFrame(rows)


def main():
    all_products = fetch_products()

    all_products_df = process_products(all_products)

    del all_products

    print("Total products:", len(all_products_df))

    os.makedirs(settings.data_dir, exist_ok=True)
    all_products_df.to_parquet(settings.products_parquet_path, index=False)
    print(f"{settings.products_parquet_path} saved")
    all_products_df.to_csv(settings.products_csv_path, index=False)
    print(f"{settings.products_csv_path} saved")


if __name__ == "__main__":
    main()
