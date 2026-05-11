from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Recsys WordPress WooCommerce API"

    host: str = "localhost"
    port: int = 8000

    wc_url: str
    wc_consumer_key: str
    wc_consumer_secret: str
    events_api_url: str

    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = base_dir / "data"
    raw_events_path: Path = data_dir / "raw_events.csv"
    events_path: Path = data_dir / "events.csv"
    popular_items_path: Path = data_dir / "popular_items.csv"
    rec_model_path: Path = data_dir / "als_model.pkl"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
