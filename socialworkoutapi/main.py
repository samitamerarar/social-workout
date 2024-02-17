import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from socialworkoutapi.database import database
from socialworkoutapi.logging_conf import configure_logging
from socialworkoutapi.routers.post import router as post_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When app startup
    configure_logging()
    await database.connect()
    yield
    # When app shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)


app.include_router(post_router, prefix="/posts")


# Whenever there is an exception raised (e.g. 404) in our routes, this is called
# no need to do logger.error before each `raise HTTPException()` in our routes code.
@app.exception_handler(HTTPException)
async def http_exeption_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
