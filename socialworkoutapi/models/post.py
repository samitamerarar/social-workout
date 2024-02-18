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


class UserPostWithLikes(UserPost):
    # Enable ORM, pydantic returns return_value.body if return_value["body"] fails
    model_config = ConfigDict(from_attributes=True)

    likes: int


class UserPostWithComments(BaseModel):
    post: UserPostWithLikes
    comments: list[Comment]


class PostLikeIn(BaseModel):
    post_id: int


class PostLike(PostLikeIn):
    id: int
    user_id: int
