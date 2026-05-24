from fastapi import Header, HTTPException

from app.core.config import settings


# In real HTTP: X-Recommender-API-Key
def verify_api_key(x_recommender_api_key: str = Header(None)):
    if x_recommender_api_key != settings.recommender_api_key:
        raise HTTPException(
            status_code=403, detail="Invalid Recommender API key"
        )

    return True
