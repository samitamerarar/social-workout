import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from socialworkoutapi.database import database
from socialworkoutapi.logging_conf import configure_logging
from socialworkoutapi.routers.post import router as post_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When app startup
    configure_logging()
    logger.info("Hello")
    await database.connect()
    yield
    # When app shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(post_router, prefix="/posts")
