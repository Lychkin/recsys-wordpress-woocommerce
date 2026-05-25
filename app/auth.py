from fastapi import Header, HTTPException

from app.core.config import settings


# In real HTTP: X-Recommender-API-Key (Header)
def verify_api_key(
    secret_key: str = Header(None, alias=settings.recommender_api_header)
):
    if secret_key != settings.recommender_api_key:
        raise HTTPException(
            status_code=403, detail="Invalid Recommender API key"
        )

    return True
