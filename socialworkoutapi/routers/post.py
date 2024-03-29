import logging
from enum import Enum
from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, HTTPException, Request, Depends
from socialworkoutapi.database import comment_table, database, post_table, like_table
from socialworkoutapi.models.post import (
    UserPost, UserPostIn,
    Comment, CommentIn,
    UserPostWithComments,
    PostLike, PostLikeIn,
    UserPostWithLikes
)
from socialworkoutapi.models.user import User
from socialworkoutapi.security import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)


# partial and reusable query
select_post_and_likes = (
    sqlalchemy.select(
        post_table, sqlalchemy.func.count(like_table.c.id).label("likes")  # these columns
    )
    .select_from(post_table.outerjoin(like_table))  # merge 2 tables
    .group_by(post_table.c.id)  # group by post id
)


async def find_post(post_id: int):
    logger.info(f"Finding Post with id: {post_id}")

    query = post_table.select().where(post_table.c.id == post_id)

    logger.debug(query)
    return await database.fetch_one(query)


@router.post("/create", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]):
    logger.info("Creating post")

    data = {**post.dict(), "user_id": current_user.id}
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


class PostSorting(str, Enum):
    new = "new"
    old = "old"
    most_likes = "most_likes"


@router.get("/all", response_model=list[UserPostWithLikes])
async def get_all_posts(sorting: PostSorting = PostSorting.new):  # (e.g. /all?sorting=most_likes)
    logger.info("Getting all posts")

    if sorting == PostSorting.new:
        query = select_post_and_likes.order_by(post_table.c.id.desc())
    elif sorting == PostSorting.old:
        query = select_post_and_likes.order_by(post_table.c.id.asc())
    elif sorting == PostSorting.most_likes:
        query = select_post_and_likes.order_by(sqlalchemy.desc("likes"))

    logger.debug(query)

    return await database.fetch_all(query)


@router.post("/comment", response_model=Comment, status_code=201)
# DI
async def create_comment(comment: CommentIn, request: Request, current_user: Annotated[User, Depends(get_current_user)]):
    logger.info("Creating comment")

    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    data = {**comment.dict(), "user_id": current_user.id}
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    logger.info(f"Getting comments on post: {post_id}")

    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    logger.info(f"Getting post {post_id} with comments")

    query = select_post_and_likes.where(post_table.c.id == post_id)

    logger.debug(query)

    post = await database.fetch_one(query)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id)
    }


@router.post("/like", response_model=PostLike, status_code=201)
async def like_post(like: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]):
    logger.info("Liking post")

    post = await find_post(like.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    data = {**like.dict(), "user_id": current_user.id}
    query = like_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
