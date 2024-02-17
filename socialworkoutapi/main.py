from contextlib import asynccontextmanager
from fastapi import FastAPI

from socialworkoutapi.database import database
from socialworkoutapi.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When app startup
    await database.connect()
    yield
    # When app shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(post_router, prefix="/posts")
