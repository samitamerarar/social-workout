import logging

from fastapi import APIRouter, HTTPException, status, Request

from socialworkoutapi.models.user import UserIn
from socialworkoutapi.security import (get_user, get_password_hash, authenticate_user,
                                       create_access_token, get_subject_for_token_type, create_confirmation_token)
from socialworkoutapi.database import database, user_table

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn, request: Request):
    if await get_user(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with that email already exists!")

    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User created. Please confirm your email.",
            "confirmation_url": request.url_for(  # create url for the confirm_email endpoint
                "confirm_email", token=create_confirmation_token(user.email)
            )
            }


@router.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirm/{token}")
async def confirm_email(token: str):
    email = get_subject_for_token_type(token, "confirmation")

    # Set confirmed on user record to True
    query = (user_table.update().where(user_table.c.email == email).values(confirmed=True))

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User confirmed!"}
