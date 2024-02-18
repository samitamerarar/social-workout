from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    email: str


# we define it like this so we dont return the password
class UserIn(User):
    password: str
