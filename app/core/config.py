from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Recsys WordPress WooCommerce API"

    host: str
    port: int

    recommender_api_key: str
    recommender_api_header: str

    wc_url: str
    wc_consumer_key: str
    wc_consumer_secret: str
    events_api_url: str

    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_dir: Path = base_dir / "data"

    raw_events_parquet_path: Path = data_dir / "raw_events.parquet"
    raw_events_csv_path: Path = data_dir / "raw_events.csv"

    events_parquet_path: Path = data_dir / "events.parquet"
    events_csv_path: Path = data_dir / "events.csv"

    products_parquet_path: Path = data_dir / "products.parquet"
    products_csv_path: Path = data_dir / "products.csv"

    popularity_parquet_path: Path = data_dir / "popular_items.parquet"
    popularity_csv_path: Path = data_dir / "popular_items.csv"

    hybrid_model_path: Path = data_dir / "hybrid_model.pkl"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
