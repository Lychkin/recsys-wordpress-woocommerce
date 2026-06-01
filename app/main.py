from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routers import recommend
from app.ml.exceptions import ItemNotFoundError
from app.ml.loader import ModelManager
from app.auth import verify_api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    ModelManager.load_model()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(recommend.router)


@app.get("/", dependencies=[Depends(verify_api_key)])
def root():
    return {"message": "Recsys API is running"}


@app.exception_handler(ItemNotFoundError)
def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.get("/")
def root():
    return {"message": " API is running (recsys)"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host=settings.host, port=settings.port, reload=True
    )
