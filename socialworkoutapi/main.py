from fastapi import FastAPI
from socialworkoutapi.routers.post import router as post_router

app = FastAPI()


app.include_router(post_router, prefix="/posts")
