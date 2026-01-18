from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_EVENTS_PATH = DATA_DIR / "raw_events.csv"
EVENTS_PATH = DATA_DIR / "events.csv"
POPULAR_ITEMS_PATH = DATA_DIR / "popular_items.csv"

MODEL_PATH = DATA_DIR / "als_model.pkl"
