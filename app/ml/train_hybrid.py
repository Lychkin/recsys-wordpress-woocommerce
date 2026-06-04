import pandas as pd

from app.ml.cf_recommender import CollaborativeRecommender
from app.ml.cbf_recommender import ContentBasedRecommender
from app.ml.hybrid_recommender import HybridFilter

from app.core.config import settings

products = pd.read_parquet(settings.products_parquet_path)

events = pd.read_parquet(settings.events_parquet_path)

popularity = pd.read_parquet(settings.popularity_parquet_path)

cf = CollaborativeRecommender()
cf.fit(events)

cb = ContentBasedRecommender()
cb.fit(products)

hybrid = HybridFilter(als_weight=0.7, content_weight=0.3)

hybrid.fit(cf, cb, events, popularity)

hybrid.save(settings.hybrid_model_path)

print("saved")
