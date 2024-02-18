from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    # Enable ORM, pydantic returns return_value.body if return_value["body"] fails
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    # Enable ORM, pydantic returns return_value.body if return_value["body"] fails
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserPostWithComments(BaseModel):
    post: UserPost
    comments: list[Comment]
